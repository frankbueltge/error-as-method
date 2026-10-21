import zlib,struct,sys,glob
def load(fn):
    d=open(fn,'rb').read(); i=8; idat=b''
    while i<len(d):
        l,=struct.unpack('>I',d[i:i+4]); t=d[i+4:i+8]; c=d[i+8:i+8+l]
        if t==b'IHDR': w,h,bd,ct=struct.unpack('>IIBB',c[:10])
        if t==b'IDAT': idat+=c
        i+=12+l
    raw=zlib.decompress(idat); bpp={2:3,6:4,0:1,4:2}[ct]; st=w*bpp
    out=[];prev=bytearray(st);p=0
    for y in range(h):
        f=raw[p];p+=1;line=bytearray(raw[p:p+st]);p+=st
        for x in range(st):
            a=line[x-bpp] if x>=bpp else 0;b=prev[x];c=prev[x-bpp] if x>=bpp else 0
            if f==1:line[x]=(line[x]+a)&255
            elif f==2:line[x]=(line[x]+b)&255
            elif f==3:line[x]=(line[x]+(a+b)//2)&255
            elif f==4:
                pp=a+b-c;pa=abs(pp-a);pb=abs(pp-b);pc=abs(pp-c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        out.append(bytes(line));prev=line
    return w,h,bpp,out
base=load(sys.argv[1])
for f in sys.argv[2:]:
    o=load(f)
    if o[:2]!=base[:2]: print(f,'size',o[:2]);continue
    w,h,bpp=base[0],base[1],base[2]
    ys=[y for y in range(h) if base[3][y]!=o[3][y]]
    if not ys: print(f,'identical');continue
    xs=[x//bpp for y in ys for x in range(w*bpp) if base[3][y][x]!=o[3][y][x]]
    print(f,'rows',min(ys),max(ys),len(ys),'cols',min(xs),max(xs),len(xs))
