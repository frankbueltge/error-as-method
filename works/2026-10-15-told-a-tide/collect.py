"""collect.py <maker>: copies the maker's index.html and NOTE.md from its work folder into makers/<maker>/, and
lists (does not copy) its scratch folder into makers/<maker>/SCRATCH.txt with sizes and SHA-256, so a reader can
see what the maker wrote for itself. The scratch scripts are copied to makers/<maker>/scratch/ if they are text
under 200 kB (they are the evidence of decoding)."""
import hashlib, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p for p in json.load(open(os.path.join(HERE, "plan.json")))}
m = sys.argv[1]; p = plan[m]; out = os.path.join(HERE, "makers", m); os.makedirs(out, exist_ok=True)
for fn in ("index.html", "NOTE.md"):
    s = os.path.join(p["folder"], fn)
    if os.path.exists(s): shutil.copy(s, os.path.join(out, fn))
lines = []
for root, _, files in os.walk(p["scratch"]):
    for fn in sorted(files):
        s = os.path.join(root, fn); rel = os.path.relpath(s, p["scratch"]); b = open(s, "rb").read()
        lines.append("%8d  %s  %s" % (len(b), hashlib.sha256(b).hexdigest()[:16], rel))
        if len(b) < 200_000 and fn.rsplit(".", 1)[-1] in ("py", "js", "mjs", "txt", "md", "json", "csv", "sh", "html", "svg", "tsv"):
            d = os.path.join(out, "scratch", os.path.dirname(rel)); os.makedirs(d, exist_ok=True); shutil.copy(s, os.path.join(d, fn))
open(os.path.join(out, "SCRATCH.txt"), "w").write("\n".join(lines) + "\n")
print(m, p["cell"], len(lines), "scratch files")
