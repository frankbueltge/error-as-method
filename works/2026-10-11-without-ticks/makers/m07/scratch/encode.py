import json
d=json.load(open('ink.json'));cols=d['cols']
A='abcdefghijklmnopqrstuvwxyz'
out=[]
for c in cols:
    s='';z=0
    q=[min(25,round(v*25)) if v>0.03 else 0 for v in c]
    i=0
    while i<len(q):
        if q[i]==0:
            j=i
            while j<len(q) and q[j]==0: j+=1
            n=j-i
            s+= (str(n) if n>1 else '')+'a'; i=j
        else:
            s+=A[q[i]]; i+=1
    out.append(s)
enc='|'.join(out)
open('ink.enc','w').write(enc)
print(len(enc), d['dot']*25)
