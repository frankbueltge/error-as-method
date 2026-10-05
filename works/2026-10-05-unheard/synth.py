"""Make ringing the practice cannot hear. Parameters come from iterations/iN.json.

  python3 synth.py iterations/i1.json /tmp/.../i1.wav

Rows: two pulls of rounds, a plain course of Plain Bob Minor, two pulls of rounds. Place notation
x16x16x16x16x16x12 (12 changes a lead, 5 leads; checked below to come round and to be true).
Each bell is a sum of decaying partials at ratios of its prime. Seeded: same file, same sound.
"""
import json, sys, wave
import numpy as np

SR = 22050


def changes(row, pn):
    r = list(row)
    if pn == "x":
        for i in range(0, len(r) - 1, 2):
            r[i], r[i + 1] = r[i + 1], r[i]
        return r
    places = {int(c) - 1 for c in pn}
    i = 0
    while i < len(r) - 1:
        if i in places:
            i += 1
            continue
        r[i], r[i + 1] = r[i + 1], r[i]
        i += 2
    return r


def plain_bob_minor():
    lead = ["x", "16", "x", "16", "x", "16", "x", "16", "x", "16", "x", "12"]
    rounds = [1, 2, 3, 4, 5, 6]
    rows, r = [rounds], rounds
    for _ in range(5):
        for pn in lead:
            r = changes(r, pn)
            rows.append(r)
    assert rows[-1] == rounds, "does not come round"
    assert len({tuple(x) for x in rows[:-1]}) == 60, "false: a row repeats"
    return rows


def all_rows():
    rounds = [[1, 2, 3, 4, 5, 6]] * 4
    return rounds + plain_bob_minor()[1:] + rounds[:3]


def strike_times(rows, p, rng):
    """Blow times. p: blow (s), gap (blow-units after each backstroke row), jitter (s, sd)."""
    t, out = 0.5, []
    for i, row in enumerate(rows):
        for b in row:
            out.append((t + rng.normal(0, p.get("jitter", 0.0)), b))
            t += p["blow"]
        if i % 2 == 1:
            t += p["blow"] * p.get("gap", 1.0)
    return out


def bell(prime, p, rng, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    y = np.zeros(n)
    for ratio, amp, decay in p["partials"]:
        f = prime * ratio * (1 + rng.normal(0, p.get("detune", 0.0)))
        y += amp * np.exp(-tt / decay) * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6.28))
    att = int(p.get("attack", 0.002) * SR)
    y[:att] *= np.linspace(0, 1, att)
    if p.get("clang", 0):  # the clapper's strike: a short burst of noise
        k = int(0.012 * SR)
        y[:k] += p["clang"] * rng.normal(0, 1, k) * np.linspace(1, 0, k)
    return y


def render(p, out):
    rng = np.random.default_rng(p.get("seed", 108))
    rows = all_rows()
    blows = strike_times(rows, p, rng)
    total = blows[-1][0] + 4
    y = np.zeros(int(total * SR))
    cache = {}
    for t, b in blows:
        if b not in cache or p.get("fresh", False):
            cache[b] = bell(p["primes"][b - 1], p, rng, 3.5)
        s = cache[b]
        i = int(t * SR)
        y[i:i + len(s)] += s[:len(y) - i] * p.get("level", [1] * 6)[b - 1]
    if p.get("room", 0):  # a crude tower: a few late echoes
        for d, g in ((0.031, 0.5), (0.067, 0.35), (0.113, 0.25), (0.19, 0.15)):
            k = int(d * SR)
            y[k:] += p["room"] * g * y[:-k]
    if p.get("noise", 0):
        y += p["noise"] * rng.normal(0, 1, len(y))
    y = y / np.abs(y).max() * 0.8
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    json.dump({"rows": rows, "blows": [[round(t, 4), b] for t, b in blows]},
              open(out.replace(".wav", ".rows.json"), "w"))


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
