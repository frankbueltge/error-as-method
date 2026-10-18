"""facedata.py: writes face-data.js (what index.html shows) and thumbs/mNN.jpg (440 x 320) from the committed
evidence: plan.json, makers/mNN/NOTE.md (title), seasons.json, coder/H/answers.json, results.json and
materials/hourly.json. Nothing is typed by hand into the face's data."""
import json, os, random, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding="utf-8"))
plan, S, A, R, H = J("plan.json")["makers"], J("seasons.json"), J("coder", "H", "answers.json"), J("results.json"), J("materials", "hourly.json")
makers = []
for p in plan:
    m = p["maker"]
    title = re.sub(r"^#+\s*", "", open(os.path.join(HERE, "makers", m, "NOTE.md"), encoding="utf-8").read().strip().splitlines()[0]).strip()
    fw = [{"claim": c["claim"], "step": c["step"], "standing": c["standing"], "quote": c["quotes"][0]["text"]}
          for c in A[m]["claims"] if c["from_when"] == "yes" and c["topic"] == "when"]
    kind = [c["claim"] for c in A[m]["claims"] if c["topic"] == "what" and c["favoured"] == "yes"]
    makers.append({"m": m, "cell": p["cell"], "title": title, "season": S["makers"][m]["words"], "cls": S["makers"][m]["class"],
                   "when": fw, "kind": kind[0] if kind else "", "held_apart": R["makers"][m]["held_apart"]})
    Image.open(os.path.join(HERE, "shots", m + ".png")).convert("RGB").resize((440, 320), Image.LANCZOS).save(
        os.path.join(HERE, "thumbs", m + ".jpg"), quality=78)
random.Random(1350).shuffle(makers)
data = {"makers": makers, "cells": R["cells"], "premise": R["S133.PREMISE"], "temp_f": H["soil_temp_2in_degF"],
        "start": H["start_local_standard_time"]}
open(os.path.join(HERE, "face-data.js"), "w", encoding="utf-8").write("window.FACE=" + json.dumps(data, ensure_ascii=False) + ";\n")
print(len(makers), [x["m"] for x in makers])
