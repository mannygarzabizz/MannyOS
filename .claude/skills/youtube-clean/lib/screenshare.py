"""Clean screen-share layer for YouTube Clean ('screen' mode).  Needs sections/<sec>/screen.mp4 from scripts/build_screen.py
(1920x930, chrome already cropped, frame i == voice.mkv frame i, cuts cross-dissolved). Never read the raw recording.

Grid (layout.SCREEN / layout.SCREEN_CARD): capture card 1480x716 r28 at (60,182) | 40 px gutter | presenter 280x716 r36 at (1580,182).
Same top, same bottom, 60 px frame margins. NO TEXT while the screen share is on screen (Albert, 2026-09-20): no title line
above the card (title() is RETIRED - do not call it), no caption below it, no call-outs over the capture. Point with FocusTrack
or an accent ring instead. Card + presenter + white ground, nothing else.

  import screenshare as SS
  SCR=SS.Screen(__file__)                                  # in scenes.py
  FOCUS=SS.FocusTrack([(0,.5,.5,1),(12.0,.30,.40,1.8),(20.5,.5,.5,1)])   # section-local s, centre (0-1 of the capture), zoom
  def graphics(beat,t,S,at):
      T=beat['start']+t
      im=SS.card(SCR,T,focus=FOCUS(T))                     # RGBA 1920x1080 layer
      SS.title(im,'Playground','Multiple choice')          # optional, stays for the whole stretch
      return im

Rules: Screen Studio already zooms - add your own FOCUS push-in only while the source is un-zoomed (SCR.zoomed(T) is False) and
the thing he talks about is unreadable at 1x on a phone; GENTLE: 1.2-1.4x normal, 1.6x hard cap (Albert, 2026-09-20), one push per
stretch, moves >= 0.8 s, hold >= 4 s, back to 1x after; prefer an accent ring over a zoom. Never chase the cursor. `SS.card(..., rect=)` lets the
card grow to the full frame for a 'full' moment: rect=SS.FULL (1800x872 at (60,104)) with the presenter in 'full' bubble ONLY
if the bubble corner (x>1540,y>700) is empty in the capture - look at the frame.
"""
import json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
import layout as L
from draw import sf
RECT=L.SCREEN[:4];R=L.SCREEN[4];FULL=(60,104,1800,872);SW,SH=1920,930
class Screen:
 def __init__(self,scenes_file,name='screen'):
  """name='screen' = the voice-synced capture; any other name = a B-roll clip from scripts/build_screen_clip.py (clip-local time)."""
  d=Path(scenes_file).resolve().parent;self.path=d/f'{name}.mp4';self.meta=json.load(open(d/f'{name}_meta.json'));self.N=self.meta['frames']
  self.p=None;self.pos=-1;self.last=None;self.cache={}
 def zoomed(self,T):n=min(self.N-1,max(0,round(T*L.FPS)));return self.meta['zoomed'][n]
 def _open(self,n):
  if self.p:self.p.kill()
  self.p=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{max(0,(n-.5)/L.FPS):.4f}','-i',str(self.path),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE,bufsize=SW*SH*3);self.pos=n-1
 def frame(self,T):
  n=min(self.N-1,max(0,round(T*L.FPS)))
  if n in self.cache:return self.cache[n]
  if self.p is None or n<=self.pos or n>self.pos+90:self._open(n)
  while self.pos<n:
   b=self.p.stdout.read(SW*SH*3);self.pos+=1
   if len(b)==SW*SH*3:self.last=Image.frombuffer('RGB',(SW,SH),b,'raw','RGB',0,1).copy()
  self.cache={n:self.last};return self.last
class FocusTrack:
 """[(t,cx,cy,zoom),...] -> smooth interpolation; cx,cy in 0-1 of the capture."""
 def __init__(self,keys):self.k=sorted(keys)
 def __call__(self,T):
  k=self.k
  if T<=k[0][0]:return k[0][1:]
  for a,b in zip(k,k[1:]):
   if T<=b[0]:
    u=L.smooth((T-a[0])/max(1e-6,b[0]-a[0]));return tuple(p+(q-p)*u for p,q in zip(a[1:],b[1:]))
  return k[-1][1:]
_sh={}
def _shadow(w,h,r):
 if (w,h,r) not in _sh:
  pad=90;a=Image.new('L',(w+2*pad,h+2*pad),0);ImageDraw.Draw(a).rounded_rectangle((pad,pad,pad+w,pad+h),radius=r,fill=70)
  a=a.filter(ImageFilter.GaussianBlur(28));s=Image.new('RGBA',a.size,(0,0,0,0));s.putalpha(a);_sh[(w,h,r)]=(s,pad)
 return _sh[(w,h,r)]
def card(scr,T,focus=None,rect=RECT,r=R,opacity=1.):
 x,y,w,h=[round(v) for v in rect];src=scr.frame(T);cx,cy,z=focus or (.5,.5,1.);z=max(1.,z)
 bw,bh=SW/z,SW/z*h/w
 if bh>SH:bh=SH;bw=bh*w/h
 bx=min(max(cx*SW-bw/2,0),SW-bw);by=min(max(cy*SH-bh/2,0),SH-bh)
 pic=src.resize((w,h),Image.Resampling.LANCZOS if bw>w else Image.Resampling.BICUBIC,box=(bx,by,bx+bw,by+bh))
 im=Image.new('RGBA',(L.W,L.H),(255,255,255,0));s,pad=_shadow(w,h,r);im.alpha_composite(s,(x-pad,y-pad+18))
 im.paste(pic,(x,y),L.card_mask(w,h,r));ImageDraw.Draw(im).rounded_rectangle((x,y,x+w-1,y+h-1),radius=r,outline=(227,227,230,255),width=2)
 if opacity<1:im.putalpha(im.getchannel('A').point(lambda a:int(a*opacity)))
 return im
def _ink_left(txt,f):
 """Measured offset from the draw origin to the first visibly inked column (alpha > 40) - exact flush alignment."""
 m=Image.new('L',(int(f.getlength(txt))+80,120),0);ImageDraw.Draw(m).text((20,20),txt,font=f,fill=255)
 cols=np.nonzero(np.asarray(m).max(0)>40)[0];return int(cols.min())-20 if len(cols) else 0
def title(im,head,sub=None,x=RECT[0],y=104):
 """RETIRED 2026-09-20 - Albert wants NO text above the screen share. Kept only so old scenes.py files still import; do not
 call it in new sections. One calm title line above the capture card, ink of the first letter exactly at x (default 60)."""
 d=ImageDraw.Draw(im);f=sf(40,'Semibold');x=x-_ink_left(head,f);d.text((x,y),head,font=f,fill=L.INK)
 if sub:d.text((x+f.getlength(head)+22,y+6),'·  '+sub,font=sf(34,'Regular'),fill=L.GRAY)
 return im
