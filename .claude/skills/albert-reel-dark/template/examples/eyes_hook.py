"""ACCEPTED EXAMPLE (Freebuff reel, Sept 2026) — the animated eyes-emoji hook Albert asked for and kept.
No-face hook: the eyes pop in, look left, blink, look right over the first spoken phrase, then shrink up out of the way and
WATCH each icon land on its spoken name; blink on a later word, widen on the payoff word.

Why it is redrawn: Apple Color Emoji only ships a ~155 px bitmap, which is mush at 500 px. `eyes(lx,ly,blink)` rebuilds
it 1:1 at 2x: white oval with soft grey edge shading, brown->gold iris gradient with a dark rim, dark pupil, white glint,
iris clipped by the eye shape. lx -1..1 (the shipped emoji is lx=-1), ly 0..1 looks down, blink 0..1 squashes the eye.
`_track()` gives snappy 0.14 s saccades that END on their key time (eyes move before the thing they look at).
Rules that came out of review: never show empty slot outlines before an icon lands; icons land on their own names
(lead 0.13 s); keep the eyes alive for the whole beat; first music hit / beat drop goes on the first icon landing.
"""
from draw import *
import sys,numpy as np
sys.path.insert(0,str(P/'helpers'))
def clip(p,r=16):
 m=Image.new('L',p.size);ImageDraw.Draw(m).rounded_rectangle((0,0,p.width-1,p.height-1),r,fill=255)
 p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel('A')),np.array(m))));return p
def diamond(im,x,y,r,col):ImageDraw.Draw(im).polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=col)

# --- stand-in tile for the demo below; in a project use your own brand tile function (white squircle + real mark) ---
def tile(name,size):return apptile({'OpenAI':'ChatGPT','DeepSeek':'Claude','Zai':'Notion'}.get(name,name),int(size))
# ---------- hook (full): the eyes emoji looks left and right, then watches the three model marks land ----------
from PIL import ImageFilter
@lru_cache(None)
def _eye_white(q=2):
 """One eye of the Apple eyes emoji, redrawn at high resolution: white oval with soft grey edge shading."""
 w,h=285*q,480*q;m=Image.new('L',(w,h));ImageDraw.Draw(m).ellipse((2,2,w-3,h-3),fill=255)
 im=Image.new('RGBA',(w,h),'#85858B');core=Image.new('L',(w,h));ImageDraw.Draw(core).ellipse((26*q,30*q,w-26*q,h-30*q),fill=255);core=core.filter(ImageFilter.GaussianBlur(20*q))
 im.paste(Image.new('RGBA',(w,h),'white'),(0,0),core);im.putalpha(m);return im,m
@lru_cache(None)
def _iris(q=2):
 d=168*q;im=blank(d,d);g=Image.linear_gradient('L').resize((d,d))
 col=Image.composite(Image.new('RGBA',(d,d),'#F7BE00'),Image.new('RGBA',(d,d),'#5B2A00'),g);m=Image.new('L',(d,d));ImageDraw.Draw(m).ellipse((0,0,d-1,d-1),fill=255);im.paste(col,(0,0),m)
 rim=blank(d,d);ImageDraw.Draw(rim).ellipse((0,0,d-1,d-1),outline=(70,32,0,200),width=5*q);im.alpha_composite(rim.filter(ImageFilter.GaussianBlur(2*q)))
 p=118*q;o=(d-p)//2;ImageDraw.Draw(im).ellipse((o-4*q,o-2*q,o+p-4*q,o+p-2*q),fill='#2B1200')
 hl=blank(d,d);ImageDraw.Draw(hl).ellipse((22*q,22*q,70*q,70*q),fill='white');im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(1.5*q)));return im
