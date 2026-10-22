import sys,pickle
x0,x1,y0,y1=map(int,sys.argv[1:5]);names=sys.argv[5:]
D={n:pickle.load(open('cache_%s.pkl'%n,'rb')) for n in names}
for i in range(len(names)):
  for j in range(i+1,len(names)):
    A=D[names[i]];B=D[names[j]];bpp=A[2]
    c=sum(1 for y in range(y0,y1) for x in range(x0,x1) if A[3][y][x*bpp:x*bpp+3]!=B[3][y][x*bpp:x*bpp+3])
    print(names[i],names[j],c)
