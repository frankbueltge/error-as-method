"""collect.py <maker> <first|second> <report-file>

Copies the maker's scratch folder (index.html, NOTE.md, renders/) into makers/<maker>/<stage>/ and
its report, verbatim, into reports/<maker>-<stage>.md. Checks that data.js is unchanged.
"""
import json, os, sys, shutil, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
mid, stage, rep = sys.argv[1], sys.argv[2], sys.argv[3]
plan = {p["maker"]: p for p in json.load(open(os.path.join(HERE, "plan.json")))["plan"]}[mid]
src = plan["folder"]
d = hashlib.sha256(open(os.path.join(src, "data.js"), "rb").read()).hexdigest()
assert d == plan["data_sha256"], "data.js changed"
dst = os.path.join(HERE, "makers", mid, stage)
if os.path.exists(dst): shutil.rmtree(dst)
os.makedirs(dst)
for f in sorted(os.listdir(src)):
    if f == "data.js": continue
    s = os.path.join(src, f)
    (shutil.copytree if os.path.isdir(s) else shutil.copy)(s, os.path.join(dst, f))
os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
shutil.copy(rep, os.path.join(HERE, "reports", "%s-%s.md" % (mid, stage)))
extra = sorted(set(os.listdir(src)) - {"data.js", "index.html", "NOTE.md", "renders"})
print(mid, stage, "copied;", "extra files:", extra or "none")
