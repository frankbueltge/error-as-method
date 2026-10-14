import json
d=json.load(open('cols.json')); cols=d['cols']; mean=d['mean']
P=295/61.0
x0=3
# running mean baseline per column over one period
def base(x):
    vs=[mean[i] for i in range(max(3,x-2),min(298,x+3)) if mean[i] is not None]; return sum(vs)/len(vs)
for P in [295/61.0, 295/60.0, 295/59.0, 295/57.0, 295/62.0]:
  B=10; acc=[0]*B; wts=[0]*B
  for x in range(3,298):
    b=base(x)
    for y,wt in cols[x]:
        ph=((x-x0)/P)%1; k=int(ph*B); acc[k]+=(y-b)*wt; wts[k]+=wt
  prof=[acc[k]/max(wts[k],1e-9) for k in range(B)]
  print(round(P,3), ' '.join(f'{v:6.1f}' for v in prof), 'amp',round(max(prof)-min(prof),1))
