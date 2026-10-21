"""elements.py : turns PubChem's periodic-table CSV (sources/) into data/elements.js, the one file every
page of tonight reads (Session 145). Columns keep PubChem's names and order. A cell left empty by PubChem
becomes null. The ten columns declared numeric before any maker ran are parsed as numbers; YearDiscovered
keeps PubChem's word "Ancient" where it has no year. Every other column stays the string PubChem gave."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
NUMERIC = ["AtomicNumber", "AtomicMass", "Electronegativity", "AtomicRadius", "IonizationEnergy",
           "ElectronAffinity", "MeltingPoint", "BoilingPoint", "Density", "YearDiscovered"]
def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "sources", "pubchem-periodictable.csv"), encoding="utf-8")))
    out = []
    for r in rows:
        e = {}
        for k, v in r.items():
            if v == "": e[k] = None
            elif k in NUMERIC and v != "Ancient": e[k] = int(v) if v.lstrip("-").isdigit() else float(v)
            else: e[k] = v
        out.append(e)
    return out
def js(elements): return "const ELEMENTS = " + json.dumps(elements, ensure_ascii=False) + ";\n"
if __name__ == "__main__":
    E = load(); fields = list(E[0])
    json.dump({"fields": fields, "numeric": NUMERIC, "string": [f for f in fields if f not in NUMERIC]},
              open(os.path.join(HERE, "fields.json"), "w"), indent=1)
    sys.stdout.write(js(E))
