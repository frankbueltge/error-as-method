"""load.py: the 731 daily values in day order (day 1 = 2024-01-01, a Monday)."""
import json, datetime
def load():
    items = json.load(open('sources/full-moon-2024-2025.json'))['items']
    by = {it['timestamp'][:8]: it['views'] for it in items}
    d0 = datetime.date(2024, 1, 1)
    days = [(d0 + datetime.timedelta(i)).strftime('%Y%m%d') for i in range(731)]
    return [by.get(d) for d in days], days   # None where the API returned no row
