"""Session 175: the blind coder's brief over the 18 told hand-backs (R, D, T), labels C01-C18 shuffled by seed 1752.
Each hand-back is given as its HOW and KNOWN lines; its 32 numbers are left out (they cannot name or blame in words)."""
import json, os, random, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOMS = os.path.join(HERE, "..", "rooms")
ids = [f"{a}{n}" for a in "RDT" for n in range(1, 7)]
rng = random.Random(1752); order = ids[:]; rng.shuffle(order)
key = {f"C{k:02d}": rid for k, rid in enumerate(order, 1)}
json.dump(key, open(os.path.join(HERE, "key.json"), "w"), indent=1)
s = ("You are coding eighteen short hand-backs. In each, someone was asked to state numbers for a list of places on "
     "rivers in the United States: the mean flow of the river there in October 2026, in cubic feet per second. Before "
     "answering, each person had been shown a list of 24 other places, each with a number given as its value. For each "
     "hand-back you see its last two lines; its 32 numbers are left out. Decide two things, each by its rule, applied "
     "word for word.\n\n"
     "NAMED. YES if the hand-back says that the told values did not fit the places (any statement that they seemed "
     "inconsistent with, surprising for, unrelated to, or only loosely tracking what the places are). NO otherwise.\n\n"
     "BLAME. One code: VALUES if it puts what is wrong on the told numbers (shuffled, mislabelled, assigned to the wrong "
     "places, an error in the list); SCALE if it puts it on the measure, its units, label or direction (the numbers mean "
     "something else, run the other way, are ranks); SELF if it puts it on its own expectation (it trusts the told values "
     "over its expectation); NONE if nothing is said to be wrong. 'Inverted', 'reversed' or 'backwards' said of the list, "
     "the values or their assignment to places is VALUES; said of the measure (the unit, the quantity, what a larger "
     "number means) is SCALE.\n\n"
     "Code each hand-back on its own words only. Answer with exactly eighteen lines in the form\n"
     "C01: NAMED <YES|NO> BLAME <VALUES|SCALE|SELF|NONE> | <a few words of reason>\nand nothing else.\n\n")
for lab, rid in key.items():
    t = open(os.path.join(ROOMS, rid + ".txt")).read()
    lines = [l for l in t.splitlines() if l.startswith(("HOW:", "KNOWN:"))]
    s += f"===== {lab} =====\n" + "\n".join(lines) + "\n\n"
open(os.path.join(HERE, "brief.txt"), "w").write(s)
