"""Experiment 39, Asked Three Ways (Session 158): keys, orders and briefs, fixed before any maker runs.

Run: python3 prepare.py   (writes plan.json and briefs/*.txt; seed 158)
"""
import csv, json, random
from pathlib import Path

HERE = Path(__file__).parent
SEED = 158

def read(name):
    rows = list(csv.reader(open(HERE / "sources" / name)))
    return [h.strip() for h in rows[0]], rows[1:]

ph, prow = read("probly.csv")
nh, nrow = read("numberly.csv")
keys = [{"phrase": p, "kind": "probability"} for p in ph] + [{"phrase": p, "kind": "number"} for p in nh]

QUESTION = {"probability": 'What probability would you assign to the phrase "{p}"?',
            "number": 'What number would you assign to the phrase "{p}"?'}

ARMS = {"A": 12, "P": 6, "O": 6}

HEAD = {
"A": """Below are 27 questions. Answer each one with a single number, as yourself. Probabilities are percentages from 0 to 100.""",
"P": """Below are 27 questions. In 2015, 46 people answered exactly these questions in an online poll, each person once, each giving a single number (probabilities as percentages from 0 to 100).

For each question, do not answer it yourself. State how the 46 people's answers were spread: give the 10th, 25th, 50th, 75th and 90th percentile of their answers.""",
"O": """Below are 27 questions. Imagine 46 fresh instances of yourself: the same model as you, each in a new conversation with no memory of this one, each given exactly this list of questions with the instruction "Answer each one with a single number, as yourself. Probabilities are percentages from 0 to 100."

For each question, do not answer it yourself. State how those 46 instances' answers would be spread: give the 10th, 25th, 50th, 75th and 90th percentile of their answers.""",
}

FOOT = {
"A": """Format your whole answer exactly like this, and nothing else:
ANSWERS
1: <number>
2: <number>
...
27: <number>
HOW: in at most 40 words, how you arrived at the numbers.
TOOLS: every tool, program, file or search you used, or "none".""",
"P": """Format your whole answer exactly like this, and nothing else:
SPREADS
1: p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>
...
27: p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>
KNOWN: do you know this poll or its data? Say yes or no, and if yes, from where, in at most 30 words.
HOW: in at most 40 words, how you arrived at the spreads.
TOOLS: every tool, program, file or search you used, or "none".""",
}
FOOT["O"] = FOOT["P"].replace("do you know this poll or its data?", "have you seen data on how instances like you answer these questions?")

NOTOOLS = "Do not use any tool, program, file, search or lookup of any kind. Answer from what you have here."

rng = random.Random(SEED)
plan = {"seed": SEED, "keys": keys, "question": QUESTION, "arms": ARMS, "orders": {}}
(HERE / "briefs").mkdir(exist_ok=True)
for arm, n in ARMS.items():
    for i in range(1, n + 1):
        mid = f"{arm}{i}"
        order = list(range(len(keys)))
        rng.shuffle(order)
        plan["orders"][mid] = order
        items = "\n".join(f"{j+1}: " + QUESTION[keys[k]["kind"]].format(p=keys[k]["phrase"]) for j, k in enumerate(order))
        brief = "\n\n".join([HEAD[arm], NOTOOLS, items, FOOT[arm]]) + "\n"
        (HERE / "briefs" / f"{mid}.txt").write_text(brief)
(HERE / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
print("briefs:", sum(ARMS.values()))
