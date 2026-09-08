#!/usr/bin/env python3
"""Workspace governance CLI for the GOHA SEO monorepo.

All mutating commands are dry-run unless --apply is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - Python < 3.11 guard
    raise SystemExit("Python 3.11+ is required (tomllib is unavailable).") from exc

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "workspace.toml"
REVIEW_STATES = {"review", "approved", "published"}
GENERATED_NAMES = {"node_modules", ".next", "build", "dist", "www", "venv", ".venv", "__pycache__"}
GENERATED_SUFFIXES = (".app",)
TOPIC_ID_RE = re.compile(r"^[^/]+/[^/]+/[^/]+$")


def load_config() -> dict:
    with CONFIG_PATH.open("rb") as handle:
        return tomllib.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def topic_dirs() -> list[Path]:
    pattern = ROOT / "clients"
    return sorted(path for path in pattern.glob("*/brands/*/keywords/*") if path.is_dir())


def workflow_for(client: str, brand: str, slug: str) -> str:
    text = f"{client} {brand} {slug}".lower()
    if client == "Home-Credit":
        return "finance"
    if client == "Heritage":
        return "travel"
    regulated_tokens = ("nghi-dinh", "quy-dinh", "luat-", "an-toan-thuc-pham", "bao-hiem")
    if any(token in text for token in regulated_tokens):
        return "regulated"
    return "standard"


def artifact_map(path: Path, canonical: list[str]) -> dict[str, str]:
    return {name.removesuffix(".md").replace("-", "_"): name for name in canonical if (path / name).is_file()}


def write_topic_manifest(path: Path, config: dict, apply: bool) -> str:
    client = path.parents[3].name
    brand = path.parents[1].name
    slug = path.name
    workflow = workflow_for(client, brand, slug)
    canonical = config["topic"]["canonical_files"]
    artifacts = artifact_map(path, canonical)
    required = set(config["workflows"][workflow]["required"])
    status = "review" if required.issubset(set(artifacts.values())) else "backlog"
    lines = [
        "schema_version = 1",
        f"id = {toml_string(f'{client}/{brand}/{slug}')}",
        f"client = {toml_string(client)}",
        f"brand = {toml_string(brand)}",
        f"slug = {toml_string(slug)}",
        f"workflow = {toml_string(workflow)}",
        f"status = {toml_string(status)}",
        f"updated_at = {toml_string(date.today().isoformat())}",
        "",
        "[artifacts]",
    ]
    lines.extend(f"{key} = {toml_string(value)}" for key, value in sorted(artifacts.items()))
    content = "\n".join(lines) + "\n"
    destination = path / "topic.toml"
    if apply:
        destination.write_text(content, encoding="utf-8")
    return str(destination.relative_to(ROOT))


def normalize_topic_files(path: Path, apply: bool) -> list[str]:
    actions: list[str] = []
    aliases = {
        "intent-analysis.md": "search-intent.md",
        "article-final.md": "article.md",
        "article-new.md": "article.md",
        "outline/outline.md": "outline.md",
    }
    for source_name, target_name in aliases.items():
        source, target = path / source_name, path / target_name
        if not source.is_file():
            continue
        if target.exists() and sha256(source) == sha256(target):
            actions.append(f"DELETE duplicate {source.relative_to(ROOT)}")
            if apply:
                source.unlink()
        elif not target.exists():
            actions.append(f"MOVE {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(target))
        else:
            attachment = path / "attachments" / f"legacy-{source.name}"
            actions.append(f"PRESERVE {source.relative_to(ROOT)} -> {attachment.relative_to(ROOT)}")
            if apply:
                attachment.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(attachment))
    if apply:
        outline_dir = path / "outline"
        if outline_dir.is_dir() and not any(outline_dir.iterdir()):
            outline_dir.rmdir()
    return actions


def migration_pairs(config: dict) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    clients = ROOT / "clients"
    for key, normalized_brand in config["migration"]["brand_map"].items():
        client, source_tail = key.split("/", 1)
        source = clients / client / source_tail
        target = clients / client / "brands" / normalized_brand / "keywords"
        if source.is_dir():
            pairs.append((source, target))
    return pairs


def command_migrate(args: argparse.Namespace) -> int:
    config = load_config()
    actions: list[str] = []
    for source, target in migration_pairs(config):
        for topic in sorted(path for path in source.iterdir() if path.is_dir()):
            destination = target / topic.name
            if destination.exists():
                print(f"ERROR collision: {destination.relative_to(ROOT)}", file=sys.stderr)
                return 2
            actions.append(f"MOVE {source.relative_to(ROOT)} -> {destination.relative_to(ROOT)}")
            if args.apply:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(topic), str(destination))
        if args.apply and source.is_dir() and not any(source.iterdir()):
            source.rmdir()
    dirs = topic_dirs() if args.apply else []
    if args.apply:
        for path in dirs:
            actions.extend(normalize_topic_files(path, True))
            write_topic_manifest(path, config, True)
    print(json.dumps({"apply": args.apply, "actions": actions, "topics": len(dirs)}, ensure_ascii=False, indent=2))
    return 0


def command_verify_migration(args: argparse.Namespace) -> int:
    current: dict[str, list[str]] = defaultdict(list)
    skipped = {".git", "graphify-out", ".graphify-venv", "node_modules", ".next", "build", "dist", "venv"}
    for current_root, dirs, files in os.walk(ROOT):
        dirs[:] = [name for name in dirs if name not in skipped and not name.endswith(".app")]
        for name in files:
            path = Path(current_root) / name
            current[sha256(path)].append(str(path.relative_to(ROOT)))
    deleted_raw = subprocess.check_output(["git", "ls-files", "--deleted", "-z"], cwd=ROOT)
    deleted = [item.decode("utf-8", "surrogateescape") for item in deleted_raw.split(b"\0") if item]
    matches: list[dict[str, object]] = []
    missing: list[str] = []
    for old_path in deleted:
        blob = subprocess.run(
            ["git", "show", f"HEAD:{old_path}"], cwd=ROOT, check=True, stdout=subprocess.PIPE
        ).stdout
        digest = hashlib.sha256(blob).hexdigest()
        if digest in current:
            matches.append({"old": old_path, "new": current[digest], "sha256": digest})
        else:
            missing.append(old_path)
    report = {
        "date": date.today().isoformat(),
        "deleted": len(deleted),
        "matched": len(matches),
        "missing": missing,
        "mappings": matches,
    }
    if args.write:
        output = ROOT / "reports" / f"migration-{date.today().isoformat()}.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(output.relative_to(ROOT))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if missing else 0


def validate_topic(path: Path, config: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = path / "topic.toml"
    if not manifest.is_file():
        return [f"missing manifest: {path.relative_to(ROOT)}"], warnings
    try:
        with manifest.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"invalid manifest {manifest.relative_to(ROOT)}: {exc}"], warnings
    expected = f"{path.parents[3].name}/{path.parents[1].name}/{path.name}"
    if data.get("id") != expected or not TOPIC_ID_RE.match(str(data.get("id", ""))):
        errors.append(f"id/path mismatch: {manifest.relative_to(ROOT)}")
    workflow = data.get("workflow")
    if workflow not in config["workflows"]:
        errors.append(f"unknown workflow: {manifest.relative_to(ROOT)}")
        return errors, warnings
    artifacts = data.get("artifacts", {})
    for relative in artifacts.values():
        candidate = path / relative
        if not candidate.is_file() or candidate.resolve().parent != path.resolve():
            errors.append(f"bad artifact {relative}: {manifest.relative_to(ROOT)}")
    required = set(config["workflows"][workflow]["required"])
    present = set(artifacts.values())
    missing = sorted(required - present)
    if missing:
        message = f"incomplete {expected}: {', '.join(missing)}"
        if data.get("status") in REVIEW_STATES:
            errors.append(message)
        else:
            warnings.append(message)
    return errors, warnings


def generated_dirs() -> list[Path]:
    results: list[Path] = []
    for base_name in ("projects", "tools", "scripts"):
        base = ROOT / base_name
        if not base.exists():
            continue
        for current, dirs, _files in os.walk(base):
            current_path = Path(current)
            kept: list[str] = []
            for name in dirs:
                candidate = current_path / name
                if name in GENERATED_NAMES or name.endswith(GENERATED_SUFFIXES) or "-darwin-" in name:
                    results.append(candidate)
                else:
                    kept.append(name)
            dirs[:] = kept
    return sorted(set(results))


def duplicate_groups(config: dict | None = None) -> list[list[str]]:
    hashes: dict[tuple[int, str], list[str]] = defaultdict(list)
    for base_name in ("clients", "data"):
        base = ROOT / base_name
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.name != "topic.toml" and path.stat().st_size:
                hashes[(path.stat().st_size, sha256(path))].append(str(path.relative_to(ROOT)))
    groups = [paths for paths in hashes.values() if len(paths) > 1]
    if config is None:
        return groups
    declared = {
        frozenset((item["canonical"], item["reference"]))
        for item in config.get("duplicate_references", [])
    }
    return [paths for paths in groups if frozenset(paths) not in declared]


def command_validate(_args: argparse.Namespace) -> int:
    config = load_config()
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, str] = {}
    topics = topic_dirs()
    for path in topics:
        topic_errors, topic_warnings = validate_topic(path, config)
        errors.extend(topic_errors)
        warnings.extend(topic_warnings)
        manifest = path / "topic.toml"
        if manifest.is_file():
            with manifest.open("rb") as handle:
                data = tomllib.load(handle)
            topic_id = data.get("id")
            if topic_id in seen:
                errors.append(f"duplicate id {topic_id}: {seen[topic_id]} and {manifest.relative_to(ROOT)}")
            seen[topic_id] = str(manifest.relative_to(ROOT))
    legacy = sorted(str(path.relative_to(ROOT)) for path in (ROOT / "clients").glob("*/keywords*"))
    errors.extend(f"legacy keyword root: {path}" for path in legacy)
    result = {"topics": len(topics), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def command_audit(_args: argparse.Namespace) -> int:
    config = load_config()
    generated = generated_dirs()
    duplicates = duplicate_groups(config)
    validation_errors: list[str] = []
    validation_warnings: list[str] = []
    for path in topic_dirs():
        errors, warnings = validate_topic(path, config)
        validation_errors.extend(errors)
        validation_warnings.extend(warnings)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    tracked_paths = [item.decode("utf-8", "surrogateescape") for item in tracked if item]
    sensitive_names = {".env", "credentials.json", "token.json"}
    sensitive = [path for path in tracked_paths if Path(path).name in sensitive_names or Path(path).suffix in {".pem", ".key"}]
    tracked_generated = [
        path for path in tracked_paths
        if any(part in GENERATED_NAMES for part in Path(path).parts)
        or any(part.endswith(GENERATED_SUFFIXES) for part in Path(path).parts)
    ]
    report = {
        "topics": len(topic_dirs()),
        "generated_directories": [str(path.relative_to(ROOT)) for path in generated],
        "generated_bytes": sum(sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) for path in generated),
        "duplicate_groups": duplicates,
        "tracked_sensitive_files": sensitive,
        "tracked_generated_files": tracked_generated,
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if validation_errors else 0


def command_clean(args: argparse.Namespace) -> int:
    targets = generated_dirs()
    for path in targets:
        print(("DELETE " if args.apply else "WOULD DELETE ") + str(path.relative_to(ROOT)))
        if args.apply:
            shutil.rmtree(path)
    return 0


def command_graph(args: argparse.Namespace) -> int:
    marker = ROOT / "graphify-out" / ".graphify_python"
    python = marker.read_text(encoding="utf-8").strip() if marker.is_file() else sys.executable
    command = [python, "-m", "graphify", "update", "."]
    if args.force:
        command.append("--force")
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit").set_defaults(func=command_audit)
    sub.add_parser("validate").set_defaults(func=command_validate)
    migrate = sub.add_parser("migrate")
    migrate.add_argument("--apply", action="store_true")
    migrate.set_defaults(func=command_migrate)
    verify = sub.add_parser("verify-migration")
    verify.add_argument("--write", action="store_true")
    verify.set_defaults(func=command_verify_migration)
    clean = sub.add_parser("clean")
    clean.add_argument("--apply", action="store_true")
    clean.set_defaults(func=command_clean)
    graph = sub.add_parser("graph")
    graph.add_argument("--force", action="store_true")
    graph.set_defaults(func=command_graph)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
