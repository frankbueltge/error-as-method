from PIL import Image
import math
im=Image.open('/tmp/claude-0/s133/mk/m11/work/record.jpg').convert('L');px=im.load()
prof=[max(0,(255-px[x,83])+(255-px[x,84]) - 100) for x in range(300)]
# find runs of dark
runs=[];inr=False
for x in range(300):
  d=min(px[x,83],px[x,84])<150
  if d and not inr: s=x;inr=True
  if not d and inr: runs.append((s,x-1));inr=False
if inr: runs.append((s,299))
print(len(runs))
print([(a,b,b-a+1) for a,b in runs])
# weighted centers
cs=[]
for a,b in runs:
  w=sum(prof[x] for x in range(a,b+1)); cs.append(sum(prof[x]*x for x in range(a,b+1))/w)
import statistics
n=len(cs)
# linear fit
mx=statistics.mean(range(n)); my=statistics.mean(cs)
sl=sum((i-mx)*(c-my) for i,c in enumerate(cs))/sum((i-mx)**2 for i in range(n))
print('slope',sl,'intercept',my-sl*mx)
print([round(c-(my-sl*mx)-sl*i,2) for i,c in enumerate(cs)])
