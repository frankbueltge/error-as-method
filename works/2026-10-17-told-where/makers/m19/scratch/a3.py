from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m19/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
b=4.825; a=4.0
# linear fit of block centers
import statistics
cs=[4.0,8.5,13.5,18,23,28,33,38,42,47,52,57,62,67,71,76,81,86,91,95.5,100,105,110,115,119,124,129,134,139,144,148.5,153,158,163,168,173,177,182,187,192,197,202,206,211,216,221,226,230.5,235,240,245,250,254.5,259.5,264,269,274,279,283.5,288,293.5]
n=len(cs); k=list(range(n)); mk=sum(k)/n; mc=sum(cs)/n
b=sum((ki-mk)*(c-mc) for ki,c in zip(k,cs))/sum((ki-mk)**2 for ki in k); a=mc-b*mk
print('fit a=%.3f b=%.4f'%(a,b))
# leftmost / rightmost ink centroid
def colink(x): return sum(255-p[x,y] for y in range(H))
print([colink(x) for x in range(0,6)],[colink(x) for x in range(292,300)])
# daily top: for each day between night k and k+1, min y with p<150
for d in range(n-1):
  x1=int(cs[d])+1; x2=int(cs[d+1])
  ys=[y for x in range(x1,x2+1) for y in range(0,82) if p[x,y]<150]
  ink=sum(max(0,230-p[x,y])*(83.5-y) for x in range(x1,x2+1) for y in range(0,81))
  print(d, min(ys) if ys else None, round(ink/1000,1))
