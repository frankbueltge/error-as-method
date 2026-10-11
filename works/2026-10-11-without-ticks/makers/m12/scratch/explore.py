import csv,statistics as st,collections
rows=list(csv.DictReader(open('../work/births.csv')))
print(len(rows), rows[-1])
for r in rows:
  for k in r: r[k]=int(r[k])
by=collections.defaultdict(list)
for r in rows: by[r['day_of_week']].append(r['births'])
for k in sorted(by): print(k, round(st.mean(by[k])))
yr=collections.defaultdict(int)
for r in rows: yr[r['year']]+=r['births']
print(dict(yr))
# ratio to same-weekday mean of that year-month
key=collections.defaultdict(list)
for r in rows: key[(r['year'],r['month'],r['day_of_week'])].append(r['births'])
md=collections.defaultdict(list)
for r in rows:
  m=st.mean(key[(r['year'],r['month'],r['day_of_week'])]); md[(r['month'],r['date_of_month'])].append(r['births']/m)
s=sorted(((st.mean(v),k) for k,v in md.items()))
print(s[:15]); print(s[-10:])
print(min(rows,key=lambda r:r['births']), max(rows,key=lambda r:r['births']))
