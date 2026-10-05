"""N channel, rhythm per bell: intervals between successive blows of the same bell, from blows.json.
With n bells rung open-handstroke, a bell's interval is n blow-units handstroke to backstroke and
n+1 back to hand, give or take its place in the row."""
import json, sys
import numpy as np
b = json.load(open(sys.argv[1]))
for bell in range(1, 7):
    ts = np.array([t for t, x in b if x == bell and 20 < t < 170])
    iv = np.diff(ts); iv = iv[iv < 4]
    h, e = np.histogram(iv, bins=np.arange(0.9, 3.01, 0.1))
    print(f"bell {bell}: n={len(iv)} median {np.median(iv):.3f}  " + " ".join(f"{e_:.1f}:{h_}" for h_, e_ in zip(h, e) if h_))
