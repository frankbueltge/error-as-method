"""Build face-data.js from people/ and curators/ and results.json. Usage: face_data.py <work dir>"""
import json, os, re, sys
W = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(W, "people/pool-160.jsonl"))]
res = json.load(open(os.path.join(W, "results.json")))
D = json.load(open(os.path.join(W, "people/draws.json")))
KIND = {"P": "person", "X": "other", "S": "settlement", "D": "navigation page", "W": "creative work", "T": "sport",
        "B": "building or site", "O": "organism", "G": "natural feature"}

def section(text, name):
    m = re.search(r"^#+\s*(?:\d+\.\s*)?" + name + r"[^\n]*\n(.*?)(?=^#+\s|\Z)", text, re.M | re.S | re.I)
    return m.group(1).strip() if m else ""

def captions(text, labels):
    body = section(text, "caption")
    out = {}
    for m in re.finditer(r"^\|\s*\**([a-l])\**\s*\|[^|]*\|\s*(.*?)\s*\|\s*`?(typical|unusual)`?\s*\|", body, re.M | re.I):
        out[m.group(1)] = m.group(2)
    if len(out) == 12: return out
    hits = list(re.finditer(r"^[\s>*#|_-]*\(?\**\s*([a-l])\s*[\.\):]", body, re.M))
    for i, h in enumerate(hits):
        seg = body[h.start(): hits[i + 1].start() if i + 1 < len(hits) else len(body)]
        lines = [l.strip() for l in seg.split("\n") if l.strip()]
        first = re.sub(r"^\W*[a-l][\.\):]\s*", "", lines[0])
        rest = " ".join(lines[1:])
        cap = rest if rest else first
        cap = re.sub(r"[*`]|\b(typical|unusual)\b\s*[—:-]?\s*|^[—–-]\s*", "", cap, flags=re.I).strip(" —–-|")
        if h.group(1) not in out: out[h.group(1)] = cap
    return out

def clean(cap, title):
    head = title.split(" (")[0][:12].lower()
    if cap.lower().startswith(head) and " — " in cap:
        cap = cap.split(" — ", 1)[1]
    return cap.strip()

cur = {}
for cid, c in res["curators"].items():
    fin = open(os.path.join(W, "curators", cid, "final.md")).read()
    wall = section(fin, "wall")
    wall = re.sub(r"[*_`]", "", wall)
    caps = captions(fin, "abcdefghijkl")
    its = [x for x in res["items"] if x["cur"] == cid]
    cur[cid] = {"arm": c["arm"], "draw": c["draw"], "rating": c["rating"], "wall": wall,
                "items": [{"n": x["n"], "l": x["label"], "tag": x["tag"], "v1": x["tag_v1"], "cap": clean(caps.get(x["label"], ""), x["title"])} for x in its],
                "replaced": c["replaced"]}
pool = [{"t": r["title"], "k": r["kind"], "w": r["words"], "lead": r["lead"][:220], "u": r["url"]} for r in rows]
out = {"pool": pool, "kinds": KIND, "cur": cur, "draws": D["draws"], "bykind": res["by_kind"],
       "null": {"median": D["tvd_null_median"], "p05": D["tvd_null_p05"], "p95": D["tvd_null_p95"]}}
open(os.path.join(W, "face-data.js"), "w").write("window.RA=" + json.dumps(out, ensure_ascii=False) + ";\n")
print("ok", len(json.dumps(out)))
