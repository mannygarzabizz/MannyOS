#!/usr/bin/env python3
"""Proof that picture and sound are 1:1.   python3 verify_sync.py <project_dir> [--final]

Default: checks sections/*/voice.mkv — for frames at the START, MIDDLE and END of each section, finds which camera-source
moment the picture really shows and compares it with the moment its audio comes from (camera is 25 fps -> +-40 ms is the floor).
--final: checks the rendered sections/<sec>/<sec>.mp4 — which voice.mkv frame the presenter card shows ~1 s before the end
(largest-drift point). Card is assumed in the split position there (x=1250,y=80,610x920); a section ending in face mode
reads noisy — check it by eye. Exit code 1 if anything exceeds 40 ms (voice) / 67 ms (final)."""
import json,glob,subprocess,sys,numpy as np
P=sys.argv[1];final='--final' in sys.argv;bad=0
def grab(path,t,vf,n):
    b=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{max(t,0):.4f}','-i',path,'-frames:v','1','-vf',vf,'-f','rawvideo','pipe:1']);a=np.frombuffer(b,np.uint8).astype(np.float32)
    return None if len(a)!=n else (a-a.mean())/(a.std()+1e-6)
for d in sorted(glob.glob(f'{P}/sections/*/')):
    if not glob.glob(d+'timeline.json'): continue
    T=json.load(open(d+'timeline.json'));name=d.rstrip('/').split('/')[-1];res=[]
    if not final:
        segs=[s for s in T['timeline'] if s['f1']-s['f0']>20];vf='scale=160:90,format=gray'
        for s in (segs[0],segs[len(segs)//2],segs[-1]):
            i=(s['f0']+s['f1'])//2;g=grab(d+'voice.mkv',i/30+1e-3,vf,160*90);expect=s['src_t']+(i-s['f0'])/30
            res.append(40*min(range(-12,13),key=lambda k:float(((grab(T['cam'],expect+k*.04+1e-3,vf,160*90)-g)**2).mean())))
        lim=40
    else:
        # sample 14 moments across the section; keep only those with a DISTINCT best match (presenter moving, card in split)
        D=T['audio_s'];cf='crop=560:860:1275:110,scale=61:92,format=gray';cv='crop=658:1010:711:35,scale=61:92,format=gray'
        for t in np.linspace(1.0,D-1.0,14):
            g=grab(d+name+'.mp4',t,cf,61*92)
            if g is None: continue
            curve=[]
            for k in range(-15,16):
                v=grab(d+'voice.mkv',t+k/30,cv,61*92);curve.append(9e9 if v is None else float(((v-g)**2).mean()))
            kb=int(np.argmin(curve));srt=sorted(curve)
            if srt[0]<0.35 and srt[0]<0.6*np.median(curve): res.append(round((kb-15)/30*1000))
        lim=67
        if not res: print('??  '+name,'no usable moments (card not in split / presenter still) - check by eye');continue
    ok=all(abs(x)<=lim for x in res);bad+=not ok;print(('ok  ' if ok else 'BAD ')+name,res,'ms')
sys.exit(1 if bad else 0)
