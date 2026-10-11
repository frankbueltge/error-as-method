import pickle, math
W=1100; R=6; A1=5.2624
C,comps=pickle.load(open('cc.pkl','rb'))
# integral image for fast window sums
X0,X1,Y0,Y1=81,1080,10,449
I=[[0.0]*(X1-X0+1) for _ in range(Y1-Y0+1)]
for y in range(Y0,Y1):
    row=0.0
    for x in range(X0,X1):
        row+=C[y*W+x]; I[y-Y0+1][x-X0+1]=I[y-Y0][x-X0+1]+row
def win(x,y):
    a,b=max(X0,x-R)-X0,min(X1,x+R+1)-X0; c,d=max(Y0,y-R)-Y0,min(Y1,y+R+1)-Y0
    return (I[d][b]-I[c][b]-I[d][a]+I[c][a])/((b-a)*(d-c))
masses=[]
for p in comps:
    m=0
    for j in p:
        cb=min(0.97,win(j%W,j//W)); f=-math.log(1-cb)/cb if cb>1e-6 else 1
        m+=C[j]*f/A1
    masses.append(m)
pickle.dump(masses,open('mass.pkl','wb')); print(sum(masses))
