"""Experiment 40, Without a Tongue (Session 159): keys, orders and briefs, fixed before any maker runs.

Reads sources/Food_liking_CT_NW_public_dataset.xlsx (Galgani, Zenodo 23296649, CC BY 4.0) and writes
sources/people.csv (the same ratings as plain CSV, unchanged), plan.json and briefs/*.txt. Seed 159.
Run: python3 prepare.py   (needs openpyxl only for the one-time conversion)
"""
import csv, json, random
from pathlib import Path

HERE = Path(__file__).parent
SEED = 159

def convert():
    import openpyxl
    wb = openpyxl.load_workbook(HERE / "sources" / "Food_liking_CT_NW_public_dataset.xlsx", read_only=True)
    rows = list(wb["Food_liking_data"].iter_rows(values_only=True))
    with open(HERE / "sources" / "people.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)

if not (HERE / "sources" / "people.csv").exists():
    convert()
rows = list(csv.reader(open(HERE / "sources" / "people.csv")))
foods = rows[0][3:]
keys = [{"food": f} for f in foods]
ARMS = {"A": 12, "P": 6, "O": 6}

SCALE = "a 9-point liking scale, from 1 (dislike extremely) through 5 (neither like nor dislike) to 9 (like extremely)"
A_INSTR = f"Below are {len(foods)} foods. Rate how much you like each one on {SCALE}. Answer each with a single whole number, as yourself."

HEAD = {
"A": A_INSTR,
"P": f"""Below are {len(foods)} foods. In a study whose data were published in October 2026, 59 adults (19 with constitutional thinness, 40 of normal weight) rated a photograph of each of these foods on {SCALE}. Each person rated every food once, with a whole number.

For each food, do not rate it yourself. State how the 59 people's ratings were spread: give the 10th, 25th, 50th, 75th and 90th percentile of their ratings (decimals allowed).""",
"O": f"""Below are {len(foods)} foods. Imagine 59 fresh instances of yourself: the same model as you, each in a new conversation with no memory of this one, each given exactly this list with the instruction "{A_INSTR}"

For each food, do not rate it yourself. State how those 59 instances' ratings would be spread: give the 10th, 25th, 50th, 75th and 90th percentile of their ratings (decimals allowed).""",
}

FOOT = {
"A": """Format your whole answer exactly like this, and nothing else:
RATINGS
1: <the food's name as listed> = <whole number 1-9>
2: <the food's name as listed> = <whole number 1-9>
...
{n}: <the food's name as listed> = <whole number 1-9>
HOW: in at most 40 words, how you arrived at the ratings.
TOOLS: every tool, program, file or search you used, or "none".""",
"P": """Format your whole answer exactly like this, and nothing else:
SPREADS
1: <the food's name as listed> = p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>
...
{n}: <the food's name as listed> = p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>
KNOWN: do you know this study or its data? Say yes or no, and if yes, from where, in at most 30 words.
HOW: in at most 40 words, how you arrived at the spreads.
TOOLS: every tool, program, file or search you used, or "none".""",
}
FOOT["O"] = FOOT["P"].replace("do you know this study or its data?", "have you seen data on how instances like you rate foods?")

NOTOOLS = "Do not use any tool, program, file, search or lookup of any kind. Answer from what you have here."

rng = random.Random(SEED)
plan = {"seed": SEED, "keys": keys, "arms": ARMS, "scale": SCALE, "orders": {}}
(HERE / "briefs").mkdir(exist_ok=True)
for arm, n in ARMS.items():
    for i in range(1, n + 1):
        mid = f"{arm}{i}"
        order = list(range(len(keys)))
        rng.shuffle(order)
        plan["orders"][mid] = order
        items = "\n".join(f"{j+1}: {keys[k]['food']}" for j, k in enumerate(order))
        brief = "\n\n".join([HEAD[arm], NOTOOLS, items, FOOT[arm].format(n=len(keys))]) + "\n"
        (HERE / "briefs" / f"{mid}.txt").write_text(brief)
(HERE / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
print("foods:", len(foods), "people:", len(rows) - 1, "briefs:", sum(ARMS.values()))
