from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m17/work/record.jpg').convert('L');W,H=im.size;p=im.load()
bot=[sum(255-p[x,y] for y in (83,84)) for x in range(W)]
# gap (daytime) centers: columns where bot is low between 3..296
low=[x for x in range(3,297) if bot[x]<120]
# group
g=[];cur=[low[0]]
for x in low[1:]:
  if x-cur[-1]<=1: cur.append(x)
  else: g.append(cur);cur=[x]
g.append(cur)
c=[sum(a)/len(a) for a in g]
print(len(c));print([round(v,1) for v in c])
n=len(c);import statistics
# assign day index by rounding difference/4.8
idx=[0];
for i in range(1,n): idx.append(idx[-1]+round((c[i]-c[i-1])/4.8))
mx=statistics.mean(idx);my=statistics.mean(c)
sl=sum((a-mx)*(b-my) for a,b in zip(idx,c))/sum((a-mx)**2 for a in idx)
print('period px',sl,'intercept',my-sl*mx,'last idx',idx[-1])
print('first and last dark cols',[x for x in range(W) if bot[x]>150][:3],[x for x in range(W) if bot[x]>150][-3:])
