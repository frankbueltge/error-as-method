import sys,json,re,statistics,hashlib
sys.path.insert(0,sys.argv[2]); import syl
S=sys.argv[1]; syl.load(f'{S}/cmu/cmudict.dict')
raw=open(f'{S}/dl/pp.json','rb').read()
d=json.loads(raw)['data']
red=[]
for p in d:
    t=p['title']
    if t.count('/')>=2: lines=[x.strip() for x in t.split('/') if x.strip()]
    else:
        st=[x.strip() for x in (p.get('selftext') or '').split('\n') if x.strip()]
        lines=st if len(st)==3 else [x.strip() for x in t.split('/') if x.strip()]
    red.append({'id':p['id'],'created_utc':p['created_utc'],'lines':lines})
J=json.load(open(f'{S}/journal_parsed.json'))
jour=[dict(issue=x['issue'],**p) for x in J for p in x['poems']]
def stat(name,ps):
    tot=[];k575=0;three=0;exact=0
    for p in ps:
        c,ok=syl.poem(p['lines']); p['counts']=c; p['dict_ok']=ok
        tot.append(sum(c)); 
        if len(c)==3: three+=1
        if c==[5,7,5]: k575+=1
        if ok: exact+=1
    print(name,len(ps),'3-line',three,'5-7-5',k575,'median total',statistics.median(tot),'all-words-in-dict',exact)
stat('reddit',red); stat('journal',jour)
json.dump({'reddit':red,'journal':jour,'reddit_sha256':hashlib.sha256(raw).hexdigest(),'reddit_bytes':len(raw)},open(f'{S}/sheets.json','w'),ensure_ascii=False,indent=0)
