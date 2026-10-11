"""build.py -- writes face-data.js for the face from plan.json, ledger.json, coder/answers.json, keys/coder.json,
the makers' NOTE.md files and the source table. Also computes where 9 September 2009 (16,081 births, the busiest
day) sits in each picture, by the same formulas prepare.py drew them with, for the face's lens."""
import csv, datetime, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
plan, L, A, K = J("plan.json"), J("ledger.json"), J("coder/answers.json"), J("keys/coder.json")
coder = {K[p]["maker"]: A[p] for p in K}
d0, d1, lo, hi = datetime.date(2000, 1, 1), datetime.date(2015, 1, 1), 5000, 17000
def xy(d, b, W, Hh, Lm, Rm, Tm, Bm):
    return (Lm + (d - d0).days / (d1 - d0).days * (W - Lm - Rm), Tm + (hi - b) / (hi - lo) * (Hh - Tm - Bm))
day = datetime.date(2009, 9, 9)
rows = list(csv.reader(open(os.path.join(H, "materials", "births.csv"), encoding="utf-8")))
hit = [",".join(r) for r in rows if r[:3] == ["2009", "9", "9"]][0]
assert hit.endswith(",16081")
works = []
order = [p["maker"] for p in plan if p["arm"] == "T"] + [p["maker"] for p in plan if p["arm"] == "I"] + [p["maker"] for p in plan if p["arm"] == "L"]
for m in order:
    note = open(os.path.join(H, "makers", m, "NOTE.md"), encoding="utf-8").read().strip().split("\n")
    title = note[0].lstrip("# ").strip()
    body = " ".join(x.strip() for x in note[1:] if x.strip())
    works.append({"id": m, "arm": L[m]["arm"], "title": title, "note": body, "unit": L[m]["unit"], "form": L[m]["form"],
                  "named": L[m]["named"], "coder": {"close": coder[m]["close"], "guess": coder[m]["guess"], "conf": coder[m]["conf"]}})
face = {"snip": "\n".join(",".join(r) for r in rows[:6]) + "\n…\n" + hit + "\n…",
        "hitRow": hit,
        "lens": {"png": dict(zip(("x", "y"), xy(day, 16081, 1100, 500, 80, 20, 20, 50))), "jpg": dict(zip(("x", "y"), xy(day, 16081, 480, 220, 6, 6, 6, 6)))},
        "named": list(next(iter(L.values()))["named"].keys()), "works": works}
open(os.path.join(H, "face-data.js"), "w", encoding="utf-8").write("window.FACE = " + json.dumps(face, ensure_ascii=False, indent=1) + ";\n")
print(face["lens"], len(works))
