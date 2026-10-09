"""looks.py -- M1 and M2, mechanical, from the makers' folders and the viewer's logs. Writes looks.json."""
import json, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))["plan"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
log = lambda m, st: [json.loads(l) for l in open(os.path.join(HERE, "makers", m, st, "renders", "log.jsonl"))] \
    if os.path.exists(os.path.join(HERE, "makers", m, st, "renders", "log.jsonl")) else []
out = []
for p in plan:
    m = p["maker"]
    f1 = sha(os.path.join(HERE, "makers", m, "first", "index.html"))
    f2 = sha(os.path.join(HERE, "makers", m, "second", "index.html"))
    l1, l2 = log(m, "first"), log(m, "second")
    after = l2[len(l1):]
    r = {"maker": m, "return": p["return"], "notes_from": p["notes_from"],
         "looks_before_return": len(l1),
         "last_look_is_first_handin": bool(l1) and l1[-1]["sha256"] == f1,
         "reopened": f1 != f2, "looks_after_return": len(after),
         "looked_first": bool(after) and after[0]["sha256"] == f1,
         "last_look_is_second_handin": bool(l2) and l2[-1]["sha256"] == f2,
         "note_changed": sha(os.path.join(HERE, "makers", m, "first", "NOTE.md")) != sha(os.path.join(HERE, "makers", m, "second", "NOTE.md"))}
    out.append(r)
    print(r)
json.dump(out, open(os.path.join(HERE, "looks.json"), "w"), indent=1)
