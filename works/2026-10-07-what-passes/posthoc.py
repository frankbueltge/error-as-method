"""Post-hoc checks, made after home.py and score.py, kept apart from the strict count.
1. Which days break their fortnight (ratio >= 2), so the readings' dates can be compared.
2. Why A5's reading answered 'no' on R4: the carried ear draws its waveform panel from every
   20th sample (perceive.py, mode_S: ts[::20], x[::20]). At 44,100 Hz on bells that is 0.45 ms;
   at one value per sample it is one value in five hours.
  python3 posthoc.py -> posthoc.json"""
import json
from statistics import median
from datetime import date, timedelta
q = json.load(open("series.json"))["q"]
days = [q[i:i + 96] for i in range(0, len(q), 96)]
dr = [max(d) - min(d) for d in days]
breaks = []
for i, r in enumerate(dr):
    nb = [dr[j] for j in range(max(0, i - 7), min(len(dr), i + 8)) if j != i]
    if r / median(nb) >= 2:
        breaks.append({"day": str(date(2026, 4, 1) + timedelta(i)), "ratio": round(r / median(nb), 2),
                       "range_cfs": round(r, 1), "mean_cfs": round(sum(days[i]) / 96, 1)})
d = [q[i + 1] - q[i] for i in range(len(q) - 1)]; m = max(abs(v) for v in d); x = [v / m for v in d]
lo = 96 * 103  # from 13 July
out = {"days_breaking_fortnight_ratio_ge_2": breaks,
       "A5_max_abs_all_samples": 1.0, "A5_max_abs_drawn": round(max(abs(v) for v in x[::20]), 3),
       "A5_from_13_July_max_abs_all_samples": round(max(abs(v) for v in x[lo:]), 3),
       "A5_from_13_July_max_abs_drawn": round(max(abs(v) for v in x[(20 - lo % 20) % 20 + lo::20]), 3),
       "A5_full_scale_cfs_per_15_min": m}
json.dump(out, open("posthoc.json", "w"), indent=1); print(json.dumps(out, indent=1))
