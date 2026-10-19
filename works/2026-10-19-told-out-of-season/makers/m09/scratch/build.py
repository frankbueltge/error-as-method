import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
X0,X1=2.0,297.0; pph=(X1-X0)/1463  # px per hour
SHIFT=3  # cells start 3h before recorder's midnight, so each daily rise sits at the left of its cell
L,R=70,1030; cell=(R-L)/61; inner=cell*0.58
Y0,Y1=4,86; T,B=130,650
dots=[]; n=0
for x in range(W):
    for y in range(H):
        v=px[x,y]
        if v>=165: continue
        h=(x-X0)/pph + SHIFT
        k=int(h//24); 
        if k<0: k=0
        if k>60: k=60
        ph=(h-24*k)/24
        cx=L+k*cell+ph*inner
        cy=T+(y-Y0)/(Y1-Y0)*(B-T)
        a=min(1,(165-v)/120)
        dots.append((round(cx,1),round(cy,1),round(a,2)))
print(len(dots),file=sys.stderr)
data=",".join(f"{a},{b},{c}" for a,b,c in dots)
open(sys.argv[2],'w').write(data)
