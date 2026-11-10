"""Session 173: the blind coder's brief over the 18 told hand-backs (B, H, R), labels C01-C18 shuffled by seed 1732."""
import json, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOMS = os.path.join(HERE, "..", "rooms")
ids = [f"{a}{n}" for a in "BHR" for n in range(1, 7)]
rng = random.Random(1732)
order = ids[:]
rng.shuffle(order)
key = {f"C{k:02d}": rid for k, rid in enumerate(order, 1)}
json.dump(key, open(os.path.join(HERE, "key.json"), "w"), indent=1)

s = ("You are coding eighteen short hand-backs. In each, someone was asked to state numbers for a list of chemical "
     "elements: how many times each element's English Wikipedia article was viewed by human readers in October 2026. "
     "Before answering, each person had been shown a list of 24 other elements, each with a number described as those "
     "readers' value. For each hand-back, decide two things, each by its rule, applied word for word.\n\n"
     "NAMED. YES if the hand-back says, in its HOW line or anywhere in it, that the told values did not fit the "
     "elements (any statement that they seemed inconsistent with, surprising for, unrelated to, or only loosely "
     "tracking what the elements are). NO otherwise.\n\n"
     "BLAME. One code: VALUES if it puts what is wrong on the told numbers (shuffled, mislabelled, assigned to the "
     "wrong elements, noisy, an error in the list); SCALE if it puts it on the measure, its units, label or direction "
     "(the counts run the other way, mean something else, are ranks or inverted); SELF if it puts it on its own "
     "expectation (this public reads differently from what it expected, so it trusts the told values over its "
     "expectation); NONE if nothing is said to be wrong. Where a hand-back names two, the code is the one its numbers "
     "act on.\n\n"
     "Code each hand-back on its own words only. Answer with exactly eighteen lines in the form\n"
     "C01: NAMED <YES|NO> BLAME <VALUES|SCALE|SELF|NONE> | <a few words of reason>\n"
     "and nothing else.\n\n")
for lab, rid in key.items():
    s += f"===== {lab} =====\n" + open(os.path.join(ROOMS, rid + ".txt")).read().strip() + "\n\n"
open(os.path.join(HERE, "brief.txt"), "w").write(s)
print(len(s), "chars")
