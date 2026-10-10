"""build.py -- writes face-data.js (window.FACE) for index.html from the record: plan, notes, coder answers,
carry.json and carry_i.json. The works are shown in an order shuffled with seed 1192, not by arm."""
import html, json, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f)))
res, carry, ci = J("results.json"), J("carry.json"), J("carry_i.json")
rows = res["rows"]
def note(m):
    t = open(os.path.join(HERE, "makers", m, "NOTE.md"), encoding="utf-8").read().strip().split("\n")
    return t[0].lstrip("# ").strip(), " ".join(x for x in t[1:] if x.strip())
def carried(m):
    a = rows[m]["arm"]
    if a == "I":
        c = ci[m]; return "838 values read back from the plot’s pixels; %d of the 838 exactly as in the source, %d years placed where the source has none%s." % (c["exact"], len(c["years_not_in_source"]), " (counted by this practice\u2019s decode of the drawing, a lower bound)" if m in ("m01", "m10") else "")
    return "all 838 values, exactly, retyped by the maker’s own code from the %s." % ("table" if a == "T" else "sentences")
order = sorted(rows); random.Random(1192).shuffle(order)
works = []
for m in order:
    title, text = note(m)
    if m == "m04":
        text += " [As handed in, the page throws a script error in a browser (it declares a variable named top, which the browser reserves) and shows nothing. The maker had checked it in a stand-in, not a browser.]"
    if m == "m12":
        text += " [The work labels 812 as ‘the first written date, at a flower banquet at court’. The maker’s report says that claim was removed. It was not; it is the maker’s, and this practice did not verify it.]"
    r = rows[m]
    works.append({"id": m, "arm": r["arm"], "title": title, "note": text, "carried": carried(m),
                  "coder": {"guess": r["guess"], "conf": r["conf"], "why": r["why"]}})
lines = open(os.path.join(HERE, "materials", "bloom.csv"), encoding="utf-8").read().split("\n")
snipT = "\n".join(lines[:7]) + "\n…"
snipP = "\n".join(open(os.path.join(HERE, "materials", "bloom.txt"), encoding="utf-8").read().split("\n")[:4]) + "\n…"
hits = sum(1 for m in rows if rows[m]["guess"] == rows[m]["arm"])
after = open(os.path.join(HERE, "after.html"), encoding="utf-8").read()
face = {"snip": {"T": snipT, "P": snipP}, "coderHits": hits, "works": works, "afterHTML": after}
open(os.path.join(HERE, "face-data.js"), "w", encoding="utf-8").write("window.FACE = " + json.dumps(face, ensure_ascii=False, indent=1) + ";\n")
print("ok", len(works), hits)
