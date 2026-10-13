import json
cols=json.load(open('cols.json'))
xs=[i for i,c in enumerate(cols) if c[0]>0]
print('x extent',xs[0],xs[-1])
N=1464
x0,x1=xs[0],xs[-1]
# value per column, larger=higher -> v = 90-y
pts=[(x,90-c[1]) for x,c in enumerate(cols) if c[1] is not None]
def idx(x): return (x-x0+0.5)/(x1-x0+1)*N  # approx hour index at column centre
# daily fold in 24 bins of ~6h coarse: use 8 bins of 3h
for P,B,name in ((24,8,'day'),(168,14,'week')):
  acc=[[0,0] for _ in range(B)]
  for x,v in pts:
    i=idx(x); b=int((i%P)/P*B)
    acc[b][0]+=v; acc[b][1]+=1
  print(name,[round(a/n,1) for a,n in acc])
# per-day mean
days=[[0,0] for _ in range(61)]
for x,v in pts:
  d=int(idx(x)//24); days[min(d,60)][0]+=v; days[min(d,60)][1]+=1
dm=[round(a/n,1) for a,n in days]
for w in range(9): print(w, dm[w*7:w*7+7])
