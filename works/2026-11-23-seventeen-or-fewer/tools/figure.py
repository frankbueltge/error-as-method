"""figure.svg: total syllables per poem, one dot per poem, five rows; filled = exactly 5-7-5."""
import json, os, sys
W = sys.argv[1]
r = json.load(open(os.path.join(W, 'results.json')))
pc = json.load(open(os.path.join(W, 'people', 'counts.json')))
rows = [('forum, people (50)', [x['counts'] for x in pc['forum_all_100'][:50]], '#9a958a'),
        ('journal, people (50)', [x['counts'] for x in pc['journal_all_105'][:50]], '#4f7385'),
        ('makers, no sheet (12)', [p['final']['counts'] for p in r['poems'] if p['arm'] == 'W'], '#c2502a'),
        ('makers, forum sheet (12)', [p['final']['counts'] for p in r['poems'] if p['arm'] == 'F'], '#c2502a'),
        ('makers, journal sheet (12)', [p['final']['counts'] for p in r['poems'] if p['arm'] == 'J'], '#c2502a')]
x0, dx, y0, dy, d = 200, 26, 70, 80, 7
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{y0+dy*len(rows)+40}" viewBox="0 0 760 {y0+dy*len(rows)+40}" font-family="Georgia,serif" font-size="13">',
       '<rect width="100%" height="100%" fill="#f6f4ef"/>',
       '<text x="20" y="26" font-size="15" fill="#1d1d1b">Syllables per haiku. Each dot one poem; filled = exactly 5-7-5.</text>']
for t in range(4, 23, 2):
    out.append(f'<text x="{x0+(t-4)*dx}" y="{y0+dy*len(rows)+20}" fill="#77746c" text-anchor="middle">{t}</text>')
out.append(f'<line x1="{x0+13*dx}" x2="{x0+13*dx}" y1="{y0-14}" y2="{y0+dy*len(rows)-10}" stroke="#c9c4b8" stroke-dasharray="3 3"/>')
for i, (lab, cs, col) in enumerate(rows):
    y = y0 + dy * i + 28
    n575 = sum(c == [5, 7, 5] for c in cs)
    out.append(f'<text x="20" y="{y+4}" fill="#1d1d1b">{lab}</text><text x="20" y="{y+20}" fill="#77746c" font-size="11">{n575} are 5-7-5</text>')
    stack = {}
    for c in cs:
        t = sum(c); k = stack.get(t, 0); stack[t] = k + 1
        cx = x0 + (t - 4) * dx + (k % 3 - 1) * (d + 1); cy = y - (k // 3) * (d - 2) + 4
        fill = col if c == [5, 7, 5] else 'none'
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{d/2}" fill="{fill}" stroke="{col}"/>')
out.append('</svg>')
open(os.path.join(W, 'figure.svg'), 'w').write('\n'.join(out))
