import sys,pickle,csv
sys.path.insert(0,'.')
import png
# overlay.py name out scale x0 y0 x1 y1 lat0 y0px pxdeg_y lon0 x0px pxdeg_x
n,out=sys.argv[1],sys.argv[2];s=int(sys.argv[3]);X0,Y0,X1,Y1=map(int,sys.argv[4:8])
la0,ly,ky,lo0,lx,kx=map(float,sys.argv[8:14])
def dms(t):
  return int(t[:-6])+int(t[-6:-4])/60+int(t[-4:])/360000
r=list(csv.DictReader(open('data/bridges.csv')))
W,H,bpp,R=pickle.load(open('cache_%s.pkl'%n,'rb'))
img=[bytearray(b''.join(R[y][x*bpp:x*bpp+3] for x in range(W))) for y in range(H)]
for b in r:
  y=round(ly+(la0-dms(b['LAT_016']))*ky); x=round(lx-(dms(b['LONG_017'])-lo0)*kx)
  if 0<=y<H and 0<=x<W: img[y][x*3:x*3+3]=bytes([255,0,255])
rows=[]
for y in range(Y0,Y1):
  l=bytearray()
  for x in range(X0,X1): l+=img[y][x*3:x*3+3]*s
  for _ in range(s): rows.append(l)
png.write(out,(X1-X0)*s,len(rows),rows)
