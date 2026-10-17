from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=lambda x,y:max(0,255-px[x,y]-20)
# daylight weight: ink above row 80 weighted by height
w=[sum(ink(x,y)*(83.5-y) for y in range(0,81)) for x in range(W)]
# cluster: find minima-separated groups using threshold
th=max(w)*0.08
groups=[];cur=[]
for x in range(W):
    if w[x]>th: cur.append(x)
    elif cur: groups.append(cur);cur=[]
if cur: groups.append(cur)
cs=[sum(x*w[x] for x in g)/sum(w[x] for x in g) for g in groups]
print(len(groups))
print([round(c,2) for c in cs])
import statistics
d=[b-a for a,b in zip(cs,cs[1:])]
print([round(v,2) for v in d])
n=len(cs); xs=list(range(n))
mx=sum(xs)/n; my=sum(cs)/n
sl=sum((a-mx)*(b-my) for a,b in zip(xs,cs))/sum((a-mx)**2 for a in xs)
print('slope px/day',sl,'intercept',my-sl*mx)
print('residuals',[round(c-(my-sl*mx+sl*i),2) for i,c in enumerate(cs)])
