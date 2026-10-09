"""Captions over Albert FULL SCREEN ('cam' mode) — shared so section agents do not re-implement it.

In scenes.py:
    import camcaps
    CAM_CAPS=[dict(text='Two years in stealth', on=['two','years','stealth'], after=11.0, end=14.5),
              dict(text="Can't even say hello 👋", on=["can't",'even','say','hello.','hello.'], after=23.4, end=24.95)]
    overlay=camcaps.make_overlay(CAM_CAPS)          # the runner calls scenes.overlay(beat,t,S,at,st) above the presenter

text  : what is shown (1–5 words; emoji allowed as its own token). Sparse: about one caption per 4–6 s, never every sentence.
on    : for each shown token, the SPOKEN word whose onset brings it in (first match at/after `after`, section seconds).
after : section time from which to search the transcript;  end: section time at which the caption fades out.
Style : white SF Pro Semibold 80 px, soft dark shadow, bottom scrim, word-by-word (8 px rise, 0.18 s), lead 0.13 s.
Sound : every camcap gets the SAME soft click as the cinematic captions (Albert, 2026-09-20: "I like those, add them to the
        captions when I am full screen"). Do not hand-write the cues - run  python3 scripts/camcap_clicks.py <project> <sec>
        after the scenes.py edit; it reads CAM_CAPS' resolved word times and merges caption-mouse-down cues into sfx.json.
Only drawn while the card (nearly) fills the frame, and never in the first/last 0.3 s of the section."""
import json,re
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from draw import sf,canvas,ease,smooth
import emoji
LEAD=.13;SIZE=80;BASE=905
def _bare(s):return re.sub(r"[^a-z0-9.$%']",'',s.lower())
def _fade(im,a):
 if a>=1:return im
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:int(v*max(0,a))));return im
@lru_cache(maxsize=512)
def _word(word,size):
 if emoji.is_emoji(word):
  e=emoji.emoji(word,round(size*1.08));return e,e.width,None
 f=sf(size,'Semibold');b=f.getbbox(word,anchor='ls');pad=40;w,h=b[2]-b[0]+2*pad,b[3]-b[1]+2*pad
 shd=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]+4),word,font=f,anchor='ls',fill=(0,0,0,210));shd=shd.filter(ImageFilter.GaussianBlur(9))
 t2=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(t2).text((pad-b[0],pad-b[1]+2),word,font=f,anchor='ls',fill=(0,0,0,120));shd.alpha_composite(t2.filter(ImageFilter.GaussianBlur(2)))
 ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]),word,font=f,anchor='ls',fill='white');return shd,f.getlength(word),(b[0]-pad,b[1]-pad)
@lru_cache(None)
def _scrim():
 g=np.zeros((1080,1920,4),np.uint8);y=np.arange(1080);g[...,3]=(np.clip((y-640)/440,0,1)**1.6*120)[:,None].astype(np.uint8);return Image.fromarray(g,'RGBA')
def make_overlay(caps,transcript='transcript.json'):
 import sys;here=Path(sys.modules['scenes'].__file__).resolve().parent if 'scenes' in sys.modules else Path('.')
 T=json.load(open(here/transcript));W=T['words'] if isinstance(T,dict) else T;D=W[-1]['end']
 def wt(word,after):
  m=[w for w in W if w['start']>=after-.02 and _bare(w['text'])==_bare(word)];return m[0]['start'] if m else after
 for c in caps:
  toks=c['text'].split();on=list(c.get('on') or toks);on+= [on[-1]]*(len(toks)-len(on))
  c['_times']=[max(.3,wt(w,c['after'])-LEAD) for w in on[:len(toks)]];c['_start']=min(c['_times']);c['_end']=min(c['end'],D-.3)
 def overlay(b,t,S,at,st):
  Tt=b['start']+t;k=smooth((st.w-1500)/400)*st.opacity
  if k<=0:return None
  live=[c for c in caps if c['_start']<=Tt<c['_end']]
  if not live:return None
  c=live[0];toks=c['text'].split();gap=sf(SIZE,'Semibold').getlength(' ');tiles=[_word(w,SIZE) for w in toks]
  width=sum(a for _,a,_ in tiles)+gap*(len(toks)-1);x=960-width/2;im=canvas();fo=smooth((c['_end']-Tt)/.18)*k
  im.alpha_composite(_fade(_scrim(),min(1,ease((Tt-c['_start'])/.3))*fo))
  for (tile,adv,off),tw in zip(tiles,c['_times']):
   e=ease((Tt-tw)/.18)
   if e>0:
    px,py=(x,BASE-SIZE*.36-tile.height/2) if off is None else (x+off[0],BASE+off[1])
    im.alpha_composite(_fade(tile,e*fo),(round(px),round(py+8*(1-e))))
   x+=adv+gap
  return im
 return overlay

def click_cues(caps,peak_db=-27,also_last=False):
 """Soft caption clicks for camcaps (Albert, 2026-09-20). Call AFTER make_overlay (it resolves the word times):
 one cue as each caption's first word lands, plus its last word with also_last=True. Returns sfx.json rows; the usual
 route is scripts/camcap_clicks.py, which merges them for you."""
 out=[]
 for c in caps:
  ts=c.get('_times')
  if not ts:raise RuntimeError('call camcaps.make_overlay(CAM_CAPS) before click_cues() - word times are not resolved yet')
  want=[ts[0]]+([ts[-1]] if also_last and len(ts)>1 and ts[-1]-ts[0]>.35 else [])
  for t in want:out.append({'file':'caption-mouse-down.wav','t':round(float(t),3),'peak_db':peak_db,'why':f'camcap "{c["text"]}"'})
 return sorted(out,key=lambda r:r['t'])
