"""Build face-data.js: per page a declared background colour, whether it tiles an image, and its iconic markers.
People's pages carry no path or title, only the order of the draw. usage: python3 -I tools/facedata.py PAGEDIR"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import code
from bgcolor import bg
pagedir = sys.argv[1]
man = json.load(open("people/MANIFEST.json")); res = json.load(open("results.json"))
KEYS = list(res["people"]["rates"].keys())[:12]
def row(html):
    c = code(html); col, img = bg(html)
    return {"bg": col, "img": img, "m": [i for i, k in enumerate(KEYS) if c["iconic"][k]], "w": c["plain"]["words"]}
people = [row(open(f"{pagedir}/{p['sha256'][:16]}.html", "rb").read().decode("utf-8", "replace"))
          for p in man["pages"] if p["role"] == "scored"]
makers = {}
for m in sorted(os.listdir("makings")):
    r = row(open(f"makings/{m}/index.html", encoding="utf-8", errors="replace").read())
    r["est"] = res["makers"][m]["estimates"]; r["traj"] = res["makers"][m]["trajectory"]; makers[m] = r
out = {"keys": KEYS, "people": people, "makers": makers, "rates": res["people"]["rates"],
       "sheet_rates": res["sheet"]["rates"], "pred": res["predictions"]}
open("face-data.js", "w").write("window.FACE=" + json.dumps(out, separators=(",", ":")) + ";\n")
print(len(people), len(makers), KEYS)
