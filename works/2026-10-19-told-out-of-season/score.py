"""score.py -- written before any maker runs (Session 137). Reads plan.json, coder/H/answers.json and the eighteen
pages (makers/mNN/index.html) and writes results.json. Rules, as fixed in PREDICTIONS.md:
  a maker MAKES A WHEN-CLAIM if coder H lists at least one claim with from_when "yes";
  it HOLDS APART if any of its from_when "yes" claims has standing "given" or "against";
  it DERIVES if any of its from_when "yes" claims has step "derived";
  it DOUBTS if it holds apart, or coder H's `fit` is "disagree"            (S136.RESCUE's `doubt`);
  it goes SOUTH if coder H's `hemisphere` is "south";
  it RESCUES if it does not doubt, makes a when-claim, and coder H lists at least one premise  (S136.RESCUE's `rescue`);
  it COLLIDES if it doubts or goes south                                    (S135.DEFAULT's count);
  a page CARRIES THE DATE if its source matches DATE_RE (case-insensitive);
  it NAMES WATER if any `what` claim's text contains river, stream, creek, discharge, runoff, melt, glacier or snow.
S135.DEFAULT: falsified if fewer than 3 of 6 C makers collide, or at least 3 of 6 A makers collide; otherwise held.
S136.RESCUE: among the C makers, void if doubt + rescue < 3; falsified if doubt >= rescue; otherwise held."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
DATE_RE = re.compile(r"\b(january|february|march|october|november|december|2025|winter|autumn|fall|summer|spring|solstice|equinox)\b", re.I)
WATER = ("river", "stream", "creek", "discharge", "runoff", "melt", "glacier", "snow")
plan = json.load(open(os.path.join(HERE, "plan.json")))["makers"]
A = json.load(open(os.path.join(HERE, "coder", "H", "answers.json")))
out = {"makers": {}, "cells": {}}
for p in plan:
    m, c = p["maker"], p["cell"]
    a = A.get(m, {}); cl = a.get("claims", [])
    fw = [x for x in cl if x.get("from_when") == "yes"]
    page = open(os.path.join(HERE, "makers", m, "index.html"), encoding="utf-8", errors="replace").read()
    hits = sorted(set(h.lower() for h in DATE_RE.findall(page)))
    held = any(x.get("standing") in ("given", "against") for x in fw)
    doubt = held or a.get("fit") == "disagree"
    south = a.get("hemisphere") == "south"
    out["makers"][m] = {"cell": c, "when_claim": bool(fw), "held_apart": held,
        "derives": any(x.get("step") == "derived" for x in fw), "n_from_when": len(fw),
        "fit": a.get("fit"), "hemisphere": a.get("hemisphere"), "n_premises": len(a.get("premises", [])),
        "doubt": doubt, "south": south, "rescue": (not doubt) and bool(fw) and bool(a.get("premises")),
        "collide": doubt or south, "page_date_hits": hits, "page_carries_date": bool(hits),
        "names_water": any(any(k in x.get("claim", "").lower() for k in WATER) for x in cl if x.get("topic") == "what")}
KEYS = ("when_claim", "held_apart", "derives", "doubt", "south", "rescue", "collide", "page_carries_date", "names_water")
for c in ("C", "A", "N"):
    ms = [v for v in out["makers"].values() if v["cell"] == c]
    out["cells"][c] = {k: sum(1 for v in ms if v[k]) for k in KEYS}; out["cells"][c]["n"] = len(ms)
C, Ac = out["cells"]["C"], out["cells"]["A"]
out["S135.DEFAULT"] = "falsified" if (C["collide"] < 3 or Ac["collide"] >= 3) else "held"
out["S136.RESCUE"] = ("void" if C["doubt"] + C["rescue"] < 3 else "falsified" if C["doubt"] >= C["rescue"] else "held")
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out["cells"], indent=1), out["S135.DEFAULT"], out["S136.RESCUE"])
