"""Experiment 35, Twin Chips: choose the chips, make their twins, deal them to the makers.

Seed 151. Reads sources/rgb.txt (the xkcd colour survey's 949 named colours, CC0).
Writes plan.json and, for every maker, the brief it is handed (briefs/).
Standard library only. The sheets for the lookers are drawn by sheets.py.
"""
import json, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 151
N_CHIPS = 24
MAKERS = {"N": ["n1", "n2", "n3", "n4", "n5", "n6"], "S": ["s1", "s2", "s3", "s4", "s5", "s6"]}


def srgb_to_lab(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


def load_crowd():
    rows = []
    for line in open(os.path.join(HERE, "sources", "rgb.txt"), encoding="utf8"):
        if line.startswith("#"):
            continue
        name, hx = line.rstrip("\n").split("\t")[:2]
        rows.append((name.strip(), hx.strip().lower()))
    return rows


def main():
    crowd = load_crowd()
    labs = {hx: srgb_to_lab(hx) for _, hx in crowd}
    hexes = set(labs)
    rng = random.Random(SEED)
    pool = list(crowd)
    rng.shuffle(pool)
    chips = []
    for name, hx in pool:
        if len(chips) == N_CHIPS:
            break
        lab = labs[hx]
        # its nearest other crowd colour must be far enough that a twin stays inside the name's own region
        nearest = min(de(lab, labs[h]) for _, h in crowd if h != hx)
        if nearest < 6:
            continue
        rgb = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
        twin = None
        for _ in range(4000):
            d = [rng.choice([-4, -3, -2, 2, 3, 4]) for _ in range(3)]
            t = [min(255, max(0, c + e)) for c, e in zip(rgb, d)]
            th = "#%02x%02x%02x" % tuple(t)
            if th in hexes:
                continue
            tl = srgb_to_lab(th)
            dd = de(lab, tl)
            if not (1.0 <= dd <= 2.0):
                continue
            near = min(crowd, key=lambda r: de(tl, labs[r[1]]))
            if near[1] != hx:
                continue
            twin = (th, round(dd, 3))
            break
        if twin is None:
            continue
        chips.append({"id": "c%02d" % (len(chips) + 1), "crowd_name": name, "on": hx, "off": twin[0],
                      "de_twin": twin[1], "nearest_other_de": round(nearest, 2)})
    deal = {}
    for cond, ms in MAKERS.items():
        for mi, m in enumerate(ms):
            order = list(range(N_CHIPS))
            rng.shuffle(order)
            seq = []
            for k, ci in enumerate(order):
                c = chips[ci]
                side = "on" if (ci + mi) % 2 == 0 else "off"
                seq.append({"slot": k + 1, "chip": c["id"], "side": side, "hex": c[side]})
            deal[m] = {"condition": cond, "chips": seq}
    plan = {"seed": SEED, "source": "sources/rgb.txt", "n_chips": N_CHIPS,
            "twin_rule": "each channel moved by 2 to 4 units; hex not in the crowd list; CIELAB dE76 from the original between 1.0 and 2.0; the crowd colour nearest the twin is still the original",
            "chip_rule": "drawn in seeded order from the 949 crowd colours; kept only if no other crowd colour lies within dE76 6",
            "deal_rule": "maker i of a condition sees chip j on-list when (i+j) is even, its twin otherwise; so every chip is named on-list by three makers and as a twin by three, in each condition",
            "chips": chips, "deal": deal}
    json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print(len(chips), "chips")
    for c in chips:
        print(c["id"], c["on"], c["off"], c["de_twin"])


if __name__ == "__main__":
    main()
