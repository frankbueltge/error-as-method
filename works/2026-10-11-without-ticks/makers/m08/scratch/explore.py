import csv,statistics as st,collections,datetime
R=list(csv.DictReader(open('/tmp/claude-0/s121/mk/m08/work/births.csv')))
print(len(R))
for r in R:
  for k in r: r[k]=int(r[k])
# check completeness
d0=datetime.date(2000,1,1)
ds=[datetime.date(r['year'],r['month'],r['date_of_month']) for r in R]
print(ds[0],ds[-1],len(set(ds)), (ds[-1]-ds[0]).days+1)
bad=[r for r in R if datetime.date(r['year'],r['month'],r['date_of_month']).isoweekday()!=r['day_of_week']]
print('dow mismatches',len(bad))
dow=collections.defaultdict(list)
for r in R: dow[r['day_of_week']].append(r['births'])
for k in sorted(dow): print(k, round(st.mean(dow[k])))
yr=collections.defaultdict(list)
for r in R: yr[r['year']].append(r['births'])
for k in sorted(yr): print(k, sum(yr[k]), round(st.mean(yr[k])))
b=[r['births'] for r in R]; print(min(b),max(b))
# day of year relative to expected (dow x year mean)
m={(r['year'],r['day_of_week']):0 for r in R}
exp={k:st.mean([r['births'] for r in R if (r['year'],r['day_of_week'])==k]) for k in m}
md=collections.defaultdict(list)
for r in R: md[(r['month'],r['date_of_month'])].append(r['births']/exp[(r['year'],r['day_of_week'])])
s=sorted(md.items(), key=lambda kv: st.mean(kv[1]))
for k,v in s[:15]: print('low',k,round(st.mean(v),3),len(v))
for k,v in s[-10:]: print('high',k,round(st.mean(v),3),len(v))
# friday 13
f13=[r['births']/exp[(r['year'],5)] for r in R if r['day_of_week']==5 and r['date_of_month']==13]
f6=[r['births']/exp[(r['year'],5)] for r in R if r['day_of_week']==5 and r['date_of_month'] in (6,20)]
print('fri13',round(st.mean(f13),3),len(f13),'fri6/20',round(st.mean(f6),3))
dup=collections.Counter(ds); print([k for k,v in dup.items() if v>1])
