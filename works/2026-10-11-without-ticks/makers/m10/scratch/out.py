import datetime as dt
W,H=480,220
d=open('births.raw','rb').read()
x0,x1=5.5,473.5
start=dt.date(2000,1,1)
def date(x): return start+dt.timedelta(days=round((x-x0)/(x1-x0)*5478))
for y in range(25,45):
  for x in range(W):
    v=d[y*W+x]
    if v<190: print(y,x,v,date(x))
