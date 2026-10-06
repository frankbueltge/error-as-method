"""Arrays for the face, from the per-second series (after home.py; display only, decides nothing).
python3 posthoc.py sources/fnew-2026-8.csv.gz -> face.json"""
import gzip, json, sys
import numpy as np
d = np.array([float(l.split(",")[1]) for l in gzip.open(sys.argv[1], "rt").read().splitlines()[1:]]) - 50
sec = np.arange(len(d))
p = np.bincount(sec % 1800, d, 1800) / (len(d) / 1800)
p = np.convolve(np.r_[p[-15:], p, p[:15]], np.ones(31) / 31, "valid")
n = 3600; fr = d.reshape(-1, n); fr = fr - fr.mean(1, keepdims=True)
S = np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2; fq = np.fft.rfftfreq(n, 1); h = np.arange(len(S)) % 24
b = (fq > 1 / 150) & (fq < 1 / 11); e = np.array([S[h == k][:, b].sum(1).mean() for k in range(24)])
hourly = [float(d[(sec // 3600) % 24 == k].mean()) for k in range(24)]
H = json.load(open("home.json"))
json.dump({"halfhour_mHz": [round(x * 1e3, 2) for x in p[::10]], "band_11_150_rel": [round(x, 3) for x in e / np.median(e)],
           "line60_ratio": H["E3"]["by_hour_utc"], "hourly_mean_mHz": [round(x * 1e3, 2) for x in hourly],
           "day12": [round(float(x) * 1e3, 1) for x in d[11 * 86400:12 * 86400].reshape(-1, 60).mean(1)]}, open("face.json", "w"))
print("ok")
