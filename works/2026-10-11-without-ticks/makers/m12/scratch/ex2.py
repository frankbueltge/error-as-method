import csv,statistics as st,collections,datetime
rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(open('../work/births.csv'))]
key=collections.defaultdict(list)
for r in rows: key[(r['year'],r['month'],r['day_of_week'])].append(r['births'])
for r in rows:
  r['ratio']=r['births']/st.median(key[(r['year'],r['month'],r['day_of_week'])])
out=sorted(rows,key=lambda r:r['ratio'])
for r in out[-15:]: print(r)
print()
for r in rows:
  if r['month']==r['date_of_month'] and r['year']%100==r['month']: print('rep',r)
f13=[r['ratio'] for r in rows if r['date_of_month']==13 and r['day_of_week']==5]
print('fri13',len(f13),st.mean(f13))
for r in rows:
  if r['month']==2 and r['date_of_month']==29: print('leap',r)
# weekday share
wk=[r['births'] for r in rows if r['day_of_week']<6]; we=[r['births'] for r in rows if r['day_of_week']>=6]
print(min(wk),max(we))
