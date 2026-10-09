"""Captions for YouTube Clean.

BODY  key_phrase(): 1-4 word key phrases, SF Pro Semibold 64-84 px, sentence case, ink #1D1D1F on white, each word rises
      8 px and fades in over 0.18 s, optional New York italic / coloured emphasis word, real Apple emoji tokens.
      Always kept inside the graphics stage (x 70..1180) unless area='full'; never under the presenter card.
INTRO cinematic(): the reels' full-screen editorial captions (helpers/editorial_caption.py) at 120-170 px for 1920x1080,
      cinematic_groups() builds the word groups from the transcript (click SFX go on first/last word of each group).

Scene-side use (inside graphics()):      captions.key_phrase(im,'Fast thinking ⚡',t,start=1.2,end=3.4,y=880,emph={'thinking':'italic'})
Runner-side use (scenes.py CAPTIONS=[]): dict(beat='b2',text='Fast thinking ⚡',start='fast',end=3.4,y=880,
                                              words=['fast','thinking'],emph={'thinking':'italic'})
      start / end / words entries may be floats (beat-local seconds) or spoken words resolved with at(beat, word).
"""
import sys,re,math
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));sys.path.insert(0,str(P/'helpers'))
from draw import sf,ny,ease,smooth,INK,GREEN,RED,BLUE,GRAY
import layout as L
import emoji as E
import editorial_caption as editorial

MIN_SIZE,MAX_SIZE=64,84
RISE,FADE=8,.18
COLORS={'green':GREEN,'red':RED,'blue':BLUE,'gray':GRAY,'ink':INK}
LEAD=.13   # visuals that must land on a word lead it by ~0.13 s

def _style(word,emph):
 """-> (italic,color) for a caption word. emph: {'word':'italic'|'green'|'red'|'blue'|'#hex'|'italic green'}"""
 if not emph:return False,None
 key=re.sub(r'[^\w$%.]','',word.lower())
 for k,v in emph.items():
  if re.sub(r'[^\w$%.]','',k.lower())==key:
   it='italic' in v;c=[COLORS.get(p,p) for p in v.split() if p!='italic'];return it,(c[0] if c else None)
 return False,None
def _font(size,italic):return ny(round(size*1.04),'Medium',italic=True) if italic else sf(size,'Semibold')

@lru_cache(maxsize=2048)
def _tile(word,size,italic,color):
 """One word as an RGBA tile drawn as ONE string on its baseline (never per-glyph). -> (tile, advance, ascent_offset)"""
 if E.is_emoji(word):
  s=round(size*1.08);im=E.emoji(word,s);return im,s,'emoji'
 f=_font(size,italic);b=f.getbbox(word,anchor='ls');pad=6
 im=Image.new('RGBA',(b[2]-b[0]+2*pad,b[3]-b[1]+2*pad),(0,0,0,0))
 ImageDraw.Draw(im).text((pad-b[0],pad-b[1]),word,font=f,anchor='ls',fill=color)
 return im,f.getlength(word),(b[0]-pad,b[1]-pad)

def _measure(words,size,emph):
 gap=sf(size,'Semibold').getlength(' ');x=0;items=[]
 for w in words:
  it,c=_style(w,emph);tile,adv,off=_tile(w,size,it,c or INK);items.append((w,tile,adv,off,x));x+=adv+gap
 return items,x-gap

def fit(text,size,max_w,emph=None):
 """Largest size in [64,size] that fits max_w on one line; else two balanced lines at 64+."""
 words=text.split();size=int(max(MIN_SIZE,min(MAX_SIZE,size)))
 s=size
 while s>=MIN_SIZE:
  if _measure(words,s,emph)[1]<=max_w:return s,[words]
  s-=2
 if len(words)>1:
  best=None
  for k in range(1,len(words)):
   a,b=words[:k],words[k:];s=size
   while s>=MIN_SIZE and max(_measure(a,s,emph)[1],_measure(b,s,emph)[1])>max_w:s-=2
   wid=abs(_measure(a,max(s,MIN_SIZE),emph)[1]-_measure(b,max(s,MIN_SIZE),emph)[1])
   if best is None or (s,-wid)>(best[0],-best[2]):best=(s,[a,b],wid)
  return max(best[0],MIN_SIZE),best[1]
 return MIN_SIZE,[words]

