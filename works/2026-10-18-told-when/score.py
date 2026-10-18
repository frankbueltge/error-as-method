"""score.py -- written before any maker runs (Session 135). Reads plan.json, coder/H/answers.json and the twelve
pages (makers/mNN/index.html) and writes results.json. Rules, as fixed in PREDICTIONS.md:
  a maker MAKES A WHEN-CLAIM if coder H lists at least one claim with from_when "yes";
  it HOLDS APART if any of its from_when "yes" claims has standing "given" or "against";
  it DERIVES if any of its from_when "yes" claims has step "derived";
  a page CARRIES THE DATE if its visible-text-and-script source matches DATE_RE (case-insensitive);
  a maker NAMES SOIL if any `what` claim's text contains "soil" or "ground" or "earth" (substring, lower case);
  it NAMES TEMPERATURE if any favoured `what` claim's text contains "temperat".
S133.PREMISE (works/FALSIFIERS.md): void if fewer than 4 of the 6 W makers make a when-claim; falsified if at least
3 of the W makers hold apart; otherwise held."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
DATE_RE = re.compile(r"\b(july|september|august|2025|summer|autumn|equinox)\b", re.I)
plan = json.load(open(os.path.join(HERE, "plan.json")))["makers"]
A = json.load(open(os.path.join(HERE, "coder", "H", "answers.json")))
out = {"makers": {}, "cells": {}}
for p in plan:
    m, c = p["maker"], p["cell"]
    cl = A.get(m, {}).get("claims", [])
    fw = [x for x in cl if x.get("from_when") == "yes"]
    page = open(os.path.join(HERE, "makers", m, "index.html"), encoding="utf-8", errors="replace").read()
    hits = sorted(set(h.lower() for h in DATE_RE.findall(page)))
    what = [x for x in cl if x.get("topic") == "what"]
    out["makers"][m] = {"cell": c, "when_claim": bool(fw),
        "held_apart": any(x.get("standing") in ("given", "against") for x in fw),
        "derives": any(x.get("step") == "derived" for x in fw),
        "n_from_when": len(fw), "n_derived": sum(1 for x in fw if x.get("step") == "derived"),
        "page_date_hits": hits, "page_carries_date": bool(hits),
        "names_soil": any(any(k in x.get("claim", "").lower() for k in ("soil", "ground", "earth")) for x in what),
        "names_temperature": any("temperat" in x.get("claim", "").lower() for x in what if x.get("favoured") == "yes"),
        "kind_from_when": any(x.get("topic") == "what" and x.get("from_when") == "yes" for x in cl)}
for c in ("N", "W"):
    ms = [v for v in out["makers"].values() if v["cell"] == c]
    out["cells"][c] = {k: sum(1 for v in ms if v[k]) for k in
        ("when_claim", "held_apart", "derives", "page_carries_date", "names_soil", "names_temperature", "kind_from_when")}
    out["cells"][c]["n"] = len(ms)
w = out["cells"]["W"]
out["S133.PREMISE"] = ("void" if w["when_claim"] < 4 else "falsified" if w["held_apart"] >= 3 else "held")
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out["cells"], indent=1), out["S133.PREMISE"])
