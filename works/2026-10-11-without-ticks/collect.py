"""collect.py -- copies each maker's index.html and NOTE.md from its work folder to makers/<m>/, and lists
(name, bytes, sha256 prefix) every file in its scratch folder to makers/<m>/SCRATCH.json. Scripts in the
scratch folder (.py, .js, .sh, .mjs) are copied to makers/<m>/scratch/ as evidence of what the maker did with its
file (M1); data files are listed, not copied. Reports are pasted verbatim into reports/<m>.md as they arrive."""
import hashlib, json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
for p in json.load(open(os.path.join(HERE, "plan.json"))):
    dst = os.path.join(HERE, "makers", p["maker"])
    os.makedirs(dst, exist_ok=True)
    extra = []
    for f in sorted(os.listdir(p["folder"])):
        if f in ("index.html", "NOTE.md"):
            shutil.copy(os.path.join(p["folder"], f), dst)
        elif f != p["file"]:
            extra.append(f)
    listing = []
    for root, _, files in os.walk(p["scratch"]):
        for f in sorted(files):
            fp = os.path.join(root, f); rel = os.path.relpath(fp, p["scratch"])
            b = open(fp, "rb").read()
            listing.append({"file": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()[:16]})
            if os.path.splitext(f)[1] in (".py", ".js", ".sh", ".mjs") and len(b) < 200000:
                os.makedirs(os.path.join(dst, "scratch", os.path.dirname(rel)), exist_ok=True)
                shutil.copy(fp, os.path.join(dst, "scratch", rel))
    json.dump({"work_extra": extra, "scratch": listing}, open(os.path.join(dst, "SCRATCH.json"), "w"), indent=1)
    print(p["maker"], p["arm"], sorted(os.listdir(dst)), "extra:", extra, "scratch files:", len(listing))
