"""figure.py: writes figure.svg from results.json and plan.json: per cell, how many makers said they had been told,
how many pages draw a check against a named kind, and what the told sentence's own kind came to in the maker's
words; and the inquirers' forecast beside it."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "results.json")))
pm = R["per_maker"]; cells = R["cells"]
said = {c: sum(pm[m]["C10"] == "yes" or pm[m]["C7"] == "yes" for m in cells[c]) for c in "TFN"}
drew = {c: sum(pm[m]["page_K2"] == "yes" for m in cells[c]) for c in "TFN"}
inq = R["S129.INQUIRY"]["per_inquirer"]; pred = {c: sum(v["I2"] == "yes" for v in inq.values() if v["cell"] == c) for c in "TF"}
prem = {c: sum(v["I3"] == "yes" for v in inq.values() if v["cell"] == c) for c in "TF"}
COL = {"T": "#2f6b4f", "F": "#a4471f", "N": "#2d5470"}; NAME = {"T": "told the truth (carbon dioxide)", "F": "told a falsehood (a tidal harbour)", "N": "told nothing"}
W, Hh = 860, 360; s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia,serif">' % (W, Hh, W, Hh),
    '<rect width="%d" height="%d" fill="#f3f0e8"/>' % (W, Hh),
    '<text x="20" y="30" font-size="19" fill="#1c1e21">Told True: eighteen makers, one record, three sentences</text>',
    '<text x="20" y="52" font-size="12.5" fill="#5d6067">Each square is one maker. Filled: yes. Empty: no.</text>']
rows = [("said in its report that it had been told what the record is", said, "N/A"), ("its page draws or states a check against a named kind", drew, None)]
y0 = 90
for j, c in enumerate("TFN"):
    x0 = 20 + j * 280
    s.append('<text x="%d" y="%d" font-size="14" fill="%s">%s</text>' % (x0, y0, COL[c], NAME[c]))
    for i, (lab, d, na) in enumerate(rows):
        yy = y0 + 22 + i * 62
        s.append('<text x="%d" y="%d" font-size="11" fill="#5d6067">%s</text>' % (x0, yy, lab if j == 0 or True else ""))
        if c == "N" and na: s.append('<text x="%d" y="%d" font-size="13" fill="#5d6067">nothing to say</text>' % (x0, yy + 24)); continue
        for k in range(6):
            fill = COL[c] if k < d[c] else "none"
            s.append('<rect x="%d" y="%d" width="20" height="20" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x0 + k * 26, yy + 8, fill, COL[c]))
        s.append('<text x="%d" y="%d" font-size="15" fill="#1c1e21">%d of 6</text>' % (x0 + 165, yy + 24, d[c]))
y1 = 260
s.append('<line x1="20" y1="%d" x2="%d" y2="%d" stroke="#d6cfbf"/>' % (y1 - 22, W - 20, y1 - 22))
s.append('<text x="20" y="%d" font-size="13" fill="#1c1e21">Before any maker ran, eight agents of the same kind read the told briefs without the picture (Orne\'s pre-inquiry).</text>' % y1)
for j, c in enumerate("TF"):
    x0 = 20 + j * 280
    s.append('<text x="%d" y="%d" font-size="12.5" fill="%s">%s brief: %d of 4 expect a work built on it as given;</text>' % (x0, y1 + 26 + 0, COL[c], "true" if c == "T" else "false", prem[c]))
    s.append('<text x="%d" y="%d" font-size="12.5" fill="%s">%d of 4 expect a work about checking it.</text>' % (x0, y1 + 44, COL[c], pred[c]))
s.append('<text x="580" y="%d" font-size="12.5" fill="#5d6067">Right about the truth,</text>' % (y1 + 26))
s.append('<text x="580" y="%d" font-size="12.5" fill="#5d6067">wrong about the falsehood.</text>' % (y1 + 44))
s.append('<text x="20" y="%d" font-size="11" fill="#5d6067">Record: CO2 at 31 m, NOAA tall tower, West Branch, Iowa, 15 Jul to 13 Sep 2019 (CC0). Codes: coder B (reports), coder D (pages only), coder Q (inquiry).</text>' % (Hh - 18))
s.append("</svg>")
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s)); print(said, drew, pred, prem)
