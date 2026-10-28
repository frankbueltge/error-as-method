"""Session 160: read the people's ratings and write the twenty briefs (seed 160 for item orders).
The people: Data_Study2.xlsx of Zenodo record 23658923 (CC BY 4.0), 96 participants x 50 English phrases,
column 'English-Morality' (1-7); empty cells are the rows a participant marked 'misunderstand' and are left out.
Run: python3 prepare.py   (writes plan.json and briefs/*.txt)
"""
import json, random
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
wb = openpyxl.load_workbook(HERE / "sources" / "Data_Study2.xlsx", read_only=True)
rows = list(wb.active.iter_rows(values_only=True))
head, rows = rows[0], rows[1:]
ci = {h: i for i, h in enumerate(head) if h}
items = {}
for r in rows:
    wid = r[ci["Word_ID"]]
    it = items.setdefault(wid, {"id": wid, "phrase": r[ci["English Phrases"]], "valence": r[ci["Moral Valence"]],
                                "foundation": r[ci["Moral Foundation"]], "en": [], "zh": []})
    if r[ci["English-Morality"]] is not None:
        it["en"].append(r[ci["English-Morality"]])
    if r[ci["Chinese-Morality"]] is not None:
        it["zh"].append(r[ci["Chinese-Morality"]])
items = [items[k] for k in sorted(items)]
assert len(items) == 50

ARMS = {"A": 8, "P": 6, "T": 6}
rng = random.Random(160)
orders = {}
for arm, n in ARMS.items():
    for k in range(1, n + 1):
        o = list(range(50)); rng.shuffle(o); orders[f"{arm}{k}"] = o

SCALE = "a 7-point scale from 1 (very immoral) through 4 (neither moral nor immoral) to 7 (very moral)"
PEOPLE = ("In a study whose data were published in October 2026, 96 adults who speak both Chinese and English rated "
          "how moral or immoral each of the actions below is, on " + SCALE + ". They rated each action once as a "
          "Chinese phrase and once as an English phrase. The ratings asked about here are the ones they gave to the "
          "English phrases, exactly as listed. Each person rated each phrase once, with a whole number.")
TOLD = ("One thing is known from earlier tests of this kind. When instances of you described a group of people's "
        "ratings that they could not have seen, their stated medians moved, on average, only about half of the way "
        "from the ratings instances of you give themselves to the group's actual ratings. Take that into account.")
NOTOOLS = "Do not use any tool, program, file, search or lookup of any kind. Answer from what you have here."

def listing(o):
    return "\n".join(f"{i + 1}: {items[j]['phrase']}" for i, j in enumerate(o))

def brief(mid):
    arm, o = mid[0], orders[mid]
    if arm == "A":
        return (f"Below are 50 actions. Rate how moral or immoral each action is on {SCALE}. Answer each with a single "
                f"whole number, as yourself.\n\n{NOTOOLS}\n\n{listing(o)}\n\n"
                "Format your whole answer exactly like this, and nothing else:\nRATINGS\n"
                "1: <the action as listed> = <whole number 1-7>\n...\n50: <the action as listed> = <whole number 1-7>\n"
                "HOW: in at most 40 words, how you arrived at the ratings.\n"
                "TOOLS: every tool, program, file or search you used, or \"none\".\n")
    told = f"\n\n{TOLD}" if arm == "T" else ""
    return (f"Below are 50 actions. {PEOPLE}\n\nFor each action, do not rate it yourself. State how the 96 people's "
            f"ratings were spread: give the 10th, 25th, 50th, 75th and 90th percentile of their ratings (decimals "
            f"allowed).{told}\n\n{NOTOOLS}\n\n{listing(o)}\n\n"
            "Format your whole answer exactly like this, and nothing else:\nSPREADS\n"
            "1: <the action as listed> = p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>\n...\n"
            "50: <the action as listed> = p10=<n> p25=<n> p50=<n> p75=<n> p90=<n>\n"
            "KNOWN: do you know this study or its data? Say yes or no, and if yes, from where, in at most 30 words.\n"
            "HOW: in at most 40 words, how you arrived at the spreads.\n"
            "TOOLS: every tool, program, file or search you used, or \"none\".\n")

(HERE / "briefs").mkdir(exist_ok=True)
for mid in orders:
    (HERE / "briefs" / f"{mid}.txt").write_text(brief(mid))
json.dump({"seed": 160, "arms": ARMS, "orders": orders, "items": items}, open(HERE / "plan.json", "w"), indent=1,
          ensure_ascii=False)
print("items", len(items), "briefs", len(orders))
