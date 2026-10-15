import json, math
pts=json.load(open('peaks.json'))
xs=[p[0] for p in pts]; x0,x1=min(xs),max(xs)
t=lambda x:(x-x0)/(x1-x0)*1463
# per hour-of-day bins (3h) : weighted mean value and low quantile
bins=[[] for _ in range(8)]
for x,y,m in pts:
  h=t(x)%24; bins[int(h//3)].append((89-y,m))
for i,b in enumerate(bins):
  b.sort(); tot=sum(m for _,m in b); acc=0; q={}
  for v,m in b:
    acc+=m
    for qq in(.1,.5,.9):
      if qq not in q and acc>=qq*tot: q[qq]=v
  print(f'{i*3:02d}-{i*3+3:02d}h  n={len(b)} mass={tot} q10={q[.1]:.0f} q50={q[.5]:.0f} q90={q[.9]:.0f}')
# per block phase
for b in range(6):
  sel=[p for p in pts if b*1464/6<=t(p[0])<(b+1)*1464/6]
  mv=sum((89-p[1])*p[2] for p in sel)/sum(p[2] for p in sel)
  re=sum(p[2]*((89-p[1])-mv)*math.cos(2*math.pi*t(p[0])/24) for p in sel); im=sum(p[2]*((89-p[1])-mv)*math.sin(2*math.pi*t(p[0])/24) for p in sel)
  print('block',b,'hour of min',round((math.atan2(im,re)/(2*math.pi)*24+12)%24,1))
# daily: per day min value and median
days=[[] for _ in range(61)]
for x,y,m in pts:
  d=min(60,int(t(x)//24)); days[d].append((89-y,m))
out=[]
for d in days:
  d.sort(); tot=sum(m for _,m in d); acc=0; med=None
  for v,m in d:
    acc+=m
    if med is None and acc>=tot/2: med=v
  out.append((d[0][0] if d else None, med, d[-1][0] if d else None, round(tot/320)))
print(out)
