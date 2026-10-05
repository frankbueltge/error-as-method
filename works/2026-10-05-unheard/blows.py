"""N channel, second instrument: one onset detector per bell, each listening to that bell's nominal.
Nominals are the six read off the long-term spectrum (readings/R-2-N-out-partials.txt).
Writes blows.json: [[t, bell], ...], bells numbered 1 (highest) to 6."""
import json, sys
import numpy as np
from perceive import load, stft
NOM = [1534.2, 1367.4, 1318.9, 1152.0, 1022.8, 915.2]
wav = sys.argv[1]; out = sys.argv[2]
x, sr = load(wav)
mag, f, t = stft(x, sr, n=2048, hop=128)
blows = []
for b, nf in enumerate(NOM, 1):
    band = (f > nf - 15) & (f < nf + 15)
    e = np.log1p(1000 * mag[:, band].sum(1))
    d = np.diff(e, prepend=e[0])
    # rise over 4 frames (~23 ms)
    r = e - np.concatenate([np.full(4, e[0]), e[:-4]])
    thr = np.percentile(r, 97)
    last = -1
    for i in range(1, len(r) - 1):
        if r[i] > thr and r[i] >= r[i - 1] and r[i] > r[i + 1] and t[i] - last > 0.9:
            blows.append([round(float(t[i]), 3), b, float(r[i] / thr)]); last = t[i]
blows.sort()
# a blow heard in two bands within 40 ms belongs to the band where it rose most
kept = []
for bl in blows:
    if kept and bl[0] - kept[-1][0] < 0.04:
        if bl[2] > kept[-1][2]:
            kept[-1] = bl
        continue
    kept.append(bl)
blows = [[t_, b_] for t_, b_, _ in kept]
json.dump(blows, open(out, "w"))
print(len(blows), "blows;", {b: sum(1 for _, x in blows if x == b) for b in range(1, 7)})
