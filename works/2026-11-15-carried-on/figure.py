"""figure.svg: the map of the face, static. Run after score.py and posthoc.py: python3 -I figure.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(HERE, 'face-data.js')).read()
face = json.loads(txt[len('window.CARRIED='):-2])
W, L, ROWH, MAX = 820, 90, 80, 0.5
X = lambda d: L + min(d, MAX) / MAX * (W - L - 20)
H = 40 + ROWH * 4 + 60
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif">',
     f'<rect width="{W}" height="{H}" fill="#f6f3ec"/>',
     '<text x="0" y="20" font-size="15" fill="#1d1b17">How far each version of four Dutch folk songs moved from the song</text>']
for i, s in enumerate(face['songs']):
    y = 50 + i * ROWH + ROWH / 2
    o.append(f'<rect x="{X(s["null_p10"]):.1f}" y="{y-28}" width="{X(MAX)-X(s["null_p10"]):.1f}" height="56" fill="#e6dfd0"/>')
    o.append(f'<line x1="{X(0)}" x2="{X(MAX)}" y1="{y}" y2="{y}" stroke="#d8d1c2"/>')
    o.append(f'<text x="0" y="{y-4}" font-size="14" fill="#1d1b17">Song {s["key"]}</text>')
    o.append(f'<text x="0" y="{y+12}" font-size="10" fill="#6d675c">{s["meter"]}, {len(s["people"])} sung</text>')
    for j, p in enumerate(s['people']):
        o.append(f'<circle cx="{X(p["d"]):.1f}" cy="{y-10-(j%3)*6}" r="4.5" fill="#b4532a" opacity=".85"/>')
    for j, p in enumerate(s['parallel']):
        o.append(f'<rect x="{X(p["d"])-4.5:.1f}" y="{y+5+(j%2)*7}" width="9" height="9" fill="#2c5d8f"/>')
    for j, p in enumerate(s['chain']):
        o.append(f'<circle cx="{X(p["d"]):.1f}" cy="{y+25}" r="7" fill="#6a3f8f"/><text x="{X(p["d"]):.1f}" y="{y+28.5}" font-size="9" text-anchor="middle" fill="#fff">{j+1}</text>')
    o.append(f'<circle cx="{X(0)}" cy="{y}" r="6" fill="#1d1b17"/>')
yb = 50 + 4 * ROWH
for v in [0, .1, .2, .3, .4, .5]:
    o.append(f'<text x="{X(v):.1f}" y="{yb+8}" font-size="10" text-anchor="middle" fill="#6d675c">{"the song" if v == 0 else v}</text>')
o.append(f'<text x="0" y="{yb+34}" font-size="11" fill="#6d675c"><tspan fill="#b4532a">●</tspan> singers and songbooks (MTC-ANN)   <tspan fill="#2c5d8f">■</tspan> machine makers alone   <tspan fill="#6a3f8f">●</tspan> machine chain 1→5   shaded: where other songs begin (10th percentile)</text>')
o.append(f'<text x="0" y="{yb+50}" font-size="11" fill="#6d675c">Distance: note alignment, pitch against the key, duration against the pulse (posthoc.py). All 40 machine versions end on the keynote; 13 of 18 sung versions of song A end on the third.</text>')
o.append('</svg>')
open(os.path.join(HERE, 'figure.svg'), 'w').write('\n'.join(o))
