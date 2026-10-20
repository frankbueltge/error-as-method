"""make_packet.py <rooms>: the coder's packet. Items I1-I6 are the text under "The wrong reading" in the six
E notes; notes N01-N12 are the twelve NOTE.md files whole. Both shuffled with seed 143; key.json holds the map."""
import json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); rooms = sys.argv[1]
plan = json.load(open(os.path.join(HERE, "..", "plan.json")))["rooms"]
rng = random.Random(143)
E = [p["room"] for p in plan if p["arm"] == "E"]; ALL = [p["room"] for p in plan]
note = lambda r: open(os.path.join(rooms, r, "NOTE.md")).read().strip()
def wrong(r):
    t = note(r).split("## The wrong reading", 1)[1]
    return re.sub(r"\n\(.*?\)\s*$", "", t.strip(), flags=re.S).strip()
ei = E[:]; rng.shuffle(ei); ni = ALL[:]; rng.shuffle(ni)
open(os.path.join(HERE, "items.txt"), "w").write("\n\n".join(f"I{i+1}\n{wrong(r)}" for i, r in enumerate(ei)) + "\n")
open(os.path.join(HERE, "notes.txt"), "w").write("\n\n".join(f"N{i+1:02d}\n{note(r)}" for i, r in enumerate(ni)) + "\n")
json.dump({"items": {f"I{i+1}": r for i, r in enumerate(ei)}, "notes": {f"N{i+1:02d}": r for i, r in enumerate(ni)}},
          open(os.path.join(HERE, "key.json"), "w"), indent=1)
