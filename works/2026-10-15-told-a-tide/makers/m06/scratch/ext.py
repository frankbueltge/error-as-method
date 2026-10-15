from PIL import Image
import math,json
g=Image.open('/tmp/claude-0/s128/mk/m06/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
cols=[sum(255-p[x,y] for y in range(H)) for x in range(W)]
rows=[sum(255-p[x,y] for x in range(W)) for y in range(H)]
print('cols',cols[:6],cols[-6:]); print('rows', rows[:6], rows[-6:])
c=json.load(open('peaks.json'))['colmean']
k=7; r=[c[i]-sum(c[max(0,i-k):i+k+1])/len(c[max(0,i-k):i+k+1]) for i in range(W)]
best=[]
for i in range(4600,5100,5):
  P=i/1000; f=2*math.pi/P
  a=sum(r[j]*math.cos(f*j) for j in range(W)); b=sum(r[j]*math.sin(f*j) for j in range(W)); best.append((round(math.hypot(a,b)),P))
print(sorted(best)[-5:])
print('col darkness min/median', min(cols), sorted(cols)[150], max(cols))
