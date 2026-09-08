#!/usr/bin/env python3
import argparse, concurrent.futures as cf
import json, math, re, sys, urllib.request, zipfile
from collections import Counter
from html import unescape
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

BASE = "https://heritagevietnamairlines.com"
UA = {"User-Agent": "Mozilla/5.0 InternalLinkResearch/1.0"}
STOP = set("của và là ở tại với những các một trong cho về từ trên dưới giữa qua theo nơi được đến đi có không này đó khi để như vào ra lại hơn cùng của mình đã đang sẽ hay mà thì vì bởi nên rất cũng còn chỉ người du lịch việt nam heritage".split())

def get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.status, r.read()

def clean_html(s):
    s = re.sub(r"<(script|style|nav|footer|aside)\b[^>]*>.*?</\1>", " ", s, flags=re.I|re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()

def parse_page(url):
    final, status, raw = get(url)
    html = raw.decode("utf-8", "ignore")
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.I|re.S)
    if not h1:
        h1 = re.search(r"<h2\b[^>]*>(.*?)</h2>", html, re.I|re.S)
    title = clean_html(h1.group(1)) if h1 else ""
    start = h1.end() if h1 else 0
    tail = html[start:]
    cut = re.search(r"(?:Có thể bạn cũng quan tâm|Cùng chuyên mục|bài viết liên quan|Bài viết liên quan|### ĐĂNG KÝ|<footer\b)", tail, re.I)
    if cut: tail = tail[:cut.start()]
    body = clean_html(tail)
    return {"url": final, "status": status, "title": title, "body": body}

def sitemap_urls():
    _,_,raw = get(BASE + "/wp-sitemap.xml")
    root = ET.fromstring(raw)
    maps = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and "post-sitemap" in (e.text or "")]
    urls=[]
    for sm in maps:
        try:
            _,_,data=get(sm); r=ET.fromstring(data)
            urls += [e.text.strip() for e in r.iter() if e.tag.endswith("loc") and e.text and "/en/" not in e.text]
        except Exception as exc: print("sitemap error",sm,exc,file=sys.stderr)
    return sorted(set(u for u in urls if urlparse(u).path not in ("", "/")))

def xlsx_urls(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read("xl/sharedStrings.xml"))
    vals=[]
    for si in root:
        value="".join((node.text or "") for node in si.iter() if node.tag.endswith("}t"))
        if value.startswith("http"): vals.append(value.strip())
    return list(dict.fromkeys(vals))

def words(s):
    return [w.lower() for w in re.findall(r"[A-Za-zÀ-ỹĐđ]+", s) if len(w)>1 and w.lower() not in STOP]

def phrases(body):
    # Preserve exact surface form; favor capitalized entities and compact noun-like spans.
    found=[]
    for m in re.finditer(r"(?<![\wÀ-ỹ])(?:[A-ZÀ-ỸĐ][\wÀ-ỹ’'\-]*(?:\s+|$)){1,6}", body):
        p=m.group(0).strip(" ,.;:–—()[]\"“”")
        if 2 <= len(words(p)) <= 6 and len(p)>=4: found.append(p)
    # Known descriptive spans discovered by punctuation boundaries.
    for sent in re.split(r"[.!?;:\n]", body):
        toks=sent.strip().split()
        for n in (4,3,2):
            for i in range(max(0,len(toks)-n+1)):
                p=" ".join(toks[i:i+n]).strip(" ,.;:–—()[]\"“”")
                ws=words(p)
                if len(ws)>=2 and all(len(x)>2 for x in ws): found.append(p)
    return list(dict.fromkeys(found))

def title_candidates(title):
    toks=re.findall(r"[A-Za-zÀ-ỹĐđ0-9]+", title)
    out=[]
    for n in range(min(6,len(toks)),0,-1):
        for i in range(len(toks)-n+1):
            raw=" ".join(toks[i:i+n]); ws=words(raw)
            if not ws: continue
            raw_parts=raw.lower().split()
            if raw_parts[0] in STOP or raw_parts[-1] in STOP: continue
            if n==1: continue
            elif len(ws)<2 and n<3: continue
            # Exclude title boilerplate and generic intent phrases.
            if any(x in raw.lower() for x in ("điểm du lịch", "việt nam", "heritage guide", "hành trình", "khám phá")) and len(ws)<3: continue
            out.append(raw)
    return list(dict.fromkeys(out))

def find_surface(body, raw):
    low=body.lower(); needle=raw.lower(); start=0
    while True:
        pos=low.find(needle,start)
        if pos<0: return None
        left=body[pos-1] if pos else " "
        end=pos+len(raw); right=body[end] if end<len(body) else " "
        if not (left.isalnum() or left=="_") and not (right.isalnum() or right=="_"):
            return body[pos:end]
        start=pos+1

