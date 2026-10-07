"""figure.svg: who bears the error, by coder, against metrology's convention. Standard library only."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "results.json")))
rows = [("the practice", r["practice"]), ("fresh reader A", r["readers"]["A"]["counts"]),
        ("fresh reader B", r["readers"]["B"]["counts"]), ("as VIM 2.16 would read", {"J": 29})]
col = {"R": "#2f5d7c", "B": "#7a4f8f", "X": "#9b9488", "J": "#9a5a1c"}
lab = {"R": "held term wrong", "B": "both", "X": "neither", "J": "judged term wrong"}
W, x0, bw, unit = 760, 190, 520, 520 / 29
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 310" font-family="Georgia,serif" font-size="13">',
       f'<rect width="{W}" height="310" fill="#f4f1ea"/>',
       '<text x="20" y="30" font-size="17" fill="#1d1c1a">Which term of the difference was wrong? 29 registered errors, F-164 to F-192</text>']
for k, (name, c) in enumerate(rows):
    y = 60 + k * 46
    out.append(f'<text x="20" y="{y+19}" fill="#1d1c1a">{name}</text>')
    x = x0
    for key in ("R", "B", "X", "J"):
        n = c.get(key, 0)
        if not n: continue
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{n*unit:.1f}" height="28" fill="{col[key]}"/>')
        out.append(f'<text x="{x+4:.1f}" y="{y+19}" fill="#fff">{n}</text>')
        x += n * unit
for i, key in enumerate(("R", "B", "X", "J")):
    out.append(f'<rect x="{x0+i*135}" y="252" width="12" height="12" fill="{col[key]}"/><text x="{x0+i*135+17}" y="262" fill="#1d1c1a">{lab[key]}</text>')
out.append('<text x="20" y="284" fill="#6d675d" font-size="11.5">Metrology subtracts the reference from the measured value, so the reference never bears the error.</text>')
out.append('<text x="20" y="298" fill="#6d675d" font-size="11.5">In this register the held term alone was wrong in 13 of 29 by the practice\'s reading, 8 and 10 by two fresh readers.</text>')
out.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(out))
