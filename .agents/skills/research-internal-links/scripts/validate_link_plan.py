#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html import unescape
from urllib.parse import urlparse


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 InternalLinkValidator/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.geturl(), response.status, response.read().decode("utf-8", "ignore")


def text(html):
    html = re.sub(r"<(script|style|nav|footer|aside)\b[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    match = re.search(r"<(?:article|main)\b[^>]*>(.*?)</(?:article|main)>", html, flags=re.I | re.S)
    body = match.group(1) if match else html
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", unescape(body)).strip()


def host(url):
    return urlparse(url).netloc.lower().removeprefix("www.")


def main():
    parser = argparse.ArgumentParser(description="Validate an internal-link plan JSON file")
    parser.add_argument("plan")
    args = parser.parse_args()
    with open(args.plan, encoding="utf-8") as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        raise SystemExit("Plan must be a JSON array")

    source_cache = {}
    target_cache = {}
    seen = set()
    failures = 0
    for number, row in enumerate(rows, 1):
        source = row.get("source_url", "").strip()
        anchor = row.get("anchor_text", "").strip()
        target = row.get("target_url", "").strip()
        errors = []
        if not all((source, anchor, target)):
            errors.append("missing required field")
        elif host(source) != host(target):
            errors.append("cross-domain target")
        elif source.rstrip("/") == target.rstrip("/"):
            errors.append("self-link")
        pair = (source.rstrip("/"), target.rstrip("/"))
        if pair in seen:
            errors.append("duplicate source-target pair")
        seen.add(pair)

        if source and anchor:
            try:
                if source not in source_cache:
                    source_cache[source] = text(fetch(source)[2])
                if anchor not in source_cache[source]:
                    errors.append("anchor not found verbatim in likely article body")
            except Exception as exc:
                errors.append(f"source fetch failed: {exc}")
        if target:
            try:
                if target not in target_cache:
                    target_cache[target] = fetch(target)[:2]
                final_url, status = target_cache[target]
                if status >= 400:
                    errors.append(f"target HTTP {status}")
                if host(final_url) != host(target):
                    errors.append("target redirects cross-domain")
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                errors.append(f"target fetch failed: {exc}")

        state = "FAIL" if errors else "PASS"
        print(f"{state} row {number}: {anchor!r} -> {target}")
        for error in errors:
            print(f"  - {error}")
        failures += bool(errors)
    print(f"\nValidated {len(rows)} rows; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
