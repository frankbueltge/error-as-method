"""Hand verdicts on sample.json (P5), typed in by the reader of the sixty comments, Session 104.
Columns: bare, error, located, other (a third party named as having noticed), admin.
Read by meaning, not by word: 'located' = names the specific place or item the error sits in
(equation, lemma, section, the proof of the main result, a named computation)."""
import json
Y, N = 1, 0
V = {  # n: (bare, error, located, other, admin, note)
 1:(Y,N,N,N,N,""), 2:(N,N,N,N,N,"views changed"), 3:(Y,N,N,N,N,""), 4:(Y,N,N,N,N,""),
 5:(N,N,N,N,Y,"text reuse"), 6:(Y,N,N,N,N,"page count only"), 7:(N,N,N,N,N,"merged"),
 8:(Y,N,N,N,N,""), 9:(Y,N,N,N,N,""),
 10:(N,Y,N,N,N,"not a withdrawal of this paper: claims withdrawn in internal review"),
 11:(Y,N,N,N,N,""), 12:(Y,N,N,N,N,"date only"), 13:(Y,N,N,N,N,"version history only"),
 14:(N,N,N,N,N,"no longer wishes"), 15:(N,N,N,N,N,"'various reasons': a reason that says nothing"),
 16:(Y,N,N,N,N,""), 17:(N,Y,N,N,N,"'corrected version' implies an error, names none"),
 18:(N,N,N,N,N,"not up to date"), 19:(N,Y,Y,N,N,"located by its object, 'non-vanishing mod p'"),
 20:(N,N,N,N,N,"permissions/ethics"), 21:(N,N,N,N,N,""), 22:(N,N,N,N,N,"published elsewhere"),
 23:(N,N,N,N,N,"'academic reasons'"), 24:(N,Y,Y,N,N,"Section 2"), 25:(Y,N,N,N,N,""),
 26:(N,N,N,N,N,"journal policy"), 27:(N,N,N,N,N,"newer version"), 28:(N,N,N,N,Y,"authorship dispute"),
 29:(N,Y,Y,N,N,"proof of the main result"), 30:(N,N,N,N,N,"incomplete, not wrong"),
 31:(N,Y,N,N,N,"notation, 'the algorithm': not a place"), 32:(N,N,N,N,N,"revised"),
 33:(N,N,N,N,N,"improved"), 34:(N,Y,Y,N,N,"misconduct, Table 2 and Figures 6-8"),
 35:(N,Y,Y,Y,N,"Lemma 6.8; a named colleague"), 36:(N,Y,Y,N,N,"Section 4"), 37:(N,Y,N,N,N,""),
 38:(N,Y,N,N,N,""), 39:(N,Y,N,N,N,"'wrong description'"), 40:(N,Y,Y,N,N,"gap in proof of main result"),
 41:(N,N,N,N,N,"solved by others"), 42:(N,N,N,N,N,"model modification"), 43:(N,N,N,N,N,"replaced"),
 44:(N,N,N,N,N,"crank responses"), 45:(N,N,N,N,N,"superseded"), 46:(Y,N,N,N,N,""),
 47:(N,N,N,N,N,"new version"), 48:(Y,N,N,N,N,""), 49:(N,N,N,N,N,"a journal submission withdrawn, not the paper"),
 50:(Y,N,N,N,N,""), 51:(N,Y,Y,N,N,"named computation"), 52:(N,Y,N,N,N,"a mistaken conclusion about a release"),
 53:(Y,N,N,N,N,""), 54:(N,Y,N,N,N,"'the current argument'"), 55:(N,Y,N,N,N,"'no longer think it is correct'"),
 56:(N,N,N,N,Y,"inflammatory content"), 57:(N,Y,Y,N,N,"equation 1"), 58:(N,N,N,N,N,"subsumed"),
 59:(N,N,N,N,N,"newer version"), 60:(N,N,N,N,N,"to be modified, not said wrong"),
}
assert sorted(V) == list(range(1, 61))
s = json.load(open("sample.json"))
out = [dict(id=r["id"], n=r["n"], **dict(zip(["bare","error","located","other","admin","note"], V[r["n"]]))) for r in s]
json.dump(out, open("hand.json", "w"), ensure_ascii=False, indent=1)
print({k: sum(o[k] for o in out) for k in ["bare","error","located","other","admin"]})
