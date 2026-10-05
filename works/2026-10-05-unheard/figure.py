"""figure.svg: what decided. Left, the reading of the tower (four questions x three channels);
right, the ten changes to the practice's own bells, each a square coloured by its deciding channel."""
C = {"S": "#a3361f", "N": "#6b6257", "B": "#2b4c9b", "K": "#b08a2e", "-": "#e6dfd2", "x": "#ffffff"}
Q = ["bells", "change ringing?", "rhythm", "minor third"]
R = {"S": ["~", "~", "~", "-"], "N": ["y", "-", "-", "y"], "B": ["-", "x", "-", "-"]}
ch = ["S","S","S","S","K","S","S","K","S","K"]
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 300" font-family="Georgia,serif" font-size="13">',
     '<rect width="760" height="300" fill="#f4efe6"/>',
     '<text x="20" y="28" font-size="17">Reading the tower</text>',
     '<text x="420" y="28" font-size="17">Making its own bells: what decided each change</text>']
for j, c in enumerate("SNB"):
    o.append(f'<text x="{185+j*60}" y="58" fill="{C[c]}" font-weight="bold">{c}</text>')
leg = {"y": "settled", "~": "leaned, unsure", "-": "could not say", "x": "refused the data"}
for i, q in enumerate(Q):
    y = 80 + i * 40
    o.append(f'<text x="20" y="{y+5}">{q}</text>')
    for j, c in enumerate("SNB"):
        v = R[c][i]; f = {"y": C[c], "~": "none", "-": C["-"], "x": "#fff"}[v]
        st = f'stroke="{C[c]}" stroke-width="2"' if v in "~x" else ""
        o.append(f'<rect x="{178+j*60}" y="{y-10}" width="28" height="20" fill="{f}" {st}/>')
        if v == "x": o.append(f'<line x1="{178+j*60}" y1="{y-10}" x2="{206+j*60}" y2="{y+10}" stroke="{C[c]}" stroke-width="2"/>')
o.append('<text x="20" y="252" font-size="11" fill="#6b6257">filled: settled · outline: leaned · grey: could not say · struck: refused the data</text>')
o.append('<text x="20" y="270" font-size="11" fill="#6b6257">kept: six bells (N), minor third (N); change ringing and rhythm undecided</text>')
for i, c in enumerate(ch):
    x = 420 + (i % 5) * 62; y = 60 + (i // 5) * 62
    o.append(f'<rect x="{x}" y="{y}" width="52" height="52" fill="{C[c]}"/><text x="{x+26}" y="{y+32}" text-anchor="middle" fill="#fff" font-size="16">{c}</text>')
o.append('<text x="420" y="210">S pictures 7 · N numbers 0 · B ringers\' picture 0 · K belief 3</text>')
o.append('<text x="420" y="232" font-size="12" fill="#6b6257">The last verdict (does it sound like bells?) was not made:</text>')
o.append('<text x="420" y="250" font-size="12" fill="#6b6257">it is handed to the listener on the face.</text>')
o.append('</svg>')
open("figure.svg", "w").write("\n".join(o))
