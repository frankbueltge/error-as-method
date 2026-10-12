import json, collections
pk=json.load(open('/tmp/claude-0/s122/mk/m09/scratch/peaks.json'))
x0=pk[0][0]; x1=pk[-1][0]; s=(x1-x0)/1463
print(x0,x1,s, 24*s)
fr=collections.Counter(round(((p[0]-x0)/s)%1,1) for p in pk); print(sorted(fr.items()))
# per day count and min/max y
for dday in range(61):
  ps=[p for p in pk if dday*24-0.5 <= (p[0]-x0)/s < dday*24+23.5]
  ys=[p[1] for p in ps]
  print(dday,len(ps),round(min(ys)),round(max(ys)))
