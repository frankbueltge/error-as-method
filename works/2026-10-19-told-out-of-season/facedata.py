"""facedata.py: writes face-data.js (what index.html shows) from the committed evidence: plan.json, makers/mNN/NOTE.md
(title), coder/H/answers.json (favoured kind, premises, fit, hemisphere), results.json and materials/hourly.json.
Nothing is typed by hand into the face's data except KIND, the practice's grouping of coder H's favoured `what`
claims into four classes, made after reading and applied by the keyword rule below (first match wins)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding="utf-8"))
plan, A, R, H = J("plan.json")["makers"], J("coder", "H", "answers.json"), J("results.json"), J("materials", "hourly.json")
KIND = [("stream", r"stream|river|flow|discharge"), ("store", r"heater|stove|store|reservoir|tank|battery"),
        ("sun", r"temperature|sun"), ("other", r".")]
makers = []
for p in plan:
    m = p["maker"]; a = A[m]
    title = re.sub(r"^#+\s*", "", open(os.path.join(HERE, "makers", m, "NOTE.md"), encoding="utf-8").read().strip().splitlines()[0]).strip()
    fav = [c["claim"] for c in a["claims"] if c["topic"] == "what" and c["favoured"] == "yes"]
    fav = fav[0] if fav else ""
    kind = next(k for k, rx in KIND if re.search(rx, fav, re.I))
    quote = next((q["text"] for c in a["claims"] if c["topic"] == "what" and c["favoured"] == "yes" for q in c["quotes"]), "")
    makers.append({"m": m, "cell": p["cell"], "title": title, "kind": kind, "fav": fav, "quote": quote,
                   "premises": [x["premise"] for x in a["premises"]], "fit": a["fit"], "hemisphere": a["hemisphere"],
                   "doubt": R["makers"][m]["doubt"], "rescue": R["makers"][m]["rescue"], "south": R["makers"][m]["south"]})
tally = {c: {k: sum(1 for x in makers if x["cell"] == c and x["kind"] == k) for k, _ in KIND} for c in "CAN"}
data = {"makers": makers, "cells": R["cells"], "tally": tally, "default": R["S135.DEFAULT"], "rescue": R["S136.RESCUE"],
        "q": H["discharge_cfs"], "start": H["start_local_standard_time"]}
open(os.path.join(HERE, "face-data.js"), "w", encoding="utf-8").write("window.FACE=" + json.dumps(data, ensure_ascii=False) + ";\n")
json.dump(tally, open(os.path.join(HERE, "kinds.json"), "w"), indent=1)
print(json.dumps(tally))
for x in makers: print(x["m"], x["cell"], x["kind"], x["title"])
