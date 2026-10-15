import sys,math
d=open(sys.argv[1],'rb').read()
parts=d.split(b'\n',3); w,h=map(int,parts[1].split()); px=parts[3]
g=lambda x,y: px[y*w+x]
# point cloud: every pixel ink as weight
pts=[]
for x in range(1,w-1):
    for y in range(h):
        i=255-g(x,y)-40
        if i>0: pts.append(((x+0.5)*1464/300, h-y, i))
W=sum(p[2] for p in pts); mu=sum(p[1]*p[2] for p in pts)/W
def power(P):
    c=sum((p[1]-mu)*p[2]*math.cos(2*math.pi*p[0]/P) for p in pts); s=sum((p[1]-mu)*p[2]*math.sin(2*math.pi*p[0]/P) for p in pts)
    return (c*c+s*s)/W/W, math.degrees(math.atan2(s,c))
for P in [22,23,23.5,23.6,23.7,23.8,23.93,24.0,24.1,24.2,24.5,24.84,25.82,12.0,12.42,12.66,11.97,8.0,6.21,6.0]:
    pw,ph=power(P); print(P, "%.4f"%pw, "%.0f"%ph)
best=max(((power(P/100)[0],P/100) for P in range(2200,2600,2)))
print("best",best)
