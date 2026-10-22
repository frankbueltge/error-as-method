"""Draw each looker's sheet: 24 chips on white, numbered, as a PNG. Standard library only."""
import json, os, struct, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = {  # 5x7 digits
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}
CHIP, GAP, LABEL, COLS, SCALE = 140, 30, 40, 6, 3


def png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(px[y * w * 3:(y + 1) * w * 3]) for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def sheet(chips):
    rows = (len(chips) + COLS - 1) // COLS
    w = GAP + COLS * (CHIP + GAP)
    h = GAP + rows * (CHIP + LABEL + GAP)
    px = bytearray([255] * (w * h * 3))
    for k, c in enumerate(chips):
        x0 = GAP + (k % COLS) * (CHIP + GAP)
        y0 = GAP + (k // COLS) * (CHIP + LABEL + GAP)
        rgb = [int(c["hex"][i:i + 2], 16) for i in (1, 3, 5)]
        for y in range(y0, y0 + CHIP):
            for x in range(x0, x0 + CHIP):
                px[(y * w + x) * 3:(y * w + x) * 3 + 3] = bytes(rgb)
        s = str(c["slot"])
        tx = x0 + CHIP // 2 - len(s) * 6 * SCALE // 2
        ty = y0 + CHIP + 8
        for j, ch in enumerate(s):
            for r, line in enumerate(FONT[ch]):
                for q, bit in enumerate(line):
                    if bit == "1":
                        for dy in range(SCALE):
                            for dx in range(SCALE):
                                X, Y = tx + j * 6 * SCALE + q * SCALE + dx, ty + r * SCALE + dy
                                px[(Y * w + X) * 3:(Y * w + X) * 3 + 3] = b"\x00\x00\x00"
    return w, h, px


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    os.makedirs(os.path.join(HERE, "sheets"), exist_ok=True)
    for m, d in plan["deal"].items():
        if d["condition"] != "S":
            continue
        w, h, px = sheet(d["chips"])
        png(os.path.join(HERE, "sheets", m + ".png"), w, h, px)
        print(m, w, h)


if __name__ == "__main__":
    main()
