"""The six adapters: the only thing that varies tonight. Committed before the material.

  python3 adapt.py sources/merced-11264500-2026-04-01_07-31.rdb

Reads the USGS NWIS instantaneous-values file (tab-separated; column 5 discharge in cubic feet per
second, one value per 15 minutes) and writes series.json (the values, in order, with gaps held)
and six WAV files, out/A1.wav ... out/A6.wav, 44,100 Hz, 16-bit, mono. The carried ear
(carried/perceive.py, carried/rhythm.py, byte-identical with works/2026-10-05-unheard/) reads
each of them unchanged. Every adapter is a defensible audification; none is a strawman.

  A1  literal       one value = one sample; x = 2 (Q - min) / (max - min) - 1
  A2  slowed x4     as A1, each step linearly interpolated over 4 samples
  A3  one minute    as A1, each step interpolated over 226 samples (122 days -> ~60 s, the length
                    Session 109 chose for the grid's month)
  A4  day only      one value = one sample; h = Q - centred running mean over 96 values (one day);
                    x = h / max|h|
  A5  change        one value = one sample; d = first difference of Q; x = d / max|d|
  A6  day, slow     h as A4, interpolated over 226 samples, x = h / max|h|

The running mean at the edges uses the values available (a shorter window). A missing or
non-numeric value repeats the previous value; their count is written to series.json.
"""
import json, os, struct, sys, wave

RATE = 44100


def read(path):
    vals, stamps, held = [], [], 0
    for line in open(path):
        if line.startswith("#") or not line.startswith("USGS"):
            continue
        c = line.rstrip("\n").split("\t")
        try:
            v = float(c[4])
        except (ValueError, IndexError):
            v = None
        if v is None:
            held += 1
            v = vals[-1]
        vals.append(v); stamps.append(c[2] + " " + c[3])
    return vals, stamps, held


def interp(x, k):
    if k == 1:
        return list(x)
    out = []
    for i in range(len(x) - 1):
        a, b = x[i], x[i + 1]
        out.extend(a + (b - a) * j / k for j in range(k))
    out.append(x[-1])
    return out


def daymean(q, w=96):
    h = w // 2; n = len(q); pre = [0.0]
    for v in q:
        pre.append(pre[-1] + v)
    out = []
    for i in range(n):
        lo, hi = max(0, i - h), min(n, i + h)
        out.append((pre[hi] - pre[lo]) / (hi - lo))
    return out


def write(path, x):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(round(max(-1.0, min(1.0, v)) * 32767))) for v in x))


def adapters(q):
    lo, hi = min(q), max(q)
    lin = [2 * (v - lo) / (hi - lo) - 1 for v in q]
    m = daymean(q)
    h = [a - b for a, b in zip(q, m)]; hm = max(abs(v) for v in h)
    hn = [v / hm for v in h]
    d = [q[i + 1] - q[i] for i in range(len(q) - 1)]; dm = max(abs(v) for v in d)
    return {"A1": lin, "A2": interp(lin, 4), "A3": interp(lin, 226),
            "A4": hn, "A5": [v / dm for v in d], "A6": interp(hn, 226)}


if __name__ == "__main__":
    q, stamps, held = read(sys.argv[1])
    os.makedirs("out", exist_ok=True)
    json.dump({"n": len(q), "held": held, "first": stamps[0], "last": stamps[-1], "q": q},
              open("series.json", "w"))
    for name, x in adapters(q).items():
        write(f"out/{name}.wav", x)
        print(name, len(x), "samples", round(len(x) / RATE, 3), "s")
