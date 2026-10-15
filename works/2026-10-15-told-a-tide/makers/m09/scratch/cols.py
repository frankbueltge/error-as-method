import sys
d=open(sys.argv[1],'rb').read()
parts=d.split(b'\n',3); w,h=map(int,parts[1].split()); px=parts[3]
g=lambda x,y: px[y*w+x]
out=[]
for x in range(w):
    ink=[(255-g(x,y)) for y in range(h)]
    ys=[y for y in range(h) if ink[y]>90]
    tot=sum(i for i in ink if i>40)
    out.append((x,min(ys) if ys else -1,max(ys) if ys else -1,len(ys),tot))
for o in out: print(*o)
