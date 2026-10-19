"""handover.py <lineage> <version> -- lays out the room of the fresh maker who makes version k of a P or T lineage.

Copies the kept v(k-1) index.html and NOTE.md into room k, and the kept render of v(k-1) as current.png.
Writes the maker's brief to briefs/run/<L>-v<k>.md from briefs/plain.md or briefs/test.md, filled in.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
L, k = sys.argv[1], int(sys.argv[2])
plan = json.load(open(os.path.join(HERE, "plan.json")))
lin = {x["lineage"]: x for x in plan["lineages"]}[L]
assert lin["arm"] in "PT" and k >= 2
room = lin["rooms"][k - 1]
prev = os.path.join(HERE, "lineages", L, "v%d" % (k - 1))
for f in ("index.html", "NOTE.md"):
    shutil.copy(os.path.join(prev, f), os.path.join(room, f))
shutil.copy(os.path.join(HERE, "shots", "%s-v%d.png" % (L, k - 1)), os.path.join(room, "current.png"))
t = open(os.path.join(HERE, "briefs", "plain.md" if lin["arm"] == "P" else "test.md")).read()
t = t.replace("{FOLDER}", room).replace("{RENDER}", plan["render"]).replace("{K}", str(k))
os.makedirs(os.path.join(HERE, "briefs", "run"), exist_ok=True)
open(os.path.join(HERE, "briefs", "run", "%s-v%d.md" % (L, k)), "w").write(t)
print(room)