def key_phrase(im,text,t,start=0.,end=None,x=None,y=880,size=76,align='center',emph=None,word_times=None,stagger=.12,
               area='stage',max_w=None,color=INK,out=.15):
 """Draw a body key phrase on RGBA `im` at time t (same clock as start/end). Returns the bbox (x0,y0,x1,y1) or None.
 x: left edge (align='left') or centre (align='center'); default = stage centre. y: vertical centre of the first line.
 word_times: absolute entrance time per word (spoken onsets - LEAD); default start + i*stagger."""
 if t<start or (end is not None and t>=end):return None
 x0a,x1a=(L.STAGE[0],L.STAGE[2]) if area=='stage' else (L.SAFE+40,L.W-L.SAFE-40)
 if area!='stage' and y+size>L.BUBBLE[1]-40:x0a,x1a=L.W-(L.BUBBLE[0]-60),L.BUBBLE[0]-60   # low full-frame captions stay clear of the bubble, still centred
 max_w=min(max_w or (x1a-x0a),x1a-x0a);size,lines=fit(text,size,max_w,emph)
 fade=1. if end is None else smooth((end-t)/out)
 lh=round(size*1.18);i=0;bbox=None
 for li,words in enumerate(lines):
  items,width=_measure(words,size,emph)
  if x is None:lx=(x0a+x1a)/2-width/2
  else:lx=x-width/2 if align=='center' else x
  lx=min(max(lx,x0a),x1a-width)                      # never leave the stage / go under the card
  base=y+li*lh+size*.35                              # baseline so that y is the optical middle of the caps
  for (w,tile,adv,off,dx) in items:
   tw_=word_times[i] if word_times and i<len(word_times) and word_times[i] is not None else start+i*stagger
   e=ease((t-tw_)/FADE);i+=1
   if e<=0:continue
   a=e*fade
   if off=='emoji':px,py=lx+dx,base-size*.36-tile.height/2+RISE*(1-e)
   else:px,py=lx+dx+off[0],base+off[1]+RISE*(1-e)
   tl=tile
   if a<1:tl=tile.copy();tl.putalpha(tile.getchannel('A').point(lambda v:int(v*a)))
   im.alpha_composite(tl,(int(round(px)),int(round(py))))
  b=(lx,base-size,lx+width,base+size*.3);bbox=b if bbox is None else (min(bbox[0],b[0]),min(bbox[1],b[1]),max(bbox[2],b[2]),max(bbox[3],b[3]))
 return bbox

# ---------- runner-side CAPTIONS spec ----------
def resolve(spec,at,beats):
 """Turn a CAPTIONS dict into absolute section times. Words are looked up with at(beat, word) and led by LEAD."""
 b=beats[spec['beat']];nth=spec.get('nth',0)
 def T(v,default):
  if v is None:return default
  if isinstance(v,(int,float)):return b['start']+float(v)
  r=at(spec['beat'],v,None,nth)
  return default if r is None else b['start']+r-LEAD
 s=dict(spec);s['_start']=T(spec.get('start'),b['start']);s['_end']=T(spec.get('end'),b['end'])
 if isinstance(spec.get('end'),str):s['_end']+=LEAD
 wt=spec.get('words');s['_word_times']=[T(w,None) for w in wt] if wt else None
 if s['_word_times']:
  s['_start']=min([s['_start']]+[w for w in s['_word_times'] if w is not None])
 return s
def draw_spec(im,s,t):
 return key_phrase(im,s['text'],t,s['_start'],s['_end'],x=s.get('x'),y=s.get('y',880),size=s.get('size',76),align=s.get('align','center'),
                   emph=s.get('emph'),word_times=s['_word_times'],stagger=s.get('stagger',.12),area=s.get('area','stage'),max_w=s.get('max_w'))

# ---------- intro cinematic captions ----------
def bare(s):return re.sub(r'[^a-z0-9.$%]','',s.lower())
def cinematic_groups(beats,words,beat_names,cap=3,maxchars=20,fps=30):
 """Word groups for full-screen cinematic captions (same grouping rule as the reels' render.py)."""
 G=[]
 for b in beats:
  if b['name'] not in beat_names:continue
  ww=[w for w in words if b['start']<=w['start']<b['end']];groups=[];cur=[]
  for w in ww:
   if cur and (len(cur)>=cap or len(' '.join(x['text'] for x in cur+[w]))>maxchars):groups.append(cur);cur=[]
   cur.append(w)
   if re.search(r'[.,!?]$',w['text']) and len(cur)>=2:groups.append(cur);cur=[]
  if cur:groups.append(cur)
  for k,ws in enumerate(groups):
   G.append({'scene':b['name'],'mode':'full','text':' '.join(w['text'].strip('.,!?"') for w in ws).upper(),
             'start':math.floor(ws[0]['start']*fps)/fps,'end':math.floor(groups[k+1][0]['start']*fps)/fps if k+1<len(groups) else b['end'],
             'words':[{'text':w['text'],'entry_frame':math.floor(w['start']*fps)} for w in ws]})
 return G
def cinematic(im,g,n,y=560,x=None):
 """Draw cinematic group g at output frame n, centred on (x or 960, y). g may carry 'big' (120-170), 'color', 'cap'."""
 row=editorial.render_words(g,n);cx=L.W/2 if x is None else x
 im.alpha_composite(row,(int(round(cx-row.width/2)),int(round(y-row.height/2))));return row
