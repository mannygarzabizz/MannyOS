"""edit/matches.json → edit/edl.json (camera seconds, playback order, per section).  python3 build_edl.py CAM SCREEN
Cut points sit on the quietest 5 ms frame near each boundary; pieces are split at inner pauses > 0.40 s (the gap is removed);
intro joins are tighter than body joins; a bogus long previous word no longer blocks the search window. Prints loud cut
points to inspect. Needs edit/cam.wav (16 kHz mono of the camera audio)."""
import json,numpy as np,wave
W=[w for w in json.load(open('edit/raw/transcripts/cam.json'))['words'] if w['type']=='word']
M=json.load(open('edit/matches.json'))
# Per-video fixes go here: Scribe sometimes stretches a word's end over silence or fuses a stutter into one token.
# OVERRIDE_END={word_index: true_end_s}; FORCE_SPLIT={word_index_after_which_to_split}; read true times from an RMS profile.
OVERRIDE_END={}
for i,e in OVERRIDE_END.items(): W[i]['end']=e
FORCE_SPLIT=set()
w=wave.open('edit/cam.wav'); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
hop=int(sr*.005); n=len(x)//hop; db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-7)
def quiet(a,b,prefer):  # quietest 5ms frame in [a,b]; tie → closest to prefer
    a=max(a,0); i0,i1=int(a/.005),max(int(b/.005),int(a/.005)+1); seg=db[i0:i1]; k=int(np.argmin(seg+0.02*np.abs(np.arange(i0,i1)*.005-prefer)/.005)); return (i0+k)*.005, float(seg[k])
ranges=[]; warn=[]
for m in M:
    intro=m['sec']=='00-intro'; head,tail=(.05,.07) if intro else (.06,.11)
    # split the piece at internal pauses > 0.40 s
    parts=[];a=m['i0']
    for i in range(m['i0'],m['i1']):
        if W[i+1]['start']-W[i]['end']>0.40 or i in FORCE_SPLIT: parts.append((a,i)); a=i+1
    parts.append((a,m['i1']))
    for (p,q) in parts:
        ps=W[p-1]['end'] if p>0 else 0
        if p>0 and W[p-1]['end']-W[p-1]['start']>1.5: ps=W[p]['start']-0.3
        nx=W[q+1]['start'] if q+1<len(W) else 1e9
        s0=W[p]['start']; e0=W[q]['end']
        s,sd=quiet(max(ps+.005,s0-head-.06),s0-.01,s0-head); e,ed=quiet(e0+.02,min(nx-.005,e0+tail+.08),e0+tail)
        if e<=e0: e=e0+.02
        if sd>-32: warn.append(('start',round(s,2),round(sd,1),W[p]['text']))
        if ed>-32: warn.append(('end',round(e,2),round(ed,1),W[q]['text']))
        ranges.append({'sec':m['sec'],'start':round(s,3),'end':round(e,3),'text':' '.join(W[i]['text'] for i in range(p,q+1))})
# merge ranges that are contiguous in source with tiny gaps
out=[]
for r in ranges:
    if out and out[-1]['sec']==r['sec'] and 0<=r['start']-out[-1]['end']<0.12: out[-1]['end']=r['end']; out[-1]['text']+=' '+r['text']
    else: out.append(r)
import sys
CAM,SCREEN=sys.argv[1],sys.argv[2]   # python3 build_edl.py /abs/camera.mp4 /abs/screen-recording.mov
json.dump({'sources':{'cam':CAM,'screen':SCREEN},'ranges':out},open('edit/edl.json','w'),indent=1)
short=[r for r in out if r['end']-r['start']<0.8]
if short:
    print('MICRO-FRAGMENTS (< 0.8 s between cuts — flash as double jump cuts in full-screen mode; attach to a neighbour or drop):')
    for r in short: print('  ',r['sec'],round(r['start'],2),repr(r['text']))
secs={}
for r in out: secs.setdefault(r['sec'],[0,0]); secs[r['sec']][0]+=1; secs[r['sec']][1]+=r['end']-r['start']
for k,v in secs.items(): print(k,v[0],'ranges',round(v[1],1),'s')
print('total',round(sum(v[1] for v in secs.values())),'s; loud cut points:',len(warn))
for x_ in warn: print(' ',x_)
