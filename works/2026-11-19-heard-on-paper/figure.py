"""Heard on Paper -- the face's full-bleed spectrograms (face/<k>.png), face-data.js and figure.svg.
Run after prepare.py, score.py, posthoc.py:  python3 figure.py
The face images are drawn from the same clips by the same rule as the makers' images, without axes, so that a
playhead can run across them; the makers saw the versions with axes in spectrograms/."""
import json, os, subprocess, html
import numpy as np
from scipy import signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 22050
songs = json.load(open(os.path.join(HERE, "songs.json")))["songs"]
meas = {s["key"]: s for s in json.load(open(os.path.join(HERE, "measured.json")))["songs"]}
res = json.load(open(os.path.join(HERE, "results.json")))
hand = json.load(open(os.path.join(HERE, "coding_hand.json")))
os.makedirs(os.path.join(HERE, "face"), exist_ok=True)

for s in songs:
    k = s["key"]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "clips", k + ".mp3"), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(float)
    fmax = meas[k]["fmax_hz"]
    f, t, S = signal.spectrogram(x, SR, nperseg=512, noverlap=448)
    m = f <= fmax
    D = 10 * np.log10(S[m] + 1e-12)
    vmax = np.percentile(D, 99.7)
    fig = plt.figure(figsize=(10, 2.6), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.pcolormesh(t, f[m], D, cmap="Greys", vmin=vmax - 55, vmax=vmax, shading="auto")
    ax.set_xlim(0, len(x) / SR)
    fig.savefig(os.path.join(HERE, "face", k + ".png"))
    plt.close(fig)

data = {"songs": [{"key": s["key"], "species": s["species"], "sci": s["sci"], "canon": s["canon"], "canon_url": s["canon_url"],
                   "xc": s["xc"], "recordist": s["recordist"], "licence": s["licence"],
                   "len": meas[s["key"]]["clip_len_s"]} for s in songs],
        "items": [{"maker": i["maker"], "arm": i["arm"], "key": i["key"], "count": i["count"], "phrase": i["phrase"],
                   "grounds": i["grounds"], "species": i["species"], "confidence": i["confidence"],
                   "code": hand["rows"][i["maker"] + i["key"]]} for i in res["items"]],
        "results": res["results"], "tally": hand["tally"]}
open(os.path.join(HERE, "face-data.js"), "w").write("window.HEARD=" + json.dumps(data, ensure_ascii=False) + ";\n")

# figure.svg: per song, the published words and the eight makers' phrases, coloured by the hand code
COL = {"used": "#b3261e", "avoided": "#1f4e8c", "shaped": "#7a5ea8", "picture": "#6b665c"}
W, rowh, top = 1180, 118, 70
H = top + rowh * len(songs) + 40
e = html.escape
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>',
     '<text x="20" y="30" font-size="20" fill="#1d1b18">Heard on Paper: what people wrote, and what eight makers who cannot hear wrote</text>',
     '<text x="20" y="52" font-size="12" fill="#6b665c" font-family="system-ui,sans-serif">'
     '<tspan fill="#b3261e">■ used a known rendering</tspan>   <tspan fill="#1f4e8c">■ named it and avoided it</tspan>   '
     '<tspan fill="#7a5ea8">■ says knowledge shaped it</tspan>   <tspan fill="#6b665c">■ from the picture</tspan>   '
     'U = not told the bird, N = told it. Hand coding, post hoc.</text>']
for r, s in enumerate(songs):
    y = top + r * rowh
    o.append(f'<line x1="20" x2="{W-20}" y1="{y}" y2="{y}" stroke="#d9d3c5"/>')
    o.append(f'<text x="20" y="{y+22}" font-size="15" fill="#1d1b18">{e(s["species"])}</text>')
    o.append(f'<text x="20" y="{y+42}" font-style="italic" fill="#1d1b18">people: “{e(s["canon"])}”</text>')
    its = [i for i in data["items"] if i["key"] == s["key"]]
    its.sort(key=lambda i: i["maker"])
    for j, i in enumerate(its):
        cx = 20 + (j % 2) * 580; cy = y + 64 + (j // 2) * 22
        ph = i["phrase"] if len(i["phrase"]) < 70 else i["phrase"][:67] + "…"
        o.append(f'<text x="{cx}" y="{cy}" font-family="system-ui,sans-serif" font-size="12.5"><tspan fill="{COL[i["code"]]}" font-weight="bold">{i["maker"]}</tspan> <tspan fill="#1d1b18">{e(ph)}</tspan></text>')
o.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(o))
print("ok")
