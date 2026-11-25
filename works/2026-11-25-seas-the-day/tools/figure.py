"""figure.svg: every name, by how many registered recreational boats bear it; the register's 200 and each arm's 60."""
import json, math, os, sys

here = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(here, "..")
exec(open(os.path.join(W, "face-data.js")).read().replace("window.SEAS=", "D=").rstrip().rstrip(";"), globals())
COL = {"people": "#1f5f7a", "E": "#b5452b", "D": "#8a6a12", "G": "#6b4c8a"}
LAB = {"people": "the register, 200 drawn", "E": "E: names only", "D": "D: own numbers first", "G": "G: people's numbers given"}


def X(f):
    v = 0 if f <= 0 else 1 + math.log10(f)
    return 210 + 760 * v / 4.0


def jit(i):
    x = math.sin(i * 12.9898) * 43758.5453
    return x - math.floor(x)


out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" font-family="Georgia,serif">',
       '<rect width="1000" height="380" fill="#f3efe6"/>',
       f'<rect x="{X(2)-4:.1f}" y="40" width="{X(9.5)-X(2)+8:.1f}" height="270" fill="#e6dfcf"/>',
       f'<text x="{X(4.2):.1f}" y="54" font-size="12" text-anchor="middle" fill="#5d6a72">shared by 2 to 9</text>',
       '<text x="16" y="24" font-size="16" fill="#1d2a33">How many registered boats carry each name: the register\'s names and three arms of machine makers</text>']
for f, l in [(0, "none"), (1, "1"), (10, "10"), (100, "100"), (1000, "1,000")]:
    out.append(f'<line x1="{X(f):.1f}" x2="{X(f):.1f}" y1="40" y2="310" stroke="#c9c1b1"/>')
    out.append(f'<text x="{X(f):.1f}" y="328" font-size="12" text-anchor="middle" fill="#1d2a33">{l}</text>')
out.append('<text x="590" y="350" font-size="12" text-anchor="middle" fill="#5d6a72">valid recreational vessels in the US register bearing exactly this name, 25 Nov 2026 (log scale; makers\' inventions at "none")</text>')
prof = {"people": D["profiles"]["people_score"], "E": D["profiles"]["E"], "D": D["profiles"]["D"], "G": D["profiles"]["G"]}
for ri, k in enumerate(["people", "E", "D", "G"]):
    yc = 85 + ri * 64
    p = prof[k]
    out.append(f'<text x="12" y="{yc-2}" font-size="13" fill="#1d2a33">{LAB[k]}</text>')
    out.append(f'<text x="12" y="{yc+14}" font-size="11" fill="#5d6a72">median {p["median_freq"]:g}; 100+: {p["FREQ100"]:g} %; 2–9: {p["FREQ2_9"]:g} %</text>')
    for i, d in enumerate(D["ladder"][k]):
        f = d["f"]
        x = X(0) + (jit(i * 7 + ri) - .5) * 30 if f == 0 else X(f * (1 + (jit(i + ri * 997) - .5) * .18))
        y = yc + (jit(i * 3 + ri * 11) - .5) * 36
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{COL[k]}" fill-opacity=".75"/>')
    out.append(f'<line x1="{X(p["median_freq"]):.1f}" x2="{X(p["median_freq"]):.1f}" y1="{yc-22}" y2="{yc+22}" stroke="{COL[k]}" stroke-width="3"/>')
out.append(f'<text x="{X(337):.1f}" y="370" font-size="11" text-anchor="middle" fill="#b5452b">SERENITY: 337 boats; on 16 of 18 makers\' lists</text>')
out.append("</svg>")
open(os.path.join(W, "figure.svg"), "w").write("\n".join(out))
print("ok")
