"""shelf.py: the union of each instrument's two shelf lists, alphabetised, and the blind labels S1-S5
(seed 149) under which coder A sees them beside experiment 28's general shelf."""
import json, os, random, re
H = os.path.dirname(os.path.abspath(__file__)); out = {}
for t in ["PLOT", "CYCLES", "GAPS", "DIGITS"]:
    lines = []
    for k in (1, 2):
        lines += [re.sub(r"^\d+\.\s*", "", l).strip() for l in open(os.path.join(H, "shelf", "%s-%d.txt" % (t, k))) if l.strip()]
    out[t] = sorted(lines)
out["GENERAL28"] = [l.strip() for l in open(os.path.join(H, "..", "2026-10-20-first-to-hand", "shelf", "shelf.txt")) if l.strip()]
names = list(out); random.Random(149).shuffle(names)
key = {"S%d" % (i + 1): n for i, n in enumerate(names)}
os.makedirs(os.path.join(H, "coder"), exist_ok=True)
for s, n in key.items():
    open(os.path.join(H, "coder", s + ".txt"), "w").write("\n".join(out[n]) + "\n")
json.dump(key, open(os.path.join(H, "coder", "shelf-key.json"), "w"), indent=1)
print(key, {n: len(v) for n, v in out.items()})
