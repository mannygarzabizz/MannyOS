"""Match the keep-list to exact word timings.  Run from the project root:  python3 match_targets.py
Reads edit/targets.py (T=[(section, window_start, window_end, kept_text), …] in playback order, text in Scribe's own
spelling) + edit/raw/transcripts/cam.json → edit/matches.json. The LAST occurrence inside the window wins (last take).
Unmatched lines are printed: fix the text (Scribe fuses stutters into one token, e.g. "model—the") and re-run."""
import json,re,sys; sys.path.insert(0,'edit'); from targets import T
W=[w for w in json.load(open('edit/raw/transcripts/cam.json'))['words'] if w['type']=='word']
n=lambda s:re.sub(r"[^a-z0-9%']",'',s.lower().replace('’',"'"))
WN=[n(w['text']) for w in W]
out=[];bad=0
for sec,a,b,txt in T:
    tk=[n(x) for x in txt.split()]; tk=[x for x in tk if x]
    hit=None
    for i in range(len(W)-len(tk)+1):
        if W[i]['start']<a-0.5 or W[i+len(tk)-1]['end']>b+0.5: continue
        if WN[i:i+len(tk)]==tk: hit=i
    if hit is None: bad+=1; print('NO MATCH:',sec,a,txt[:70]); continue
    out.append({'sec':sec,'i0':hit,'i1':hit+len(tk)-1,'start':W[hit]['start'],'end':W[hit+len(tk)-1]['end'],'text':txt})
# order + overlap sanity
for p,q in zip(out,out[1:]):
    if q['i0']<=p['i1']: print('OVERLAP/ORDER:',p['text'][:40],'|',q['text'][:40])
json.dump(out,open('edit/matches.json','w'),indent=1); print(len(out),'matched',bad,'unmatched; speech total',round(sum(o['end']-o['start'] for o in out)),'s')
