import zlib,struct
def read(fn):
  b=open(fn,'rb').read(); i=8; idat=b''
  while i<len(b):
    n=struct.unpack('>I',b[i:i+4])[0]; t=b[i+4:i+8]; d=b[i+8:i+8+n]; i+=12+n
    if t==b'IHDR': W,H,bd,ct=struct.unpack('>IIBB',d[:10])
    elif t==b'IDAT': idat+=d
  raw=zlib.decompress(idat); bpp={2:3,6:4,0:1,4:2}[ct]; st=W*bpp
  rows=[];prev=bytearray(st);p=0
  for y in range(H):
    f=raw[p];p+=1;line=bytearray(raw[p:p+st]);p+=st
    for x in range(st):
      a=line[x-bpp] if x>=bpp else 0;bb=prev[x];c=prev[x-bpp] if x>=bpp else 0
      if f==1: line[x]=(line[x]+a)&255
      elif f==2: line[x]=(line[x]+bb)&255
      elif f==3: line[x]=(line[x]+(a+bb)//2)&255
      elif f==4:
        pp=a+bb-c;pa=abs(pp-a);pb=abs(pp-bb);pc=abs(pp-c)
        pr=a if pa<=pb and pa<=pc else (bb if pb<=pc else c)
        line[x]=(line[x]+pr)&255
    rows.append(bytes(line));prev=line
  return W,H,bpp,rows
def write(fn,W,H,px):
  raw=b''.join(b'\x00'+bytes(r) for r in px)
  def ch(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
  open(fn,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b''))
