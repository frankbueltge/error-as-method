"""The grid's own tool: the checks named in readings/R-1..R-3, run on the per-second series and
nothing else. Written after the three readings were committed.

Thresholds that the readings left in words are fixed here, before the first run, and marked FIXED-HERE:
  E1/G2 "clearly larger"  -> the 1,800 s profile range is at least 2x the 1,700 s control range
  E3 "differs by time of day" -> the hourly 60 s peak ratio spans at least a factor 2
  python3 home.py sources/fnew-2026-8.csv.gz  -> home.json
"""
import gzip, json, re, sys, random
import numpy as np
sys.path.insert(0, "carried/ear")
from perceive import onsets  # the ear's own detector, for E5's shuffled control

raw = gzip.open(sys.argv[1], "rt").read().splitlines()[1:]
f = np.array([float(l.split(",")[1]) for l in raw]); assert len(f) == 31 * 86400
d = f - 50.0; N = len(d); sec = np.arange(N)
R = {}
def put(k, verdict, **kw): R[k] = {"verdict": verdict, **kw}

def profile(x, P):
    k = sec[:len(x)] % P; return np.bincount(k, x, P) / np.bincount(k, None, P)
def rng(p): return float(p.max() - p.min())

# E1 / G2: the half-hour profile against a 1,700 s control
p1800, p1700 = profile(d, 1800), profile(d, 1700)
r1, r0 = rng(p1800), rng(p1700)
sm = lambda p: np.convolve(np.r_[p[-30:], p, p[:30]], np.ones(61) / 61, "valid")
put("E1", "G" if r1 >= 2 * r0 else "H", range_1800_mHz=round(r1 * 1e3, 2), range_1700_mHz=round(r0 * 1e3, 2),
    smoothed_60s_mHz=[round(rng(sm(p1800)) * 1e3, 2), round(rng(sm(p1700)) * 1e3, 2)],
    where_max_s=int(p1800.argmax()), where_min_s=int(p1800.argmin()), rule="FIXED-HERE: >= 2x control")
