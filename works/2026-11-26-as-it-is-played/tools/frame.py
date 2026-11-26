"""Build the frame and draw the pool for experiment 62 (Session 188).

Reads the first 40 MiB of the Lichess open database file for October 2026
(lichess_db_standard_rated_2026-10.pgn.zst, CC0), decompresses the complete
games in that prefix, computes each game's features, and draws the pool of
60 games by seed 188. Player names and game URLs are dropped.

usage: python frame.py <prefix.pgn.zst> <outdir>
"""
import io, json, random, sys
import chess, chess.pgn, zstandard

SEED = 188
POOL = 60

def speed(event):
    e = event.lower()
    for s in ("ultrabullet", "bullet", "blitz", "rapid", "classical", "correspondence"):
        if s in e:
            return s
    return "other"

def features(game):
    h = game.headers
    board = game.board()
    moves, sans, fens, clocks = [], [], [board.board_fen()], []
    node = game
    while node.variations:
        node = node.variations[0]
        sans.append(board.san(node.move))
        board.push(node.move)
        fens.append(board.board_fen())
        c = node.clock()
        clocks.append(None if c is None else round(c, 1))
    plies = len(sans)
    term = h.get("Termination", "")
    res = h.get("Result", "*")
    if board.is_checkmate():
        ending = "checkmate"
    elif res == "1/2-1/2":
        ending = "draw"
    elif term == "Time forfeit":
        ending = "time"
    elif term == "Abandoned":
        ending = "abandoned"
    elif term == "Normal" and res in ("1-0", "0-1"):
        ending = "resignation"
    else:
        ending = "other"
    try:
        we, be = int(h.get("WhiteElo", 0)), int(h.get("BlackElo", 0))
    except ValueError:
        we = be = 0
    return {
        "event": h.get("Event", ""), "speed": speed(h.get("Event", "")),
        "time_control": h.get("TimeControl", ""), "utc": h.get("UTCDate", "") + " " + h.get("UTCTime", ""),
        "white_elo": we, "black_elo": be, "mean_elo": (we + be) / 2,
        "result": res, "termination": term, "ending": ending,
        "eco": h.get("ECO", ""), "opening": h.get("Opening", ""),
        "plies": plies, "moves": (plies + 1) // 2, "san": sans, "fens": fens, "clocks": clocks,
        "has_eval": "%eval" in str(game.variations[0].comment if game.variations else ""),
    }

def main(src, outdir):
    chunks = []
    with open(src, "rb") as fh:
        reader = zstandard.ZstdDecompressor().stream_reader(fh)
        while True:
            try:
                c = reader.read(1 << 20)
            except zstandard.ZstdError:
                break  # the prefix ends mid-block; keep what decompressed
            if not c:
                break
            chunks.append(c)
    text = b"".join(chunks).decode("utf-8", "replace")
    print("decompressed bytes:", len(text))
    # drop the final, probably truncated, game
    cut = text.rfind("\n\n[Event ")
    text = text[:cut]
    stream = io.StringIO(text)
    frame = []
    while True:
        g = chess.pgn.read_game(stream)
        if g is None:
            break
        if g.errors:
            continue
        frame.append(g)
    print("games in frame:", len(frame))
    first, last = frame[0].headers.get("UTCDate") + " " + frame[0].headers.get("UTCTime"), \
                  frame[-1].headers.get("UTCDate") + " " + frame[-1].headers.get("UTCTime")
    rng = random.Random(SEED)
    idx = sorted(rng.sample(range(len(frame)), 400))
    # 400 drawn: the first 60 by draw order become the pool; all 400 give the people's reference
    order = idx[:]
    rng.shuffle(order)
    feats = []
    for k, i in enumerate(order):
        f = features(frame[i])
        f["draw"] = k
        f["frame_index"] = i
        feats.append(f)
    # summary of the whole frame (cheap features only, no move replay)
    summ = {"games": len(frame), "first_utc": first, "last_utc": last, "endings": {}, "speeds": {}}
    for g in frame:
        h = g.headers
        sp = speed(h.get("Event", ""))
        summ["speeds"][sp] = summ["speeds"].get(sp, 0) + 1
    json.dump(summ, open(f"{outdir}/frame-summary.json", "w"), indent=1)
    json.dump(feats, open(f"{outdir}/drawn-400.json", "w"))
    print(json.dumps(summ, indent=1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
