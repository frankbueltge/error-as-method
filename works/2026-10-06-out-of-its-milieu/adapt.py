"""The adapters: the only code written tonight that stands between the grid and the carried
instruments. Committed before the data was fetched. Nothing in carried/ is edited.

  python3 adapt.py sources/fnew-2026-8.csv

Reads the NESO 1-second file (first column a timestamp, second the frequency in Hz) and writes:
  series.json          per-second facts: count of seconds, missing seconds, first/last timestamp
  carried/ear/month.wav       the month audified: one grid second = one sample at 44,100 Hz,
                               x = (f - 50) / 0.5 clipped to [-1, 1] (the statutory band 49.5-50.5
                               fills the full scale), missing seconds = 0 (= 50 Hz), 16-bit mono
  carried/grid24/data.js      D = {start: "2026-08-01", lod: [...]}: one value per minute, the mean
                               deviation (f - 50) in mHz, fed in where the instrument expects
                               one value per day in ms; a minute with no data repeats the last value
  carried/mould/data.js       D = [[t_ms, lat, lon, depth, mag, magType, type, status, net, place], ...]
                               one row per minute: lon = -180 + 360 * minute_of_day / 1440,
                               lat = 59 - 2 * (day - 1), depth 0, mag = 10 * (mean f - 50)
                               (one magnitude unit = 0.1 Hz), magType "hz10", type "minute",
                               status "reviewed", net "neso", place "GB grid, YYYY-MM-DD HH:MM"
Both JS instruments get minutes, not seconds, because their home materials held thousands of
records (10,870 events; 23,623 days), not millions; this is the one reduction tonight, named here.
"""
import csv, json, sys, wave, struct, math
from datetime import datetime, timezone

path = sys.argv[1]
secs = {}
with open(path, newline="") as fh:
    r = csv.reader(fh); head = next(r)
    for row in r:
        if len(row) < 2 or not row[1].strip(): continue
        ts = row[0].strip().replace("T", " ").rstrip("Z")
        try: t = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        except ValueError: continue
        secs[int(t.timestamp())] = float(row[1])
t0 = min(secs); t1 = max(secs)
# the month runs from the first midnight (UTC) to the last second present
start = datetime.fromtimestamp(t0, timezone.utc).replace(hour=0, minute=0, second=0)
s0 = int(start.timestamp()); n = t1 - s0 + 1
missing = sum(1 for k in range(s0, t1 + 1) if k not in secs)
json.dump({"header": head, "seconds_present": len(secs), "span_seconds": n, "missing_seconds": missing,
           "first": datetime.fromtimestamp(t0, timezone.utc).isoformat(), "last": datetime.fromtimestamp(t1, timezone.utc).isoformat(),
           "min_hz": min(secs.values()), "max_hz": max(secs.values())}, open("series.json", "w"), indent=1)

with wave.open("carried/ear/month.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
    buf = bytearray()
    for k in range(s0, t1 + 1):
        f = secs.get(k); x = 0.0 if f is None else max(-1.0, min(1.0, (f - 50) / 0.5))
        buf += struct.pack("<h", int(round(x * 32767)))
    w.writeframes(bytes(buf))

mins, rows, last = [], [], 0.0
for m in range(n // 60 + (1 if n % 60 else 0)):
    v = [secs[k] for k in range(s0 + 60 * m, s0 + 60 * m + 60) if k in secs]
    if v: last = sum(v) / len(v) - 50
    mins.append(round(last * 1000, 2))
    t = s0 + 60 * m; d = datetime.fromtimestamp(t, timezone.utc); mod = d.hour * 60 + d.minute
    lon = -180 + 360 * mod / 1440; lat = 59 - 2 * (d.day - 1)
    rows.append([t * 1000, lat, round(lon, 4), 0, round(10 * last, 3), "hz10", "minute", "reviewed", "neso",
                 f"GB grid, {d:%Y-%m-%d %H:%M}"])
open("carried/grid24/data.js", "w").write("const D=" + json.dumps({"start": start.strftime("%Y-%m-%d"), "lod": mins}, separators=(",", ":")) + ";\n")
open("carried/mould/data.js", "w").write("const D=" + json.dumps(rows, separators=(",", ":")) + ";\n")
print(json.load(open("series.json")), len(mins), "minutes")
