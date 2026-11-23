import re,json,sys
CMU={}
def load(p):
    for l in open(p,encoding='utf-8'):
        w,*ph=l.split()
        w=re.sub(r'\(\d+\)$','',w)
        n=sum(1 for x in ph if x[-1].isdigit())
        CMU.setdefault(w,set()).add(n)
def guess(w):
    w=w.lower(); 
    if not w: return 0
    v=re.findall(r'[aeiouy]+',w); n=len(v)
    if w.endswith('e') and not w.endswith(('le','ee','ye')) and n>1: n-=1
    if w.endswith('es') and not w.endswith(('ses','ces','zes','ges','xes','shes','ches')) and n>1: n-=1
    if w.endswith('ed') and not w.endswith(('ted','ded')) and n>1: n-=1
    return max(1,n)
def word(w):
    w=w.lower().strip("'’-")
    if not w: return 0,True
    if w.isdigit(): return len(w),False
    if w in CMU: return min(CMU[w]),True
    w2=w.replace('’',"'")
    if w2 in CMU: return min(CMU[w2]),True
    if '-' in w: 
        s=[word(x) for x in w.split('-')]; return sum(a for a,b in s), all(b for a,b in s)
    return guess(w),False
def line(l):
    ws=re.findall(r"[A-Za-z0-9’'\-]+",l)
    r=[word(w) for w in ws]
    return sum(a for a,b in r), all(b for a,b in r)
def poem(lines):
    c=[line(l) for l in lines]
    return [a for a,b in c], all(b for a,b in c)