R["G2"] = dict(R["E1"]); R["G2"]["note"] = "same check as E1"
# E2: day in the minute means
m = d.reshape(-1, 60).mean(1); mc = m - m.mean()
ac = lambda L: float((mc[:-L] * mc[L:]).sum() / (mc * mc).sum())
a12, a24, a36 = ac(720), ac(1440), ac(2160)
put("E2", "G" if a24 > a12 and a24 > a36 else "H", ac_12h=round(a12, 4), ac_24h=round(a24, 4), ac_36h=round(a36, 4))
# E3: a 60 s line, and whether it changes by hour
def spec(x, n=3600):
    fr = x[: len(x) // n * n].reshape(-1, n); fr = fr - fr.mean(1, keepdims=True)
    return (np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2), np.fft.rfftfreq(n, 1)
S, fq = spec(d); Sm = S.mean(0)
def ratio(Sv, f0):
    i = int(np.argmin(abs(fq - f0))); nb = (fq > 0.8 * f0) & (fq < 1.2 * f0) & (abs(fq - f0) > 0.02 * f0)
    return float(Sv[i - 1:i + 2].max() / np.median(Sv[nb]))
r60, r15 = ratio(Sm, 1 / 60), ratio(Sm, 1 / 15)
hour = (np.arange(len(S)) % 24)
byh = [ratio(S[hour == h].mean(0), 1 / 60) for h in range(24)]
put("E3", "G" if r60 >= 3 and max(byh) / min(byh) >= 2 else ("U" if r60 >= 3 else "H"), peak_ratio_60s=round(r60, 2),
    peak_ratio_15s=round(r15, 2), by_hour_utc=[round(x, 2) for x in byh], rule="FIXED-HERE: hourly span >= 2x")
# E4: daily quiet in the second-to-second increments
inc = np.diff(d); hh = (sec[1:] // 3600) % 24
sd = np.array([inc[hh == h].std() for h in range(24)])
put("E4", "G" if sd.min() <= 0.7 * np.median(sd) else "H", sd_by_hour_mHz=[round(x * 1e3, 3) for x in sd],
    min_over_median=round(float(sd.min() / np.median(sd)), 3), quiet_hour_utc=int(sd.argmin()))
# E5: the ear's onset count on a shuffled month
x = np.clip(d / 0.5, -1, 1); x = np.round(x * 32767) / 32768
n_real = len(onsets(x, 44100)); xs = x.copy(); np.random.default_rng(109).shuffle(xs); n_shuf = len(onsets(xs, 44100))
put("E5", "H" if n_shuf >= 0.8 * n_real else "G", onsets_real=n_real, onsets_shuffled=n_shuf, seed=109)
# E6: do the 'partials' recur? decided on the printed list
lists = [list(map(float, re.findall(r"[\d.]+", l.split("[")[1]))) for l in open("seen/ear-N.txt") if "[" in l]
allf = [v for L in lists for v in L]
rec = max(sum(any(abs(v - c) <= 5 for v in L) for L in lists) for c in allf)
put("E6", "H" if rec <= len(lists) / 4 else "G", onset_lists=len(lists), most_recurrent_count=rec)
# E7
w = float(((f >= 49.875) & (f <= 50.125)).mean())
put("E7", "G" if w >= 0.95 else "H", share_within_0125=round(w, 4), share_within_02=round(float((abs(d) <= 0.2).mean()), 5))
# E8: the half-hour profile in days 15-23
dd = d[14 * 86400: 23 * 86400]
r_sub = rng(profile(dd, 1800))
put("E8", "H" if r_sub >= 0.7 * r1 else "G", range_days15_23_mHz=round(r_sub * 1e3, 2), range_month_mHz=round(r1 * 1e3, 2))
# mould cells: 8 minutes x 1 day, lowest minute mean
cell = m.reshape(-1, 8).min(1)          # 5,580 cells in time order
put("M1", "G" if (cell < 0).mean() >= 0.7 else "H", share_below_50=round(float((cell < 0).mean()), 4))
put("M2", "G" if (cell <= -0.1).mean() >= 0.25 else "H", share_at_or_below_49_9=round(float((cell <= -0.1).mean()), 4))
cc = cell - cell.mean(); acc = lambda L: float((cc[:-L] * cc[L:]).sum() / (cc * cc).sum())
put("M3", "G" if acc(1) > 0.4 and acc(4) > 0.15 else "H", lag1=round(acc(1), 3), lag4=round(acc(4), 3))
col = cell.reshape(31, 180).mean(0)
put("M4", "H" if rng(col) > 0.02 else "G", column_range_Hz=round(rng(col), 4))
# grid24
hourly = np.array([d[(sec // 3600) % 24 == h].mean() for h in range(24)])
put("G1", "G" if rng(hourly) > 0.010 else "H", hourly_mean_mHz=[round(v * 1e3, 2) for v in hourly], range_mHz=round(rng(hourly) * 1e3, 2))
p95 = np.percentile(m, 95); runs = 0; cur = 0
for v in m:
    cur = cur + 1 if v > p95 else 0
    if cur == 60: runs += 1
put("G3", "G" if runs >= 5 else "H", runs_ge_60min_above_p95=runs, p95_mHz=round(float(p95) * 1e3, 2))
s1, s4 = m[: 8 * 1440].std(), m[23 * 1440:].std()
put("G4", "H" if 0.85 <= s1 / s4 <= 1.18 else "G", std_ratio_days1_8_over_24_31=round(float(s1 / s4), 3))
json.dump(R, open("home.json", "w"), indent=1)
for k, v in R.items(): print(k, v["verdict"], {a: b for a, b in v.items() if a not in ("verdict", "sd_by_hour_mHz", "by_hour_utc", "hourly_mean_mHz")})
