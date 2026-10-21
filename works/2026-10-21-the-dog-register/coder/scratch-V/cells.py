import sys; sys.path.insert(0,'/tmp/claude-0/s146root/packets/V/scratch'); from png import load
from collections import Counter
def cells(path,x0=54,y0=92,p=8,ncol=128,n=10106):
    w,h,rows,px=load(path); out=[]
    for i in range(n):
        r,c=divmod(i,ncol); x=x0+p*c; y=y0+p*r
        sig=tuple(px(x+dx,y+dy) for dy in range(1,6) for dx in range(1,6))
        out.append(sig)
    return out
