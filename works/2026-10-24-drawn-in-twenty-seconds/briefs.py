#!/usr/bin/env python3
"""Write the 18 briefs from brief-template.txt, plan.json and orders.json. Arm S sees nothing;
arm F is shown the six S drawings of each thing (sheets/F-nn.png, made by sheets.py); arm H is shown
six people's drawings (sheets/H-nn.png). Nothing is said about the six in either arm."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SHEETS = "/tmp/k"  # a neutral path: the words around a brief steer a maker (experiment 11)
tpl = open(os.path.join(HERE, "brief-template.txt")).read()
cats = [c["category"] for c in json.load(open(os.path.join(HERE, "plan.json")))["categories"]]
orders = json.load(open(os.path.join(HERE, "orders.json")))
os.makedirs(os.path.join(HERE, "briefs"), exist_ok=True)
for maker, order in orders.items():
    arm = maker[0]
    lines = []
    for k, ci in enumerate(order, 1):
        line = f"{k}: Draw: {cats[ci]}"
        if arm in "FH":
            line += f"   (first open {SHEETS}/{arm}-{ci + 1:02d}.png)"
        lines.append(line)
    shown = ("" if arm == "S" else
             "\nBefore you draw each item, open the image file named beside it with your file-reading tool. "
             "Each image shows six drawings of that thing made by others.\n")
    exc = "" if arm == "S" else ", except reading the twelve image files named below"
    text = tpl.replace("{SHOWN}", shown).replace("{EXCEPT}", exc).replace("{ITEMS}", "\n".join(lines))
    open(os.path.join(HERE, "briefs", maker + ".txt"), "w").write(text)
print("wrote", len(orders))
