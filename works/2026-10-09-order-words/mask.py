"""mask.py a|b|c <scratch-dir> -- builds the blind coders' folders; keys are written to keys/.

a  seed 1180: the twelve first-hand-in pictures as A.png .. L.png              (coder A, notes)
b  seed 1181: each S/X maker's first picture with the three notes it received,
             and each S/X maker that changed, its second picture with the same notes;
             shuffled as P01.png ..                                             (coder B, fit)
c  seed 1182: each maker that changed, first and second picture as Qnn-X/Y,
             order within the pair drawn                                        (coder C, pairs)
"""
import json, os, random, shutil, sys, string, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))["plan"]
os.makedirs(os.path.join(HERE, "keys"), exist_ok=True)
mode, out = sys.argv[1], sys.argv[2]
if os.path.exists(out): shutil.rmtree(out)
os.makedirs(out)
shots = lambda stage, m: os.path.join(HERE, "shots", stage, m + ".png")


def changed(m):
    f = lambda s: hashlib.sha256(open(os.path.join(HERE, "makers", m, s, "index.html"), "rb").read()).hexdigest()
    return f("first") != f("second")


if mode == "a":
    ms = [p["maker"] for p in plan]
    random.Random(1180).shuffle(ms)
    key = {}
    for L, m in zip(string.ascii_uppercase, ms):
        shutil.copy(shots("first", m), os.path.join(out, L + ".png")); key[L] = m
    json.dump(key, open(os.path.join(HERE, "keys", "coder-a.json"), "w"), indent=1)
elif mode == "b":
    notes = json.load(open(os.path.join(HERE, "notes.json")))       # maker -> its own three notes
    items = []
    for p in plan:
        if p["return"] in "SX":
            given = notes[p["notes_from"]]
            items.append((p["maker"], "first", given))
            if changed(p["maker"]):
                items.append((p["maker"], "second", given))
    random.Random(1181).shuffle(items)
    key, shown = {}, {}
    for i, (m, st, given) in enumerate(items, 1):
        k = "P%02d" % i
        shutil.copy(shots(st, m), os.path.join(out, k + ".png"))
        key[k] = {"maker": m, "stage": st}; shown[k] = {"picture": k + ".png", "notes": given}
    json.dump(shown, open(os.path.join(out, "items.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(key, open(os.path.join(HERE, "keys", "coder-b.json"), "w"), indent=1)
elif mode == "c":
    ms = [p["maker"] for p in plan if changed(p["maker"])]
    rng = random.Random(1182); rng.shuffle(ms)
    key = {}
    for i, m in enumerate(ms, 1):
        k = "Q%02d" % i; flip = rng.random() < 0.5
        x, y = ("second", "first") if flip else ("first", "second")
        shutil.copy(shots(x, m), os.path.join(out, k + "-X.png")); shutil.copy(shots(y, m), os.path.join(out, k + "-Y.png"))
        key[k] = {"maker": m, "X": x, "Y": y}
    json.dump(key, open(os.path.join(HERE, "keys", "coder-c.json"), "w"), indent=1)
print(mode, "->", out, sorted(os.listdir(out)))
