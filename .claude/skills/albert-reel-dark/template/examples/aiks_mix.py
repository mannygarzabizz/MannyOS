"""Voice + SFX + music for the "AI killed software" reel.

Caption mouse-down on the first and last word of every full-screen cinematic group (Albert's rule). Presenter chips
stay silent. The hook is FULL AUTO: one synthesised machine-gun round (audio/sources/mg-round.wav) per shot from
parts/hook.shot_times, -19 dB in the burst, -16 dB on the first round, the pistol crack (gunshot.wav) -15 dB plus a
whoosh on the last round that breaks the tile. One click per UI press, quiet pops for things that land, whooshes
for flips, sweeps, camera moves and card growth, approved Timeless excerpt under the voice with gentle ducking.
"""
from pathlib import Path
import json,subprocess,wave,re,sys,numpy as np
P=Path(__file__).resolve().parent;A=P/'audio/sources'
B=json.load(open(P/'edit/beats.json'));S={b['name']:b for b in B};D=B[-1]['end'];sr=48000
TOK=json.load(open(P/'edit/transcript.json'))['words']
def bare(s):return re.sub(r'[^a-z0-9.]','',s.lower())
def at(name,word,default=0,nth=0):
 b=S[name];ww=[w for w in TOK if b['start']-.01<=w['start']<b['end']-.01 and bare(w['text'])==bare(word)]
 return ww[nth]['start']-b['start'] if len(ww)>nth else default
def abs_(name,word,default=0,nth=0):return S[name]['start']+at(name,word,default,nth)
out=np.zeros((round(D*sr),2));cues=[];_src={}
def cue(t,f,peak,role):
 if not (0<=t<D):return
 if f not in _src:_src[f]=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/f),'-f','f32le','-ac','2','-ar',str(sr),'pipe:1']),np.float32).reshape(-1,2).astype(float)
 x=_src[f].copy();x*=10**(peak/20)/(abs(x).max()+1e-12);s=round(t*sr);e=min(len(out),s+len(x))
 if e>s:out[s:e]+=x[:e-s]
 cues.append({'time':round(t,4),'source':'sources/'+f,'peak_dbfs':peak,'role':role})

# --- caption clicks: first and last word of every full-screen group -----------------------------
G=json.load(open(P/'caption-groups.json'));frames=set()
for g in G:
 if g['mode']=='full':frames.update([g['words'][0]['entry_frame'],g['words'][-1]['entry_frame']])
for n in sorted(frames):cue(n/30,'caption-mouse-down.wav',-25 if n/30<S['hook']['end'] else -27,'full-screen caption click')

# --- the hook: full auto into the Salesforce tile ---------------------------------------------------
sys.path.insert(0,str(P/'parts'));sys.path.insert(0,str(P))
try:import hook as _hook
except ImportError:import mg_hook as _hook
_shots=[S['hook']['start']+x for x in _hook.shot_times(at)]
for i,ts_ in enumerate(_shots[:-1]):cue(ts_,'mg-round.wav',-16 if i==0 else -19,f'round {i+1} hits the Salesforce tile')
cue(_shots[-1],'gunshot.wav',-15,'last round breaks the tile');cue(_shots[-1]+.02,'whoosh-snap.mp3',-23,'Salesforce tile breaks into shards')

