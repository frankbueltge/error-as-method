import json,math
exec(open('fit.py').read().split('M=[[0.0]')[0].replace("float(sys.argv[1]) if len(sys.argv)>1 else 2.25","2.36").replace("float(sys.argv[2]) if len(sys.argv)>2 else 296.8","296.48"))
ys=json.load(open('fit_2.36_296.48_5.0.json'))['ys']
M=[[0.0]*W for _ in range(H)]
for i in range(N):
  for (p,q),c in K(xs[i],ys[i]).items():
    if 0<=p<W and 0<=q<H: M[q][p]+=c
pos=neg=tot=0
miss=[]
for q in range(78):
  for p in range(W):
    r=D[q][p]-min(255,M[q][p]); tot+=D[q][p]
    if r>0: pos+=r
    else: neg-=r
    if r>90: miss.append((p,q,r))
print('tot',tot,'unexplained',pos,'overdrawn',neg)
print(len(miss),miss[:40])
