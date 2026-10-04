"""Reads the drawn table (Destatis GENESIS 45211-0013, fetched 2026-10-04, Data licence Germany
attribution 2.0) and writes data.js. Keeps every cell as written, including the symbols '.', '-'
and '0,0', because the table's own notation is part of the material."""
import json, hashlib
raw = open("sources/45211-0013_00.csv", "rb").read()
rows = []
for line in raw.decode("latin-1").splitlines():
    p = line.split(";")
    if len(p) == 6 and p[1].isdigit():
        rows.append({"state": p[0], "year": int(p[1]), "real": p[2], "real_chg": p[3], "nom": p[4], "nom_chg": p[5]})
assert len(rows) == 80, len(rows)
open("data.js", "w").write("const DATA = " + json.dumps(rows, ensure_ascii=False) + ";\n")
json.dump({"file": "sources/45211-0013_00.csv",
           "url": "https://genesis.destatis.de/genesisWS/downloads/00/tables/45211-0013_00.csv",
           "catalogue_entry": "https://www.govdata.de/ckan/api/3/action/package_show?id=umsatz-im-grosshandel-bundeslander-jahre-preisarten0e0e4",
           "fetched": "2026-10-04", "http": 200, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
           "table_stand": "14.09.2026 19:52:50 (from the file's footer)",
           "licence": "Datenlizenz Deutschland - Namensnennung - Version 2.0, https://www.govdata.de/dl-de/by-2-0; per https://www.destatis.de/EN/Service/Legal-Notice/CopyrightGENESISOnlineDatabase.html",
           "attribution": "Data source: Statistisches Bundesamt (Destatis), Genesis-Online, retrieved 2026-10-04; Data licence by-2-0 (www.govdata.de/dl-de/by-2-0); own representation",
           "why": "the drawn material: index 153,657 of the GovData catalogue, see draw-log.json"},
          open("sources/MANIFEST.json", "w"), ensure_ascii=False, indent=1)
print(len(rows), "rows")
