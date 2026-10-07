"""render.py -> renders/T1.svg T2.svg T3.svg T4.svg and renders/T5.txt, the five translations.
render.js turns the SVGs into PNGs. Day numbers only; no titles; nothing names the quantity."""
import os, math, statistics as st
from load import load
v, days = load()
v = [x if x is not None else 0 for x in v]
N = len(v)
os.makedirs('renders', exist_ok=True)
F = 'font-family="DejaVu Sans Mono, monospace" font-size="13" fill="#111"'
def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
def nice(top):
    e = 10 ** math.floor(math.log10(top)); 
    for m in (1, 2, 2.5, 5, 10):
        if top / (m * e) <= 8: return m * e
X0, Y0, W, H = 80, 15, 1500, 350
def xaxis():
    b = f'<line x1="{X0}" y1="{Y0+H}" x2="{X0+W}" y2="{Y0+H}" stroke="#111"/>'
    for dd in [1] + list(range(50, 731, 50)) + [731]:
        x = X0 + W * (dd - 1) / (N - 1)
        b += f'<line x1="{x:.1f}" y1="{Y0+H}" x2="{x:.1f}" y2="{Y0+H+4}" stroke="#111"/><text x="{x:.1f}" y="{Y0+H+18}" text-anchor="middle" {F}>{dd}</text>'
    return b + f'<text x="{X0+W/2}" y="{Y0+H+36}" text-anchor="middle" {F}>day</text>'
def yaxis(ticks, f):
    b = f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0+H}" stroke="#111"/>'
    for t in ticks:
        y = f(t)
        b += f'<line x1="{X0-4}" y1="{y:.1f}" x2="{X0}" y2="{y:.1f}" stroke="#111"/><text x="{X0-8}" y="{y+4:.1f}" text-anchor="end" {F}>{t:g}</text>'
    return b
# T1 daily line, linear
top = max(v); step = nice(top); ymax = step * math.ceil(top / step)
fy = lambda t: Y0 + H - H * t / ymax
pts = ' '.join(f'{X0 + W*i/(N-1):.2f},{fy(x):.2f}' for i, x in enumerate(v))
open('renders/T1.svg', 'w').write(svg(1600, 420, xaxis() + yaxis([step * k for k in range(int(ymax / step) + 1)], fy)
     + f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="1"/>'))
# T2 daily line, log
lo = 10 ** math.floor(math.log10(max(1, min(v)))); hi = 10 ** math.ceil(math.log10(top))
fl = lambda t: Y0 + H - H * (math.log10(max(t, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
ticks = [m * 10 ** e for e in range(int(math.log10(lo)), int(math.log10(hi)) + 1) for m in (1, 2, 5) if lo <= m * 10 ** e <= hi]
pts = ' '.join(f'{X0 + W*i/(N-1):.2f},{fl(x):.2f}' for i, x in enumerate(v))
open('renders/T2.svg', 'w').write(svg(1600, 420, xaxis() + yaxis(ticks, fl)
     + f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="1"/>'))
# T3 weekly sums as bars; week k = days 7k-6..7k; week 105 holds days 729-731 only
wk = [sum(v[i:i + 7]) for i in range(0, N, 7)]
top = max(wk); step = nice(top); ymax = step * math.ceil(top / step)
fy = lambda t: Y0 + H - H * t / ymax
bw = W / len(wk); body = ''
for k, s in enumerate(wk):
    body += f'<rect x="{X0 + k*bw + 1:.1f}" y="{fy(s):.1f}" width="{bw-2:.1f}" height="{Y0+H-fy(s):.1f}" fill="#111"/>'
xa = f'<line x1="{X0}" y1="{Y0+H}" x2="{X0+W}" y2="{Y0+H}" stroke="#111"/>'
for k in [1] + list(range(10, len(wk) + 1, 10)) + [len(wk)]:
    x = X0 + (k - 0.5) * bw
    xa += f'<line x1="{x:.1f}" y1="{Y0+H}" x2="{x:.1f}" y2="{Y0+H+4}" stroke="#111"/><text x="{x:.1f}" y="{Y0+H+18}" text-anchor="middle" {F}>{k}</text>'
xa += f'<text x="{X0+W/2}" y="{Y0+H+36}" text-anchor="middle" {F}>week (week k = days 7k-6 to 7k)</text>'
open('renders/T3.svg', 'w').write(svg(1600, 420, xa + yaxis([step * k for k in range(int(ymax / step) + 1)], fy) + body))
# T4 grid: one column per week, one row per position in the week (row 1 = the weekday of day 1), grey by log value
lmin, lmax = math.log(max(1, min(v))), math.log(max(v))
g = lambda x: int(245 - 245 * (math.log(max(x, 1)) - lmin) / (lmax - lmin))
cs, gx, gy = 13, 60, 40; body = ''
for i, x in enumerate(v):
    c, r = divmod(i, 7); gg = g(x)
    body += f'<rect x="{gx + c*cs}" y="{gy + r*cs}" width="{cs-1}" height="{cs-1}" fill="rgb({gg},{gg},{gg})"/>'
for r in range(7): body += f'<text x="{gx-8}" y="{gy + r*cs + 11}" text-anchor="end" {F}>{r+1}</text>'
for c in [0] + list(range(9, 105, 10)) + [104]:
    body += f'<text x="{gx + c*cs + 6}" y="{gy-8}" text-anchor="middle" {F}>{c+1}</text>'
body += f'<text x="{gx}" y="{gy-26}" {F}>column = week k (days 7k-6 to 7k); row = position in the week</text>'
ky = gy + 7 * cs + 30
for n, t in enumerate([m * 10 ** e for e in range(0, 9) for m in (1, 3) if lmin <= math.log(m * 10 ** e) <= lmax]):
    gg = g(t); body += f'<rect x="{gx + n*70}" y="{ky}" width="66" height="16" fill="rgb({gg},{gg},{gg})" stroke="#111" stroke-width="0.5"/><text x="{gx + n*70 + 33}" y="{ky+32}" text-anchor="middle" {F}>{t:g}</text>'
open('renders/T4.svg', 'w').write(svg(gx + 105 * cs + 40, ky + 50, body))
# T5 a table: one row per calendar month, by day range; median, maximum, day of the maximum
rows = ['month  days      median     maximum  day_of_max']
for y in (2024, 2025):
    for m in range(1, 13):
        idx = [i for i, d in enumerate(days) if d[:6] == f'{y}{m:02d}']
        k = max(idx, key=lambda i: v[i]); n = (y - 2024) * 12 + m
        rows.append(f'{n:>5}  {idx[0]+1:>3}-{idx[-1]+1:<3}  {st.median(v[i] for i in idx):>9g}  {v[k]:>10}  {k+1:>10}')
open('renders/T5.txt', 'w').write('\n'.join(rows) + '\n')
print('rendered')
