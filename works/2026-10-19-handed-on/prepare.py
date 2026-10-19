"""prepare.py -- builds data.js from the Nobel Foundation's laureate list and lays out the six lineages.

python3 prepare.py <scratch-root>

Six lineages, one material, one first brief (briefs/brief.md), one viewer each (render.js, Session 117's file).
Each lineage has four versions, v1 to v4. The arm of each lineage is drawn here with seed 140, before any maker:

  P  hand-over, plain: v2, v3, v4 are each made by a NEW maker, fresh, who sees only the folder: the last
     index.html, the lineage's NOTE.md, current.png, data.js, the viewer.                  (briefs/plain.md)
  T  hand-over, test: the same, with the working paper's I2 test and its halt.              (briefs/test.md)
  K  kept: the v1 maker is sent back three times in the same conversation with Session 139's
     sentence, "Make the next version of your work."                                        (briefs/again-K.md)

Every room is a folder outside this repository with a neutral name drawn here, so neither the experiment's
name nor the lineage's arm is in reach of a maker (F-195).
"""
import json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 140
FIELDS = ["year", "category", "name", "kind", "born", "country", "share", "motivation", "amount_sek_today"]


def frac(s):
    a, b = (s.split("/") + ["1"])[:2]
    return round(int(a) / int(b), 4)


def rows():
    out = []
    for x in json.load(open(os.path.join(HERE, "sources", "laureates.json")))["laureates"]:
        org = "orgName" in x
        name = (x["orgName"] if org else x.get("knownName") or x["fullName"])["en"]
        kind = "organisation" if org else {"female": "woman", "male": "man"}.get(x.get("gender"), None)
        b = x.get("founded" if org else "birth") or {}
        born = (b.get("date") or "")[:4]
        born = int(born) if born.isdigit() else None
        place = b.get("place") or {}
        country = (place.get("countryNow") or {}).get("en")
        for p in x["nobelPrizes"]:
            out.append([int(p["awardYear"]), p["category"]["en"], name, kind, born, country, frac(p["portion"]),
                        (p.get("motivation") or {}).get("en"), p.get("prizeAmountAdjusted")])
    return sorted(out, key=lambda r: (r[0], r[1], r[2]))


def data_js(rs):
    return "window.PRIZES = " + json.dumps({
        "source": "Nobel Prize API v2.1, laureates, api.nobelprize.org, fetched 2026-10-19 (CC0)",
        "fields": FIELDS, "count": len(rs), "rows": rs}, separators=(",", ":"), ensure_ascii=False) + ";\n"


if __name__ == "__main__":
    root = os.path.abspath(sys.argv[1])
    rs = rows()
    open(os.path.join(HERE, "data.js"), "w").write(data_js(rs))
    rng = random.Random(SEED)
    arms = ["P", "P", "T", "T", "K", "K"]
    rng.shuffle(arms)
    rooms = ["r%02d" % i for i in range(1, 19)]
    rng.shuffle(rooms)
    lineages = []
    for i, arm in enumerate(arms, 1):
        L = "L%d" % i
        n = 4 if arm in "PT" else 1  # P and T need a room per maker; K keeps one room
        lineages.append({"lineage": L, "arm": arm, "rooms": [os.path.join(root, "rooms", rooms.pop()) for _ in range(n)]})
    os.makedirs(os.path.join(root, "viewer"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "render.js"), os.path.join(root, "viewer", "render.js"))
    for L in lineages:
        for r in L["rooms"]:
            os.makedirs(r, exist_ok=True)
            shutil.copy(os.path.join(HERE, "data.js"), r)
    json.dump({"seed": SEED, "render": os.path.join(root, "viewer", "render.js"), "lineages": lineages},
              open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print(len(rs), "rows;", [(L["lineage"], L["arm"]) for L in lineages])
