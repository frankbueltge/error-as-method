import json, zlib, struct
L=json.load(open('layout.json'))
W,H,S=1100,800,2
img=[[ (243,239,230) for _ in range(W*S)] for _ in range(H*S)]
def hexc(c): c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
for r in L['rects']:
    c=hexc(r['c'])
    for y in range(int(r['y']*S),int((r['y']+r['h'])*S)):
        for x in range(int(r['x']*S),int((r['x']+r['w'])*S)): img[y][x]=c
for l in L['lines']:
    c=hexc(l['c']); n=int(max(abs(l['x2']-l['x1']),abs(l['y2']-l['y1']))*S)+1
    for i in range(n+1):
        x=l['x1']+(l['x2']-l['x1'])*i/max(n,1); y=l['y1']+(l['y2']-l['y1'])*i/max(n,1)
        if 0<=int(y*S)<H*S and 0<=int(x*S)<W*S: img[int(y*S)][int(x*S)]=c
for d in L['dots']:
    c=hexc(d['c']); r=d['r']*S; cx=d['x']*S; cy=d['y']*S
    for y in range(int(cy-r),int(cy+r)+1):
        for x in range(int(cx-r),int(cx+r)+1):
            if (x+.5-cx)**2+(y+.5-cy)**2<=r*r and 0<=y<H*S and 0<=x<W*S: img[y][x]=c
for t in L['texts']:
    # approximate text as a box
    size=float([p for p in t['f'].split() if p.endswith('px')][0][:-2]); w=len(t['t'])*size*0.5
    x=t['x']+t.get('dx',0); x0={'left':x,'right':x-w,'center':x-w/2}[t['a']]
    for y in range(int((t['y']-size*0.7)*S),int(t['y']*S)):
        for xx in range(int(x0*S),int((x0+w)*S)):
            if 0<=xx<W*S and 0<=y<H*S and (y+xx)%3==0: img[y][xx]=(120,120,200)
raw=b''.join(b'\x00'+bytes([v for p in row for v in p]) for row in img)
def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
open('preview.png','wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W*S,H*S,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,6))+chunk(b'IEND',b''))
print('ok',len(L['dots']))
