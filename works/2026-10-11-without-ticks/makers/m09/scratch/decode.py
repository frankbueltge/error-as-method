import zlib, struct, sys, json
def readpng(p):
    d=open(p,'rb').read(); i=8; idat=b''
    while i<len(d):
        L,=struct.unpack('>I',d[i:i+4]); t=d[i+4:i+8]; c=d[i+8:i+8+L]; i+=12+L
        if t==b'IHDR': w,h,bd,ct=struct.unpack('>IIBB',c[:10])
        elif t==b'IDAT': idat+=c
    raw=zlib.decompress(idat); bpp=3; stride=w*bpp; out=[]; prev=bytearray(stride); k=0
    for y in range(h):
        f=raw[k]; k+=1; line=bytearray(raw[k:k+stride]); k+=stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+b)&255
            elif f==3: line[x]=(line[x]+(a+b)//2)&255
            elif f==4:
                p_=a+b-c; pa,pb,pc=abs(p_-a),abs(p_-b),abs(p_-c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        out.append(bytes(line)); prev=line
    return w,h,out
w,h,rows=readpng(sys.argv[1])
g=[[ (r[3*x]+r[3*x+1]+r[3*x+2])//3 for x in range(w)] for r in rows]
json.dump({'w':w,'h':h,'g':g},open(sys.argv[2],'w'))
