"""Session 161: draw the 32 sentences, apply the study's exclusions, write the briefs and the people's values.
Run: python3 prepare.py   (reads sources/, writes plan.json, people.json and briefs/)
The people's values go to people.json and are not printed: they are scored only after every maker has answered.
"""
import csv, json, random, statistics as st
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).parent
SEED = 161
rows = list(csv.DictReader(open(HERE / "sources" / "data_E5.csv")))

# Exclusions (a)-(d) of the study's own plan (analysis_plan_E5.md, section 5); (e) cannot be applied, ids are pseudonyms.
by_pid = defaultdict(list)
for r in rows:
    by_pid[r["pid"]].append(r)
excluded = {}
for pid, rs in by_pid.items():
    why = []
    if any(abs(int(r["rating"]) - int(r["expect"])) > 1 for r in rs if r["type"] == "attn"):
        why.append("a")
    good = [int(r["rating"]) for r in rs if r["type"] == "filler" and r["item"].startswith("G")]
    bad = [int(r["rating"]) for r in rs if r["type"] == "filler" and r["item"].startswith("B")]
    if good and bad and not (st.mean(bad) <= st.mean(good) - 1.5):
        why.append("b")
    timed = [r for r in rs if r["type"] in ("crit", "filler", "attn")]
    if sum(1 for r in timed if int(r["rt"]) < 1000) > 0.2 * len(timed):
        why.append("c")
    if rs[0]["excl_d"] == "TRUE":
        why.append("d")
    if why:
        excluded[pid] = why

# The draw: 32 items, each given one of the 8 conditions, 4 sentences per condition.
conds = [(t, s, p) for t in ("pp", "rc") for s in ("noisland", "island") for p in ("insitu", "extrap")]
rng = random.Random(SEED)
items = sorted({r["item"] for r in rows if r["type"] == "crit"}, key=int)
rng.shuffle(items)
pick = {it: conds[i % 8] for i, it in enumerate(items)}
ratings = defaultdict(list)
sent = {}
for r in rows:
    if r["type"] == "crit" and r["pid"] not in excluded and (r["mtype"], r["island"], r["pos"]) == pick[r["item"]]:
        ratings[r["item"]].append(int(r["rating"]))
        sent[r["item"]] = r["sentence"]
keys = sorted(pick, key=int)
key_list = [{"key": f"k{int(it):02d}", "item": it, "cond": "/".join(pick[it]), "sentence": sent[it]} for it in keys]

def q(v, p):
    v = sorted(v); i = (len(v) - 1) * p; lo = int(i); hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)

people = {k["key"]: {"n": len(ratings[k["item"]]), "median": st.median(ratings[k["item"]]),
                     "mean": round(st.mean(ratings[k["item"]]), 4),
                     "p10": q(ratings[k["item"]], .1), "p25": q(ratings[k["item"]], .25),
                     "p75": q(ratings[k["item"]], .75), "p90": q(ratings[k["item"]], .9),
                     "ratings": sorted(ratings[k["item"]])} for k in key_list}
json.dump(people, open(HERE / "people.json", "w"), indent=1)
n_incl = len(by_pid) - len(excluded)

PROJ = "Do not use any tool, program, file, search or lookup of any kind. Answer from what you have here."
INTRO_A = ("Below are 32 English sentences. Rate how natural each sentence sounds as a sentence of English, on a 7-point "
           "scale from 1 (completely unnatural) to 7 (completely natural). Answer each with a single whole number, as yourself.")
WHO = (f"In a study whose data were collected online in October 2026, {n_incl} adults whose first language is English, living "
       "in the US or the UK, each read sentences one at a time and rated how natural each sounded, on a 7-point scale from 1 "
       "(completely unnatural) to 7 (completely natural), with a whole number. Each sentence below was rated by between "
       f"{min(p['n'] for p in people.values())} and {max(p['n'] for p in people.values())} of them.")
DESC_7 = ("For each sentence, do not rate it yourself. State how those people's ratings were spread, on their own 1 to 7 scale: "
          "give the 10th, 25th, 50th, 75th and 90th percentile of their ratings, and their mean rating (decimals allowed).")
DESC_100 = ("For each sentence, do not rate it yourself. State how those people's ratings were spread, but give every number "
            "on a 0 to 100 scale on which 0 is their rating 1 and 100 is their rating 7, so that any position between can be "
            "stated: give the 10th, 25th, 50th, 75th and 90th percentile of their ratings, and their mean rating, each as any "
            "number from 0 to 100.")
TAIL_A = ("Format your whole answer exactly like this, and nothing else:\nRATINGS\n1: <n>\n...\n32: <n>\n"
          "HOW: in at most 40 words, how you rated.\nTOOLS: every tool, program, file or search you used, or \"none\".")
TAIL_D = ("Format your whole answer exactly like this, and nothing else:\nSPREADS\n"
          "1: p10=<n> p25=<n> p50=<n> p75=<n> p90=<n> mean=<n>\n...\n32: p10=<n> p25=<n> p50=<n> p75=<n> p90=<n> mean=<n>\n"
          "KNOWN: do you know this study or its data? Say yes or no, and if yes, from where, in at most 30 words.\n"
          "HOW: in at most 40 words, how you arrived at the spreads.\n"
          "TOOLS: every tool, program, file or search you used, or \"none\".")
(HERE / "briefs").mkdir(exist_ok=True)
plan = {"seed": SEED, "excluded": excluded, "n_participants": len(by_pid), "n_included": n_incl,
        "keys": key_list, "orders": {}}
for arm, n in (("A", 6), ("S", 6), ("F", 6)):
    for i in range(1, n + 1):
        mid = f"{arm}{i}"
        order = [k["key"] for k in key_list]
        rng.shuffle(order)
        plan["orders"][mid] = order
        lines = "\n".join(f"{j}: {next(k['sentence'] for k in key_list if k['key'] == kk)}" for j, kk in enumerate(order, 1))
        if arm == "A":
            text = f"{INTRO_A}\n\n{PROJ}\n\n{lines}\n\n{TAIL_A}\n"
        else:
            text = f"Below are 32 English sentences. {WHO}\n\n{DESC_7 if arm == 'S' else DESC_100}\n\n{PROJ}\n\n{lines}\n\n{TAIL_D}\n"
        (HERE / "briefs" / f"{mid}.txt").write_text(text)
json.dump(plan, open(HERE / "plan.json", "w"), indent=1)
print("participants", len(by_pid), "excluded", len(excluded), "included", n_incl)
print("raters per sentence", min(p["n"] for p in people.values()), "to", max(p["n"] for p in people.values()))
print("conditions", sorted({k["cond"] for k in key_list}))
