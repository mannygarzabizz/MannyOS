"""16:9 layout for YouTube Clean (numbers from ~/.claude/skills/youtube-clean/layout.md).

White 1920x1080 ground, 30 fps. Graphics stage on the left, presenter card on the right.
The card is a rounded rectangle (antialiased 4x mask, soft shadow), cropped from the camera frame at FULL source
height, centred on the face (`face_cx`). Three modes, 0.35 s smooth() moves between them:

  split        card 610x920 r48 at (1250,80)            default body look
  full         card -> 300x300 r40 bubble at (1560,720) graphics own the frame
  full:hidden  card shrinks into the bubble spot and fades out (intro)
  cam          card grows to the whole 1920x1080 frame, r -> 0 (presenter full screen; captions go on top via scenes.overlay())
  face         card 900x920 r48 at (510,80)             opinion line, caption only
  screen       card 280x716 r36 at (1580,182)           screen share: the capture card (screenshare.py) sits at (60,182) 1480x716

API
  track=ModeTrack([(0,'split'),(4.2,'full'),(8.0,'split')],duration)   # times = when the move STARTS (section-local s)
  st=track.state(t)             -> CardState(x,y,w,h,r,opacity,zoom)
  composite_card(im,cam,st,face_cx=1040,face_cy=470)   im: RGBA/RGB 1920x1080, cam: numpy HxWx3 uint8 camera frame
  face_cx may be a number or [(t,cx),...] keyframes -> use face_at(face_cx,t)
"""
from functools import lru_cache
from collections import namedtuple
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

W,H,FPS=1920,1080,30
GROUND=(255,255,255)
INK='#1D1D1F';GRAY='#6E6E73';LINE='#E3E3E6';BLUE='#0071E3';GREEN='#1E8E3E';RED='#FF3B30';HILITE=(255,214,10,95)
CARD=(1250,80,610,920,48)        # x,y,w,h,r  (split)
BUBBLE=(1560,720,300,300,40)     # full
FACE=(510,80,900,920,48)         # face
STAGE=(70,80,1180,1000)          # x0,y0,x1,y1 -> 1110x920
STAGE_W,STAGE_H=STAGE[2]-STAGE[0],STAGE[3]-STAGE[1]
SAFE=60                          # nothing important within 60 px of a frame edge
MOVE=.35                         # card move duration, smooth()
CLEAN_FRAMES=8                   # first/last frames of a section: white + split card only
SHADOW=dict(dy=18,blur=28,alpha=70)
BUBBLE_ZOOM=1.45                 # the bubble crops tighter round the face; split/face keep the full source height

CardState=namedtuple('CardState','x y w h r opacity zoom')
_MODES={'split':CardState(*CARD,1.,1.),'full':CardState(*BUBBLE,1.,BUBBLE_ZOOM),'face':CardState(*FACE,1.,1.),
        'full:hidden':CardState(BUBBLE[0]+60,BUBBLE[1]+60,180,180,40,0.,BUBBLE_ZOOM)}
_MODES['hidden']=_MODES['full:hidden']
SCREEN=(60,182,1480,716,28)      # x,y,w,h,r  clean screen-share card ('screen' mode) - see screenshare.py
SCREEN_CARD=(1580,182,280,716,36)# slim presenter card beside it: same top, same bottom, 40 px gutter, 60 px frame margins
_MODES['screen']=CardState(*SCREEN_CARD,1.,1.)   # screen share: big chrome-free capture left, slim presenter right, everything on one grid
_MODES['cam']=CardState(0,0,W,H,0,1.,1.)   # ADDITIVE (intro rev 4): presenter full screen - the card grows to the frame, radius eases to 0, no shadow once it fills the frame

def smooth(v):v=max(0.,min(1.,v));return v*v*(3-2*v)
def mode_state(mode):return _MODES[mode]
def stage_mode(mode):return 'full' if mode.startswith('full') or mode=='hidden' else mode

