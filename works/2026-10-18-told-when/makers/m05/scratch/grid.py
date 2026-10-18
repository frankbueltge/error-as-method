from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s135/mk/m05/work/record.jpg').convert('L')
W,H=im.size
centers=[5.5,10,14.5,19.2,23.8,28.4,33,37.5,42.4,46.8,51.5,56,60.6,65.4,69.6,74.5,78.9,83.5]
# fit linear
n=len(centers); mx=(n-1)/2; my=sum(centers)/n
b=sum((i-mx)*(c-my) for i,c in enumerate(centers))/sum((i-mx)**2 for i in range(n)); a=my-b*mx
print('spacing',b,'offset',a)
grid=[]
for L in range(n):
    yc=a+b*L
    ys=[y for y in range(H) if abs(y-yc)<=1.6]
    row=[max(255-im.getpixel((x,y)) for y in ys) for x in range(W)]
    grid.append(row)
for L in range(n):
    print('%2d '%L+''.join('#' if v>140 else ('+' if v>70 else '.') for v in grid[L]))
json.dump(grid,open('grid.json','w'))
# per column mean level
mean=[]
for x in range(W):
    w=[max(0,grid[L][x]-60) for L in range(n)]
    s=sum(w); mean.append(sum(L*w[L] for L in range(n))/s if s else None)
json.dump(mean,open('mean.json','w'))
# periodogram of detrended mean
xs=[x for x in range(W) if mean[x] is not None]
# detrend with running mean of 15
def rm(x):
    v=[mean[k] for k in range(max(0,x-7),min(W,x+8)) if mean[k] is not None]; return sum(v)/len(v)
r=[(x,mean[x]-rm(x)) for x in xs]
for P in [3,3.5,4,4.5,4.75,4.92,5.1,5.5,6,7,8,9.84,12]:
    c=sum(v*math.cos(2*math.pi*x/P) for x,v in r); s=sum(v*math.sin(2*math.pi*x/P) for x,v in r)
    print(P, round(math.hypot(c,s),1), round(math.degrees(math.atan2(s,c))))
