"""N channel, rhythm: autocorrelation of the onset-strength envelope.
Open handstroke ringing on n bells puts 2n blows and one empty beat in each whole pull,
so a pull lasts 2n+1 blow-intervals; even ringing without a gap would last 2n."""
import sys
import numpy as np
from perceive import load
wav = sys.argv[1]; t0, t1 = float(sys.argv[2]), float(sys.argv[3])
x, sr = load(wav, t0, t1)
hop, n = 128, 1024
fr = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
f = np.fft.rfftfreq(n, 1 / sr)
m = np.log1p(100 * np.abs(np.fft.rfft(fr, axis=1))[:, (f > 300) & (f < 4000)])
env = np.maximum(np.diff(m, axis=0), 0).sum(1); env -= env.mean()
ac = np.correlate(env, env, "full")[len(env) - 1:]; ac /= ac[0]
lag = np.arange(len(ac)) * hop / sr
def peaks(lo, hi, k=5):
    s = [(ac[i], lag[i]) for i in range(1, len(ac) - 1) if lo < lag[i] < hi and ac[i] > ac[i-1] and ac[i] >= ac[i+1]]
    return sorted(s, reverse=True)[:k]
print(f"window {t0}-{t1} s")
print("strongest periodicities 0.1-0.6 s (blow scale):", [(round(l,3), round(a,3)) for a,l in peaks(0.1,0.6)])
print("strongest periodicities 1.0-4.0 s (row / pull scale):", [(round(l,3), round(a,3)) for a,l in peaks(1.0,4.0)])
