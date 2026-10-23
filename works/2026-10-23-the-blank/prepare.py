"""Session 153: draw the cues and make the keys for The Blank. Seed 153.

usage: python3 prepare.py <dir holding the eight USF Cue_Target_Pairs files>

Three arms, 24 keys each, six fresh makers per arm, each maker in its own order.
  S  a printed cue: the norms print what 100-160 people wrote on its blank.
  P  two cues at once: no norm prints what people write for a pair. Half the pairs share an
     associate in the norms (FORCED), half share none (UNFORCED).
  N  the S cue again, with the people's most frequent word excluded. No norm prints it either.
"""
import json
import random
import re
import sys

import usf

SEED = 153
rng = random.Random(SEED)
cues = usf.load(sys.argv[1])


def ranked(c):
    return sorted(c["resp"].items(), key=lambda kv: (-kv[1], kv[0]))


def eligible(w, c):
    r = ranked(c)
    return (re.fullmatch(r"[A-Z]{3,10}", w) and c["G"] >= 100 and len(r) >= 3
            and r[0][1] > r[1][1])


pool = sorted(w for w, c in cues.items() if eligible(w, c))
rng.shuffle(pool)

# S and N: eight cues per stratum of the people's top share.
strata = {"low": (0, .15), "mid": (.15, .35), "high": (.35, 1.01)}
chosen = {k: [] for k in strata}
for w in pool:
    top = ranked(cues[w])[0][1] / cues[w]["G"]
    for k, (lo, hi) in strata.items():
        if lo <= top < hi and len(chosen[k]) < 8:
            chosen[k].append(w)
    if all(len(v) == 8 for v in chosen.values()):
        break
single = [(w, k) for k in strata for w in chosen[k]]
used = {w for w, _ in single}

# P: pairs from the rest of the pool.
rest = [w for w in pool if w not in used]
forced, unforced = [], []
i = 0
while len(forced) < 12 or len(unforced) < 12:
    a, b = rest[i], rest[i + 1]
    i += 2
    ca, cb = cues[a], cues[b]
    shared = set(ca["resp"]) & set(cb["resp"]) - {a, b}
    best = max(((min(ca["resp"][t] / ca["G"], cb["resp"][t] / cb["G"]), t) for t in shared),
               default=(0, None))
    linked = b in ca["resp"] or a in cb["resp"]
    if best[0] >= .05 and len(forced) < 12:
        forced.append({"a": a, "b": b, "kind": "FORCED", "shared": best[1],
                       "shared_min_fsg": round(best[0], 3)})
    elif not shared and not linked and len(unforced) < 12:
        unforced.append({"a": a, "b": b, "kind": "UNFORCED", "shared": None,
                         "shared_min_fsg": 0})

keys = {"S": [], "P": [], "N": []}
for n, (w, k) in enumerate(single):
    r = ranked(cues[w])
    G = cues[w]["G"]
    keys["S"].append({"id": f"S{n+1:02d}", "cue": w, "stratum": k, "G": G,
                      "people": r, "p_three_agree": round(usf.p_three_agree(cues[w]), 4)})
    keys["N"].append({"id": f"N{n+1:02d}", "cue": w, "excluded": r[0][0], "stratum": k,
                      "G": G, "people": r, "second": r[1][0]})
for n, p in enumerate(forced + unforced):
    p["id"] = f"P{n+1:02d}"
    p["people_a"] = ranked(cues[p["a"]])[:8]
    p["people_b"] = ranked(cues[p["b"]])[:8]
    keys["P"].append(p)


def line(arm, k):
    if arm == "S":
        return f"{k['cue']} ________"
    if arm == "P":
        return f"{k['a']} + {k['b']} ________"
    return f"{k['cue']} ________   (not {k['excluded']})"


TASK = {
    "S": ("Below are 24 English words, each with a blank next to it. For each word, write on its "
          "blank the first word that comes to mind that is meaningfully related or strongly "
          "associated to the presented word."),
    "P": ("Below are 24 pairs of English words, each pair with a blank next to it. For each pair, "
          "write on its blank the first word that comes to mind that is meaningfully related or "
          "strongly associated to both presented words at once."),
    "N": ("Below are 24 English words, each with a blank next to it and one word in brackets. For "
          "each word, write on its blank the first word that comes to mind that is meaningfully "
          "related or strongly associated to the presented word, other than the word in brackets."),
}
TEMPLATE = open("brief-template.txt").read()

deal = {}
for arm in "SPN":
    for m in range(1, 7):
        order = list(range(24))
        rng.shuffle(order)
        deal[f"{arm}{m}"] = [keys[arm][j]["id"] for j in order]
        items = "\n".join(f"{i+1}. {line(arm, keys[arm][j])}" for i, j in enumerate(order))
        with open(f"briefs/{arm}{m}.txt", "w") as fh:
            fh.write(TEMPLATE.replace("{TASK}", TASK[arm]).replace("{ITEMS}", items))

json.dump({"seed": SEED, "keys": keys, "deal": deal}, open("plan.json", "w"), indent=1)
for arm in "SPN":
    print(arm, [k.get("cue") or (k["a"] + "+" + k["b"]) for k in keys[arm]])
print("E[people, three agree] over S:", round(sum(k["p_three_agree"] for k in keys["S"]), 2))
