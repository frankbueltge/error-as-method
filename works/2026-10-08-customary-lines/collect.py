"""collect.py m01 m02 ... -- copies each maker's index.html and NOTE.md from its scratch folder
(plan.json) into makers/<id>/, with data.js beside it so the work opens as it was made."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p for p in json.load(open(os.path.join(HERE, "plan.json")))}
for m in sys.argv[1:]:
    src, dst = plan[m]["folder"], os.path.join(HERE, "makers", m)
    os.makedirs(dst, exist_ok=True)
    found = sorted(f for f in os.listdir(src) if f != "others")
    for f in ("index.html", "NOTE.md"):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
    shutil.copy(os.path.join(HERE, "data.js"), os.path.join(dst, "data.js"))
    print(m, plan[m]["arm"], "files in folder:", found)
