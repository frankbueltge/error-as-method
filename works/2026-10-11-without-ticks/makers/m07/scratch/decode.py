import zlib,struct,json,sys
d=open('/tmp/claude-0/s121/mk/m07/work/births.png','rb').read()
i=8;idat=b''
while i<len(d):
    l=struct.unpack('>I',d[i:i+4])[0];t=d[i+4:i+8]
    if t==b'IHDR': W,H=struct.unpack('>II',d[i+8:i+16])
    if t==b'IDAT': idat+=d[i+8:i+8+l]
    i+=12+l
raw=zlib.decompress(idat);bpp=3;stride=W*bpp
rows=[];prev=bytearray(stride);p=0
for y in range(H):
    f=raw[p];p+=1;line=bytearray(raw[p:p+stride]);p+=stride
    for x in range(stride):
        a=line[x-bpp] if x>=bpp else 0;b=prev[x];c=prev[x-bpp] if x>=bpp else 0
        if f==1: line[x]=(line[x]+a)&255
        elif f==2: line[x]=(line[x]+b)&255
        elif f==3: line[x]=(line[x]+(a+b)//2)&255
        elif f==4:
            pa=abs(b-c);pb=abs(a-c);pc=abs(a+b-2*c)
            pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
            line[x]=(line[x]+pr)&255
    rows.append(line);prev=line
g=[[ (r[3*x]+r[3*x+1]+r[3*x+2])//3 for x in range(W)] for r in rows]
cols=set()
for r in rows:
    for x in range(W): cols.add((r[3*x],r[3*x+1],r[3*x+2]))
print(W,H,len(cols))
json.dump(g,open('/tmp/claude-0/s121/mk/m07/scratch/gray.json','w'))
