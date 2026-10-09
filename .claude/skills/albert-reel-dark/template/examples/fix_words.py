"""Explicit transcript corrections for the final cut (run after every re-transcribe)."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.load(open(P/'edit/final-timing/transcripts/tight.json'));w=[x for x in d['words'] if x.get('type','word')=='word']
def merge(seq,new):
 for i in range(len(w)-len(seq)+1):
  if [x['text'].lower().strip('.,') for x in w[i:i+len(seq)]]==seq:
   w[i]['text']=new+(',' if w[i+len(seq)-1]['text'].endswith(',') else '');w[i]['end']=w[i+len(seq)-1]['end'];del w[i+1:i+len(seq)];return True
 return False
merge(['a','hundred','dollars'],'$100') or merge(['hundred','dollars'],'$100');merge(['one','hundred','percent'],'100%')
out=[]
for x in w:
 x['text']={'FreeBuff,':'Freebuff,','twenty':'20','"install"':'"Install"','fuck':'f***'}.get(x['text'],x['text'])
 m=re.match(r'^(GPT|DeepSeek|GLM)-?(\d\.\d[,.]?)$',x['text'])
 if m:
  mid=x['start']+(x['end']-x['start'])*(.5 if m.group(1)=='DeepSeek' else .42);out+=[{**x,'text':m.group(1),'end':round(mid-.02,3)},{**x,'text':m.group(2),'start':round(mid,3)}]
 else:out.append(x)
json.dump({'words':out},open(P/'edit/transcript.json','w'),indent=1)
print(' '.join(f"{x['text']}[{x['start']:.2f}]" for x in out[:16]));print(' '.join(x['text'] for x in out))
e=json.load(open(P/'edit/edl.json'))
for r in e['ranges']:r['end']=r['start']+round((r['end']-r['start'])/r.get('speed',1)*30)/30
json.dump(e,open(P/'edit/edl-audit.json','w'))
