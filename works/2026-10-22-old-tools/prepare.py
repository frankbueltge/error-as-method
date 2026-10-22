"""prepare.py: assigns the 16 rooms to the four instruments (seed 149) and writes plan.json.
Run once, before any agent. The rooms live outside the repository while makers work (ROOT below) and are
copied in afterwards."""
import json, random, os, shutil, sys
H = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else None
arms = ["P"] * 4 + ["C"] * 4 + ["G"] * 4 + ["D"] * 4
random.Random(149).shuffle(arms)
tool = {"P": "plot.py", "C": "cycles.py", "G": "gaps.py", "D": "digits.py"}
plan = {"seed": 149, "arms": {"P": "PLOT", "C": "CYCLES", "G": "GAPS", "D": "FIRST DIGITS"},
        "rooms": [{"room": "r%02d" % (i + 1), "arm": a, "instrument": tool[a]} for i, a in enumerate(arms)]}
json.dump(plan, open(os.path.join(H, "plan.json"), "w"), indent=1)
if ROOT:
    for r in plan["rooms"]:
        d = os.path.join(ROOT, r["room"]); os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(H, "instruments", r["instrument"]), os.path.join(d, "instrument.py"))
        shutil.copy(os.path.join(H, "instruments", "_common.py"), os.path.join(d, "_common.py"))
print(json.dumps(plan["rooms"]))
