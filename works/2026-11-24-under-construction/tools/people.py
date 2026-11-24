"""Code the people's pages (scored and sheet) with features.code; write people/coded.json.
usage: python3 -I tools/people.py PAGEDIR people/MANIFEST.json people/coded.json"""
import json, sys, os, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import code
pagedir, man, outp = sys.argv[1:4]
m = json.load(open(man))
rows = []
for p in m["pages"]:
    html = open(f"{pagedir}/{p['sha256'][:16]}.html", "rb").read().decode("utf-8", "replace")
    c = code(html); c["role"] = p["role"]; c["sha256"] = p["sha256"]; c["last_modified"] = p["last_modified"]
    rows.append(c)
json.dump(rows, open(outp, "w"), indent=0)
sc = [r for r in rows if r["role"] == "scored"]
print("scored", len(sc), "median iconic", statistics.median(r["n_iconic"] for r in sc),
      "mean", round(statistics.mean(r["n_iconic"] for r in sc), 2))
for k in sc[0]["iconic"]:
    print(f"  {k:20s} {sum(r['iconic'][k] for r in sc)}")
for k in sc[0]["plain"]:
    v = [r["plain"][k] for r in sc]
    print(f"  {k:20s} {statistics.median(v) if not isinstance(v[0], bool) else sum(v)}")
from collections import Counter
print(sorted(Counter(r["n_iconic"] for r in sc).items()))
print("years", sorted(Counter(r["last_modified"][:4] for r in sc).items()))
