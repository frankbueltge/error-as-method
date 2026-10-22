"""bridges.py (Session 147): the inventory as the makers get it. Twelve of the 123 published columns of FHWA's
2025 delimited file for Delaware (sources/DE25.txt) are kept, with their published names (fields.json). The file's
text qualifier is a single quote (FHWA's download page); it is removed, and trailing blanks are trimmed. Numbers as
numbers (LAT_016 and LONG_017 lose their leading zero by becoming numbers), empty cells as null. No row is dropped
or changed: 874 bridges."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "fields.json")))
def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "sources", "DE25.txt"), encoding="latin-1"), quotechar="'"))
    out = []
    for r in rows:
        o = {}
        for f in F["fields"]:
            v = r[f].strip()
            o[f] = None if v == "" else ((float(v) if "." in v else int(v)) if f in F["numeric"] else v)
        out.append(o)
    return out
def csv_text(rows):
    import io; s = io.StringIO(); w = csv.DictWriter(s, F["fields"], lineterminator="\n"); w.writeheader()
    for r in rows: w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    return s.getvalue()
def js(rows): return "const BRIDGES = " + json.dumps(rows, ensure_ascii=False) + ";\n"
if __name__ == "__main__":
    R = load(); print(len(R)); print(R[0]); print(R[-1])
