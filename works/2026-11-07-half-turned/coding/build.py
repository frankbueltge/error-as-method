"""Blind coding brief for Half Turned: 18 told hand-backs (B, H, R) under labels C01-C18, order by seed 1722."""
import json, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
names = [f"{a}{i}" for a in "BHR" for i in range(1, 7)]
order = names[:]
random.Random(1722).shuffle(order)
key = {f"C{k + 1:02d}": n for k, n in enumerate(order)}
head = ("You are coding eighteen short hand-backs. In each, someone was asked to state numbers for a list of "
        "occupations. Before answering, each person had been shown a list of 24 other occupations, each with a number "
        "described as those people's value. For each hand-back, decide one thing by this rule, applied word for word:\n\n"
        "YES if the hand-back says, in its HOW line or anywhere in it, that the told values did not fit the occupations "
        "(any statement that they seemed inconsistent with, surprising for, unrelated to, or only loosely tracking what "
        "the occupations are).\nNO otherwise.\n\nCode each hand-back on its own words only.\n")
parts = [head]
for lab, n in key.items():
    parts.append(f"\n===== {lab} =====\n" + (HERE.parent / "rooms" / f"{n}.txt").read_text().strip() + "\n")
parts.append("\nAnswer with exactly eighteen lines, C01: YES or C01: NO and so on, then one line NOTE: <anything unclear>.\n"
             "Use no tool except one: write your answer to /home/user/error-as-method/works/2026-11-07-half-turned/coding/answer.txt "
             "with your file-writing tool, then hand back the same text.\n")
(HERE / "brief.txt").write_text("".join(parts))
(HERE / "key.json").write_text(json.dumps(key, indent=1))
mine = {"B1": "NO", "B2": "NO", "B3": "NO", "B4": "NO", "B5": "NO", "B6": "NO",
        "H1": "YES", "H2": "YES", "H3": "YES", "H4": "YES", "H5": "YES", "H6": "YES",
        "R1": "YES", "R2": "YES", "R3": "YES", "R4": "YES", "R5": "YES", "R6": "YES"}
(HERE / "mine.json").write_text(json.dumps(mine, indent=1))
