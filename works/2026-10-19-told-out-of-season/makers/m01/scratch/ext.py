from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m01/work/record.jpg').convert('L'); W,H=im.size; p=im.load()
X0,X1=2.5,297.0
N=1464
def xofh(h): return X0+h*(X1-X0)/(N-1)
# column darkness profiles
cols=[]
for x in range(W):
    cols.append([(y,max(0,200-p[x,y])) for y in range(H) if p[x,y]<200])
def top(x): 
    c=[y for y,w in cols[x] if w>70]; return min(c) if c else None
# phase: for each column, top; find columns where top jumps up a lot vs previous bottom
jumps=[]
for x in range(3,212):
    a=[y for y,w in cols[x-1] if w>70]; b=[y for y,w in cols[x] if w>70]
    if a and b and min(b) < max(a)-12 and min(b)<min(a)-5:
        jumps.append(x)
print(jumps)
# convert jump x to hour mod 24
for x in jumps:
    h=(x-X0)*(N-1)/(X1-X0); print(x, round(h,1), round(h%24,1))
