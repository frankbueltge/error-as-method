"""render.py -> renders/T1.svg T2.svg T4.svg and renders/T3.txt (the four translations).
render.js turns the SVGs into PNGs. Axes in day numbers only; no titles; nothing names the source."""
import os
from load import load
kp, ap, _ = load()
os.makedirs('renders', exist_ok=True)
F = 'font-family="DejaVu Sans Mono, monospace" font-size="13" fill="#111"'
def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
def axes(x0, y0, w, h, ymax, yticks, xdays=365):
    b = f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#111"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#111"/>'
    for t in yticks:
        y = y0 + h - h*t/ymax
        b += f'<line x1="{x0-4}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="#111"/><text x="{x0-8}" y="{y+4:.1f}" text-anchor="end" {F}>{t:g}</text>'
    for dd in [1] + list(range(30, 366, 30)) + [365]:
        x = x0 + w*(dd-1)/(xdays-1)
        b += f'<line x1="{x:.1f}" y1="{y0+h}" x2="{x:.1f}" y2="{y0+h+4}" stroke="#111"/><text x="{x:.1f}" y="{y0+h+18}" text-anchor="middle" {F}>{dd}</text>'
    b += f'<text x="{x0+w/2}" y="{y0+h+36}" text-anchor="middle" {F}>day</text>'
    return b
# T1: all 2920 values as a line
x0, y0, w, h = 50, 15, 1530, 350
flat = [v for d in kp for v in d]
pts = ' '.join(f'{x0 + w*i/2919:.2f},{y0 + h - h*v/9:.2f}' for i, v in enumerate(flat))
open('renders/T1.svg', 'w').write(svg(1600, 420, axes(x0, y0, w, h, 9, range(0, 10)) + f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="0.8"/>'))
# T2: 27-day rows, grey by daily max
dmax = [max(d) for d in kp]
cw, ch, gx, gy = 30, 30, 60, 30
body = ''
for i, m in enumerate(dmax):
    r, c = divmod(i, 27)
    g = int(255 - 255*m/9)
    body += f'<rect x="{gx + c*cw}" y="{gy + r*ch}" width="{cw-2}" height="{ch-2}" fill="rgb({g},{g},{g})"/>'
for r in range(14):
    body += f'<text x="{gx-6}" y="{gy + r*ch + 19}" text-anchor="end" {F}>{r*27+1}</text>'
for c in range(0, 27, 2):
    body += f'<text x="{gx + c*cw + 14}" y="{gy-8}" text-anchor="middle" {F}>+{c}</text>'
ky = gy + 14*ch + 20
for k in range(10):
    g = int(255 - 255*k/9)
    body += f'<rect x="{gx + k*40}" y="{ky}" width="38" height="16" fill="rgb({g},{g},{g})" stroke="#111" stroke-width="0.5"/><text x="{gx + k*40 + 19}" y="{ky+32}" text-anchor="middle" {F}>{k}</text>'
body += f'<text x="{gx}" y="{ky+52}" {F}>rows: first day of row; columns: days after it; shade: largest value of the day</text>'
open('renders/T2.svg', 'w').write(svg(gx + 27*cw + 20, ky + 64, body))
# T3: table
with open('renders/T3.txt', 'w') as f:
    for i, d in enumerate(kp):
        f.write(f'day {i+1:03d}  max {max(d):.3f}  mean {sum(d)/8:.3f}\n')
# T4: 7-day running mean of daily mean ap (centred; edges use the days available)
dap = [sum(a)/8 for a in ap]
rm = [sum(dap[max(0, i-3):i+4])/len(dap[max(0, i-3):i+4]) for i in range(365)]
ym = max(rm)*1.1
step = 10 if ym < 80 else 20
pts = ' '.join(f'{x0 + w*i/364:.2f},{y0 + h - h*v/ym:.2f}' for i, v in enumerate(rm))
open('renders/T4.svg', 'w').write(svg(1600, 420, axes(x0, y0, w, h, ym, range(0, int(ym)+1, step)) + f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="1.5"/>'))
print('rendered')
