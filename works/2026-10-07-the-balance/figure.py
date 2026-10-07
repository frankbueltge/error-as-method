"""figure.py: results.json -> figure.svg (transition codes per lineage, blind filled, open outlined; v0 form names)."""
import json
r = json.load(open('results.json'))
col = {'SCHEMA': '#2f5d8a', 'STRIKE': '#8a3b2f', 'ADD': '#9a958b', 'SAME': '#d8d3c9'}
v0 = {'P1': 'beam balance, dome pans', 'P2': 'beam balance, stacked slabs', 'B1': 'breathing disc', 'B2': 'breathing disc', 'C1': 'breathing disc on a dial', 'C2': 'breathing disc'}
arm = {'P1': 'plain', 'P2': 'plain', 'B1': 'test', 'B2': 'test'}
W, H = 820, 360
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f3f1ec"/>',
     '<text x="20" y="28" font-size="17" fill="#1d1c1a">The Balance — sixteen hand-overs, coded</text>',
     '<text x="20" y="48" fill="#6d6a63">filled: blind coder, pictures only · outlined: the practice, with notes and code</text>']
for j, h in enumerate(['v0: the first form', 'v0→v1', 'v1→v2', 'v2→v3', 'v3→v4']):
    s.append(f'<text x="{230 + j * 115 if j else 110}" y="80" fill="#6d6a63">{h}</text>')
for i, L in enumerate(['P1', 'P2', 'B1', 'B2']):
    y = 100 + i * 46
    s.append(f'<text x="20" y="{y + 18}" fill="#1d1c1a">{L}</text><text x="48" y="{y + 18}" fill="#6d6a63" font-size="11">{arm[L]}</text>')
    s.append(f'<text x="110" y="{y + 18}" fill="#1d1c1a" font-size="12">{v0[L]}</text>')
    for k in range(1, 5):
        x = 230 + (k - 1) * 115
        b, o = r['blind'][f'{L}-{k}'], r['open'][f'{L}-{k}']
        s.append(f'<rect x="{x + 115}" y="{y}" width="52" height="26" fill="{col[b]}"/>')
        s.append(f'<text x="{x + 115 + 26}" y="{y + 17}" text-anchor="middle" fill="{"#1d1c1a" if b == "SAME" else "#fff"}" font-size="10" font-family="monospace">{b}</text>')
        s.append(f'<rect x="{x + 115 + 56}" y="{y + 1}" width="50" height="24" fill="none" stroke="{col[o] if o != "SAME" else "#6d6a63"}" stroke-width="2"/>')
        s.append(f'<text x="{x + 115 + 81}" y="{y + 17}" text-anchor="middle" fill="{col[o] if o != "SAME" else "#6d6a63"}" font-size="10" font-family="monospace">{o}</text>')
s.append('<line x1="20" x2="800" y1="290" y2="290" stroke="#cfcac0"/>')
s.append('<text x="20" y="312" fill="#1d1c1a">Control, same v0 brief in a folder with no name: C1 breathing disc on a dial, C2 breathing disc. Neither names a balance.</text>')
s.append('<text x="20" y="334" fill="#6d6a63">All four makers in works/2026-10-07-the-balance/ took “balance” as the theme. Source: results.json, CONTROL.md.</text>')
s.append('</svg>')
open('figure.svg', 'w').write('\n'.join(s))
