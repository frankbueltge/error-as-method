import csv,statistics as st,collections,datetime as dt
R=[r for r in csv.DictReader(open('../work/births.csv'))]
for r in R:
  for k in r: r[k]=int(r[k])
print(len(R), min(r['births'] for r in R), max(r['births'] for r in R))
# check dow consistency
bad=sum(1 for r in R if dt.date(r['year'],r['month'],r['date_of_month']).isoweekday()!=r['day_of_week']); print('bad dow',bad)
yr=collections.defaultdict(list)
for r in R: yr[r['year']].append(r['births'])
for y in sorted(yr): print(y,len(yr[y]),sum(yr[y]))
dw=collections.defaultdict(list)
for r in R: dw[r['day_of_week']].append(r['births'])
for d in sorted(dw): print('dow',d,round(st.mean(dw[d])))
# ratio to a centered 7-day... simpler: ratio to year-dow mean
m={}
g=collections.defaultdict(list)
for r in R: g[(r['year'],r['day_of_week'])].append(r['births'])
for k in g: m[k]=st.mean(g[k])
dd=collections.defaultdict(list)
for r in R: dd[(r['month'],r['date_of_month'])].append(r['births']/m[(r['year'],r['day_of_week'])])
s=sorted(dd.items(),key=lambda kv:st.mean(kv[1]))
for k,v in s[:15]: print('low',k,round(st.mean(v),3))
for k,v in s[-10:]: print('high',k,round(st.mean(v),3))
# 13th effect fridays
f13=[r['births']/m[(r['year'],5)] for r in R if r['day_of_week']==5 and r['date_of_month']==13]
f6=[r['births']/m[(r['year'],5)] for r in R if r['day_of_week']==5 and r['date_of_month'] in (6,20)]
print('fri13',round(st.mean(f13),3),len(f13),'fri6/20',round(st.mean(f6),3))
s=sorted(R,key=lambda r:r['births'])
print([ (r['year'],r['month'],r['date_of_month'],r['births']) for r in s[:8]])
print([ (r['year'],r['month'],r['date_of_month'],r['births']) for r in s[-8:]])
