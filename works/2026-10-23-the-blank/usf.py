"""Read the USF Free Association Norms, Appendix A (Nelson, McEvoy & Schreiber 1998).

The eight Cue_Target_Pairs files are not committed (copyright Nelson, McEvoy & Schreiber);
their URLs and hashes are in sources/MANIFEST.json. Pass the directory that holds them.

Returns {cue: {"G": participants given the cue, "resp": {target: participants producing it}}}.
Appendix A lists only targets produced by two or more participants; the rest of each cue's
group gave idiosyncratic responses (one participant each), which cannot make three agree.
"""
import os
import re

FILES = ["A-B", "C", "D-F", "G-K", "L-O", "P-R", "S", "T-Z"]


def norm(w):
    """The scoring rule, fixed before any maker ran: upper case, letters only, and a final S
    dropped when at least three letters remain (BOOKS = BOOK)."""
    w = re.sub(r"[^A-Z]", "", w.upper())
    if len(w) >= 4 and w.endswith("S") and not w.endswith("SS"):
        w = w[:-1]
    return w


def load(d):
    cues = {}
    for f in FILES:
        with open(os.path.join(d, "Cue_Target_Pairs." + f), encoding="latin-1") as fh:
            for line in fh:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 6 or parts[0] == "CUE" or not parts[3].isdigit():
                    continue
                cue, target, G, P = parts[0], parts[1], int(parts[3]), int(parts[4])
                c = cues.setdefault(cue, {"G": G, "resp": {}})
                t = norm(target)
                c["resp"][t] = c["resp"].get(t, 0) + P
    return cues


def comb3(n):
    return n * (n - 1) * (n - 2) / 6


def p_three_agree(c):
    """Probability that three participants drawn without replacement from the cue's group
    gave the same (normalised) response."""
    G = c["G"]
    return sum(comb3(n) for n in c["resp"].values()) / comb3(G)
