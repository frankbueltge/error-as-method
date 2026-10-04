"""Measure the swell seen by eye at V04: the size of the tidal-band wobble over time.
Same transform as variants.js (raw minus centred 31-day mean), absolute value, centred 365-day mean.
Reports the envelope's local minima and the strongest period between 5 and 30 years. Needs data.js (harvest.py)."""
import json, re, math
s = open("data.js").read(); start = re.search(r'start:"([^"]+)"', s).group(1)
lod = [float(x) for x in re.search(r"lod:\[([^\]]*)\]", s).group(1).split(",")]
def cmean(a, w):
    h = w // 2; c = [0.0]
    for x in a: c.append(c[-1] + x)
    return [(c[min(len(a), k + h + 1)] - c[max(0, k - h)]) / (min(len(a), k + h + 1) - max(0, k - h)) for k in range(len(a))]
m31 = cmean(lod, 31); env = cmean([abs(a - b) for a, b in zip(lod, m31)], 365)
y0 = int(start[:4]); yr = lambda k: y0 + k / 365.25
W = 1500   # a minimum is the lowest point within four years either side, clipped at the ends
mins = [round(yr(k), 1) for k in range(400, len(env) - 400) if env[k] == min(env[max(0, k - W):k + W])]
# collapse runs
uniq = []
for m in mins:
    if not uniq or m - uniq[-1] > 3: uniq.append(m)
mu = sum(env) / len(env); e = [x - mu for x in env]
best = max(((sum(x * math.cos(2 * math.pi * k / (P * 365.25)) for k, x in enumerate(e)) ** 2 + sum(x * math.sin(2 * math.pi * k / (P * 365.25)) for k, x in enumerate(e)) ** 2, P) for P in [p / 10 for p in range(50, 301)]))
out = {"envelope_ms_min_max": [round(min(env), 3), round(max(env), 3)], "local_minima_year": uniq, "strongest_period_years_5_to_30": best[1],
       "spacing_of_minima": [round(b - a, 1) for a, b in zip(uniq, uniq[1:])]}
json.dump(out, open("swell.json", "w"), indent=1); print(out)
