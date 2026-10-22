"""Shared by the four instruments (Session 149). Reads one column of a CSV, parses times, writes SVG."""
import csv, sys, json, math, datetime, os

def read(path, col):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096); f.seek(0)
        try: dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error: dialect = csv.excel
        rows = list(csv.reader(f, dialect))
    head, body = rows[0], rows[1:]
    if col not in head: sys.exit("column %r not in header %r" % (col, head))
    i = head.index(col)
    return [r[i].strip() if i < len(r) else "" for r in body]

def num(s):
    try:
        x = float(s.replace(",", "")) if s else None
        return x if x is not None and math.isfinite(x) else None
    except ValueError: return None

def when(s):
    """seconds since 1970 for an ISO date/datetime or a plain number; None otherwise"""
    if not s: return None
    try:
        d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        if d.tzinfo is None: d = d.replace(tzinfo=datetime.timezone.utc)
        return d.timestamp()
    except ValueError: return num(s)

def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def svg(title, sub, body, W=1000, H=560):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'font-family="Georgia, serif"><rect width="%d" height="%d" fill="#f7f4ee"/>'
            '<text x="40" y="44" font-size="22" fill="#1b1b1b">%s</text>'
            '<text x="40" y="70" font-size="14" fill="#555">%s</text>%s</svg>') % (W, H, W, H, W, H, esc(title), esc(sub), body)

def write(name, svgtext, result):
    out = os.getcwd()
    open(os.path.join(out, "reading.svg"), "w").write(svgtext)
    result["instrument"] = name
    json.dump(result, open(os.path.join(out, "reading.json"), "w"), indent=1)
    print(json.dumps(result, indent=1)[:3000]); print("wrote reading.svg and reading.json in", out)
