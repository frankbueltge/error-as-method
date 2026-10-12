"""coders.py: sets up both coders' folders. Coder A gets the twelve masked screenshots renamed w01-w12 in an
order shuffled with seed 1221 (key in keys/A.json, committed before coder A runs). Coder B gets the twelve
NOTE.md files and the twelve reports as mNN-note.md / mNN-report.md (maker numbers kept; the grain is not told)."""
import json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ms = ["m%02d" % i for i in range(1, 13)]
order = ms[:]; random.Random(1221).shuffle(order)
key = {"w%02d" % (i + 1): m for i, m in enumerate(order)}
os.makedirs(os.path.join(HERE, "keys"), exist_ok=True)
json.dump(key, open(os.path.join(HERE, "keys", "A.json"), "w"), indent=1)
A, B = "/tmp/claude-0/s122/cA", "/tmp/claude-0/s122/cB"
for d in (A, B): shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
for w, m in key.items(): shutil.copy(os.path.join(HERE, "shots", "masked", m + ".png"), os.path.join(A, w + ".png"))
for m in ms:
    shutil.copy(os.path.join(HERE, "makers", m, "NOTE.md"), os.path.join(B, m + "-note.md"))
    shutil.copy(os.path.join(HERE, "reports", m + ".md"), os.path.join(B, m + "-report.md"))
for c, d in (("A", A), ("B", B)):
    t = open(os.path.join(HERE, "coder", c, "BRIEF.md")).read().replace("{FOLDER}", d)
    open(os.path.join(HERE, "coder", c, "BRIEF.run.md"), "w").write(t)
print(key)
