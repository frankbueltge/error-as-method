"""prepare.py -- builds data.js from the Wikimedia file and lays out the makers' folders.

python3 prepare.py round1 <scratch-root>    six makers, plain brief (the family's own map)
python3 prepare.py round2 <scratch-root>    twelve makers in three arms, after round 1 is committed

The makers work outside this repository, in <scratch-root>/<id>/work/, so that nothing of this
experiment's name is in reach of them (F-195, Session 114). data.js and the viewport are the same
bytes for every maker. Only the brief's two slots vary by arm:

  R  round 1, plain                     {OTHERS} empty, {DEPART} empty
  D  round 2, plain                     {OTHERS} empty, {DEPART} empty
  B  round 2, shown                     {OTHERS} names the folder others/ (round 1's pictures and notes)
  C  round 2, shown and asked to depart {OTHERS} as B, {DEPART} "Make a work that is none of them."
"""
import json, os, random, sys, hashlib, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 116
OTHERS = ("\n\nAlso in your folder is `others/`. It holds six works other makers made from this same brief and "
          "this same material: a picture of each as it is seen at 1100 × 800 (`o1.png` to `o6.png`) and each "
          "maker's note (`o1.md` to `o6.md`).")
DEPART = " Make a work that is none of them."


def data_js():
    items = json.load(open(os.path.join(HERE, "sources", "moon-2025.json")))["items"]
    assert len(items) == 365
    assert items[0]["timestamp"].startswith("20250101") and items[-1]["timestamp"].startswith("20251231")
    days = [int(i["views"]) for i in items]
    return "window.VIEWS = " + json.dumps({"article": "Moon", "project": "en.wikipedia", "agent": "user",
                                          "first": "2025-01-01", "step": "1 day", "days": days},
                                         separators=(",", ":")) + ";\n"


def brief(folder, arm):
    t = open(os.path.join(HERE, "briefs", "brief.md")).read()
    return (t.replace("{FOLDER}", folder)
             .replace("{OTHERS}", OTHERS if arm in "BC" else "")
             .replace("{DEPART}", DEPART if arm == "C" else ""))


def write(root, mid, arm, body):
    folder = os.path.join(root, mid, "work")
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "data.js"), "w").write(body)
    if arm in "BC":
        # round 1's pictures and notes, in round 1's own order: o<k> is m0<k>
        od = os.path.join(folder, "others")
        os.makedirs(od, exist_ok=True)
        for k in range(1, 7):
            shutil.copy(os.path.join(HERE, "shots", "m%02d.png" % k), os.path.join(od, "o%d.png" % k))
            shutil.copy(os.path.join(HERE, "makers", "m%02d" % k, "NOTE.md"), os.path.join(od, "o%d.md" % k))
    b = brief(folder, arm)
    os.makedirs(os.path.join(HERE, "briefs", "run"), exist_ok=True)
    open(os.path.join(HERE, "briefs", "run", mid + ".md"), "w").write(b)
    return {"maker": mid, "arm": arm, "folder": folder,
            "data_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "brief_sha256": hashlib.sha256(b.encode()).hexdigest()}


if __name__ == "__main__":
    which, root = sys.argv[1], sys.argv[2]
    body = data_js()
    open(os.path.join(HERE, "data.js"), "w").write(body)
    path = os.path.join(HERE, "plan.json")
    plan = json.load(open(path)) if os.path.exists(path) else []
    if which == "round1":
        plan = [write(root, "m%02d" % i, "R", body) for i in range(1, 7)]
    else:
        arms = ["B"] * 4 + ["C"] * 4 + ["D"] * 4
        random.Random(SEED).shuffle(arms)
        plan = [p for p in plan if p["arm"] == "R"]
        plan += [write(root, "m%02d" % (7 + i), a, body) for i, a in enumerate(arms)]
    json.dump(plan, open(path, "w"), indent=1)
    for p in plan:
        print(p["maker"], p["arm"], p["folder"])
