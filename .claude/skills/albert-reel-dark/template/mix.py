"""Voice + SFX + music. Caption clicks on every full-screen cinematic group (user request), slash whooshes in the hook,
one click per UI activation, quiet transitions, approved Timeless excerpt under the voice."""
from pathlib import Path
import json,subprocess,wave,re,numpy as np
P=Path(__file__).resolve().parent;A=P/'audio/sources'
B=json.load(open(P/'edit/beats.json'));S={b['name']:b for b in B};D=B[-1]['end'];sr=48000
TOK=json.load(open(P/'edit/transcript.json'))['words']
def bare(s):return re.sub(r'[^a-z0-9.]','',s.lower())
def at(name,word,default=0,nth=0):
 b=S[name];ww=[w for w in TOK if b['start']-.01<=w['start']<b['end']-.01 and bare(w['text'])==bare(word)]
 return ww[nth]['start']-b['start'] if len(ww)>nth else default
out=np.zeros((round(D*sr),2));cues=[]
def cue(t,f,peak,role):
 x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/f),'-f','f32le','-ac','2','-ar',str(sr),'pipe:1']),np.float32).reshape(-1,2).astype(float)
 x*=10**(peak/20)/(abs(x).max()+1e-12);s=round(t*sr);e=min(len(out),s+len(x))
 if e>s:out[s:e]+=x[:e-s]
 cues.append({'time':round(t,4),'source':'sources/'+f,'peak_dbfs':peak,'role':role})
G=json.load(open(P/'caption-groups.json'));frames=set()
for g in G:
 if g['mode']=='full':frames.update([g['words'][0]['entry_frame'],g['words'][-1]['entry_frame']])
for n in sorted(frames):cue(n/30,'caption-mouse-down.wav',-25 if n/30<S['hook']['end'] else -27,'full-screen caption click')
h=S['hook']['start']
for t in [at('hook','kills',.94),1.50,at('hook','slop',2.16)]:cue(h+t-.11,'whoosh-snap.mp3',-22,'scythe slash')
for scene,t in [('choose',at('choose','Apple',2.55)),('agent',at('agent','agent',1.1)),('cta',at('cta','design',1.25)+.4)]:cue(S[scene]['start']+t,'first-click.wav',-26,'UI press')
for name,t in [('teach',at('teach','that',.7)),('teach',at('teach','know',1.39)),('document',at('document','saved',.52)),('investment',at('investment','millions',1.87))]:cue(S[name]['start']+t,'whoosh-snap.mp3',-31,'UI transition')
for i,n in enumerate(['Apple','Notion','Duolingo']):cue(S['brands']['start']+at('brands',n,.5+i*.65),'pop.mp3',-29,'dock magnify')
cue(S['free']['start']+at('free','free',2.4),'pop.mp3',-29,'GET pulse');cue(S['teach']['start']+at('teach','love',1.75),'pop.mp3',-30,'hearts')
mk=at('generic','making',1.75)
for k in range(2):cue(S['generic']['start']+mk+k*.16,'pop.mp3',-31,'first spits')
with wave.open(str(P/'audio/sfx.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
json.dump(cues,open(P/'audio/cue-sheet.json','w'),indent=2)
fc=f'[0:a]asplit=2[v][sc];[1:a]highpass=f=100,loudnorm=I=-29:TP=-9:LRA=7,afade=t=in:d=0.15,afade=t=out:st={D-.8}:d=0.8[m];[m][sc]sidechaincompress=threshold=0.03:ratio=2:attack=15:release=250[duck];[v][duck][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=.68:level=false:latency=true[a]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'renders/clean-voice.mp4'),'-i',str(A/'timeless-excerpt.wav'),'-i',str(P/'audio/sfx.wav'),'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',str(D),'-movflags','+faststart',str(P/'renders/FINAL-Scythe.mp4')],check=True)
json.dump({'song':'Timeless (Instrumental)','source':'https://www.youtube.com/watch?v=LiXIoqGXfh8','source_offset':23.1176,'pre_duck_lufs':-29,'note':'Approved cached excerpt reused; no new trend claim.'},open(P/'audio/music.json','w'),indent=2)
print('mixed',len(cues),'cues')