# --- surface changes / things that land --------------------------------------------------------------
L=.13
cue(S['worry']['start']+.42,'whoosh-snap.mp3',-31,'cups shuffle 1');cue(S['worry']['start']+.92,'whoosh-snap.mp3',-31,'cups shuffle 2')
cue(abs_('worry','never',1.67)-L,'pop.mp3',-28,'the software cup lifts: nothing under it');cue(abs_('worry','in',1.95)-L+.10,'whoosh-snap.mp3',-27,'software cup thrown away');cue(abs_('worry','begin',2.71)-L+.10,'whoosh-snap.mp3',-27,'second cup thrown away')
cue(abs_('hidden','actually',.25)-L+.10,'whoosh-snap.mp3',-27,'last cup thrown away')
cue(abs_('hidden','else',1.11)-L+.02,'whoosh-snap.mp3',-26,'the hat comes off');cue(abs_('hidden','else',1.11)-L+.08,'pop.mp3',-24,'the money was on his head');cue(abs_('hidden','sight.',1.81)-L,'pop.mp3',-30,'green pulse on sight')
cue(abs_('spend','US',.10)-L+.05,'whoosh-snap.mp3',-31,'the country draws in')
for i in range(10):cue(abs_('spend','companies',.46)-L+i*.06,'pop.mp3',-33,f'company {i+1} pops up on the map')
for i in range(12):cue(S['spend']['start']+abs_('spend','750',2.28)-S['spend']['start']+(abs_('spend','billion',3.48)-abs_('spend','750',2.28))*i/11,'pop.mp3',-34 if i<11 else -26,f'flap {i+1} locks')
cue(abs_('spend','year',4.68)-L,'pop.mp3',-30,'/ year pill')
for i in range(5):cue(abs_('spend','software.',5.12)-L+i*.06,'pop.mp3',-31,f'software tile {i+1} slides in')
cue(abs_('alot','not',1.16)-L,'whoosh-snap.mp3',-31,'software bar shrinks');cue(abs_('alot','this.',1.78)-L,'whoosh-snap.mp3',-26,'the other bar shoots up');cue(abs_('alot','this.',1.78)-L+.32,'pop.mp3',-27,'bar hits the top of the card')
cue(abs_('six','companies',.79)-L,'whoosh-snap.mp3',-31,'card grows for the services row');cue(abs_('six','six',2.03)-L,'pop.mp3',-27,'6x chip lands')
cue(abs_('six','4.6',3.15),'pop.mp3',-28,'4.6 lands');cue(abs_('six','trillion',3.99),'pop.mp3',-26,'$4.6T lands, green frame')
cue(abs_('six','dollars',4.45)-L,'pop.mp3',-31,'source line')
cue(S['services']['start']+.02,'whoosh-snap.mp3',-31,'camera pushes into the article');cue(abs_('services','every',1.05)-L,'whoosh-snap.mp3',-31,'highlighter sweep')
for i,wd in enumerate(['Accountants,','lawyers,','brokers,','agencies.']):cue(abs_('jobs',wd,[.11,.83,1.43,2.09][i])-L,'pop.mp3',-27,f'{wd} tile lands')
cue(abs_('why','why',.25)-L,'pop.mp3',-28,'thinking emoji hops')
_tn=abs_('tool','never',.85)-L;_ta=abs_('tool','accounting.',2.81)-L
for k in range(10):cue(_tn+(_ta-_tn)*k/9,'first-click.wav',-31,f'tab {k+1} closed')
cue(_ta+.16,'whoosh-snap.mp3',-28,'empty window collapses')
cue(abs_('done','want',.61)-L,'pop.mp3',-28,'Claude drops into the Dock');cue(abs_('done','accounting',1.03)-L,'first-click.wav',-26,'Do my accounting pressed')
for i in range(3):cue(abs_('done','accounting',1.03)-L+.14+i*.15,'pop.mp3',-31,f'task {i+1} ticked')
cue(abs_('done','done',1.63)-L,'whoosh-snap.mp3',-29,'Complete sheet drops');cue(abs_('done','done',1.63)-L+.12,'pop.mp3',-26,'big check')
cue(abs_('done','them.',2.21)-L,'first-click.wav',-28,'OK pressed');cue(abs_('done','them.',2.21)-L+.12,'whoosh-snap.mp3',-31,'notification banner')
cue(abs_('humans','now,',.58)-L,'pop.mp3',-30,'now marker');cue(abs_('humans','not',3.14)-L,'whoosh-snap.mp3',-29,'the humans drop away');cue(abs_('humans','anymore.',3.28)-L,'pop.mp3',-27,'Claude tile lands')
import shootout as _shoot
for i in range(6):cue(abs_('next','billion-dollar',.33)-L+i*.08,'pop.mp3',-31,f'SaaS tile {i+1} lands')
_T=[S['next']['start']+x for x in _shoot.shot_times(at)];_B=set(round(S['next']['start']+x,4) for x in _shoot.break_times(at))
for i,ts_ in enumerate(_T):
 if round(ts_,4) in _B:cue(ts_,'gunshot.wav',-15 if i==len(_T)-1 else -17,f'round {i+1}: tile breaks');cue(ts_+.02,'whoosh-snap.mp3',-23 if i==len(_T)-1 else -27,'shards')
 else:cue(ts_,'mg-round.wav',-19,f'round {i+1} hits a SaaS tile')
cue(abs_('service','software',.98)-L,'pop.mp3',-31,'search tabs');cue(abs_('service','companies',1.36)-L,'whoosh-snap.mp3',-31,'the businesses list in')
cue(abs_('service','acting',2.08)-L,'whoosh-snap.mp3',-27,'the AI company slides in at the top');cue(abs_('service','as',2.60)-L,'pop.mp3',-29,'row highlights');cue(abs_('service','service',2.78)-L,'pop.mp3',-30,'Accounting service chip')
cue(abs_('service','companies',3.18,1)-L,'first-click.wav',-26,'Book pressed');cue(abs_('service','companies',3.18,1)-L+.1,'pop.mp3',-28,'Booked')
for i in range(9):cue(S['skills']['start']+.12+i*.13,'pop.mp3',-32,f'skill chip {i+1}')
for i,wd in enumerate(['skills','that','know']):cue(abs_('skills',wd,[2.33,2.77,3.15][i])-L,'pop.mp3',-28,f'chip picked on {wd}')
cue(abs_('turn','into',.68)-L,'pop.mp3',-30,'shop lights on');cue(abs_('turn','AI-native',1.10)-L,'pop.mp3',-29,'Claude mark glows')
cue(abs_('turn','service',1.72)-L,'whoosh-snap.mp3',-28,'awning unrolls');cue(abs_('turn','business.',2.08)-L,'pop.mp3',-26,'OPEN sign flips')
cue(abs_('cta','guide',1.34)-L,'pop.mp3',-30,'guide chip written');cue(abs_('cta','and',3.94)-L,'first-click.wav',-26,'comment posted')
cue(abs_('cta','send',4.32)-L,'pop.mp3',-29,'guide sent');cue(abs_('cta','you',4.82,2)-L,'first-click.wav',-30,'comment liked')

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
  '-movflags','+faststart',str(P/'renders/FINAL-ai-killed-software.mp4')],check=True)
json.dump({'song':'Timeless (Instrumental)','artist':'The Weeknd, Playboi Carti',
 'source':'https://www.youtube.com/watch?v=LiXIoqGXfh8','source_offset':23.1176,'duration':round(D,2),
 'pre_duck_lufs':-29,'note':'Approved cached excerpt reused (Albert picked no song for this reel); no new trend claim.'},
 open(P/'audio/music.json','w'),indent=2)
print('mixed',len(cues),'cues')
