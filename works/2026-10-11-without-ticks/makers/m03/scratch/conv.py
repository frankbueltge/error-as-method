import json, datetime
dots=json.load(open('dots_px.json'))
S=71.66/2000
out=[]
for x,y in dots:
    b=17000-(y-20.0)/S
    yr=2000+(x-80.0)/(1000/15)
    k=int(yr); k=min(max(k,2000),2014)
    frac=yr-k
    start=datetime.date(k,1,1); n=(datetime.date(k+1,1,1)-start).days
    day=start+datetime.timedelta(days=min(n-1,max(0,int(frac*n))))
    out.append((day.isoformat(),round(b)))
out.sort()
json.dump(out,open('days.json','w'))
import collections
h=collections.Counter(v//250*250 for _,v in out)
for k in sorted(h): print(k,h[k],'#'*(h[k]//5))
print(min(out,key=lambda t:t[1]),max(out,key=lambda t:t[1]))
# dots in gap 10000-11000
print([t for t in out if 9900<t[1]<10900])
