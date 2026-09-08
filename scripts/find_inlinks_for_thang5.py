#!/usr/bin/env python3
import re
import sys
import json
import math
import urllib.request
from html import unescape
from xml.etree import ElementTree as ET
from urllib.parse import urlparse
from collections import Counter

SOURCE_URL = "https://heritagevietnamairlines.com/cac-diem-den-ly-tuong-trong-thang-5-duoc-cac-tap-chi-du-lich-viet-nam-goi-y/"
BASE = "https://heritagevietnamairlines.com"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

STOP = set("của và là ở tại với những các một trong cho về từ trên dưới giữa qua theo nơi được đến đi có không này đó khi để như vào ra lại hơn cùng của mình đã đang sẽ hay mà thì vì bởi nên rất cũng còn chỉ người du lịch việt nam heritage bài viết".split())

def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.status, r.read()

def clean_html(s):
    s = re.sub(r"<(script|style|nav|footer|aside)\b[^>]*>.*?</\1>", " ", s, flags=re.I|re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()

def parse_body(html):
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.I|re.S)
    if not h1:
        h1 = re.search(r"<h2\b[^>]*>(.*?)</h2>", html, re.I|re.S)
    title = clean_html(h1.group(1)) if h1 else ""
    start = h1.end() if h1 else 0
    tail = html[start:]
    cut = re.search(r"(?:Có thể bạn cũng quan tâm|Cùng chuyên mục|bài viết liên quan|Bài viết liên quan|### ĐĂNG KÝ|### bài viết liên quan|<footer\b)", tail, re.I)
    if cut:
        tail = tail[:cut.start()]
    body = clean_html(tail)
    return title, body

def get_page_info(url):
    try:
        final_url, status, raw = get(url)
        html = raw.decode("utf-8", "ignore")
        title, body = parse_body(html)
        words = [w for w in re.findall(r"[A-Za-zÀ-ỹĐđ0-9]+", body) if len(w) > 0]
        return {
            "url": final_url,
            "status": status,
            "title": title,
            "body": body,
            "word_count": len(words)
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

def get_all_sitemap_urls():
    try:
        _, _, raw = get(BASE + "/wp-sitemap.xml")
        root = ET.fromstring(raw)
        maps = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and "post-sitemap" in (e.text or "")]
        urls = []
        for sm in maps:
            try:
                _, _, data = get(sm)
                r = ET.fromstring(data)
                urls += [e.text.strip() for e in r.iter() if e.tag.endswith("loc") and e.text and "/en/" not in e.text]
            except Exception as e:
                print(f"Error reading {sm}: {e}", file=sys.stderr)
        return sorted(set(u for u in urls if urlparse(u).path not in ("", "/")))
    except Exception as e:
        print(f"Error fetching sitemaps: {e}", file=sys.stderr)
        return []

def extract_candidate_anchors(body):
    found = []
    # 1. Capitalized proper nouns / entities (2-6 words)
    for m in re.finditer(r"(?<![\wÀ-ỹ])(?:[A-ZÀ-ỸĐ][\wÀ-ỹ’'\-]*(?:\s+|$)){1,6}", body):
        p = m.group(0).strip(" ,.;:–—()[]\"“”'’\n\t")
        toks = p.split()
        if 1 <= len(toks) <= 6 and len(p) >= 3:
            if p.lower() not in STOP:
                found.append(p)
    # 2. Meaningful descriptive noun phrases from sentences (2-5 words)
    for sent in re.split(r"[.!?;:\n]", body):
        toks = sent.strip().split()
        for n in (4, 3, 2):
            for i in range(max(0, len(toks) - n + 1)):
                span = " ".join(toks[i:i+n]).strip(" ,.;:–—()[]\"“”'’\n\t")
                ws = [w.lower() for w in re.findall(r"[A-Za-zÀ-ỹĐđ]+", span)]
                if len(ws) >= 2 and all(len(x) > 1 for x in ws):
                    if ws[0] not in STOP and ws[-1] not in STOP:
                        found.append(span)
    return list(dict.fromkeys(found))

def find_exact_in_body(body, phrase):
    low_b = body.lower()
    low_p = phrase.lower()
    pos = low_b.find(low_p)
    if pos >= 0:
        # verify boundary
        left = body[pos-1] if pos > 0 else " "
        end = pos + len(phrase)
        right = body[end] if end < len(body) else " "
        if not (left.isalnum() or left == '_') and not (right.isalnum() or right == '_'):
            return body[pos:end]
    return None

