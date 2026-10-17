import json, sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); px=im.load(); W,H=im.size
# floor-gap centres: columns where rows 83-84 are light
g=[x for x in range(W) if (255-px[x,83])+(255-px[x,84])<120]
runs=[];cur=[g[0]]
for x in g[1:]:
  if x==cur[-1]+1: cur.append(x)
  else: runs.append(cur);cur=[x]
runs.append(cur)
cs=[sum(r)/len(r) for r in runs]
print(len(cs)); print([round(c,1) for c in cs])
# linear fit of gap centres vs index (inner runs)
inner=[c for c in cs if 2<c<297]
n=len(inner); xs=list(range(n))
mx=sum(xs)/n; my=sum(inner)/n
b=sum((i-mx)*(c-my) for i,c in zip(xs,inner))/sum((i-mx)**2 for i in xs)
a=my-b*mx
print('period px',b,'first gap',a, 'resid', [round(c-(a+b*i),2) for i,c in enumerate(inner)])
