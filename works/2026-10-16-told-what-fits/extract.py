"""extract.py <Pfynwald_10min_LM.parquet>: cuts tonight's source from the EnviDat package (doi:10.16904/envidat.778,
CC BY 4.0): every 10-minute row of series 1548 (Pfynwald-Control, tree 1038, Pinus sylvestris, point dendrometer),
variable `src` (stem radius change, micrometres), from 2024-07-09 00:00 UTC to 2024-09-07 23:50 UTC, written unchanged
(timestamps as UTC ISO strings; the package records Etc/GMT-1 = UTC+1) to sources/pfynwald_1548_src_10min_20240709_20240907.csv.
Needs pyarrow. The full package is not redistributed here: its hash is in sources/MANIFEST.json."""
import sys, os, csv, datetime as dt
import pyarrow.parquet as pq
HERE = os.path.dirname(os.path.abspath(__file__))
t = pq.read_table(sys.argv[1], filters=[("variable", "=", "src"), ("series_id", "=", 1548)]).to_pylist()
a = dt.datetime(2024, 7, 9, tzinfo=dt.timezone.utc); b = a + dt.timedelta(days=61)
rows = sorted((r for r in t if a <= r["timestamp"] < b), key=lambda r: r["timestamp"])
out = os.path.join(HERE, "sources", "pfynwald_1548_src_10min_20240709_20240907.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["timestamp_utc", "series_id", "site_name", "tree_name", "variable", "value_um", "quality_flag", "qc_severity", "valtype"])
    for r in rows:
        w.writerow([r["timestamp"].astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), r["series_id"], r["site_name"], r["tree_name"],
                    r["variable"], repr(r["value"]), r["quality_flag"], r["qc_severity"], r["valtype"]])
print(len(rows), "rows ->", out)
