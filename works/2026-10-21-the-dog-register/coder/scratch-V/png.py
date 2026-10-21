import zlib,struct
def load(p):
    b=open(p,'rb').read(); i=8; idat=b''
    while i<len(b):
        L,=struct.unpack('>I',b[i:i+4]); t=b[i+4:i+8]; d=b[i+8:i+8+L]; i+=12+L
        if t==b'IHDR': w,h,bd,ct,_,_,il=struct.unpack('>IIBBBBB',d)
        elif t==b'IDAT': idat+=d
        elif t==b'PLTE': pal=d
    assert bd==8 and il==0, (bd,il)
    bpp={2:3,6:4,0:1,4:2,3:1}[ct]
    raw=zlib.decompress(idat); stride=w*bpp; out=[]; prev=bytearray(stride); p=0
    for y in range(h):
        f=raw[p]; line=bytearray(raw[p+1:p+1+stride]); p+=1+stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; c=prev[x-bpp] if x>=bpp else 0; up=prev[x]
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+up)&255
            elif f==3: line[x]=(line[x]+((a+up)>>1))&255
            elif f==4:
                pp=a+up-c; pa=abs(pp-a); pb=abs(pp-up); pc=abs(pp-c)
                line[x]=(line[x]+(a if pa<=pb and pa<=pc else up if pb<=pc else c))&255
        out.append(bytes(line)); prev=line
    def px(x,y):
        r=out[y]
        if ct==3: k=r[x]; return tuple(pal[3*k:3*k+3])
        return tuple(r[x*bpp:x*bpp+3]) if bpp>=3 else (r[x*bpp],)*3
    return w,h,out,px
