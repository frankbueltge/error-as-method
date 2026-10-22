import sys,pickle
sys.path.insert(0,'.')
# usage: crop.py out.png scale x0 y0 x1 y1 T07 T18 ...  (stacks vertically)
out=sys.argv[1];s=int(sys.argv[2]);x0,y0,x1,y1=map(int,sys.argv[3:7]);names=sys.argv[7:]
import png
rows=[]
for n in names:
  W,H,bpp,R=pickle.load(open('cache_%s.pkl'%n,'rb'))
  for y in range(y0,y1):
    line=bytearray()
    for x in range(x0,x1):
      line+=R[y][x*bpp:x*bpp+3]*s
    for _ in range(s): rows.append(line)
  for _ in range(4): rows.append(bytearray([255,0,255])*((x1-x0)*s))
png.write(out,(x1-x0)*s,len(rows),rows)