def main():
    print("Fetching source page...", file=sys.stderr)
    src = get_page_info(SOURCE_URL)
    if "error" in src:
        print(f"Failed to fetch source: {src['error']}", file=sys.stderr)
        return
    print(f"Source Title: {src['title']}", file=sys.stderr)
    print(f"Source Body Word Count: {src['word_count']}", file=sys.stderr)

    # Known candidate target URLs from sitemap / previous research
    candidate_urls = [
        "https://heritagevietnamairlines.com/cau-truong-tien-sau-vai-muoi-hai-nhip/",
        "https://heritagevietnamairlines.com/tham-van-hoa-qua-nhung-cay-cau/",
        "https://heritagevietnamairlines.com/lang-bien-lam-du-lich/",
        "https://heritagevietnamairlines.com/noi-dat-troi-va-bien-giao-hoa/",
        "https://heritagevietnamairlines.com/nhung-cu-dap-ga-xuyen-dam-dai-dat-nuoc/",
        "https://heritagevietnamairlines.com/nhung-cung-duong-trekking-o-quang-binh/",
        "https://heritagevietnamairlines.com/tu-cuc-son-ha/",
        "https://heritagevietnamairlines.com/qua-mien-di-san/",
        "https://heritagevietnamairlines.com/kinh-su-thang-dia/",
        "https://heritagevietnamairlines.com/ky-quan-lang-tam-hue/",
        "https://heritagevietnamairlines.com/cac-loai-hinh-nghe-thuat-duoc-unesco-cong-nhan-viet-nam/",
        "https://heritagevietnamairlines.com/nhung-bai-bien-ky-ao/",
        "https://heritagevietnamairlines.com/du-lich-xanh-trong-long-dat-me/",
        "https://heritagevietnamairlines.com/tu-lan-noi-song-nui-giao-hoa-2/",
        "https://heritagevietnamairlines.com/phong-nha-ke-bang-diem-den-nhung-ky-quan/",
        "https://heritagevietnamairlines.com/ve-tham-lang-gom-thanh-ha/",
        "https://heritagevietnamairlines.com/nhung-bao-tang-hang-dau-viet-nam/",
        "https://heritagevietnamairlines.com/khi-lang-nghe-ke-chuyen-duong-dai/",
        "https://heritagevietnamairlines.com/pho-co-ben-dong-huong-giang/",
        "https://heritagevietnamairlines.com/chu-du-cung-duong-bien-dep-nhat-binh-dinh/",
        "https://heritagevietnamairlines.com/nhung-day-dao-xa-nam-nghe-bien-hat/",
        "https://heritagevietnamairlines.com/nhung-hon-ngoc-cua-vinh-bien-nha-trang/",
        "https://heritagevietnamairlines.com/du-lich-viet-nam-thien-duong-bien-mat-lanh/",
        "https://heritagevietnamairlines.com/dia-diem-du-lich-nha-trang/",
        "https://heritagevietnamairlines.com/lan-bien-o-con-dao/",
        "https://heritagevietnamairlines.com/du-lich-nam-du/",
        "https://heritagevietnamairlines.com/coi-da-dong-van/",
        "https://heritagevietnamairlines.com/giua-thien-nhien-hung-vi/",
        "https://heritagevietnamairlines.com/doc-mien-dat-nuoc-kham-pha-cac-le-hoi-o-viet-nam-trong-thang-3-4/",
        "https://heritagevietnamairlines.com/xuan-ve-tren-nhung-kinh-thanh-cu/",
        "https://heritagevietnamairlines.com/den-hoi-an-tham-lang-rau-tra-que/",
        "https://heritagevietnamairlines.com/quy-nhon-thenh-thang-bien-nui-may-troi/",
        "https://heritagevietnamairlines.com/duoi-bong-tram-tich-ly-son/",
        "https://heritagevietnamairlines.com/man-ma-vi-bien-ly-son/",
        "https://heritagevietnamairlines.com/kham-pha-khong-gian-bien-xanh-yen-binh-o-nha-trang-trong-dip-2-9/",
        "https://heritagevietnamairlines.com/nhip-song-dong-nai-va-khoang-xanh-cat-tien/",
        "https://heritagevietnamairlines.com/ba-lang-an-kiet-tac-cua-nuoc-va-lua/",
        "https://heritagevietnamairlines.com/du-lich-ninh-binh-san-sang-don-khach-dip-quoc-khanh-2-9/"
    ]

    # Fetch sitemap to add more candidate URLs
    sitemap_list = get_all_sitemap_urls()
    for u in sitemap_list:
        if u not in candidate_urls and u != SOURCE_URL:
            candidate_urls.append(u)

    print(f"Total candidate URLs to evaluate: {len(candidate_urls)}", file=sys.stderr)

    src_anchors = extract_candidate_anchors(src["body"])
    print(f"Extracted {len(src_anchors)} candidate anchor phrases from source body.", file=sys.stderr)

    results = []
    
    for i, target_url in enumerate(candidate_urls):
        if target_url == SOURCE_URL:
            continue
        tgt = get_page_info(target_url)
        if "error" in tgt or tgt["word_count"] < 1000:
            continue
        
        # Check matching anchors
        matched_anchors = []
        for a in src_anchors:
            hit = find_exact_in_body(tgt["body"], a)
            if hit:
                # Calculate relevance/specificity
                matched_anchors.append(a)
        
        if matched_anchors:
            results.append({
                "target_url": tgt["url"],
                "target_title": tgt["title"],
                "target_word_count": tgt["word_count"],
                "matched_anchors": matched_anchors
            })
            print(f"[{len(results)}] Match: {tgt['title']} ({tgt['word_count']} words) -> {len(matched_anchors)} anchors", file=sys.stderr)

    print(json.dumps({
        "source": {
            "url": src["url"],
            "title": src["title"],
            "word_count": src["word_count"]
        },
        "qualified_targets": results
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
