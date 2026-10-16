"""figure.py: writes figure.svg from results.json and, for the comparison row, experiment 21's results.json: per
cell, how many makers ended with the told kind, how many said they had been told, and how many doubted it on the
picture. The same carbon-dioxide sentence appears twice: true on experiment 21's record, false on tonight's."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "results.json")))
R21 = json.load(open(os.path.join(H, "..", "2026-10-16-told-true", "results.json")))
c = R["counts"]
rows = [("carbon dioxide, TRUE", "experiment 21, a record of CO2", R21["counts"]["C5"]["T"]["carbon"], 0, 0, "#2f6b4f"),
        ("carbon dioxide, FALSE", "tonight, a record of a pine trunk", c["C5"]["C"]["carbon"], c["C11_said_told"]["C"], c["C7_yes"]["C"], "#a4471f"),
        ("a tree's trunk, TRUE", "tonight, the same record", c["C5"]["T"]["tree"], c["C11_said_told"]["T"], c["C7_yes"]["T"], "#2f6b4f"),
        ("nothing", "tonight, the same record", c["C5"]["N"]["tree"], None, None, "#2d5470")]
W, Hh = 880, 380
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia,serif">' % (W, Hh, W, Hh),
     '<rect width="%d" height="%d" fill="#f3f0e8"/>' % (W, Hh),
     '<text x="20" y="32" font-size="19" fill="#1c1e21">Told What Fits: one sentence, once true and once false</text>',
     '<text x="20" y="54" font-size="12.5" fill="#5d6067">Six makers a row. Each square is one maker; filled means yes.</text>']
heads = ["ended with the told kind", "said it had been told", "doubted it on the picture"]
for k, h in enumerate(heads): s.append('<text x="%d" y="88" font-size="12" fill="#5d6067">%s</text>' % (330 + k * 180, h))
for j, (lab, sub, a, b, d, col) in enumerate(rows):
    y = 110 + j * 62
    s.append('<text x="20" y="%d" font-size="14.5" fill="%s">told: %s</text>' % (y + 14, col, lab))
    s.append('<text x="20" y="%d" font-size="11.5" fill="#5d6067">%s</text>' % (y + 32, sub))
    vals = [a, b, d]
    for k, v in enumerate(vals):
        x0 = 330 + k * 180
        if v is None: s.append('<text x="%d" y="%d" font-size="12" fill="#5d6067">nothing to say</text>' % (x0, y + 22)); continue
        for i in range(6):
            s.append('<rect x="%d" y="%d" width="18" height="18" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x0 + i * 23, y + 6, col if i < v else "none", col))
    if lab == "nothing": s.append('<text x="330" y="%d" font-size="11" fill="#5d6067">(first column: named the tree untold)</text>' % (y + 42))
s.append('<line x1="20" y1="%d" x2="%d" y2="%d" stroke="#d6cfbf"/>' % (Hh - 52, W - 20, Hh - 52))
s.append('<text x="20" y="%d" font-size="12.5" fill="#1c1e21">Truth made no difference. A sentence the picture could not tear was kept, and its source dropped, whether it was true or not.</text>' % (Hh - 32))
s.append('<text x="20" y="%d" font-size="11" fill="#5d6067">Record: stem radius of Scots pine 1038, Pfynwald (CH), hourly, 9 Jul to 7 Sep 2024 (TreeNet/WSL via EnviDat, CC BY 4.0). Coder B; exp. 21 row from its own results.json.</text>' % (Hh - 12))
s.append("</svg>")
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s)); print([r[2:5] for r in rows])
