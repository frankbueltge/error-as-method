#!/usr/bin/env python3
"""Session 67 probe runner — CPython.

Two modes.
  emit   : answer every probe, run the four internal-identity checks, and render
           each seed double with this runtime's DEFAULT string conversion.
  parse  : read a JSON array of strings on stdin, parse each as a number with this
           runtime's ordinary conversion, and return the IEEE-754 bit pattern.

Every answer is a string. Nothing is normalised across runtimes: the point is what
each one says in its own words.
"""
import json
import struct
import sys
import unicodedata
import itertools

SEEDS = json.load(open(__file__.rsplit("/", 1)[0] + "/seeds.json"))


def bits(x):
    return struct.pack(">d", x).hex()


def unbits(h):
    return struct.unpack(">d", bytes.fromhex(h))[0]


def cps(s):
    return " ".join("U+%04X" % ord(c) for c in s)


def emit():
    a = {}

    # ---- Family S: answers that descend from the Unicode Character Database ----
    a["S1"] = cps("ß".upper())            # LATIN SMALL LETTER SHARP S
    a["S2"] = cps("ﬁ".upper())            # LATIN SMALL LIGATURE FI
    a["S3"] = cps("İ".lower())            # LATIN CAPITAL LETTER I WITH DOT ABOVE
    a["S4"] = cps("ı".upper())            # LATIN SMALL LETTER DOTLESS I
    a["S5"] = cps("ΟΔΟΣ".lower())   # word-final sigma
    a["S6"] = cps("ᏸ".upper())            # CHEROKEE SMALL LETTER YE (Unicode 8.0)
    a["S7"] = cps("ჯ".upper())            # GEORGIAN LETTER JHAN (Mtavruli, Unicode 11.0)
    a["S8"] = cps("\U00010428".upper())        # DESERET SMALL LETTER LONG I (non-BMP)
    a["S9"] = cps("ǳ".upper())            # LATIN SMALL LETTER DZ
    a["S10"] = cps("ẞ".lower())           # LATIN CAPITAL LETTER SHARP S

    # ---- Family I: answers written by hand, per runtime ----
    a["I1"] = str(-7 % 3)
    a["I2"] = str(7 % -3)
    a["I3"] = str(-7 // 3)
    a["I4"] = str(0.1 + 0.2)
    a["I5"] = str(1 / 3)
    a["I6"] = str(1e21)
    a["I7"] = str(-0.0)
    a["I8"] = " ".join(str(round(v)) for v in (0.5, 1.5, 2.5, -0.5))
    a["I9"] = "true" if "10" < "9" else "false"
    a["I10"] = "true" if "" == 0 else "false"
    a["I11"] = str(len("\U0001d11e"))
    a["I12"] = "true" if 0.1 + 0.2 == 0.3 else "false"
    a["I13"] = " ".join(str(v) for v in sorted([10, 9, 1]))
    a["I14"] = str(2 ** 3 ** 2)
    a["I15"] = " ".join(_numify(s) for s in ("0x10", "010", "1e2", " 12 "))

    checks = {
        "L1_roundtrip": l1(),
        "L2_loose_equality": l2(),
        "L3_relational_coherence": l3(),
        "L4_division_identity": l4(),
    }

    renderings = {s["name"]: str(unbits(s["bits"])) for s in SEEDS}

    return {"runtime": "python", "version": sys.version.split()[0],
            "unicode_version": unicodedata.unidata_version,
            "answers": a, "checks": checks, "renderings": renderings}


# I15 answers in bit patterns, not in rendered digits: the question is what the
# string PARSES to, and rendering it back would fold in the I4-I7 question instead.
def _numify(s):
    try:
        return bits(float(s))
    except ValueError:
        return "error"


# L1 -- does this runtime parse back its own default rendering of a double?
def l1():
    fails = []
    for s in SEEDS:
        x = unbits(s["bits"])
        rendered = str(x)
        try:
            back = float(rendered)
        except ValueError:
            fails.append({"seed": s["name"], "rendered": rendered, "back": None})
            continue
        if bits(back) != s["bits"]:
            fails.append({"seed": s["name"], "rendered": rendered, "back": bits(back)})
    return {"tested": len(SEEDS), "violations": len(fails), "detail": fails}


# The scalar set for L2/L3: this runtime's nearest analogue of the classic set.
def _scalars():
    return [("0", 0), ("''", ""), ("'0'", "0"), ("false", False),
            ("none", None), ("'abc'", "abc"), ("[]", [])]


# L2 -- is this runtime's own equality operator transitive over that set?
def l2():
    sc = _scalars()
    viol = []
    for (na, x), (nb, y), (nc, z) in itertools.product(sc, repeat=3):
        try:
            if (x == y) and (y == z) and not (x == z):
                viol.append([na, nb, nc])
        except Exception:
            pass
    return {"operator": "==", "set_size": len(sc),
            "transitivity_violations": len(viol), "examples": viol[:5]}


# L3 -- if a<=b and a>=b, does this runtime also say a==b?
def l3():
    sc = _scalars()
    viol, incomparable = [], 0
    for (na, x), (nb, y) in itertools.product(sc, repeat=2):
        try:
            le, ge, eq = (x <= y), (x >= y), (x == y)
        except TypeError:
            incomparable += 1
            continue
        if le and ge and not eq:
            viol.append([na, nb])
    return {"pairs": len(sc) ** 2, "incomparable": incomparable,
            "violations": len(viol), "examples": viol[:5]}


# L4 -- does q*b + r == a hold, with this runtime's own // and % ?
def l4():
    viol = []
    for a in (-13, -8, -7, -1, 0, 1, 7, 8, 13):
        for b in (3, -3, 5, -5):
            q, r = a // b, a % b
            if q * b + r != a:
                viol.append([a, b, q, r])
    return {"pairs": 36, "violations": len(viol), "examples": viol[:5]}


def parse():
    strings = json.load(sys.stdin)
    out = []
    for s in strings:
        try:
            out.append(bits(float(s)))
        except Exception:
            out.append(None)
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "emit"
    print(json.dumps(emit() if mode == "emit" else parse()))
