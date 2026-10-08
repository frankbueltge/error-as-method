"""collect.py <scratch-root> <maker> -- copies one maker's folder into makers/<maker>/ (index.html, NOTE.md,
renders/ if the viewer made any, and any other file the maker left, listed so the brief's "only those two
files" can be checked). data.js is not copied again; its sha256 is checked against plan.json."""
import hashlib, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
root, m = sys.argv[1], sys.argv[2]
src = os.path.join(root, m, "work")
plan = {p["maker"]: p for p in json.load(open(os.path.join(HERE, "plan.json")))["plan"]}
assert hashlib.sha256(open(os.path.join(src, "data.js"), "rb").read()).hexdigest() == plan[m]["data_sha256"], "data.js changed"
dst = os.path.join(HERE, "makers", m)
os.makedirs(dst, exist_ok=True)
other = []
for dp, dn, fn in os.walk(src):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), src)
        if rel == "data.js":
            continue
        if not (rel in ("index.html", "NOTE.md") or rel.startswith("renders" + os.sep)):
            other.append(rel)
        os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
        shutil.copy(os.path.join(src, rel), os.path.join(dst, rel))
shutil.copy(os.path.join(HERE, "data.js"), os.path.join(dst, "data.js"))
log = os.path.join(src, "renders", "log.jsonl")
looks = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
print(json.dumps({"maker": m, "arm": plan[m]["arm"], "looks": len(looks), "other_files": other}))