def eyes(lx,ly=0,blink=0,q=2):
 """lx -1 (left, as the emoji ships) .. 1 (right); ly 0 (emoji height) .. 1 (down); blink 0..1."""
 W_,H_=620*q,480*q;out=blank(W_,H_);white,m=_eye_white(q);ir=_iris(q)
 for ex in (0,335*q):
  eye=white.copy();cx=(147+62*lx)*q;cy=(258+70*ly)*q;lay=blank(*eye.size);lay.alpha_composite(ir,(round(cx-ir.width/2),round(cy-ir.height/2)))
  lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel('A')),np.array(m))));eye.alpha_composite(lay)
  if blink>0:
   hh=max(8,round(eye.height*(1-.92*blink)));eye=eye.resize((eye.width,hh),Image.Resampling.BILINEAR);out.alpha_composite(eye,(ex,(H_-hh)//2))
  else:out.alpha_composite(eye,(ex,0))
 return out
def _track(t,keys):
 """Piecewise eased value through (time,value) keys; each move takes .14 s and ends on its key time."""
 v=keys[0][1]
 for (t1,v1) in keys[1:]:
  if t>=t1:v=v1
  elif t>t1-.14:v=lerp(v,v1,smooth((t-(t1-.14))/.14));break
  else:break
 return v
def hook(t,S,at):
 im=Image.new('RGBA',(W,H),BG);free=at('hook','free.',6.92)-.10;comp=at('hook','completely',5.96)
 ons=[at('hook','GPT',1.12)-.13,at('hook','DeepSeek',2.60)-.13,at('hook','GLM',4.34)-.13]
 names=[('OpenAI','GPT-5.6','OpenAI'),('DeepSeek','DeepSeek 4.1','DeepSeek'),('Zai','GLM 5.3','Z.ai')]
 xs=[195,540,885];cy=620;sz=290
 # eyes: left, right, then up and out of the way to watch each mark land
 up=smooth((t-(ons[0]-.22))/.3)
 lx=_track(t,[(0,-1),(.46,1),(ons[0]-.02,-.85),(ons[1]+.02,0),(ons[2]+.02,.85),(free+.05,0)]);ly=_track(t,[(0,0),(ons[0]-.02,1),(free+.05,.15)])
 bl=0
 for bt in (.38,comp+.1):
  if bt-.07<=t<bt+.09:bl=math.sin((t-(bt-.07))/.16*math.pi)
 sc=lerp(.86,.5,up);k=1+(.12*math.sin(min(1,max(0,(t-free)/.36))*math.pi) if t>=free else 0)
 e_=eyes(lx,ly,bl);ew,eh=round(620*sc*k),round(480*sc*k);e_=e_.resize((ew,eh),Image.Resampling.LANCZOS);pop=spring(t/.3)
 place(im,e_,540-ew/2,lerp(560,250,up)-eh/2,scale=max(.05,pop),opacity=min(1,t*12))
 for i,(tn,nm,mk) in enumerate(names):
  a=t-ons[i]
  if a<0:continue
  v=spring(a/.28);bob=math.sin((t-ons[i])*2.6+i)*7;jump=0;kk=1
  if t>=comp:ja=t-comp-i*.12;jump=70*math.sin(min(1,max(0,ja/.34))*math.pi)
  if t>=free:fa=t-free-i*.07;kk=1+.14*math.sin(min(1,max(0,fa/.36))*math.pi)
  place(im,tile(tn,sz),xs[i]-sz/2,cy-sz/2-160*(1-ease(a/.22))+bob-jump,scale=max(.05,(.7+.3*v)*kk),opacity=min(1,a*9),sh=True)
  la=ease((a-.12)/.25)
  if la>0:
   txt(im,nm,xs[i],cy+sz/2+44+10*(1-la),38,(29,29,31,int(255*la)),True,'Semibold');txt(im,mk,xs[i],cy+sz/2+96+10*(1-la),26,(110,110,115,int(255*la)),True)
 return im


if __name__=='__main__':
 at=lambda beat,word,default=0,nth=0:default
 ts=[.15,.4,.6,1.05,3.0,7.0];sheet=Image.new('RGB',(len(ts)*270,480),'#DDD')
 for i,t in enumerate(ts):sheet.paste(hook(t,{},at).convert('RGB').resize((270,480)),(i*270,0))
 sheet.save(Path(__file__).with_name('eyes_hook_strip.jpg'));print('ok')
