"""prepare.py -- builds data.js from the archive's table and lays out the six makers' rooms.

python3 prepare.py <scratch-root>

Six makers, one brief, one material, one viewer each (render.js, Session 117's file). After the first version
every maker is sent back five times with one fixed sentence, in the same conversation, so it keeps its memory:

  K  "Make the next version of your work."                                             (briefs/again-K.md)
  D  "Make the next version of your work, or, if you judge the work finished, say so
      and change nothing."                                                             (briefs/again-D.md)

A D maker that declines is not sent back again. Arms are drawn with seed 139. The rooms are outside this
repository, so the experiment's name is not in reach of the makers (F-195).
"""
import csv, json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 139
FIELDS = ["name", "star", "year", "method", "period_days", "radius_earth", "mass_earth", "distance_pc"]


def num(s, nd):
    return None if s == "" else round(float(s), nd)


def rows():
    out = []
    for r in csv.DictReader(open(os.path.join(HERE, "sources", "pscomppars.csv"))):
        out.append([r["pl_name"], r["hostname"], int(r["disc_year"]), r["discoverymethod"],
                    num(r["pl_orbper"], 5), num(r["pl_rade"], 3), num(r["pl_bmasse"], 3), num(r["sy_dist"], 3)])
    return sorted(out, key=lambda x: (x[2], x[0]))


def data_js(rs):
    return "window.PLANETS = " + json.dumps({
        "source": "NASA Exoplanet Archive, Planetary Systems Composite Parameters (pscomppars), fetched 2026-10-19",
        "fields": FIELDS, "count": len(rs), "rows": rs}, separators=(",", ":"), ensure_ascii=False) + ";\n"


if __name__ == "__main__":
    root = os.path.abspath(sys.argv[1])
    rs = rows()
    body = data_js(rs)
    open(os.path.join(HERE, "data.js"), "w").write(body)
    arms = ["K"] * 3 + ["D"] * 3
    random.Random(SEED).shuffle(arms)
    plan = []
    t = open(os.path.join(HERE, "briefs", "brief.md")).read()
    os.makedirs(os.path.join(HERE, "briefs", "run"), exist_ok=True)
    for i, arm in enumerate(arms, 1):
        mid = "m%02d" % i
        folder = os.path.join(root, mid, "work"); view = os.path.join(root, mid, "viewer")
        os.makedirs(folder, exist_ok=True); os.makedirs(view, exist_ok=True)
        open(os.path.join(folder, "data.js"), "w").write(body)
        shutil.copy(os.path.join(HERE, "render.js"), os.path.join(view, "render.js"))
        b = t.replace("{FOLDER}", folder).replace("{RENDER}", os.path.join(view, "render.js"))
        open(os.path.join(HERE, "briefs", "run", mid + ".md"), "w").write(b)
        plan.append({"maker": mid, "arm": arm, "folder": folder})
    json.dump({"seed": SEED, "count": len(rs), "makers": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print(len(rs), "planets;", " ".join(p["maker"] + p["arm"] for p in plan))
