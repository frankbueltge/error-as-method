"""figure.svg: the 25 verdicts in the order given, coloured by the age of the deciding rule; rules marked where minted."""
import json
R = json.load(open("results.json")); V = R["per_verdict"]; M = R["minted"]
col = {"A": "#8a8278", "B": "#b8862b", "C": "#9c2f22"}; W, H, L, cw = 860, 300, 40, 31
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="12">',
     f'<rect width="{W}" height="{H}" fill="#f4efe6"/>',
     f'<text x="{L}" y="26" font-size="15" fill="#1d1b18">Twenty-five verdicts, in the order given, coloured by the age of the rule that decided them</text>']
for i, v in enumerate(V):
    x = L + i * cw; h = {"works": 120, "unsure": 80, "fails": 50}[v["verdict"]]
    o.append(f'<rect x="{x}" y="{200 - h}" width="{cw - 5}" height="{h}" fill="{col[v["age"]]}"/>')
    o.append(f'<text x="{x + (cw - 5) / 2}" y="216" text-anchor="middle" fill="#1d1b18">{v["variant"]}</text>')
    for n, at in M.items():
        if at == v["order"]:
            o.append(f'<text x="{x + (cw - 5) / 2}" y="{194 - h}" text-anchor="middle" fill="#9c2f22">{n}</text>')
o.append(f'<text x="{L}" y="240" fill="#7d756b">tall: works · middle: unsure · short: fails. Above a bar: a rule written at that picture. Picture 24 was built from the rules.</text>')
for k, (lab, x) in {"A": ("rule older than the data", L), "B": ("written at an earlier picture", L + 230), "C": ("written at this picture", L + 470)}.items():
    o.append(f'<rect x="{x}" y="258" width="12" height="12" fill="{col[k]}"/><text x="{x + 18}" y="269" fill="#1d1b18">{lab}</text>')
f = R["fails_by_age"]
o.append(f'<text x="{L}" y="290" fill="#1d1b18">Failures in the grid: {f["A"]} by an old rule, {f["B"]} by a rule from an earlier picture, {f["C"]} by a rule written at the failing picture.</text></svg>')
open("figure.svg", "w").write("\n".join(o)); print("ok")