def tf(doc): return Counter(words(doc))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--xlsx", help="Workbook whose first-column shared strings are source URLs")
    args=ap.parse_args()
    outdir=Path("research-output"); outdir.mkdir(exist_ok=True)
    urls=xlsx_urls(args.xlsx) if args.xlsx else sitemap_urls(); print("URLs",len(urls),file=sys.stderr)
    cache=outdir/"heritage-pages-cache.json"
    if cache.exists():
        saved=json.loads(cache.read_text(encoding="utf-8")); pages=saved["pages"]; errors=saved["errors"]
        print("loaded cache",len(pages),file=sys.stderr)
    else:
        pages=[]; errors=[]
        with cf.ThreadPoolExecutor(max_workers=16) as ex:
            futs={ex.submit(parse_page,u):u for u in urls}
            for i,f in enumerate(cf.as_completed(futs),1):
                try:
                    p=f.result()
                    if p["title"] and len(p["body"])>200: pages.append(p)
                    else: errors.append({"url":futs[f],"error":"thin/unparsed"})
                except Exception as exc: errors.append({"url":futs[f],"error":repr(exc)})
                if i%100==0: print("fetched",i,file=sys.stderr)
        cache.write_text(json.dumps({"pages":pages,"errors":errors},ensure_ascii=False),encoding="utf-8")
    pages.sort(key=lambda p:p["url"])
    dfs=Counter()
    tfs=[]
    for p in pages:
        t=tf(p["title"]+" "+p["body"][:5000]); tfs.append(t); dfs.update(t.keys())
    N=len(pages)
    vecs=[]
    for t in tfs:
        v={w:(1+math.log(c))*math.log((N+1)/(dfs[w]+1)) for w,c in t.items()}
        norm=math.sqrt(sum(x*x for x in v.values())) or 1
        vecs.append({w:x/norm for w,x in v.items()})
    title_words=[set(words(p["title"])) for p in pages]
    title_phrases=[title_candidates(p["title"]) for p in pages]
    rows=[]; insufficient=[]
    for i,src in enumerate(pages):
        pv=phrases(src["body"])
        rough=[]
        for j,dst in enumerate(pages):
            if i==j: continue
            overlap=set(vecs[i]) & set(vecs[j])
            cosine=sum(vecs[i][w]*vecs[j][w] for w in overlap)
            title_hit=len(set(tfs[i]) & title_words[j])
            if cosine>=0.055 and title_hit: rough.append((cosine+title_hit*.08,j,cosine))
        rough.sort(reverse=True)
        candidates=[]
        for _,j,cosine in rough[:160]:
            best=None
            for raw in title_phrases[j]:
                ph=find_surface(src["body"],raw)
                if not ph: continue
                pw=set(words(ph)); shared=pw & title_words[j]
                rare=sum(1 for w in pw if dfs[w] <= max(4, N*.10))
                if not rare or cosine < 0.08: continue
                if ph.lower() in {"trăm năm tuổi","vườn quốc gia","thành phố đang","vẻ đẹp hoang sơ","thiên nhiên hùng vĩ","bốn mùa hoa"}: continue
                coverage=len(shared)/max(1,len(title_words[j]))
                specificity=sum(math.log((N+1)/(dfs[w]+1)) for w in pw)/len(pw)
                score=cosine*8 + coverage*1.4 + len(shared)*.45 + specificity*.18
                if len(ph)>70: continue
                if best is None or score>best[0]: best=(score,ph)
            if best: candidates.append((best[0],best[1],j,cosine))
        candidates.sort(reverse=True)
        used_targets=set(); used_anchors=[]; chosen=[]
        for score,anchor,j,cos in candidates:
            al=anchor.lower()
            if j in used_targets or any(al in x or x in al for x in used_anchors): continue
            used_targets.add(j); used_anchors.append(al)
            chosen.append({"source_url":src["url"],"source_title":src["title"],"anchor_text":anchor,
                           "target_url":pages[j]["url"],"target_title":pages[j]["title"],
                           "reason":"Cùng thực thể/chủ đề được thể hiện trong tiêu đề và nội dung bài đích.",
                           "confidence":"Cao" if cos>=0.14 else "Trung bình","verification":"Anchor khớp nguyên văn; URL live"})
            if len(chosen)==3: break
        rows += chosen
        if len(chosen)<3: insufficient.append({"url":src["url"],"title":src["title"],"count":len(chosen)})
    (outdir/"heritage-internal-links.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    md=["# Nghiên cứu internal link – Heritage Vietnam Airlines (mở rộng)","",f"- Ngày nghiên cứu: 06/08/2026",f"- Bài đã đọc: {len(pages)}",f"- Đề xuất đạt tiêu chí: {len(rows)}",f"- Bài chưa đủ 3 anchor mạnh: {len(insufficient)}","",]
    current=None
    for r in rows:
        if r["source_url"]!=current:
            current=r["source_url"]; md += [f"## {r['source_title']}","",f"Nguồn: {current}","","| Anchor text | URL đích | Bài đích | Độ tin cậy |","|---|---|---|---|"]
        md.append(f"| {r['anchor_text'].replace('|','/')} | {r['target_url']} | {r['target_title'].replace('|','/')} | {r['confidence']} |")
    md += ["","## Các bài chưa đủ 3 anchor mạnh","","| Bài nguồn | Số link đạt tiêu chí |","|---|---:|"]
    md += [f"| {x['url']} | {x['count']} |" for x in insufficient]
    (outdir/"heritage-internal-links.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    (outdir/"crawl-errors.json").write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"pages":len(pages),"rows":len(rows),"insufficient":len(insufficient),"errors":len(errors)}))

if __name__=="__main__": main()
