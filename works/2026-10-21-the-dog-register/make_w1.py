"""make_w1.py <root> : Session 146, added after the results. Packet W1: the 18 mutants whose picture differs from
the parent's (pixeldiff.json), shuffled seed 1461, each re-written with a fresh PNG nonce. Key to coder/key-W1.json."""
import json, os, random, sys
H = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(sys.argv[1])
sys.argv = [sys.argv[0], root]; src = open(os.path.join(H, "make_packets.py")).read().split("C = [")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(H))
exec(src)  # put_png and the nonce, unchanged
PD = json.load(open(os.path.join(H, "pixeldiff.json"))); M = [m for m in [a + str(i) for a in "uts" for i in range(1, 9)] if PD[m] > 0]
rng = random.Random(1461); rng.shuffle(M); P = os.path.join(root, "packets", "W1"); os.makedirs(P, exist_ok=True); key = {}
for i, m in enumerate(M, 1): put_png(os.path.join(root, "mutants", m, "final.png"), os.path.join(P, "W%02d.png" % i)); key["W%02d" % i] = m
json.dump(key, open(os.path.join(H, "coder", "key-W1.json"), "w"), indent=1); print(len(M), "pictures")
