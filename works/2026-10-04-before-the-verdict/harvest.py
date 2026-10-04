"""Fetch IERS EOP C04 (eopc04.1962-now), log it, and write data.js with the LOD column in ms.
Session 106. The raw file is not committed; its URL, size, SHA-256 and time are in harvest-log.json."""
import hashlib, json, re, sys, urllib.request, datetime
URL = "https://hpiers.obspm.fr/eoppc/eop/eopc04/eopc04.1962-now"
raw = urllib.request.urlopen(URL, timeout=120).read()
log = {"url": URL, "fetched_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
       "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
text = raw.decode("ascii", "replace").splitlines()
header = [l for l in text if l.startswith("#")]
rows = [l.split() for l in text if l.strip() and not l.startswith("#")]
# find the column named LOD in the last header line that names columns
cols = None
for l in header:   # the column line reads '# YR MM DD HH MJD x(") ... LOD(s) x Er ...'; units sit in brackets
    toks = [t.split("(")[0] for t in l.lstrip("#").split()]
    if "LOD" in toks and "MJD" in toks:
        cols = toks
if cols is None:
    sys.exit("no header naming LOD and MJD; header was:\n" + "\n".join(header[-6:]))
i_lod = cols.index("LOD"); i_mjd = cols.index("MJD")   # both stand before the error columns, so the index holds
log["columns"] = cols; log["rows"] = len(rows)
mjd = [float(r[i_mjd]) for r in rows]; lod = [float(r[i_lod]) * 1000 for r in rows]   # s -> ms
assert all(abs(mjd[k + 1] - mjd[k] - 1) < 1e-6 for k in range(len(mjd) - 1)), "not one row per day"
start = (datetime.date(1858, 11, 17) + datetime.timedelta(days=int(mjd[0]))).isoformat()
end = (datetime.date(1858, 11, 17) + datetime.timedelta(days=int(mjd[-1]))).isoformat()
log.update(first_day=start, last_day=end)
open("data.js", "w").write("const D={start:%s,lod:[%s]};\n" % (json.dumps(start), ",".join("%.4f" % v for v in lod)))
json.dump(log, open("harvest-log.json", "w"), indent=1)
print({k: log[k] for k in ("bytes", "rows", "first_day", "last_day")}, cols)
