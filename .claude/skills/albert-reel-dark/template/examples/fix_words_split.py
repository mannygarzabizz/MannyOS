"""Explicit transcript corrections for the final cut (run after every re-transcribe), plus the beat split
that does not need a cut: 'six' is one continuous take ("... $4.6 trillion in services"); the beat boundary
between the number and the source page sits on the onset of "in" (measured by Scribe on the final cut)."""
import json,re,math,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.load(open(P/'edit/final-timing/transcripts/tight.json'));w=[x for x in d['words'] if x.get('type','word')=='word']
FIX={'"free"':'free','"Free"':'free','"free",':'free,','"Free",':'free,','accountant.':'accounting.'}
def merge(seq,new):
 for i in range(len(w)-len(seq)+1):
  if [x['text'].lower().strip('.,') for x in w[i:i+len(seq)]]==seq:
   w[i]['text']=new+(',' if w[i+len(seq)-1]['text'].endswith(',') else '');w[i]['end']=w[i+len(seq)-1]['end'];del w[i+1:i+len(seq)];return True
 return False
merge(['seven','hundred','and','fifty'],'750');merge(['four','point','six'],'4.6')
out=[]
for x in w:
 x['text']=FIX.get(x['text'],x['text']);out.append(x)
json.dump({'words':out},open(P/'edit/transcript.json','w'),indent=1)
print(' '.join(f"{x['text']}[{x['start']:.2f}]" for x in out[:14]));print(' '.join(x['text'] for x in out))

# ---- audit EDL: range ends expressed in reel time (the hook is 1.12x, so its source span is not its reel span)
e=json.load(open(P/'edit/edl.json'))
for r in e['ranges']:r['end']=r['start']+round((r['end']-r['start'])/r.get('speed',1)*30)/30
json.dump(e,open(P/'edit/edl-audit.json','w'))

# ---- beat split without a cut: 'six' -> 'six' + 'services' at the onset of "in" (first "in" after "trillion")
raw=P/'edit/beats-raw.json'
if not raw.exists():shutil.copy(P/'edit/beats.json',raw)
B=json.load(open(raw));SPLIT={'six':('services','trillion','in')}
NB=[]
for b in B:
 if b['name'] in SPLIT:
  new,after,word=SPLIT[b['name']];ww=[x for x in out if b['start']<=x['start']<b['end']]
  i=next(k for k,x in enumerate(ww) if re.sub(r'[^a-z0-9.]','',x['text'].lower())==after)
  j=next(k for k in range(i+1,len(ww)) if re.sub(r'[^a-z0-9.]','',ww[k]['text'].lower())==word)
  cut=math.floor(ww[j]['start']*30)/30
  NB.append({'name':b['name'],'start':b['start'],'end':cut});NB.append({'name':new,'start':cut,'end':b['end']})
  print(f"split {b['name']} at {cut:.3f}s ('{ww[j]['text']}' onset {ww[j]['start']:.3f}) -> {new} {cut:.2f}-{b['end']:.2f}")
 else:NB.append(b)
json.dump(NB,open(P/'edit/beats.json','w'),indent=2)
print('beats:',' '.join(f"{b['name']}({b['end']-b['start']:.2f})" for b in NB))
