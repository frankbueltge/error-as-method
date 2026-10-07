"""figure.py -> figure.svg: who found which storm (16 readings + the forecast), storms ordered by peak Kp."""
import json
D = json.loads(open('data.js').read()[len('const DATA = '):-2])
evs = sorted(D['events'], key=lambda e: (e['peak_kp'], e['first']))
def kp(k):
    n = round(k*3)/3; i = round(n); f = n - i
    return f"{i}{'+' if f > .1 else ('−' if f < -.1 else '')}"
rows = [(('fresh ' if r['cond'] == 'fresh' else 'memory ') + r['t'] + ' ' + r['id'], set(r['found']), '#5b3f8c') for r in D['reads']]
rows += [('forecast ' + t, {k for k, v in D['forecast'][t].items() if v}, '#c08a2e') for t in ['T1', 'T2', 'T3', 'T4']]
L, T, cw, ch = 150, 58, 26, 16
W = L + cw*len(evs) + 20; H = T + ch*len(rows) + 52
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans Mono, monospace" font-size="10">',
     f'<rect width="{W}" height="{H}" fill="#fbfaf7"/>',
     f'<text x="10" y="18" font-size="13" fill="#1c1c1e">Unknowing: which of 21 geomagnetic storms (2025) each reading named</text>',
     f'<text x="10" y="34" fill="#68656e">columns: storms by peak Kp, weakest left; purple: found; amber: my forecast of a fresh reader</text>']
for j, e in enumerate(evs):
    s.append(f'<text x="{L + j*cw + cw/2}" y="{T-6}" text-anchor="middle" fill="#68656e">{kp(e["peak_kp"])}</text>')
for i, (lab, found, col) in enumerate(rows):
    y = T + i*ch
    if i in (8, 16): s.append(f'<line x1="10" x2="{L + cw*len(evs)}" y1="{y}" y2="{y}" stroke="#1c1c1e"/>')
    s.append(f'<text x="{L-6}" y="{y+11}" text-anchor="end" fill="#68656e">{lab}</text>')
    for j, e in enumerate(evs):
        s.append(f'<rect x="{L + j*cw + 1}" y="{y+1}" width="{cw-2}" height="{ch-2}" fill="{col if e["id"] in found else "#e7e3dc"}"/>')
x6 = L + 7*cw
s.append(f'<line x1="{x6}" x2="{x6}" y1="{T-16}" y2="{T + ch*len(rows)}" stroke="#1c1c1e" stroke-dasharray="3 3"/>')
s.append(f'<text x="10" y="{H-22}" fill="#68656e">left of the dashed line: the seven storms at 6−, counted by this experiment\'s norm; no fresh reading named one.</text>')
s.append(f'<text x="10" y="{H-8}" fill="#68656e">Data: GFZ Potsdam Kp, CC BY 4.0 (doi:10.5880/Kp.0001). Readers: copies of one reader, 8 without memory, 8 with.</text>')
s.append('</svg>')
open('figure.svg', 'w').write('\n'.join(s)); print('figure.svg', W, H)
