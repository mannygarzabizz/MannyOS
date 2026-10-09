"""Voice + SFX + music for the Opus 5.5 / CLAUDE.md reel. Caption clicks on every full-screen cinematic group,
bazooka launch / rocket / explosion in the hook, a thud for the tile drop, one click per UI press, quiet pops on
landings, the approved Timeless excerpt under the voice with gentle ducking."""
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
_cache={}
def cue(t,f,peak,role):
 if f not in _cache:_cache[f]=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/f),'-f','f32le','-ac','2','-ar',str(sr),'pipe:1']),np.float32).reshape(-1,2).astype(float)
 x=_cache[f].copy();x*=10**(peak/20)/(abs(x).max()+1e-12);s=round(max(0,t)*sr);e=min(len(out),s+len(x))
 if e>s:out[s:e]+=x[:e-s]
 cues.append({'time':round(t,4),'source':'sources/'+f,'peak_dbfs':peak,'role':role})
def T(name,word,default,nth=0):return S[name]['start']+at(name,word,default,nth)
LEAD=.13
# ---- caption clicks: first and last word of every full-screen group
G=json.load(open(P/'caption-groups.json'));frames=set()
for g in G:
 if g['mode']=='full':frames.update([g['words'][0]['entry_frame'],g['words'][-1]['entry_frame']])
