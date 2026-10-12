"""figure.py: figure.svg, the night's result as one still picture. Four rows, one per grain: the picture each maker
got (embedded as the JPEG it was, scaled up without smoothing), and the three titles its makers gave their works,
coloured by what they drew as units (coder B, B8). A rule marks where the twice-daily rhythm drops below two
pixel columns a cycle. Run: python3 figure.py"""
import base64, json, os
H = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["grain"] for p in json.load(open(os.path.join(H, "plan.json")))}
B = json.load(open(os.path.join(H, "coder", "B", "answers.json")))
holds = json.load(open(os.path.join(H, "materials", "holds.json")))
title = lambda m: open(os.path.join(H, "makers", m, "NOTE.md"), encoding="utf-8").readline().lstrip("# ").strip()
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
W, RH, IW, IH = 1000, 150, 400, 120
out = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia, serif">' % (W, 4 * RH + 110, W, 4 * RH + 110),
       '<rect width="100%" height="100%" fill="#f3f0e8"/>',
       '<text x="20" y="34" font-size="22" fill="#1b1a17">Down to the Grain</text>',
       '<text x="20" y="56" font-size="13" fill="#6b655b">One hourly record, four sizes, three makers each. Blue: drew hours fitted back. Brown: drew the pixels.</text>']
for k, g in enumerate(["G1", "G2", "G3", "G4"]):
    y = 76 + k * RH + (16 if k >= 2 else 0)
    if k == 2:
        out.append('<line x1="20" x2="%d" y1="%d" y2="%d" stroke="#b3261e" stroke-width="2"/>' % (W - 20, y - 12, y - 12))
        out.append('<text x="%d" y="%d" font-size="12" fill="#b3261e" text-anchor="end">below here the twice-daily rhythm is finer than two pixels</text>' % (W - 20, y - 18))
    b64 = base64.b64encode(open(os.path.join(H, "materials", g, "record.jpg"), "rb").read()).decode()
    w, h = holds[g]["size"]
    out.append('<image x="20" y="%d" width="%d" height="%d" preserveAspectRatio="none" style="image-rendering:pixelated" xlink:href="data:image/jpeg;base64,%s"/>' % (y, IW, IH, b64))
    out.append('<rect x="20" y="%d" width="%d" height="%d" fill="none" stroke="#d5cec0"/>' % (y, IW, IH))
    out.append('<text x="20" y="%d" font-size="12" fill="#6b655b">%d × %d px · %.1f hours a column</text>' % (y + IH + 15, w, h, holds[g]["hours_per_column"]))
    for j, m in enumerate([m for m in sorted(plan) if plan[m] == g]):
        items = B[m]["B8_units"] == "items"
        out.append('<text x="450" y="%d" font-size="17" fill="%s">%s</text>' % (y + 30 + j * 34, "#2f5d8a" if items else "#7a5a1e", esc(title(m))))
        out.append('<text x="%d" y="%d" font-size="11" fill="#6b655b" text-anchor="end">%s · %s</text>' % (W - 20, y + 30 + j * 34, m, "hours fitted back" if items else "the pixels"))
out.append('<text x="20" y="%d" font-size="11" fill="#6b655b">Water level, The Battery, New York, 15 Sep–14 Nov 2012 (NOAA CO-OPS 8518750). Makers were told none of this.</text>' % (4 * RH + 100))
open(os.path.join(H, "figure.svg"), "w", encoding="utf-8").write("\n".join(out + ["</svg>"]))
print("figure.svg", os.path.getsize(os.path.join(H, "figure.svg")))
