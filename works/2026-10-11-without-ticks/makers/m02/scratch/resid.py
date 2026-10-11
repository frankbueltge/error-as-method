import csv,statistics as st,collections,datetime as dt,json
R=[r for r in csv.DictReader(open('../work/births.csv'))]
for r in R:
  for k in r: r[k]=int(r[k])
g=collections.defaultdict(list)
for r in R: g[(r['year'],r['day_of_week'])].append(r['births'])
m={k:st.median(v) for k,v in g.items()}
for r in R: r['a']=r['births']/m[(r['year'],r['day_of_week'])]
# seasonal: rolling median +-15 days
A=[r['a'] for r in R]
for i,r in enumerate(R):
  w=A[max(0,i-15):i+16]; r['s']=st.median(w); r['res']=r['a']/r['s']
for n in range(1,13):
  y=2000+n
  r=[x for x in R if x['year']==y and x['month']==n and x['date_of_month']==n][0]
  print(y,n,n,r['day_of_week'],r['births'],round(r['res'],3))
s=sorted(R,key=lambda r:r['res'])
for r in s[:30]: print('lo',r['year'],r['month'],r['date_of_month'],r['day_of_week'],round(r['res'],3))
for r in s[-25:]: print('hi',r['year'],r['month'],r['date_of_month'],r['day_of_week'],round(r['res'],3))
json.dump([[r['year'],r['month'],r['date_of_month'],r['day_of_week'],r['births'],round(r['res'],4)] for r in R],open('res.json','w'))
