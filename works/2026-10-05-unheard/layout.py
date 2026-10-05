"""Where the spectrogram's time axis sits inside each 30-45 s picture in seen/ (the figure code of
perceive.py S, re-run on the same audio), so the face can run a playhead over the very picture the
practice judged. Writes layout.json."""
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from perceive import load, stft
out = {}
for name, wav in (("R", "/tmp/claude-0/w/R.wav"), *((f"i{k}", f"/tmp/claude-0/w/i{k}.wav") for k in range(1, 5))):
    x, sr = load(wav, 30, 45)
    mag, f, tt = stft(x, sr)
    keep = f < 4000
    fig, ax = plt.subplots(2, 1, figsize=(14, 7), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    ax[0].imshow(20 * np.log10(mag[:, keep].T + 1e-6), origin="lower", aspect="auto",
                 extent=[30, 30 + tt[-1], 0, f[keep][-1]], cmap="magma", vmin=-40, vmax=40)
    ax[0].set_ylabel("Hz")
    ts = 30 + np.arange(len(x)) / sr
    ax[1].plot(ts[::20], x[::20], lw=0.3, color="k"); ax[1].set_xlabel("s")
    fig.tight_layout()
    p = ax[0].get_position(); lo, hi = ax[0].get_xlim()
    out[name] = {"x0": round(p.x0, 5), "x1": round(p.x1, 5), "t_lo": round(lo, 4), "t_hi": round(hi, 4)}
    plt.close(fig)
json.dump(out, open("layout.json", "w"), indent=1)
print(out)
