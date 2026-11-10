"""Session 173, Read Backwards: split, deals and the 24 briefs, all fixed before any maker runs.

Input: sources/pageviews-2026-10.json (written by prepare_fetch.py from the Wikimedia REST API).
Output: plan.json, briefs/<arm><n>.txt.
"""
import json, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "sources/pageviews-2026-10.json")))
views = {r["element"]: r["views"] for r in P}
names = [r["element"] for r in P]


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den


# 1. split, seed 173: 24 contact, 32 scored
rng = random.Random(173)
shuffled = names[:]
rng.shuffle(shuffled)
contact, scored = shuffled[:24], shuffled[24:]

true_vals = [views[e] for e in contact]

# 2. reversed deal: the largest true value goes to the element with the smallest, and so on
order = sorted(range(24), key=lambda i: true_vals[i])
rev = [None] * 24
for k, i in enumerate(order):
    rev[i] = true_vals[order[23 - k]]
assert abs(spearman(true_vals, rev) + 1) < 1e-9

# 3. half-turned deal, seed 1730: first permutation with rho in [-0.62, -0.58] and no value left in place
rng = random.Random(1730)
tries = 0
while True:
    tries += 1
    perm = true_vals[:]
    rng.shuffle(perm)
    if any(p == t for p, t in zip(perm, true_vals)):
        continue
    rho = spearman(true_vals, perm)
    if -0.62 <= rho <= -0.58:
        break
half = perm
rho_half = spearman(true_vals, half)

# 4. presentation orders: contact list order and scored list order fixed once (seed 1731)
rng = random.Random(1731)
contact_order = contact[:]
rng.shuffle(contact_order)
scored_order = scored[:]
rng.shuffle(scored_order)

deal = {"B": dict(zip(contact, true_vals)), "H": dict(zip(contact, half)), "R": dict(zip(contact, rev))}

plan = {
    "session": 173,
    "contact": contact_order,
    "scored": scored_order,
    "true": {e: views[e] for e in names},
    "deals": deal,
    "rho_half_vs_true": round(rho_half, 4),
    "half_tries": tries,
    "rho_rev_vs_true": -1.0,
    "seeds": {"split": 173, "half": 1730, "order": 1731},
}
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)

WHO = ("English Wikipedia counts how often each of its articles is viewed. In October 2026 (1 to 31 October), "
       "readers viewed the article on each chemical element a certain number of times, on all devices; the count "
       "is of human readers only, with automated traffic removed. For each element, those readers' value is the "
       "number of views its English Wikipedia article received in that month.")

TAIL = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and "
        "nothing else, to the file /home/user/error-as-method/works/2026-11-08-read-backwards/rooms/{id}.txt with "
        "your file-writing tool, then hand back the same text. Answer from what is written here.\n\n"
        "Your answer is exactly 32 lines in the form\n1: views <whole number>\n2: views <whole number>\n... and then "
        "two more lines:\nHOW: <one sentence on how you arrived at the numbers>\n"
        "KNOWN: <yes, no or partly> - did you know these view counts before today?\n")

os.makedirs(os.path.join(HERE, "briefs"), exist_ok=True)
os.makedirs(os.path.join(HERE, "rooms"), exist_ok=True)
for arm in "UBHR":
    for n in range(1, 7):
        bid = f"{arm}{n}"
        s = "Below are chemical elements.\n\n" + WHO + "\n\n"
        if arm != "U":
            s += "First, here are 24 other elements, labelled T1 to T24, each with those readers' value:\n"
            for k, e in enumerate(contact_order, 1):
                s += f"T{k}. {e} -> {deal[arm][e]:,} views\n"
            s += "\n"
        s += "The 32 elements:\n" + "".join(f"{k}. {e}\n" for k, e in enumerate(scored_order, 1))
        s += ("\nFor each of the 32 numbered elements, state those readers' value for it: the number of views its "
              "English Wikipedia article received from human readers in October 2026.\n\n")
        s += TAIL.format(id=bid)
        open(os.path.join(HERE, "briefs", bid + ".txt"), "w").write(s)

print("contact", len(contact), "scored", len(scored))
print("rho half", round(rho_half, 4), "tries", tries)
sv = [views[e] for e in scored]
import math
lv = [math.log10(v) for v in sv]
m = sum(lv) / len(lv)
print("scored log10 mean %.3f sd %.3f" % (m, (sum((x - m) ** 2 for x in lv) / (len(lv) - 1)) ** 0.5))
