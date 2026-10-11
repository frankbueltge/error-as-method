import csv,collections,statistics as st,datetime
r=list(csv.DictReader(open('../work/births.csv')))
for x in r:
  for k in x: x[k]=int(x[k])
# dow factor per year
ym=collections.defaultdict(list)
for x in r: ym[(x['year'],x['month'])].append(x['births'])
ymm={k:st.mean(v) for k,v in ym.items()}
dw=collections.defaultdict(list)
for x in r: dw[(x['year'],x['day_of_week'])].append(x['births']/ymm[(x['year'],x['month'])])
dwf={k:st.median(v) for k,v in dw.items()}
for x in r: x['res']=x['births']/(ymm[(x['year'],x['month'])]*dwf[(x['year'],x['day_of_week'])])
md=collections.defaultdict(list)
for x in r: md[(x['month'],x['date_of_month'])].append(x['res'])
m=sorted((round(st.mean(v),3),k) for k,v in md.items())
print(m[:30]);print(m[-15:])
dom=collections.defaultdict(list)
for x in r: dom[x['date_of_month']].append(x['res'])
print({k:round(st.mean(v),3) for k,v in dom.items()})
f13=[x['res'] for x in r if x['date_of_month']==13 and x['day_of_week']==5]
print('fri13',st.mean(f13),len(f13))
for d in [(2012,12,12),(2011,11,11),(2010,10,10),(2009,9,9),(2008,8,8),(2007,7,7),(2006,6,6),(2005,5,5),(2001,1,1)]:
  print(d,[round(x['res'],3) for x in r if (x['year'],x['month'],x['date_of_month'])==d])
print(sorted((round(x['res'],3),x['year'],x['month'],x['date_of_month'],x['day_of_week']) for x in r)[-15:])
print({k:round(v,3) for k,v in sorted(dwf.items()) if k[0] in (2000,2014)})
