"""dogs.py (Session 146): the register as the makers get it. Twelve of the 35 published columns are kept, with
their published names; the other 23 repeat these as codes, sort keys or labels, or are constant on the day
(StichtagDat, AnzHunde). Numbers as numbers, empty cells as null. Owner age code 999 (Unbekannt) is kept as
published. No row is dropped or changed."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "fields.json")))
def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "sources", "KUL100OD1003.csv"), encoding="utf-8-sig")))
    out = []
    for r in rows:
        o = {}
        for f in F["fields"]:
            v = r[f]
            o[f] = None if v == "" else (int(v) if f in F["numeric"] else v)
        out.append(o)
    return out
def csv_text(rows):
    import io; s = io.StringIO(); w = csv.DictWriter(s, F["fields"], lineterminator="\n"); w.writeheader()
    for r in rows: w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    return s.getvalue()
def js(rows): return "const DOGS = " + json.dumps(rows, ensure_ascii=False) + ";\n"
