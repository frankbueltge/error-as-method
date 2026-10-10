"""collect.py -- copies each maker's folder (index.html, NOTE.md; the material they were given is not
copied back, it is in materials/) from /tmp/claude-0/s119/mk/<m>/work to makers/<m>/, and lists any other
file a maker wrote. Reports are pasted verbatim into reports/<m>.md as they arrive."""
import json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
for p in json.load(open(os.path.join(HERE, "plan.json"))):
    src, dst = p["folder"], os.path.join(HERE, "makers", p["maker"])
    os.makedirs(dst, exist_ok=True)
    extra = []
    for f in sorted(os.listdir(src)):
        if f in ("index.html", "NOTE.md"):
            shutil.copy(os.path.join(src, f), dst)
        elif f != p["file"]:
            extra.append(f)
    print(p["maker"], p["arm"], sorted(os.listdir(dst)), "extra:", extra)
