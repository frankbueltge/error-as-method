"""figure.py -> figure.svg: the year of hourly PM10, the field's two episodes (shaded), the readers' seven
spike days (blue ticks), and the twelve readings' marks, one row each, coloured by kind."""
import json
from load import hourly
H = hourly(); h = json.load(open('home.json')); p = json.load(open('posthoc.json')); r = json.load(open('results.json'))
W, X0, PW, TOP, BH, YM, RH = 900, 90, 800, 30, 140, 120, 13
xd = lambda d: X0 + PW*(d-1)/365
col = {'K0': '#6b4a9e', 'K1': '#2a8a7a', 'K2': '#b5862a'}
F = 'font-family="DejaVu Sans Mono, monospace"'
names = sorted(r['readers'], key=lambda n: (r['readers'][n]['translation'], n))
rowsTop = TOP + BH + 28; Hh = rowsTop + len(names)*RH + 34
b = [f'<rect width="{W}" height="{Hh}" fill="#fbfaf6"/>',
     f'<text x="{X0}" y="18" {F} font-size="12" fill="#1d1c1f">PM10, hourly, 2025. Orange: the field\'s 2 episodes. Blue: the readers\' 7 spike days.</text>']
for e in h['events']:
    b.append(f'<rect x="{xd(e["first"]):.1f}" y="{TOP}" width="{PW*e["days"]/365:.1f}" height="{BH}" fill="#d9792b" opacity="0.25"/>')
for s in p['spike_days']:
    b.append(f'<rect x="{xd(s["day"])-1:.1f}" y="{TOP}" width="{PW/365+2:.1f}" height="{BH}" fill="#2f6fb0" opacity="0.25"/>')
seg, segs = [], []
for i, v in enumerate(v for d in H for v in d):
    if v is None:
        if seg: segs.append(seg); seg = []
        continue
    seg.append(f'{X0+PW*i/8760:.1f},{TOP+BH-BH*min(v, YM)/YM:.1f}')
if seg: segs.append(seg)
b += [f'<polyline points="{" ".join(s)}" fill="none" stroke="#3a383e" stroke-width="0.4"/>' for s in segs]
y50 = TOP + BH - BH*50/YM
b.append(f'<line x1="{X0}" x2="{X0+PW}" y1="{y50:.1f}" y2="{y50:.1f}" stroke="#d9792b" stroke-dasharray="4 3"/>')
b.append(f'<text x="{X0-6}" y="{y50+4:.1f}" {F} font-size="10" text-anchor="end" fill="#67646c">50</text>')
for q in [1, 60, 120, 180, 240, 300, 360]:
    b.append(f'<text x="{xd(q):.1f}" y="{TOP+BH+14}" {F} font-size="10" text-anchor="middle" fill="#67646c">{q}</text>')
def parse(s):
    a, _, c = str(s).partition('-'); a = int(a); c = int(c) if c else a; return min(a, c), max(a, c)
for k, n in enumerate(names):
    x = json.load(open(f'readers/{n}.json')); y = rowsTop + k*RH; c = col[x['kind']]
    if k == 6: b.append(f'<line x1="{X0}" x2="{X0+PW}" y1="{y-1}" y2="{y-1}" stroke="#cfcac2"/>')
    b.append(f'<text x="{X0-6}" y="{y+10}" {F} font-size="10" text-anchor="end" fill="{c}">{n}</text>')
    for a, e in map(parse, x['answer']['singular']):
        b.append(f'<rect x="{xd(a):.1f}" y="{y+2}" width="{max(2.5, PW*(e-a+1)/365):.1f}" height="{RH-4}" fill="{c}"/>')
b.append(f'<text x="{X0}" y="{Hh-10}" {F} font-size="11" fill="#67646c">12 readings: picture (top six), table. Purple: own reader. Teal, ochre: other trainings.</text>')
open('figure.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}">' + ''.join(b) + '</svg>')
print('figure.svg')
