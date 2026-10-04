"""Harvest every arXiv record whose comment contains 'withdrawn' (Session 104).

One pass of the public API, pages of 1000, at least 3.5 s between requests
(arXiv API terms: no more than one request every three seconds).
Writes notices.json (id, published, updated, primary category, title, comment)
and harvest-log.json (each request: url, status, bytes, sha256, entries).
Descriptive metadata is CC0: https://info.arxiv.org/help/api/tou.html
"""
import hashlib, json, time, urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query?search_query=co:withdrawn&start={start}&max_results={n}&sortBy=submittedDate&sortOrder=ascending"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom",
      "o": "http://a9.com/-/spec/opensearch/1.1/"}
PAGE = 1000

def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.status, r.read()
        except Exception as e:
            print("retry", attempt, e); time.sleep(10 * (attempt + 1))
    raise SystemExit("harvest failed: " + url)

rows, log, start, total = {}, [], 0, None
while total is None or start < total:
    url = API.format(start=start, n=PAGE)
    status, body = get(url)
    root = ET.fromstring(body)
    total = int(root.find("o:totalResults", NS).text)
    entries = root.findall("a:entry", NS)
    log.append({"url": url, "status": status, "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(), "entries": len(entries),
                "totalResults": total, "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    print(start, status, len(entries), total, flush=True)
    for e in entries:
        aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[1]
        c = e.find("x:comment", NS)
        pc = e.find("x:primary_category", NS)
        rows[aid] = {"id": aid, "published": e.find("a:published", NS).text[:10],
                     "updated": e.find("a:updated", NS).text[:10],
                     "cat": pc.get("term") if pc is not None else None,
                     "title": " ".join(e.find("a:title", NS).text.split()),
                     "comment": " ".join(c.text.split()) if c is not None and c.text else ""}
    if not entries:  # the API sometimes returns an empty page; retry once later
        time.sleep(10)
        status, body = get(url); root = ET.fromstring(body)
        if not root.findall("a:entry", NS):
            log[-1]["note"] = "empty page twice; skipped"
    start += PAGE
    time.sleep(3.5)

json.dump(sorted(rows.values(), key=lambda r: r["id"]), open("notices.json", "w"), ensure_ascii=False, indent=0)
json.dump(log, open("harvest-log.json", "w"), indent=1)
print("records", len(rows), "of totalResults", total)