class ModeTrack:
 """Per-section list of (time, mode). The card starts moving at `time` and arrives MOVE seconds later."""
 def __init__(self,modes,duration=None,fps=FPS):
  modes=sorted([(float(t),m) for t,m in modes]) or [(0.,'split')]
  for _,m in modes:
   if m not in _MODES:raise ValueError(f'unknown mode {m!r}; use {sorted(_MODES)}')
  # A section may START in 'cam' (Albert full screen) when MODES begins with (0,'cam'): chapter joins are then clean cuts
  # cam->cam instead of a split blink. Anything else still starts in split.
  start_cam=modes[0] in ((0.,'cam'),(0.,'screen'))
  if not start_cam and (modes[0][0]>0 or modes[0][1]!='split'):modes=[(0.,'split')]+[x for x in modes if x[0]>0 or x[1]!='split']
  self.warnings=[]
  lead=CLEAN_FRAMES/fps
  # keep the first CLEAN_FRAMES in split
  modes=[(max(t,lead) if i else 0.,m) for i,(t,m) in enumerate(modes)]
  if duration is not None:
   back=duration-lead-MOVE-1/fps   # latest moment a move back to split may START
   if modes[-1][1] in ('cam','screen'):pass   # a section may END in 'cam' (full screen) - clean cut into the next section
   elif modes[-1][1]!='split':
    modes.append((back,'split'));self.warnings.append(f'MODES did not end in split; added ({back:.2f},"split")')
   elif len(modes)>1 and modes[-1][0]>back:
    self.warnings.append(f'last move to split started at {modes[-1][0]:.2f}s, pulled to {back:.2f}s so the last {CLEAN_FRAMES} frames are clean')
    modes[-1]=(back,'split')
   modes=sorted(modes)
  for (a,_),(b,m) in zip(modes,modes[1:]):
   if b-a<MOVE and a>0:self.warnings.append(f'mode change to {m!r} at {b:.2f}s starts before the previous move finished')
  self.modes=modes
 def mode(self,t):
  cur=self.modes[0][1]
  for a,m in self.modes:
   if t>=a:cur=m
  return cur
 def moving(self,t):return any(a<=t<a+MOVE for a,_ in self.modes[1:])
 def state(self,t):
  st=_MODES[self.modes[0][1]]
  for a,m in self.modes[1:]:
   if t<a:break
   u=smooth((t-a)/MOVE);tg=_MODES[m];st=CardState(*[p+(q-p)*u for p,q in zip(st,tg)])
  return st
 def stage_progress(self,t):
  """0 = split stage (graphics stay left), 1 = full/face: handy for scenes that want to grow with the move."""
  v=0.
  for a,m in self.modes[1:]:
   if t<a:break
   v=v+((0. if m=='split' else 1.)-v)*smooth((t-a)/MOVE)
  return v

def face_at(face_cx,t):
 """face_cx: number, or keyframes [(t,cx),...] (he moves) -> smooth interpolation."""
 if isinstance(face_cx,(int,float)):return float(face_cx)
 k=sorted(face_cx)
 if t<=k[0][0]:return float(k[0][1])
 for (a,x0),(b,x1) in zip(k,k[1:]):
  if t<=b:return x0+(x1-x0)*smooth((t-a)/max(1e-6,b-a))
 return float(k[-1][1])

def crop_box(sw,sh,w,h,face_cx,face_cy=None,zoom=1.):
 """Source crop with the card's aspect, full source height at zoom 1, centred on the face, clamped to the frame."""
 ch=sh/max(1.,zoom);cw=ch*w/h
 if cw>sw:cw=sw;ch=cw*h/w
 cx=min(max(face_cx,cw/2),sw-cw/2);cy=sh/2 if face_cy is None else min(max(face_cy+ch*.06,ch/2),sh-ch/2)
 return (cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)

@lru_cache(maxsize=512)
def card_mask(w,h,r):
 q=4;m=Image.new('L',(w*q,h*q),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w*q-1,h*q-1),radius=r*q,fill=255)
 return m.resize((w,h),Image.Resampling.LANCZOS)

@lru_cache(maxsize=512)
def card_shadow(w,h,r,k100=100):
 """Soft shadow layer (RGBA) with PAD margin. k scales offset/blur for the small bubble."""
 k=k100/100;blur=SHADOW['blur']*k;pad=int(blur*3)+2
 a=Image.new('L',(w+2*pad,h+2*pad),0);ImageDraw.Draw(a).rounded_rectangle((pad,pad,pad+w-1,pad+h-1),radius=r,fill=SHADOW['alpha'])
 a=a.filter(ImageFilter.GaussianBlur(blur));s=Image.new('RGBA',a.size,(0,0,0,0));s.putalpha(a);return s,pad

