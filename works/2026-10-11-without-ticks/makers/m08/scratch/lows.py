import csv,datetime
R=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(open('/tmp/claude-0/s121/mk/m08/work/births.csv'))]
w=[r for r in R if r['day_of_week']<=5 and r['births']<10000]
for r in w: print(r)
print(len(w))
print(min(r['births'] for r in R if r['day_of_week']>5), max(r['births'] for r in R if r['day_of_week']>5))
