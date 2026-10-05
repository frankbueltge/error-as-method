"""The practice's only senses for sound. Three translations, kept apart.

  python3 perceive.py S <wav> <outprefix> [t0 t1]   pictures only: spectrogram + waveform PNGs
  python3 perceive.py N <wav> [t0 t1]               numbers only: onsets, intervals, peaks, as text
  python3 perceive.py B <rows.json> <out.png>       the ringers' picture: rows and blue line

S prints nothing about the signal but the file names it wrote, so that a picture reading is not
contaminated by numbers. N draws nothing. Every reading in the record names the channel it used.
"""
import json, sys, wave
import numpy as np


def load(path, t0=None, t1=None):
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
    if t0 is not None:
        x = x[int(t0 * sr):int(t1 * sr)]
    return x, sr


def stft(x, sr, n=4096, hop=256):
    win = np.hanning(n)
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * win
    mag = np.abs(np.fft.rfft(frames, axis=1))
    return mag, np.fft.rfftfreq(n, 1 / sr), np.arange(len(mag)) * hop / sr


def onsets(x, sr, hop=256, n=1024):
    """Spectral flux onsets: rises of energy above 300 Hz (bells strike above the hum)."""
    win = np.hanning(n)
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * win
    mag = np.abs(np.fft.rfft(fr, axis=1))
    f = np.fft.rfftfreq(n, 1 / sr)
    mag = np.log1p(100 * mag[:, f > 300])
    flux = np.maximum(np.diff(mag, axis=0), 0).sum(1)
    flux = (flux - np.median(flux)) / (flux.std() + 1e-9)
    t = (np.arange(len(flux)) + 1) * hop / sr
    peaks = []
    for i in range(1, len(flux) - 1):
        if flux[i] > 1.5 and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1]:
            if not peaks or t[i] - peaks[-1] > 0.08:
                peaks.append(t[i])
    return np.array(peaks)


def blow_peaks(x, sr, t, dur=0.12, k=4):
    seg = x[int(t * sr):int((t + dur) * sr)]
    if len(seg) < 64:
        return []
    m = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 8192))
    f = np.fft.rfftfreq(8192, 1 / sr)
    m[f < 150] = 0
    out = []
    for _ in range(k):
        i = int(m.argmax()); out.append(round(float(f[i]), 1))
        m[max(0, i - 12):i + 12] = 0
    return out


def mode_S(wav, prefix, t0=None, t1=None):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    x, sr = load(wav, t0, t1)
    off = t0 or 0
    mag, f, tt = stft(x, sr)
    keep = f < 4000
    fig, ax = plt.subplots(2, 1, figsize=(14, 7), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    ax[0].imshow(20 * np.log10(mag[:, keep].T + 1e-6), origin="lower", aspect="auto",
                 extent=[off, off + tt[-1], 0, f[keep][-1]], cmap="magma", vmin=-40, vmax=40)
    ax[0].set_ylabel("Hz")
    ts = off + np.arange(len(x)) / sr
    ax[1].plot(ts[::20], x[::20], lw=0.3, color="k")
    ax[1].set_xlabel("s")
    fig.tight_layout(); fig.savefig(prefix + ".png", dpi=90); plt.close(fig)
    print("wrote", prefix + ".png")


def mode_N(wav, t0=None, t1=None):
    x, sr = load(wav, t0, t1)
    off = t0 or 0
    on = onsets(x, sr)
    iv = np.diff(on)
    print(f"duration {len(x)/sr:.2f} s, onsets {len(on)}")
    if len(iv):
        q = np.percentile(iv, [5, 25, 50, 75, 95])
        print("intervals s: p5 %.3f p25 %.3f median %.3f p75 %.3f p95 %.3f" % tuple(q))
        hist, edges = np.histogram(iv, bins=np.arange(0, 1.01, 0.025))
        for h, e in zip(hist, edges):
            if h:
                print(f"  {e:.3f}-{e+0.025:.3f} {'#' * min(h, 80)} {h}")
    print("first 40 onsets (s) and the 4 strongest peaks (Hz) in the 120 ms after each:")
    for t in on[:40]:
        print(f"  {off + t:8.3f}  {blow_peaks(x, sr, t)}")
    return on


def mode_B(rows_json, out):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = json.load(open(rows_json))
    n = len(rows[0])
    fig, ax = plt.subplots(figsize=(2 + n * 0.35, 0.18 * len(rows) + 1))
    for i, r in enumerate(rows):
        for j, b in enumerate(r):
            ax.text(j, -i, str(b), ha="center", va="center", fontsize=7, family="monospace")
    for bell, col in ((1, "red"), (2, "blue")):
        ys = [-i for i in range(len(rows))]
        xs = [r.index(bell) for r in rows]
        ax.plot(xs, ys, color=col, lw=1)
    ax.set_xlim(-1, n); ax.axis("off")
    fig.savefig(out, dpi=90, bbox_inches="tight"); plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "S":
        a = sys.argv[2:]
        mode_S(a[0], a[1], *(map(float, a[2:4]) if len(a) > 2 else ()))
    elif m == "N":
        a = sys.argv[2:]
        mode_N(a[0], *(map(float, a[1:3]) if len(a) > 1 else ()))
    elif m == "B":
        mode_B(sys.argv[2], sys.argv[3])
