"""render.py -> renders/T1.svg (line of every hourly value) and renders/T3.txt (table of daily max and mean
from the hourly values). Axes in day numbers only; no title, no unit; nothing names the source or place."""
import os
from load import hourly
H = hourly()
os.makedirs('renders', exist_ok=True)
F = 'font-family="DejaVu Sans Mono, monospace" font-size="13" fill="#111"'
flat = [v for d in H for v in d]
top = max(v for v in flat if v is not None)
ymax = next(m for m in (50, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000) if m >= top)
step = ymax // 5
x0, y0, w, h = 60, 15, 1520, 350
b = f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#111"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#111"/>'
for t in range(0, ymax + 1, step):
    y = y0 + h - h*t/ymax
    b += f'<line x1="{x0-4}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="#111"/><text x="{x0-8}" y="{y+4:.1f}" text-anchor="end" {F}>{t}</text>'
for dd in [1] + list(range(30, 366, 30)) + [365]:
    x = x0 + w*(dd-1)/364
    b += f'<line x1="{x:.1f}" y1="{y0+h}" x2="{x:.1f}" y2="{y0+h+4}" stroke="#111"/><text x="{x:.1f}" y="{y0+h+18}" text-anchor="middle" {F}>{dd}</text>'
b += f'<text x="{x0+w/2}" y="{y0+h+36}" text-anchor="middle" {F}>day</text>'
segs, cur = [], []
for i, v in enumerate(flat):
    if v is None:
        if cur: segs.append(cur); cur = []
        continue
    cur.append(f'{x0 + w*i/8759:.2f},{y0 + h - h*v/ymax:.2f}')
if cur: segs.append(cur)
b += ''.join(f'<polyline points="{" ".join(s)}" fill="none" stroke="#111" stroke-width="0.7"/>' for s in segs)
open('renders/T1.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="420" viewBox="0 0 1600 420"><rect width="1600" height="420" fill="#fff"/>{b}</svg>')
with open('renders/T3.txt', 'w') as f:
    for i, d in enumerate(H):
        v = [x for x in d if x is not None]
        f.write(f'day {i+1:03d}  max {max(v):.1f}  mean {sum(v)/len(v):.1f}\n' if v else f'day {i+1:03d}  max -  mean -\n')
print('rendered; y axis to', ymax)
