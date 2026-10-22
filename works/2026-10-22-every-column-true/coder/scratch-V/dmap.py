import sys,pickle
sys.path.insert(0,'.')
import png
a,b=sys.argv[1],sys.argv[2]
A=pickle.load(open('cache_%s.pkl'%a,'rb'));B=pickle.load(open('cache_%s.pkl'%b,'rb'))
W,H,bpp=A[0],A[1],A[2]
rows=[]
for y in range(H):
  l=bytearray()
  for x in range(W):
    p=A[3][y][x*bpp:x*bpp+3];q=B[3][y][x*bpp:x*bpp+3]
    if p==q: l+=bytes([255,255,255]) if sum(p)>600 else bytes([200,200,200])
    else: l+=bytes([255,0,0]) if sum(p)<sum(q) else bytes([0,0,255])
  rows.append(l)
png.write(sys.argv[3],W,H,rows)
