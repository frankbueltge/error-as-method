"""figure.svg: the 24 figures as silhouettes, word-first above, drop-first below (each drop in grey beside its figure)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.loads(open(os.path.join(HERE, "face-data.js")).read().split("=", 1)[1].rstrip().rstrip(";"))
items = D["items"]
W = [i for i in items if i["arm"] == "W"]
C = [i for i in items if i["arm"] == "C"]
key = lambda i: (i["file"], i["maker"])
W.sort(key=key)
C.sort(key=key)
CELL, GAP, X0 = 116, 8, 20


def poly(pieces, x, y, size, b, fill):
    minx, miny, maxx, maxy = b
    s = (size * 0.86) / max(maxx - minx, maxy - miny)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    out = []
    for p in pieces:
        pts = " ".join(f"{x + size / 2 + (vx - cx) * s:.1f},{y + size / 2 - (vy - cy) * s:.1f}" for vx, vy in p)
        out.append(f'<polygon points="{pts}" fill="{fill}"/>')
    return "".join(out)


def bounds(*sets):
    xs = [v[0] for s in sets for p in s for v in p]
    ys = [v[1] for s in sets for p in s for v in p]
    return min(xs), min(ys), max(xs), max(ys)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


rows = []
y = 60
rows.append(f'<text x="{X0}" y="{y - 14}" font-size="15" fill="#1f4e8c" font-family="sans-serif">FROM A WORD '
            f'(makers w1 to w4, subjects their own)</text>')
for r in range(3):
    for k, it in enumerate([i for i in W if i["file"] == f"fig{r + 1}.json"]):
        x = X0 + k * (CELL + GAP)
        rows.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" fill="#fffdf7" stroke="#d8d1c2"/>')
        rows.append(poly(it["fig"], x, y, CELL, bounds(it["fig"]), "#24211d"))
        rows.append(f'<text x="{x + 4}" y="{y + CELL + 13}" font-size="10.5" font-family="sans-serif" fill="#3a3731">'
                    f'{esc(it["name"][:22])}</text>')
    y += CELL + 26
y0 = 60
XC = X0 + 4 * (CELL + GAP) + 40
rows.append(f'<text x="{XC}" y="{y0 - 14}" font-size="15" fill="#b0442a" font-family="sans-serif">FROM A CHANCE DROP '
            f'(grey: where moved pieces lay; amber: moved)</text>')
yy = y0
for r in range(3):
    for k, it in enumerate([i for i in C if i["file"] == f"fig{r + 1}.json"]):
        x = XC + k * (CELL + GAP)
        b = bounds(it["fig"], it["drop"])
        rows.append(f'<rect x="{x}" y="{yy}" width="{CELL}" height="{CELL}" fill="#fffdf7" stroke="#d8d1c2"/>')
        moved = [any(abs(a[0] - d[0]) > 1e-3 or abs(a[1] - d[1]) > 1e-3 for a, d in zip(f, dr))
                 for f, dr in zip(it["fig"], it["drop"])]
        rows.append(poly([d for d, m in zip(it["drop"], moved) if m], x, yy, CELL, b, "#cfc8b8"))
        rows.append(poly([f for f, m in zip(it["fig"], moved) if not m], x, yy, CELL, b, "#24211d"))
        rows.append(poly([f for f, m in zip(it["fig"], moved) if m], x, yy, CELL, b, "#d9902a"))
        rows.append(f'<text x="{x + 4}" y="{yy + CELL + 13}" font-size="10.5" font-family="sans-serif" fill="#3a3731">'
                    f'{esc(it["name"][:22])}</text>')
    yy += CELL + 26
Wd = XC + 4 * (CELL + GAP) + 10
H = max(y, yy) + 30
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {H}" width="{Wd}" height="{H}">'
       f'<rect width="{Wd}" height="{H}" fill="#f3f0e8"/>' + "".join(rows) +
       f'<text x="{X0}" y="{H - 10}" font-size="11" fill="#6a6559" font-family="sans-serif">Four Cats, Twelve Drops · '
       f'Session 182, 2026-11-20 · word-first: 5 subjects in 12 figures (a sitting cat by all four makers); '
       f'drop-first: 10 subjects in 12</text></svg>')
open(os.path.join(HERE, "figure.svg"), "w").write(svg)
print("figure.svg", Wd, H)
