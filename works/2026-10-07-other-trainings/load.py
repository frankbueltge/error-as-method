"""Shared loader. hourly() -> list of 365 days x 24 values (None where missing), in CET, day 1 = 2025-01-01.
daily() -> list of 365 official daily means (None where missing). Keys of the API's data are date_start."""
import json, datetime
D0 = datetime.datetime(2025, 1, 1)
def _rows(path):
    d = json.load(open(path))['data']
    assert len(d) == 1, list(d)
    return next(iter(d.values()))
def hourly(path='sources/hourly-2025.json'):
    H = [[None]*24 for _ in range(365)]
    for start, v in _rows(path).items():
        t = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        k = int((t - D0).total_seconds() // 3600)
        if 0 <= k < 8760 and v[2] is not None: H[k // 24][k % 24] = float(v[2])
    return H
def daily(path='sources/daily-2025.json'):
    Dm = [None]*365
    for start, v in _rows(path).items():
        t = datetime.datetime.strptime(start[:10], '%Y-%m-%d')
        k = (t - D0).days
        if 0 <= k < 365 and v[2] is not None: Dm[k] = float(v[2])
    return Dm
