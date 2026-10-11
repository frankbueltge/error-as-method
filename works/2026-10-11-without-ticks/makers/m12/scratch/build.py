import csv
rows=list(csv.DictReader(open('/tmp/claude-0/s121/mk/m12/work/births.csv')))
import datetime
d=datetime.date(2000,1,1)
for i,r in enumerate(rows):
  dd=d+datetime.timedelta(i)
  assert (dd.year,dd.month,dd.day)==(int(r['year']),int(r['month']),int(r['date_of_month'])) and dd.isoweekday()==int(r['day_of_week'])
s=','.join(r['births'] for r in rows)
t=open('/tmp/claude-0/s121/mk/m12/scratch/template.html').read().replace('/*DATA*/',s)
open('/tmp/claude-0/s121/mk/m12/work/index.html','w').write(t)
print(len(t))
