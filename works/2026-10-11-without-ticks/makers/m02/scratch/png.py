import re,zlib,struct
h=open('../work/index.html').read()
W,H=1100,800
img=[[(246,243,238)]*W for _ in range(H)]
for m in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" fill="#(\w{6})"',h):
  x,y,w,hh=map(float,m.groups()[:4]);c=tuple(int(m.group(5)[i:i+2],16) for i in (0,2,4))
  for yy in range(int(y),int(y+hh)):
    for xx in range(int(x),int(x+w)):
      if 0<=xx<W and 0<=yy<H: img[yy][xx]=c
raw=b''.join(b'\0'+bytes(v for p in row for v in p) for row in img)
def ch(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
open('grid.png','wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b''))
