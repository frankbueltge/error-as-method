import json,sys,os,hashlib
sys.path.insert(0,sys.argv[2]); import syl
S=sys.argv[1]; syl.load(f'{S}/cmu/cmudict.dict')
D=json.load(open(f'{S}/sheets.json'))
red=D['reddit'][:50]; jou=D['journal'][:50]
def sheet(ps,head):
    out=[head,'']
    for k,p in enumerate(ps,1):
        out.append(f'{k}.'); out+= ['   '+l for l in p['lines']]; out.append('')
    return '\n'.join(out)
os.makedirs(f'{S}/sheetfiles',exist_ok=True)
a=sheet(red,'Fifty haiku posted by people to a public online haiku forum, 10 to 12 October 2026. Line breaks as posted (the forum shows a title line, where many people mark line breaks with "/").')
b=sheet(jou,'Fifty haiku from the web samples of a literary haiku journal, issues of 2025 and 2026. Line breaks and spacing as printed (indentation removed).')
open(f'{S}/sheetfiles/forum.txt','w').write(a); open(f'{S}/sheetfiles/journal.txt','w').write(b)
for n,ps,t in [('forum',red,a),('journal',jou,b)]:
    c=[syl.poem(p['lines'])[0] for p in ps]
    print(n,'575',sum(1 for x in c if x==[5,7,5]),'3line',sum(1 for x in c if len(x)==3),'totals',sorted(sum(x) for x in c),'sha',hashlib.sha256(t.encode()).hexdigest())
