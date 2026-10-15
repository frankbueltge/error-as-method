import json,math
d=json.load(open('cols.json'));cols=d['cols'];W=d['W'];H=d['H']
# dark-weighted pixels: find x range used
used=[x for x in range(W) if cols[x]]
print('x range',used[0],used[-1])
top=[];bot=[];med=[];cnt=[]
for x in range(W):
    ys=sorted(y for y,w in cols[x])
    if not ys: top.append(None);bot.append(None);med.append(None);cnt.append(0);continue
    top.append(ys[0]);bot.append(ys[-1]);med.append(ys[len(ys)//2]);cnt.append(len(ys))
# spread = bot - median: low tail depth
spread=[(b-m) if b is not None else 0 for b,m in zip(bot,med)]
x0,x1=used[0],used[-1]
ppd=(x1-x0+1)/61
print('px per day',ppd)
def acf(s,lag):
    n=len(s);m=sum(s)/n
    v=sum((a-m)**2 for a in s)
    return sum((s[i]-m)*(s[i+lag]-m) for i in range(n-lag))/v
s=spread[x0:x1+1]
print('acf spread',[round(acf(s,l),2) for l in range(1,16)])
md=[m for m in med[x0:x1+1]]
# periodogram of spread at periods 2..30 px
for name,ser in [('spread',s),('count',cnt[x0:x1+1]),('bot',[b or 0 for b in bot[x0:x1+1]])]:
  n=len(ser);m=sum(ser)/n
  res=[]
  for P10 in range(25,300):
    P=P10/10;w=2*math.pi/P
    c=sum((ser[i]-m)*math.cos(w*i) for i in range(n));sn=sum((ser[i]-m)*math.sin(w*i) for i in range(n))
    res.append((c*c+sn*sn,P))
  res.sort(reverse=True);print(name,[ (round(p,1),round(a)) for a,p in res[:8]])
print('med',med[x0:x1+1])
print('bot',bot[x0:x1+1])
