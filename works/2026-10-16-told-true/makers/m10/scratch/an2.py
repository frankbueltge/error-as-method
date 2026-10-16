exec(open('an.py').read().split('# periodogram')[0].replace("print(","(lambda *a,**k:None)("))
import math
x0,x1=0,297  # ink extent
n=298; z=my[:n]; m=sum(z)/n; z=[v-m for v in z]
hp=1464/ n  # hours per px approx
def pw(f):
    c=sum(z[i]*math.cos(2*math.pi*f*i) for i in range(n)); s=sum(z[i]*math.sin(2*math.pi*f*i) for i in range(n)); return (c*c+s*s)/n
for lo,hi in [(0.17,0.23),(0.36,0.45)]:
    best=sorted(((pw(lo+(hi-lo)*j/600),lo+(hi-lo)*j/600) for j in range(601)),reverse=True)[:3]
    for p_,f in best: print('f=%.4f /px period=%.3f px = %.2f h  (cycles over record %.2f) pow %.0f'%(f,1/f,hp/f,f*n,p_))
# complex demodulation at diurnal freq, window 25 px
f=sorted(((pw(0.17+0.06*j/600),0.17+0.06*j/600) for j in range(601)),reverse=True)[0][1]
amps=[]
for c0 in range(0,n-25,5):
    c=sum(z[i]*math.cos(2*math.pi*f*i) for i in range(c0,c0+25)); s=sum(z[i]*math.sin(2*math.pi*f*i) for i in range(c0,c0+25))
    amps.append((c0, 2*math.hypot(c,s)/25, math.degrees(math.atan2(s,c))))
for a in amps: print('col %3d day %5.1f amp %.1f px phase %.0f'%(a[0],(a[0]+12)*hp/24,a[1],a[2]))
