"""Builds the blind coder's brief: the 18 B, S, R hand-backs under labels C01-C18 in an order drawn by seed 1711.
Writes coding/brief.txt and coding/key.json. The coder sees no arm, no contact list and no hypothesis."""
import json, random
from pathlib import Path
HERE = Path(__file__).parent.parent
ids = [f"{a}{i}" for a in "BSR" for i in range(1, 7)]
random.Random(1711).shuffle(ids)
key = {f"C{n+1:02d}": m for n, m in enumerate(ids)}
head = ("You are coding eighteen short hand-backs. In each, someone was asked to state numbers for a list of English words. "
        "Before answering, each person had been shown a list of 24 other words, each with a number described as those people's "
        "value. For each hand-back, decide one thing by this rule, applied word for word:\n\n"
        "YES if the hand-back says, in its HOW line or anywhere in it, that the told values did not fit the words (any statement "
        "that they seemed inconsistent with, surprising for, unrelated to, or only loosely tracking what the words are).\nNO otherwise.\n\n"
        "Code each hand-back on its own words only.\n\n")
body = "".join(f"===== {c} =====\n{(HERE / 'rooms' / f'{m}.txt').read_text().strip()}\n\n" for c, m in key.items())
tail = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and nothing else, "
        f"to the file {HERE.resolve()}/coding/answer.txt with your file-writing tool, then hand back the same text.\n\n"
        "Your answer is exactly 18 lines in the form\nC01: YES or NO\n...\nC18: YES or NO\n")
(HERE / "coding" / "brief.txt").write_text(head + body + tail)
(HERE / "coding" / "key.json").write_text(json.dumps(key, indent=1))
print("written", len(key))
