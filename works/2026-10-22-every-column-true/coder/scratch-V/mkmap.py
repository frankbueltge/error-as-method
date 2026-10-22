import csv,zlib,struct,sys
r=list(csv.DictReader(open(sys.argv[1])))
def dms(s):
  d=int(s[:-6]);m=int(s[-6:-4]);sec=int(s[-4:])/100
  return d+m/60+sec/3600
W,H=300,700
px=[[(255,255,255)]*W for _ in range(H)]
pts=[(dms(x['LAT_016']),dms(x['LONG_017']),x) for x in r]
la=[p[0] for p in pts];lo=[p[1] for p in pts]
print(min(la),max(la),min(lo),max(lo))
for a,o,x in pts:
  X=int(10+(max(lo)-o)/(max(lo)-min(lo))*(W-20)); Y=int(10+(max(la)-a)/(max(la)-min(la))*(H-20))
  c={'1':(0,150,0),'3':(0,0,255),'5':(255,0,0)}[x['COUNTY_CODE_003']]
  for dx in (-1,0,1):
    for dy in (-1,0,1): px[Y+dy][X+dx]=c
raw=b''.join(b'\x00'+bytes(v for p in row for v in p) for row in px)
def ch(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
open(sys.argv[2],'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b''))
