"""Write the sixty pool games as the selectors see them (no names, no URLs, no clocks).

usage: python pool.py <drawn-400.json> <outdir>
"""
import json, os, sys

def pgn(i, g):
    head = [
        ("Game", f"{i:02d} of 60"), ("Speed", g["speed"]), ("TimeControl", g["time_control"]),
        ("WhiteElo", g["white_elo"]), ("BlackElo", g["black_elo"]), ("Result", g["result"]),
        ("Ending", g["ending"]), ("Moves", g["moves"]), ("ECO", g["eco"]), ("Opening", g["opening"]),
    ]
    out = [f'[{k} "{v}"]' for k, v in head]
    body, line = [], []
    for p, s in enumerate(g["san"]):
        tok = (f"{p // 2 + 1}. " if p % 2 == 0 else "") + s
        line.append(tok)
    text = " ".join(line) + " " + g["result"]
    # wrap at ~80
    words, cur = text.split(" "), ""
    for w in words:
        if len(cur) + len(w) + 1 > 80:
            body.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    body.append(cur)
    return "\n".join(out) + "\n\n" + "\n".join(body) + "\n"

def main(src, outdir):
    d = json.load(open(src))[:60]
    os.makedirs(outdir, exist_ok=True)
    for i, g in enumerate(d, 1):
        open(os.path.join(outdir, f"game-{i:02d}.pgn"), "w").write(pgn(i, g))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
