"""Checks the record of Out of Its Milieu against its claims. python3 verify.py"""
import json, re, subprocess, hashlib, gzip, os, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
def first(path):
    out = [l for l in subprocess.run(["git", "log", "--diff-filter=A", "--format=%h", "--", path], capture_output=True, text=True).stdout.split("\n") if l]
    return out[-1] if out else None
def before(a, b):  # a's first commit is a strict ancestor of b's first commit
    ca, cb = first(a), first(b)
    return ca and cb and ca != cb and subprocess.run(["git", "merge-base", "--is-ancestor", ca, cb]).returncode == 0
check("pre-registration before the material", before("PREDICTIONS.md", "sources/fnew-2026-8.csv.gz"))
check("adapters before the material", before("adapt.py", "sources/fnew-2026-8.csv.gz"))
check("instruments carried before the material", before("carried/CARRIED.json", "sources/fnew-2026-8.csv.gz"))
check("instrument outputs before the first reading", before("seen/ear-S.png", "readings/R-1-ear.md") and before("seen/mould.png", "readings/R-1-ear.md"))
check("grid24 outputs before the grid24 reading", before("seen/grid24-V07.png", "readings/R-3-grid24.md"))
for r in ("readings/R-1-ear.md", "readings/R-2-mould.md", "readings/R-3-grid24.md"):
    check(f"{r} before home.py (F3)", before(r, "home.py"))
check("home.py committed before its output", before("home.py", "home.json"))
C = json.load(open("carried/CARRIED.json"))
for p, v in C.items():
    check(f"carried byte-identical: {p}", hashlib.sha256(open(p, "rb").read()).hexdigest() == v["sha256"] ==
          hashlib.sha256(open("../../" + v["copied_from"], "rb").read()).hexdigest())
M = json.load(open("sources/MANIFEST.json"))["sources"][0]
check("material hash (decompressed) equals manifest", hashlib.sha256(gzip.open("sources/fnew-2026-8.csv.gz").read()).hexdigest() == M["sha256"])
R = json.load(open("results.json"))
check("16 claims scored", len(R["claims"]) == 16)
check("strict matches 11/16", R["P3"]["value"] == "11/16")
check("every H-tagged claim was H", all(c["verdict"] == "H" for c in R["claims"] if c["blind"] == "H"))
check("every miss was a G-tag the check called H", all(c["blind"] == "G" and c["verdict"] == "H" for c in R["claims"] if not c["match"]))
check("every miss has a post-hoc entry", all(c["id"] in R["posthoc"] for c in R["claims"] if not c["match"]))
page = open("index.html").read()
check("face carries the same 16 claims", len(re.findall(r'"blind": ?"[GH]"', page)) == 16)
w = len(re.sub(r"[#*`>|\[\]()]", " ", open("work.md").read()).split())
check(f"work.md at most about 600 words ({w})", w <= 640)
for f in ["index.html", "work.md", "meta.json", "figure.svg", "img/month.mp3", "img/ear.jpg", "img/ear-zoom.jpg", "img/mould.jpg", "img/grid24-V07.jpg", "img/grid24-V23.jpg", "img/grid24-V13.jpg"]:
    check("exists " + f, os.path.exists(f))
sys.exit(0 if ok else 1)
