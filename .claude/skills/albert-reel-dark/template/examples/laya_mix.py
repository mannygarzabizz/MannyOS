"""Voice + SFX + music for the Laya reel.

Caption mouse-down on the first and last word of every full-screen cinematic group (Albert's rule,
overriding the older hook-only default). Presenter chips stay silent. One click per UI press, quiet
pops for things that land, whooshes for the breakout and the surface changes, approved Timeless
excerpt under the voice with gentle ducking.
"""
from pathlib import Path
import json,subprocess,wave,re,numpy as np
P=Path(__file__).resolve().parent;A=P/'audio/sources'
B=json.load(open(P/'edit/beats.json'));S={b['name']:b for b in B};D=B[-1]['end'];sr=48000
TOK=json.load(open(P/'edit/transcript.json'))['words']
def bare(s):return re.sub(r'[^a-z0-9.]','',s.lower())
def at(name,word,default=0,nth=0):
 b=S[name];ww=[w for w in TOK if b['start']-.01<=w['start']<b['end']-.01 and bare(w['text'])==bare(word)]
 return ww[nth]['start']-b['start'] if len(ww)>nth else default
def abs_(name,word,default=0,nth=0):return S[name]['start']+at(name,word,default,nth)
out=np.zeros((round(D*sr),2));cues=[]
def cue(t,f,peak,role):
 if not (0<=t<D):return
 x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/f),'-f','f32le','-ac','2','-ar',str(sr),'pipe:1']),np.float32).reshape(-1,2).astype(float)
 x*=10**(peak/20)/(abs(x).max()+1e-12);s=round(t*sr);e=min(len(out),s+len(x))
 if e>s:out[s:e]+=x[:e-s]
 cues.append({'time':round(t,4),'source':'sources/'+f,'peak_dbfs':peak,'role':role})

# --- caption clicks: first and last word of every full-screen group -----------------------------
G=json.load(open(P/'caption-groups.json'));frames=set()
for g in G:
 if g['mode']=='full':frames.update([g['words'][0]['entry_frame'],g['words'][-1]['entry_frame']])
for n in sorted(frames):
 cue(n/30,'caption-mouse-down.wav',-25 if n/30<S['hook']['end'] else -27,'full-screen caption click')

# --- the hook: the "?" tile shoots up the Jev tile ----------------------------------------------
import sys;sys.path.insert(0,str(P/'parts'));sys.path.insert(0,str(P))
import hook as _hook
_shots=[S['hook']['start']+x for x in _hook.shot_times(at)]
for i,ts_ in enumerate(_shots):
 cue(ts_,'gunshot.wav',-15 if i in (0,len(_shots)-1) else (-17 if i<4 else -19),f'round {i+1} hits the Jev tile')
cue(_shots[-1]+.02,'whoosh-snap.mp3',-23,'Jev tile breaks into shards')

# --- surface changes / things that sweep -----------------------------------------------------------
cue(S['faster']['start']+.10,'whoosh-snap.mp3',-30,'"?" tile launches down its lane')
cue(abs_('faster','faster.',1.23)-.13,'pop.mp3',-27,'"?" crosses the line')
cue(abs_('naya','Laya,',.57)-.13-.16,'whoosh-snap.mp3',-27,'"?" tile flips over')
cue(abs_('naya','Laya,',.57)-.13,'pop.mp3',-27,'Laya wordmark lands')
cue(abs_('local','local',.47)-.13,'pop.mp3',-28,'Laya drops into the Dock')
cue(abs_('local','run',2.33)-.13+.40,'first-click.wav',-27,'return key: python triage.py')
cue(abs_('local','computer.',3.05)-.13,'pop.mp3',-30,'ran on this Mac')
cue(abs_('nocode','cannot',.97)-.13,'whoosh-snap.mp3',-30,'strike-through sweeps the code')
cue(abs_('speed','250',1.17),'pop.mp3',-27,'250 ms lands, red frame')
cue(abs_('speed','this',3.19)-.13,'whoosh-snap.mp3',-31,'card grows for the Laya row')
cue(abs_('speed','30',4.29),'pop.mp3',-26,'30 ms lands, green frame')
cue(abs_('cloud','local,',1.09)-.13,'pop.mp3',-29,'local loop starts')
cue(abs_('cloud',"doesn't",1.71)-.13+.25,'whoosh-snap.mp3',-31,'cloud drifts away')
cue(abs_('cloud','back,',3.07)-.13,'pop.mp3',-28,'done check on the laptop')
cue(abs_('muchfast','faster.',.88)-.13,'whoosh-snap.mp3',-27,'needle hits the top of the gauge')
cue(abs_('problem','base',.99)-.13-.42,'whoosh-snap.mp3',-31,'camera pushes into the README')
_ts=abs_('tuned','specific',1.81)-.13;_te=abs_('tuned','cases.',2.53)-.13
for i in range(4):cue(_ts+i*(_te-_ts)/3,'pop.mp3',-31,f'use-case chip {i+1} picked')
cue(abs_('claude','Claude.',1.13)-.13,'pop.mp3',-27,'Claude tile lands')
cue(abs_('claude','Claude.',1.13)+.12-.13,'first-click.wav',-26,'send press')
cue(abs_('cta','link',.45)-.13,'pop.mp3',-30,'repo link chip lands')
cue(abs_('cta','and',2.03)-.13,'first-click.wav',-26,'comment posted')
cue(abs_('cta','send',2.37)-.13,'pop.mp3',-29,'link sent')

with wave.open(str(P/'audio/sfx.wav'),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
cues.sort(key=lambda c:c['time']);json.dump(cues,open(P/'audio/cue-sheet.json','w'),indent=2)

fc=(f'[0:a]asplit=2[v][sc];'
    f'[1:a]highpass=f=100,loudnorm=I=-29:TP=-9:LRA=7,afade=t=in:d=0.15,afade=t=out:st={D-.8}:d=0.8[m];'
    f'[m][sc]sidechaincompress=threshold=0.03:ratio=2:attack=15:release=250[duck];'
    f'[v][duck][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=.84:level=false:latency=true[a]')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'renders/clean-voice.mp4'),
  '-i',str(A/'timeless-excerpt.wav'),'-i',str(P/'audio/sfx.wav'),'-filter_complex',fc,
  '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',str(D),
  '-movflags','+faststart',str(P/'renders/FINAL-laya.mp4')],check=True)
json.dump({'song':'Timeless (Instrumental)','artist':'The Weeknd, Playboi Carti',
 'source':'https://www.youtube.com/watch?v=LiXIoqGXfh8','source_offset':23.1176,'duration':round(D,2),
 'pre_duck_lufs':-29,'note':'Approved cached excerpt re-cut from the same verified offset; no new trend claim.'},
 open(P/'audio/music.json','w'),indent=2)
print('mixed',len(cues),'cues')
