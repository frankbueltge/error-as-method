"""extract.py <dir of fpk25196.dat ... fpk25256.dat>: cuts tonight's source from NOAA GML's SURFRAD daily files for the
Fort Peck, Montana station (48.31 N, 105.10 W, 634 m; file header), 2025 days 196-256 (15 July - 13 September 2025, UTC),
downloaded from https://gml.noaa.gov/aftp/data/radiation/surfrad/Fort_Peck_MT/2025/ (CC0 1.0, README_SURFRAD.txt).
Writes every 1-minute line's time, solar zenith angle, downwelling global solar (dw_solar, W m-2) and its QC flag,
unchanged, to sources/fpk_dwsolar_1min_20250715_20250913.csv, and the raw files' SHA-256 to sources/MANIFEST.json.
Column positions follow README_SURFRAD.txt (year jday month day hour min dt zen dw_solar qc_dwsolar ...)."""
import sys, os, csv, glob, hashlib, json
HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(sys.argv[1], "fpk25*.dat")))
assert len(files) == 61 and files[0].endswith("fpk25196.dat") and files[-1].endswith("fpk25256.dat")
man = {"source": "https://gml.noaa.gov/aftp/data/radiation/surfrad/Fort_Peck_MT/2025/", "licence": "CC0 1.0 (README_SURFRAD.txt)",
       "readme": "https://gml.noaa.gov/aftp/data/radiation/surfrad/Fort_Peck_MT/README_SURFRAD.txt", "files": {}}
out = os.path.join(HERE, "sources", "fpk_dwsolar_1min_20250715_20250913.csv"); n = 0
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["year", "jday", "month", "day", "hour", "min", "zen_deg", "dw_solar_wm2", "qc_dwsolar"])
    for p in files:
        b = open(p, "rb").read(); man["files"][os.path.basename(p)] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        lines = b.decode().split("\n"); man.setdefault("header", lines[:2])
        for line in lines[2:]:
            t = line.split()
            if len(t) < 10: continue
            w.writerow(t[0:6] + [t[7], t[8], t[9]]); n += 1
json.dump(man, open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1)
print(n, "rows ->", out)
