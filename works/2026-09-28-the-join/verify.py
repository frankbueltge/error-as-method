#!/usr/bin/env python3
"""Checks for The Join. No network. Run from anywhere inside the repository.

    python3 works/2026-09-28-the-join/verify.py
"""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AXIS = ROOT / "works" / "2026-09-20-the-borrowed-axis"
UNJUDGED = ROOT / "works" / "2026-08-28-the-unjudged"
fails = []


def check(ok, what):
    print(("  ok   " if ok else "  FAIL ") + what)
    if not ok:
        fails.append(what)


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout.strip()


# 1. the decision rule was committed before anything fetched was recorded
rel = HERE.relative_to(ROOT)
pred = git("log", "--diff-filter=A", "--format=%H", "--", str(rel / "PREDICTIONS.md")).split("\n")[-1]
man = git("log", "--diff-filter=A", "--format=%H", "--", str(rel / "sources/MANIFEST.json")).split("\n")[-1]
first = git("log", "--reverse", "--format=%H", "--", str(rel)).split("\n")[0]
check(bool(pred) and pred == first, "PREDICTIONS.md is the first commit that touches this work")
check(bool(man) and subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", pred, man]).returncode == 0
      and pred != man, "the manifest of fetches was committed after the predictions, in a later commit")
if pred:
    body = git("show", f"{pred}:{rel}/PREDICTIONS.md")
    check("M1 is taken" in body and "M3 is **excluded tonight in advance**" in body,
          "the rule choosing M1 and excluding M3 is in the predictions as first committed")

adj = json.loads((HERE / "adjudication.json").read_text(encoding="utf-8"))

# 2. the move is a subtraction and nothing else
mv = adj["position_move"]
check(mv["before"].replace(mv["subtracted"], "", 1) == mv["after"],
      "the new sentence is the old one with exactly the genus clause removed")
check(set(mv["after"].split()) <= set(mv["before"].split()), "no word enters the sentence")

# 3. C2: the source against Session 93's transcription (F-162)
# the extraction keeps the PDF's line breaks and one no-break space ("a\u00a0degradation"),
# so whitespace is normalised before comparing; nothing else is.
src = re.sub(r"\s+", " ", (AXIS / "sources" / "rheinberger-2016-vanishment.txt").read_text(encoding="utf-8"))
cases = {c["id"]: c for c in json.loads((AXIS / "cases.json").read_text(encoding="utf-8"))["cases"]}
quotes = json.loads((AXIS / "quotes.json").read_text(encoding="utf-8"))
quotes = quotes["quotes"] if isinstance(quotes, dict) and "quotes" in quotes else quotes
q13 = next(q for q in quotes if q.get("id") == "Q13")
check("deemed it to be a degradation product of the much bigger microsomal RNA that he was unable to remove "
      "from the fraction – a contaminant of the system thus" in src,
      "C2 at its source: 'deemed it to be a degradation product … a contaminant of the system thus'")
check("deemed to be a degradation product" in cases["C2"]["text"],
      "F-162 (a): cases.json drops 'it' from that quotation")
check("Q13" in cases["C2"]["source"] and "degradation" not in q13["text"],
      "F-162 (b): cases.json cites Q13, whose text is a different sentence")

# 4. C6: Session 73's record against Session 93's transcription (F-162)
ver = (UNJUDGED / "verification.json").read_text(encoding="utf-8")
check('"page_date_reported": "2010-01-26"' in ver, "C6 at Session 73's verification: reported 2010-01-26")
check("reported in 2009" in cases["C6"]["text"], "F-162 (c): cases.json says 'reported in 2009'")

# 5. the figure is what figure.py writes
out = subprocess.run([sys.executable, str(HERE / "figure.py")], capture_output=True, text=True).stdout
check(out.strip() == (HERE / "figure.svg").read_text(encoding="utf-8").strip(), "figure.svg is reproduced by figure.py")

# 6. meta.json carries what the protocol asks
meta = json.loads((HERE / "meta.json").read_text(encoding="utf-8"))
check(all(isinstance(meta.get(k), str) and meta[k].strip() for k in ("title", "date", "author", "medium", "embodies"))
      and meta["date"] == "2026-09-28", "meta.json has the five fields and tonight's date")

# 7. nothing here reaches the network
net = re.compile(r"^\s*(import|from)\s+(urllib|requests|http|socket)", re.M)
check(not any(net.search(p.read_text(encoding="utf-8")) for p in HERE.glob("*.py")),
      "no script in this work imports a network module")

# 8. nothing fetched tonight is committed
check(sorted(p.name for p in (HERE / "sources").iterdir()) == ["MANIFEST.json"],
      "sources/ holds the manifest and nothing else")

print("\n%d failed" % len(fails) if fails else "\nall checks pass")
sys.exit(1 if fails else 0)