for n in sorted(frames):cue(n/30,'caption-mouse-down.wav',-25 if n/30<S['hook']['end'] else -27,'full-screen caption click')
# ---- hook: launch on "killed", rocket in flight, explosion on "Astra"
hit=T('hook','Astra',.94)-.05;fire=min(T('hook','killed',.60)-.05,hit-.26)
cue(fire,'bazooka-launch.wav',-13,'bazooka launch');cue(fire+.03,'rocket-flight.wav',-24,'rocket flight')
cue(hit,'explosion.wav',-9,'explosion');cue(hit-.02,'whoosh-snap.mp3',-20,'impact whoosh')
# ---- opus: wordmark whoosh, the tile lands with a thud, pills pop
cue(T('opus','Opus',1.13)-LEAD,'whoosh-snap.mp3',-31,'wordmark writes');cue(T('opus','5.5',1.65)-LEAD,'pop.mp3',-29,'5.5 pops')
cue(T('opus','Opus',1.13)-LEAD,'thud.wav',-15,'tile lands on Opus');td=T('opus','dropped,',2.71)-.05;cue(td,'thud.wav',-15,'tile lands again on dropped');cue(T('opus','just',2.41)-LEAD,'whoosh-snap.mp3',-30,'jump')
# ---- solves: tiles land, the bars fill, red frame
for i in range(3):cue(S['solves']['start']+max(0,i*.07-.12+.1),'pop.mp3',-31,'frontier tile')
cue(T('solves','massive',.71)-LEAD,'whoosh-snap.mp3',-31,'bars fill');cue(T('solves','issue',1.11)-LEAD,'pop.mp3',-27,'limit frame')
for th in ('frontier','models.'):cue(T('solves',th,2.0)-LEAD,'pop.mp3',-32,'tile hop')
# ---- likeme: meme card, banner, week strip
cue(S['likeme']['start']+.05,'pop.mp3',-27,'meme card');cue(T('likeme','usage',1.73)-LEAD,'whoosh-snap.mp3',-29,'fist rises')
cue(T('likeme','limit',2.05)-LEAD,'pop.mp3',-25,'finger flicks up')
for w_,d_ in (('one',2.47),('day',2.69)):cue(T('likeme',w_,d_)-LEAD,'pop.mp3',-30,'pump')
cue(T('likeme','reset.',3.29)-LEAD,'whoosh-snap.mp3',-28,'big pump + wag')
# ---- but: tile, drain, check, file, click
cue(T('but','Opus',.37)-LEAD,'pop.mp3',-29,'Opus tile');cue(T('but','solve',1.41)-LEAD,'whoosh-snap.mp3',-30,'bar drains')
cue(T('but','it',1.71)-LEAD,'pop.mp3',-28,'green check');cue(T('but','if',1.97)-LEAD,'pop.mp3',-25,'meme takes the panel')
# ---- create: New click, tab pops
cue(S['create']['start']+.26,'first-click.wav',-26,'+ New');cue(T('create','CLAUDE.md',.67)-LEAD,'pop.mp3',-28,'CLAUDE.md tab')
# ---- write1 / write2 / rest
cue(T('write1','sub-agent."',2.79)-LEAD,'pop.mp3',-28,'sub-agent chip')
cue(T('write2','Use',2.41,1)-LEAD,'first-click.wav',-26,'model picker opens');cue(T('write2','5.5',3.15)-.05,'first-click.wav',-26,'Opus 5.5 picked');cue(T('write2','5.5',3.15)+.02,'pop.mp3',-29,'chip swaps')
cue(T('rest','include',.71)-LEAD,'whoosh-snap.mp3',-31,'lines stream in');cue(T('rest','CLAUDE.md',2.15)-LEAD,'pop.mp3',-29,'saved')
# ---- boom: celebration, fly-out, diagram
cue(T('boom','boom,',.24)-LEAD,'pop.mp3',-23,'celebration card');cue(T('boom','boom,',.24)-LEAD+.02,'whoosh-snap.mp3',-26,'confetti')
cue(T('boom','means',1.48)-LEAD,'whoosh-snap.mp3',-29,'card flies out');cue(T('boom','Claude',1.84)-LEAD,'pop.mp3',-28,'Claude tile')
for w_,d_ in (('now',2.18),('not',2.36),('always',2.66)):cue(T('boom',w_,d_)-LEAD+.16,'pop.mp3',-30,'sub-agent card')
cue(T('boom','Fable',3.44)-LEAD,'whoosh-snap.mp3',-29,'chips flip');cue(T('boom','now.',3.76)-LEAD,'pop.mp3',-29,'green pulse')
# ---- determine: locks + checks
for w_,d_ in (('determine',.41),('itself',.77),('model',1.47)):cue(T('determine',w_,d_)-LEAD,'pop.mp3',-27,'model locks')
cue(T('determine','use.',1.99)-LEAD,'pop.mp3',-30,'checks')
# ---- cta
cue(T('cta','CLAUDE.md,',1.55)-LEAD,'pop.mp3',-29,'chip writes');cue(T('cta','and',3.11)-LEAD,'first-click.wav',-26,'post')
cue(T('cta','send',3.37)-LEAD,'pop.mp3',-29,'chip goes blue');cue(T('cta','free',4.59)-LEAD,'first-click.wav',-27,'like')
with wave.open(str(P/'audio/sfx.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
json.dump(cues,open(P/'audio/cue-sheet.json','w'),indent=2)
fc=f'[0:a]asplit=2[v][sc];[1:a]highpass=f=100,loudnorm=I=-29:TP=-9:LRA=7,afade=t=in:d=0.15,afade=t=out:st={D-.8}:d=0.8[m];[m][sc]sidechaincompress=threshold=0.03:ratio=2:attack=15:release=250[duck];[v][duck][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=.84:level=false:latency=true[a]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'renders/clean-voice.mp4'),'-i',str(A/'timeless-excerpt.wav'),'-i',str(P/'audio/sfx.wav'),'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',str(D),'-movflags','+faststart',str(P/'renders/FINAL-opus55.mp4')],check=True)
json.dump({'song':'Timeless (Instrumental)','source':'https://www.youtube.com/watch?v=LiXIoqGXfh8','source_offset':23.1176,'pre_duck_lufs':-29,'note':'Approved cached excerpt reused; no new trend claim.'},open(P/'audio/music.json','w'),indent=2)
print('mixed',len(cues),'cues')