def composite_card(im,cam,st,face_cx=1040,face_cy=None):
 """Draw the presenter card for CardState `st` onto `im` (in place). cam: HxWx3 uint8 array or PIL RGB image."""
 if st.opacity<=.004 or cam is None:return im
 src=cam if isinstance(cam,Image.Image) else Image.fromarray(cam,'RGB')
 w,h,r=max(2,round(st.w)),max(2,round(st.h)),max(1,round(st.r));x,y=round(st.x),round(st.y)
 if st.r<1:r=0                                   # only the 'cam' mode reaches r<1 (every other mode has r>=40)
 box=crop_box(src.width,src.height,w,h,face_cx,face_cy,st.zoom)
 person=src.resize((w,h),Image.Resampling.LANCZOS if w<box[2]-box[0] else Image.Resampling.BICUBIC,box=box)
 big=w>FACE[2]+8                                  # only on the way to/from 'cam': do not fill the lru caches with frame-sized images
 mask=(card_mask.__wrapped__ if big else card_mask)(w,h,r);k=max(.45,min(1.,h/CARD[3]))
 sh,pad=(card_shadow.__wrapped__ if big else card_shadow)(w,h,r,round(k*100))
 if st.opacity<1:
  mask=mask.point(lambda a:int(a*st.opacity));sh=sh.copy();sh.putalpha(sh.getchannel('A').point(lambda a:int(a*st.opacity)))
 dy=round(SHADOW['dy']*k)
 if im.mode=='RGBA':im.alpha_composite(sh,(x-pad,y-pad+dy)) if _inside(im,x-pad,y-pad+dy,sh) else _safe_comp(im,sh,x-pad,y-pad+dy)
 else:im.paste(sh,(x-pad,y-pad+dy),sh)
 im.paste(person,(x,y),mask)
 return im

def _inside(im,x,y,o):return x>=0 and y>=0 and x+o.width<=im.width and y+o.height<=im.height
def _safe_comp(im,o,x,y):
 x0,y0=max(0,x),max(0,y);x1,y1=min(im.width,x+o.width),min(im.height,y+o.height)
 if x1>x0 and y1>y0:im.alpha_composite(o.crop((x0-x,y0-y,x1-x,y1-y)),(x0,y0))

def card_rect(st,margin=0):return (st.x-margin,st.y-margin,st.x+st.w+margin,st.y+st.h+margin)

def overlap_with_card(layer,st,margin=24,thresh=24):
 """Pixels of an RGBA graphics/caption layer that sit under the card (+margin). Used by the preview to warn."""
 if st.opacity<=.004:return 0
 x0,y0,x1,y1=[int(v) for v in card_rect(st,margin)];x0,y0=max(0,x0),max(0,y0)
 a=np.asarray(layer.getchannel('A').crop((x0,y0,min(W,x1),min(H,y1))))
 return int((a>thresh).sum())

def estimate_face(cam):
 """Rough face centre (cx,cy) in source pixels from a skin-tone mask (numpy only): mean of the skin pixels in the
 forehead-to-chin band (neck and shirt excluded). Always eyeball-check the result on composited frames."""
 q=4;a=np.asarray(cam).astype(int)[::q,::q];r,g,b=a[...,0],a[...,1],a[...,2];hh=a.shape[0]
 m=(r>95)&(g>50)&(b>30)&(r-g>18)&(r-g<90)&(r>b)&(g>=b-5)&(np.abs(g-b)<70)
 m[int(hh*.80):]=False
 if m.sum()<200:return None
 cs=np.convolve(m.sum(0).astype(float),np.ones(25)/25,'same');px=int(cs.argmax());lo,hi=max(0,px-50),px+50
 ys,xs=np.nonzero(m[:,lo:hi]);top=int(np.percentile(ys,3));band=m[top:top+int(hh*.34),lo:hi];ys,xs=np.nonzero(band)
 return float((xs.mean()+lo)*q),float((ys.mean()+top)*q)
if __name__=='__main__':
 # python3 lib/layout.py facecx sections/NN/voice.mkv [step_s=1]  -> per-sample estimates + a smoothed FACE_CX keyframe list
 import sys,subprocess,json
 if len(sys.argv)>=3 and sys.argv[1]=='facecx':
  src=sys.argv[2];d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
  j=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',src]))['streams'][0]
  step=float(sys.argv[3]) if len(sys.argv)>3 else 1.;ts=list(np.arange(step/2,d,step));xs=[]
  for t in ts:
   buf=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',src,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
   f=estimate_face(np.frombuffer(buf,np.uint8).reshape(j['height'],j['width'],3));xs.append(f[0] if f else np.nan);print(f't={t:7.2f}s face={f}')
  xs=np.array(xs);xs[np.isnan(xs)]=np.nanmedian(xs);sm=np.convolve(np.pad(xs,1,mode='edge'),[.25,.5,.25],'valid')
  print('FACE_CX='+str([(round(float(t),2),int(round(x))) for t,x in zip(ts,sm)]))
 else:print(__doc__)
