"""Heard on Paper -- prepare the ten clips, their spectrograms and the measured notes.

Run:  python3 prepare.py <dir with the ten downloaded xeno-canto mp3s>
Needs ffmpeg, numpy, scipy, matplotlib.

Everything here is a translation written on the night, and the record says that is where this
practice errs. So every step is a fixed rule, stated before the makers ran:

1. Decode to mono, 22,050 Hz.
2. Peak band: over the whole recording, the frequency where the loud moments stand furthest
   above the steady background (98th percentile over median, per 21.5 Hz bin, 200 Hz to 10 kHz,
   smoothed over five bins). Version 1 of this rule took the frequency with most median energy
   and found background noise in three recordings; it is kept in the journal, not here. Band = [peak / 2.2, peak * 2.2], clamped to 200 Hz .. 10.5 kHz.
3. Envelope: band energy in 10 ms frames, in dB. Floor = 20th percentile, top = 99.5th.
   Active = above floor + 0.35 * (top - floor).
4. Strophe: from the loudest active frame, extend left and right while the gap to the next
   active frame is shorter than 0.6 s. Pad 0.25 s each side. Capped at 6 s around the peak.
5. Notes: maximal runs of active frames inside the strophe, runs closer than 30 ms merged, runs
   shorter than 25 ms dropped. Their count is the measured note count.
6. Spectrogram: 0 to 11 kHz linear (0 to 3 kHz if the peak is under 1.2 kHz), grey, time axis
   in seconds, frequency in kHz. Nothing else is written on it.
"""
import json, subprocess, sys, hashlib, os
import numpy as np
from scipy import signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {"a": "towhee", "b": "barredowl", "c": "wtsparrow", "d": "ovenbird", "e": "chestnut",
         "f": "chickadee", "g": "alder", "h": "yelwarbler", "i": "cardinal", "j": "wevireo"}
SR = 22050


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def main(src):
    songs = json.load(open(os.path.join(HERE, "songs.json")))["songs"]
    out = {"rules": __doc__.split("Everything here")[1].strip(), "songs": []}
    manifest = []
    for s in songs:
        k = s["key"]; p = os.path.join(src, FILES[k] + ".mp3")
        b = open(p, "rb").read()
        manifest.append({"key": k, "url": f"https://xeno-canto.org/{s['xc']}/download",
                         "page": f"https://xeno-canto.org/{s['xc']}", "bytes": len(b),
                         "sha256": hashlib.sha256(b).hexdigest(), "licence": s["licence"],
                         "recordist": s["recordist"]})
        x = decode(p)
        # 2. peak band
        f, t, S = signal.spectrogram(x, SR, nperseg=1024, noverlap=512)
        sel = (f >= 200) & (f <= 10000)
        # contrast: what the loud moments add over the steady background, per frequency
        con = np.percentile(S[sel], 98, axis=1) / (np.median(S[sel], axis=1) + 1e-20)
        con = np.convolve(con, np.ones(5) / 5, mode="same")
        peak = float(f[sel][np.argmax(con)])
        lo, hi = max(200.0, peak / 2.2), min(10500.0, peak * 2.2)
        # 3. envelope
        hop = int(0.01 * SR)
        f2, t2, S2 = signal.spectrogram(x, SR, nperseg=512, noverlap=512 - hop)
        band = (f2 >= lo) & (f2 <= hi)
        env = 10 * np.log10(S2[band].sum(axis=0) + 1e-20)
        floor, top = np.percentile(env, 20), np.percentile(env, 99.5)
        act = env > floor + 0.35 * (top - floor)
        # 4. strophe
        smooth = np.convolve(env, np.ones(5) / 5, mode="same")
        ip = int(np.argmax(np.where(act, smooth, -1e9)))
        idx = np.where(act)[0]
        gap = int(0.6 / 0.01)
        L = R = ip
        for j in idx[idx < ip][::-1]:
            if L - j < gap: L = j
            else: break
        for j in idx[idx > ip]:
            if j - R < gap: R = j
            else: break
        L = max(L, ip - 300); R = min(R, ip + 300)
        t0 = max(0.0, t2[L] - 0.25); t1 = min(len(x) / SR, t2[R] + 0.25)
        # 5. notes
        a = act[L:R + 1].astype(int)
        runs = []; start = None
        for i, v in enumerate(a):
            if v and start is None: start = i
            if not v and start is not None: runs.append([start, i - 1]); start = None
        if start is not None: runs.append([start, len(a) - 1])
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] <= 3: merged[-1][1] = r[1]
            else: merged.append(r)
        notes = [[round(float(t2[L + r[0]] - t0), 3), round(float(t2[L + r[1]] - t0), 3)] for r in merged if r[1] - r[0] + 1 >= 3]
        # clip
        clip = x[int(t0 * SR):int(t1 * SR)]
        clip = clip / (np.max(np.abs(clip)) + 1e-9) * 0.9
        wav = os.path.join(HERE, "clips", f"{k}.wav")
        from scipy.io import wavfile
        wavfile.write(wav, SR, (clip * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-q:a", "4",
                        os.path.join(HERE, "clips", f"{k}.mp3")], check=True)
        os.remove(wav)
        # 6. spectrogram
        fmax = 3000 if peak < 1200 else 11000
        f3, t3, S3 = signal.spectrogram(clip, SR, nperseg=512, noverlap=448)
        m = f3 <= fmax
        D = 10 * np.log10(S3[m] + 1e-12)
        vmax = np.percentile(D, 99.7); vmin = vmax - 55
        fig, ax = plt.subplots(figsize=(8, 3.2), dpi=110)
        ax.pcolormesh(t3, f3[m] / 1000, D, cmap="Greys", vmin=vmin, vmax=vmax, shading="auto")
        ax.set_xlabel("seconds"); ax.set_ylabel("kHz")
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, "spectrograms", f"{k}.png"))
        plt.close(fig)
        out["songs"].append({"key": k, "peak_hz": round(peak), "band_hz": [round(lo), round(hi)],
                             "clip_from_s": round(t0, 3), "clip_to_s": round(t1, 3),
                             "clip_len_s": round(t1 - t0, 3), "fmax_hz": fmax,
                             "notes": notes, "note_count": len(notes)})
        print(k, FILES[k], "peak", round(peak), "clip", round(t0, 2), round(t1, 2), "notes", len(notes))
    json.dump(out, open(os.path.join(HERE, "measured.json"), "w"), indent=1)
    json.dump(manifest, open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
