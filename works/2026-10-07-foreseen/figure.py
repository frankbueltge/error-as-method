"""figure.py -> figure.svg: the series, the practice's 24 events (its norm for 'singular'), the readers' 47 marks,
the total solar eclipse of 2024-04-08; below, the 40-cell forecast with each reading."""
import json, os, re
from load import load
v, days = load(); h = json.load(open('home.json')); r = json.load(open('results.json')); fc = json.load(open('forecast.json'))['cells']
N = len(v); W, L, Rm, T, Hh = 1000, 48, 10, 30, 220
X = lambda d: L + (W - L - Rm) * (d - 1) / (N - 1); Y = lambda x: T + Hh * (1 - x / 4000)
F0 = 'font-family="DejaVu Sans Mono, monospace"'; F = F0 + ' font-size="10" fill="#555"'
b = [f'<rect width="{W}" height="520" fill="#f6f4ef"/>', f'<text x="{L}" y="18" {F0} font-size="12" fill="#111">Daily views, "Full moon", en.wikipedia, 2024-25. Ochre: the practice\'s norm. Blue: readers\' marks.</text>']
for t in (0, 1000, 2000, 3000, 4000):
    b.append(f'<line x1="{L}" x2="{W-Rm}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="#ddd"/><text x="{L-5}" y="{Y(t)+3:.1f}" text-anchor="end" {F}>{t}</text>')
for e in h['events']:
    b.append(f'<rect x="{X(e["start"])-2:.1f}" y="{T}" width="{max(4, X(e["end"])-X(e["start"])+4):.1f}" height="{Hh}" fill="#c9a04a" opacity=".35"/>')
b.append('<polyline fill="none" stroke="#111" stroke-width="0.9" points="' + ' '.join(f'{X(i+1):.1f},{Y(x):.1f}' for i, x in enumerate(v)) + '"/>')
cnt = {}
for f in sorted(os.listdir('readers')):
    if not f.startswith('F-'): continue
    for s in json.load(open('readers/' + f))['answer']['stands_out']:
        n = [int(x) for x in re.findall(r'\d+', s)]; m = (n[0] + n[-1]) / 2; cnt[m] = cnt.get(m, 0) + 1
        b.append(f'<circle cx="{X(m):.1f}" cy="{T+Hh+8+5*(cnt[m]-1):.1f}" r="2.3" fill="#2f5f9e"/>')
b.append(f'<text x="{X(99)+4:.1f}" y="{Y(3700):.1f}" {F0} font-size="10" fill="#b2452f">&#8592; day 99: solar eclipse, 2.93x</text>')
for d in (1, 100, 200, 300, 400, 500, 600, 700, 731):
    b.append(f'<text x="{X(d):.1f}" y="{T+Hh+52}" text-anchor="middle" {F}>{d}</text>')
# matrix
y0 = 330; TS = ['T1', 'T2', 'T3', 'T4', 'T5']; TN = ['line', 'log line', 'weekly sums', 'week grid', 'monthly table']
b.append(f'<text x="{L}" y="{y0-12}" {F0} font-size="12" fill="#111">Forecast before the data (shaded = right). Dots: two readers; red = missed. Misses: R {r["misses"]["regular"]}, S {r["misses"]["singular"]}.</text>')
for j, t in enumerate(TS): b.append(f'<text x="{260+j*140+50}" y="{y0+8}" text-anchor="middle" {F}>{t} {TN[j]}</text>')
for i, q in enumerate(fc):
    y = y0 + 16 + i * 20
    b.append(f'<text x="{L}" y="{y+13}" {F}>{q}</text>')
    for j, t in enumerate(TS):
        x = 260 + j * 140; f = fc[q][t] == 'C'
        b.append(f'<rect x="{x}" y="{y}" width="100" height="18" fill="{"#e2dccf" if f else "#fbfaf6"}" stroke="#ccc"/>')
        for k, rr in enumerate('ab'):
            c = r['cells'][f'{q}.{t}{rr}']['correct']; col = '#2f5f9e' if c == f else '#b2452f'
            b.append(f'<circle cx="{x+38+k*24}" cy="{y+9}" r="6" fill="{col if c else "none"}" stroke="{col}" stroke-width="2"/>')
open('figure.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 520" width="{W}" height="520">' + ''.join(b) + '</svg>')
