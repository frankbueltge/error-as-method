import sys
d=open(sys.argv[1],'rb').read(); W,H=300,90
for y in range(H):
    print('%2d '%y+''.join('#' if d[y*W+x]<100 else ('+' if d[y*W+x]<180 else '.') for x in range(W)))
