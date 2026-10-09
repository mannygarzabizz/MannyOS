"""Freebuff reel scene visuals. Recreated UI (no screenshots), real brand marks, Apple-styled chrome.
Every timestamp is local to the beat. Product-true copy: freebuff.com (free hours per day by model, $/yr comparison,
CLI demo lines, sample sponsored line), the Codebuff CLI ad-banner component (card layout: bold headline + "Ad",
muted description, inverted CTA + underlined domain, border tints on hover) and chatgpt.com/pricing (Free $0, Go $8,
Plus $20, Pro from $100, feature lists). The terminal session and the two site.com ads are illustrative animations."""
from draw import *
import sys,random,numpy as np
sys.path.insert(0,str(P/'helpers'))
from pointer_motion import motion
import instagram_comment as ig
ig.font=lambda n:sf(n)

FG='#2C7A40';FGL='#54A967';TBG='#0B0B0D';TFG='#E8E8EC';TMU='#85858F';TLINE='#2A2A30';DEEP='#1E8E3E'
def mono(n,weight='Regular'):return sf(n,weight,True)
def clip(p,r=16):
 m=Image.new('L',p.size);ImageDraw.Draw(m).rounded_rectangle((0,0,p.width-1,p.height-1),r,fill=255)
 p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel('A')),np.array(m))));return p
def sq(im):
 im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(squircle_mask(im.width)))));return im

# ---------- real brand tiles ----------
MARKS={'OpenAI':('openai','white',.64),'ChatGPT':('ChatGPT','white',.66),'DeepSeek':('lobe-deepseek-color','white',.70),'Zai':('lobe-zai','white',.56),
 'Meta':('lobe-meta-color','white',.68),'MiMo':('lobe-xiaomimimo','white',.66),'Upstage':('lobe-upstage-color','white',.62),
 'ClaudeCode':('lobe-claudecode-color','white',.66),'Codex':('lobe-codex-color',None,1),'Cursor':('lobe-cursor','white',.62),
 'Devin':('lobe-devin-color','white',.64),'OpenCode':('lobe-opencode','white',.58),'Freebuff':('FreebuffFill',None,1)}
@lru_cache(None)
def tile(name,size):
 if name=='Claude':return apptile('Claude',size)
 ic,bg,frac=MARKS[name];size=int(size);im=blank(size,size)
 if bg is None:
  m=icon(ic,size)
  if name=='Codex':ImageDraw.Draw(im).rectangle((0,0,size,size),fill='white')
  if name=='Freebuff':ImageDraw.Draw(im).rectangle((0,0,size,size),fill='black')
  im.alpha_composite(m)
 else:
  ImageDraw.Draw(im).rectangle((0,0,size,size),fill=bg);k=round(size*frac);im.alpha_composite(icon(ic,k),((size-k)//2,(size-k)//2))
 im=sq(im)
 if name!='Freebuff':
  ring=blank(size,size);ImageDraw.Draw(ring).rectangle((0,0,size,size),fill=(0,0,0,26));ring=sq(ring)
  inner=sq(Image.new('RGBA',(size-2,size-2),(0,0,0,255)));hole=blank(size,size);hole.alpha_composite(inner,(1,1))
  ring.putalpha(Image.fromarray(np.clip(np.array(ring.getchannel('A')).astype(int)-np.array(hole.getchannel('A')).astype(int),0,255).astype('uint8')));im.alpha_composite(ring)
 return im
MODELS=[('OpenAI','GPT-5.6 Luna',5),('DeepSeek','DeepSeek V4.1 Flash',6),('Meta','Muse Spark 1.2',6),('MiMo','MiMo 2.5',10),('Upstage','Solar Pro 4',10),('Zai','GLM 5.3 Flash',20)]

def term(w,h,title,bar=44,r=16):
 p=blank(w,h);rr(p,(0,0,w-1,h-1),TBG,r);rr(p,(0,0,w-1,bar+r),'#1B1B20',r);ImageDraw.Draw(p).rectangle((0,bar,w-1,bar+r),fill=TBG)
 ImageDraw.Draw(p).rectangle((0,bar,w-1,bar),fill=TLINE)
 for i,c in enumerate(['#FF5F57','#FEBC2E','#28C840']):ImageDraw.Draw(p).ellipse((18+i*22,bar/2-7,32+i*22,bar/2+7),fill=c)
 txt(p,title,w/2,bar/2-9,16,'#B9B9C0',True,'Medium');return p
def diamond(im,x,y,r,col):ImageDraw.Draw(im).polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=col)
def spinner(im,x,y,r,t,col=FGL,width=4):
 a=(t*420)%360;ImageDraw.Draw(im).arc((x-r,y-r,x+r,y+r),a,a+250,fill=col,width=width)
def adcard(w,head,desc,cta,domain,hover=False,n=22,inline=False):
 """Freebuff CLI ad card as ad-banner.tsx draws it: single-line border (muted, primary on hover), bold headline with the
 'Ad' disclosure on the right, muted description, inverted CTA box and underlined domain."""
 lh=round(n*1.55);rows=2 if inline else 3;h=lh*rows+30;c=blank(w,h);col=FGL if hover else '#5C5C66'
 rr(c,(1,1,w-2,h-2),(84,169,103,22) if hover else (255,255,255,5),6,col,2)
 txt(c,head,20,15,n,FGL if hover else TFG,weight='Bold',mono=True);txt(c,'Ad',w-20-mono(n).getlength('Ad'),15,n,TMU,mono=True)
 txt(c,desc,20,15+lh,n,TMU,mono=True)
 if inline:
  s=domain+' ↗';x=w-20-mono(n).getlength(s);txt(c,s,x,15+lh,n,col if hover else TMU,mono=True);ImageDraw.Draw(c).line([(x,15+lh+n+5),(x+mono(n).getlength(domain),15+lh+n+5)],fill=col if hover else TMU,width=2)
 else:
  s=f' {cta} ';bw=mono(n,'Bold').getlength(s);y=15+lh*2;ImageDraw.Draw(c).rectangle((20,y-2,20+bw,y+n+8),fill=FGL if hover else '#8A8A94');txt(c,s,20,y,n,'#0B0B0D',weight='Bold',mono=True)
  x=20+bw+14;txt(c,domain,x,y,n,TMU,mono=True);ImageDraw.Draw(c).line([(x,y+n+5),(x+mono(n).getlength(domain),y+n+5)],fill=TMU,width=2)
 return c
ADS=[('Ship faster with Vercel.','Deploy your app in seconds.','Learn more','vercel.com'),
 ('Postgres in one command','Branch, scale to zero, connect from anywhere.','Try it free','db.site.com'),
 ('Error tracking for small teams','Catch errors early.','Start free','logs.site.com')]

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

# ---------- how (split): a receipt prints out, every line is $0.00 ----------
def txm(im,s_,x,cy,n,color=INK,weight='Regular',mono_=False,right=False):
 """Text vertically centred on cy (anchor middle), left- or right-aligned at x."""
 ImageDraw.Draw(im).text((round(x),round(cy)),s_,font=sf(n,weight,mono_),fill=color,anchor='rm' if right else 'lm')
RECEIPT=[('GPT-5.6 Luna','OpenAI'),('DeepSeek V4.1 Flash','DeepSeek'),('GLM 5.3 Flash','Zai')]
def how(t,S,at,w=940,h=560):
 p=blank(w,h);pos=at('how','possible?',1.41)-.1;pw,ph=520,620
 # printer slot
 rr(p,(w/2-310,0,w/2+310,54),'#1D1D1F',20);rr(p,(w/2-280,30,w/2+280,44),'#000000',7)
 out=ease(t/1.25);vis=round(40+(ph-120)*out)      # how much paper has come out
 paper=blank(pw,ph);ImageDraw.Draw(paper).rectangle((0,0,pw,ph),fill='white')
 y=ph-40
 # content is laid out from the bottom edge (first printed) upward, so it scrolls down as it prints
 rows=[('hdr',None)]+[('row',r) for r in RECEIPT]+[('tot',None)]
 yy=ph-70
 txm(paper,'freebuff',32,yy,30,INK,'Bold');txm(paper,'receipt',pw-32,yy,22,GRAY,right=True);yy-=44
 for k in range(0,pw-64,18):ImageDraw.Draw(paper).line([(32+k,yy),(32+k+9,yy)],fill='#C7C7CC',width=2)
 yy-=52
 for nm,tn in RECEIPT:
  paper.alpha_composite(tile(tn,48),(32,yy-24));txm(paper,nm,96,yy,25,INK,'Medium');txm(paper,'$0.00',pw-32,yy,27,INK,'Semibold',True,True);yy-=76
 yy+=18
 for k in range(0,pw-64,18):ImageDraw.Draw(paper).line([(32+k,yy),(32+k+9,yy)],fill='#C7C7CC',width=2)
 yy-=56;txm(paper,'Total',32,yy,34,INK,'Bold')
 if t>=pos:
  a=t-pos;v=spring(a/.28);tot=blank(240,80);ImageDraw.Draw(tot).text((232,40),'$0.00',font=sf(52,'Bold'),fill=DEEP,anchor='rm');place(paper,tot,pw-32-240,yy-40,scale=max(.05,v),opacity=min(1,a*9))
 # zig-zag torn bottom edge
 d=ImageDraw.Draw(paper)
 for k in range(0,pw,26):d.polygon([(k,ph),(k+13,ph-14),(k+26,ph)],fill=(0,0,0,0))
 strip=paper.crop((0,ph-vis,pw,ph));jit=math.sin(t*38)*1.6*(1-out)
 place(p,strip,w/2-pw/2+jit,40,sh=True)
 rr(p,(w/2-310,0,w/2+310,40),'#1D1D1F',20);ImageDraw.Draw(p).rectangle((w/2-310,20,w/2+310,40),fill='#1D1D1F')
 ImageDraw.Draw(p).ellipse((w/2+250,12,w/2+266,28),fill=GREEN if int(t*6)%2 or out>=1 else '#2C2C2E')
 return p

# ---------- pay (full): the card is refused, ads are the payment method ----------
@lru_cache(None)
def credit_card(w=660,h=410):
 c=blank(w,h);g=Image.linear_gradient('L').resize((w,h)).rotate(35,expand=False)
 base=Image.composite(Image.new('RGBA',(w,h),'#3B3B42'),Image.new('RGBA',(w,h),'#111114'),g);c.alpha_composite(base);c=clip(c,36);d=ImageDraw.Draw(c)
 rr(c,(56,120,156,196),'#D9B45B',14);d.line([(56,158),(156,158)],fill='#A8863A',width=2);d.line([(106,120),(106,196)],fill='#A8863A',width=2);d.rounded_rectangle((84,140,128,176),8,outline='#A8863A',width=2)
 for i in range(3):d.arc((w-150-i*0,112-i*14+i*14,w-150+44+i*22,156+i*0+44),-50,50,fill='#C9C9D2',width=5) if False else d.arc((w-170+i*20,118-i*12,w-130+i*20,198+i*12),-48,48,fill='#C9C9D2',width=5)
 txt(c,'••••  ••••  ••••  ••••',56,246,40,'#EDEDF2',mono=True);txt(c,'CREDIT CARD',56,334,22,'#9A9AA6',weight='Medium',tracking=3);txt(c,'••/••',w-56-mono(26).getlength('••/••'),330,26,'#C9C9D2',mono=True)
 return c
def payrow(w,icon_kind,title,sub,state,v=1):
 """state: 'idle' | 'off' | 'on'; v animates the strike-through."""
 r=blank(w,124);on=state=='on';rr(r,(0,0,w-1,123),'#EAF6EE' if on else 'white',24,DEEP if on else '#E1E1E6',4 if on else 1);d=ImageDraw.Draw(r)
 rr(r,(28,30,92,94),'#F2F2F4' if not on else 'white',16)
 if icon_kind=='card':
  d.rounded_rectangle((40,46,80,78),6,outline='#6E6E73',width=3);d.rectangle((41,54,79,60),fill='#6E6E73')
 else:
  d.rounded_rectangle((38,44,82,80),6,outline=DEEP,width=3);d.text((60,62),'Ad',font=sf(20,'Bold'),fill=DEEP,anchor='mm')
 col='#B0B0B6' if state=='off' else INK;f=sf(32,'Semibold');d.text((116,44),title,font=f,fill=col,anchor='lm');d.text((116,84),sub,font=sf(22),fill='#B0B0B6' if state=='off' else GRAY,anchor='lm')
 if state=='off':
  bb=d.textbbox((116,44),title,font=f,anchor='lm');xb=d.textbbox((116,44),'x',font=f,anchor='ls');my=bb[3]-(d.textbbox((0,0),'x',font=f,anchor='ls')[3]-d.textbbox((0,0),'x',font=f,anchor='ls')[1])/2
  base=d.textbbox((116,44),'x',font=f,anchor='lm');my=(base[1]+base[3])/2
  d.line([(bb[0]-4,my),(bb[0]-4+(bb[2]-bb[0]+8)*v,my)],fill='#8E8E93',width=3)
 cx=w-64
 if on:checkmark(r,cx,62,22,DEEP)
 else:d.ellipse((cx-22,40,cx+22,84),outline='#C7C7CC',width=3)
 return r
def scissors(open_deg,size=300):
 """Scissors pointing right; pivot at the image centre."""
 S_=size*2;im=blank(S_,S_);c=S_/2
 for sign in (1,-1):
  lay=blank(S_,S_);d=ImageDraw.Draw(lay)
  d.polygon([(c-10,c-9),(c+size*.78,c-2),(c+size*.78,c+3),(c-10,c+11)],fill='#C9CBD1');d.line([(c-10,c+10),(c+size*.78,c+3)],fill='#8E9097',width=3)
  d.line([(c,c),(c-size*.34,c+size*.13)],fill='#1D1D1F',width=20);hx,hy=c-size*.52,c+size*.20;r=size*.17
  d.ellipse((hx-r,hy-r*.8,hx+r,hy+r*.8),outline=RED,width=20)
  if sign==-1:lay=lay.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  im.alpha_composite(lay.rotate(sign*open_deg/2,resample=Image.Resampling.BICUBIC,center=(c,c)))
 ImageDraw.Draw(im).ellipse((c-9,c-9,c+9,c+9),fill='#6E6E73');return im
def pay(t,S,at):
 im=Image.new('RGBA',(W,H),BG);card=at('pay','card.',1.04);inst=at('pay','Instead,',1.48)-.05;p2=at('pay','pay',2.18,1)-.13;ads=at('pay','ads.',3.08)
 cw,ch=660,410;cx,cy=540,440;c0=card-.52;c1=card+.02      # the cut runs left to right and finishes on "card"
 if t<inst+.75:
  e=spring(t/.34);prog=max(0,min(1,(t-c0)/(c1-c0)));cutx=round(cw*prog);cardim=credit_card()
  base_y=cy-ch/2+60*(1-ease(t/.3));op=min(1,t*8)
  if prog<1:
   im2=cardim.copy()
   if cutx>0:ImageDraw.Draw(im2).rectangle((0,ch/2-2,cutx,ch/2+2),fill=(0,0,0,0))
   place(im,im2,cx-cw/2,base_y,scale=max(.05,.8+.2*e),opacity=op,sh=True,rot=-6+6*ease(t/.4))
  else:
   a=max(0,t-c1);gap=10*ease(a/.2);fall=0;r1=r2=0;o=1
   if t>=inst:b=t-inst;fall=1900*b*b;r1=-40*b;r2=34*b;o=max(0,1-b/.6)
   top=cardim.crop((0,0,cw,ch//2-2));bot=cardim.crop((0,ch//2+2,cw,ch))
   place(im,top,cx-cw/2-gap*.6-260*max(0,t-inst),base_y-gap+fall*.55,opacity=o,sh=True,rot=r1+2*ease(a/.2))
   place(im,bot,cx-cw/2+gap*.6+220*max(0,t-inst),base_y+ch/2+2+gap+fall,opacity=o,sh=True,rot=r2-2*ease(a/.2))
  # scissors travel along the cut line, snipping
  if c0-.35<=t<c1+.45:
   sx=lerp(cx-cw/2-420,cx-cw/2-150,ease((t-(c0-.35))/.35)) if t<c0 else cx-cw/2-150+cw*prog+(520*ease((t-c1)/.45) if t>c1 else 0)
   od=26+22*math.sin((t-c0)*2*math.pi*3.2) if c0<=t<=c1 else 40
   so=min(1,(t-(c0-.35))*8)*(1-ease((t-c1-.15)/.3) if t>c1+.15 else 1)
   sc=scissors(od);place(im,sc,sx-300+60,cy-300+60*(1-ease(t/.3))*0,opacity=so)
 if t>=inst+.12:
  a=t-inst-.12;e=ease(a/.32);sh_=blank(900,560);rr(sh_,(0,0,899,559),'white',36);txt(sh_,'Pay with',40,36,40,INK,weight='Bold')
  pressed=t>=ads
  place(sh_,payrow(820,'card','Credit card','Not required','off' if t>=p2 else 'idle',ease((t-p2)/.25)),40,112)
  ra=ease((t-p2)/.28)
  if ra>0:place(sh_,payrow(820,'ads','Ads','Small text ads between agent turns','on' if pressed else 'idle'),40,256+16*(1-ra),opacity=ra)
  if pressed:
   b=t-ads;v=spring(b/.28);line(sh_,[(40,420),(860,420)],'#EBEBEF',2);txt(sh_,'Total',40,458,34,INK,weight='Semibold');s_='$0.00';tot=blank(260,90);txt(tot,s_,250-tw(s_,60,'Bold'),6,60,DEEP,weight='Bold');place(sh_,tot,600,440,scale=max(.05,v),opacity=min(1,b*9))
  motion(sh_,t,points=[(p2+.05,760,520),(ads-.04,800,318),(ads+.3,800,318),(ads+.8,700,500)],clicks=[ads],end=ads+1.3)
  place(im,sh_,90,170+40*(1-e),scale=.95+.05*e,opacity=e,sh=True)
 return im

# ---------- called (split): dock, the Freebuff tile springs in ----------
def called(t,S,at):
 im=Image.new('RGBA',(W,H),BG);fb=at('called','Freebuff,',.66)-.13
 names=['Claude','ChatGPT','Cursor','Freebuff'];ons=[.04,.12,.20,fb];xs=[255,445,635,825]
 bar=blank(800,160);rr(bar,(0,0,799,159),(255,255,255,190),38,(0,0,0,28),1);e=ease(t/.28);place(im,bar,140,500+30*(1-e),opacity=e,sh=True)
 for i,n in enumerate(names):
  if t<ons[i]:continue
  a=t-ons[i];last=i==3;s=1+.5*spring(a/.26) if last else 1;lift=70*spring(a/.26) if last else 0
  place(im,tile(n,140),xs[i]-70,580-70-lift-(140*s-140)/2,scale=s if last else max(.05,spring(a/.26)),opacity=min(1,a*7),sh=True)
  ImageDraw.Draw(im).ellipse((xs[i]-4,646,xs[i]+4,654),fill='#3A3A3C')
 if t>=fb+.12:
  a=t-fb-.12;v=spring(a/.28);lab=blank(520,250);ImageDraw.Draw(lab).text((260,70),'freebuff',font=sf(112,'Bold'),fill=INK,anchor='mm');la=ease((a-.18)/.25)
  if la>0:txt(lab,'The free coding agent',260,150+10*(1-la),38,(110,110,115,int(255*la)),True)
  place(im,lab,280,120+20*(1-ease(a/.3)),scale=.9+.1*max(.05,v),opacity=min(1,a*8))
 return im

# ---------- agent (split): the CLI session from freebuff.com, beside Claude Code and Codex ----------
def agent(t,S,at,w=940,h=560):
 p=blank(w,h);cc=at('agent','Claude',1.67)-.13;cx_=at('agent','Codex.',2.71)-.13
 tw_=640;tm=term(tw_,h,'freebuff — zsh');y=70
 diamond(tm,34,y+14,10,FGL);txt(tm,'freebuff',54,y,24,TFG,weight='Bold',mono=True);txt(tm,'GLM 5.3 Flash · ~/my-app',54+mono(24,'Bold').getlength('freebuff')+16,y+3,19,TMU,mono=True)
 cmd='add google login to my app';k=int(max(0,t-.25)/.028);txt(tm,'›',26,y+63,26,FGL,mono=True);txt(tm,cmd[:k],54,y+57,26,TFG,mono=True)
 if k<len(cmd) and int(t*5)%2==0:ImageDraw.Draw(tm).rectangle((54+mono(26).getlength(cmd[:k])+3,y+58,54+mono(26).getlength(cmd[:k])+16,y+86),fill=TFG)
 steps=[('Read 142 files · mapped the auth flow',''),('Edit src/auth/google.ts','+24 -3'),('Edit login-button.tsx','+8 -1'),('code-reviewer subagent · looks good','')]
 t0=.25+len(cmd)*.028+.1
 for i,(s,diff) in enumerate(steps):
  a=t-t0-i*.34
  if a<0:
   if a>-.34:spinner(tm,36,y+128+i*56+13,10,t)
   break
  v=ease(a/.2);yy=y+128+i*56;txt(tm,'✓',26,yy,24,(84,169,103,int(255*v)),mono=True);wd=txt(tm,s,58,yy+1,23,(232,232,236,int(255*v)),mono=True)
  if diff:
   a_,b_=diff.split(' ');txt(tm,a_,58+wd+14,yy+1,23,FGL,mono=True);txt(tm,b_,58+wd+14+mono(23).getlength(a_+' '),yy+1,23,'#E5534B',mono=True)
 da=t-t0-4*.34
 if da>0:
  v=ease(da/.25);txt(tm,'Done in 11s · 2 files changed',26,y+356,22,(133,133,143,int(255*v)),mono=True)
  ImageDraw.Draw(tm).line([(26,y+400),(tw_-26,y+400)],fill=TLINE,width=1);txt(tm,'— sponsored —',26,y+414,20,(133,133,143,int(255*v)),mono=True);txt(tm,'Ship faster with Vercel.',26,y+446,22,(232,232,236,int(255*v)),mono=True);txt(tm,'vercel.com',26+mono(22).getlength('Ship faster with Vercel. '),y+446,22,(84,169,103,int(255*v)),mono=True)
 place(p,clip(tm,16),0,0,sh=False)
 for i,(n,lab,t1) in enumerate([('ClaudeCode','Claude Code',cc),('Codex','Codex',cx_)]):
  a=t-t1
  if a<0:continue
  v=spring(a/.28);yy=40+i*262;place(p,tile(n,170),705+40,yy-40*(1-ease(a/.22)),scale=max(.05,.7+.3*v),opacity=min(1,a*9),sh=True)
  la=ease((a-.1)/.22);txt(p,lab,830,yy+184,30,(29,29,31,int(255*la)),True,'Semibold')
 return p

# ---------- price (full): chatgpt.com/pricing, recreated; camera pushes in on Pro ----------
PLANS=[('Free','Intelligence for everyday tasks','$0','Get Free',None,['Unlimited text chats with GPT-5.6 Luna','Limited messages with uploads','Limited and slower image generation','Limited voice chats','Limited deep research','Limited memory and context','Limited Codex access']),
 ('Go','Expanded access','$8','Get Go','Everything in Free and:',['More messages with tools','More uploads','More image creation','More voice chats','Longer memory']),
 ('Plus','Do more with advanced intelligence','$20','Get Plus','Everything in Go and:',['Advanced reasoning models with GPT-6 Astra and GPT-5.6','Expanded messages and uploads','More complex and accurate image creation','Expanded deep research','Expanded memory and context']),
 ('Pro','Maximize your productivity','$100','Get Pro','Everything in Plus and:',['5x more usage','Pro reasoning powered by GPT-6 Astra','Maximum Codex tasks','Unlimited and faster image creation','Maximum deep research','Maximum memory and context'])]
K=2;PW,PH=2000,1480;CARDX=[268,641,1014,1387];CARDW=345;CARDY=540
def wrapsf(s,n,width):
 out=[];cur=''
 for w_ in s.split(' '):
  c=(cur+' '+w_).strip()
  if tw(c,n)>width and cur:out.append(cur);cur=w_
  else:cur=c
 return out+[cur]
CODEX_ROW={}
@lru_cache(None)
def pricing_page():
 p=Image.new('RGBA',(PW*K,PH*K),'white');d=ImageDraw.Draw(p);k=K
 p.alpha_composite(icon('openai',34*k),(32*k,22*k));txt(p,'ChatGPT',74*k,26*k,22*k,INK,weight='Bold')
 for i,s in enumerate(['About','Features','Learn','Codex','Business','Pricing','Download']):txt(p,s,(716+i*92)*k,30*k,15*k,'#3A3A3C')
 rr(p,(1762*k,18*k,1828*k,54*k),'#0D0D0D',18*k);txt(p,'Log in',1795*k,27*k,15*k,'white',True,'Medium');rr(p,(1838*k,18*k,1966*k,54*k),'white',18*k,'#D9D9DE',k);txt(p,'Sign up for free',1902*k,27*k,15*k,INK,True,'Medium')
 txt(p,'ChatGPT',1000*k,182*k,15*k,'#3A3A3C',True);txt(p,'Pricing',1000*k,226*k,66*k,'#0D0D0D',True,'Medium');txt(p,'See pricing for our individual, business, and enterprise plans.',1000*k,340*k,17*k,'#1D1D1F',True)
 rr(p,(734*k,446*k,1266*k,504*k),'#ECECEC',16*k,'#DADADA',k);rr(p,(741*k,452*k,998*k,498*k),'white',12*k);txt(p,'Individual',880*k,465*k,15*k,INK,True,'Semibold');txt(p,'Business & Enterprise',1132*k,465*k,15*k,'#8E8E93',True,'Medium')
 for ci,(name,tag,price,btn,every,feats) in enumerate(PLANS):
  x=CARDX[ci];rr(p,(x*k,CARDY*k,(x+CARDW)*k,(PH+40)*k),'white',10*k,'#E8E8EA',k)
  txt(p,name,(x+18)*k,(CARDY+22)*k,30*k,'#0D0D0D',weight='Medium');txt(p,tag,(x+18)*k,(CARDY+64)*k,17*k,'#1D1D1F')
  if name=='Pro':txt(p,'From',(x+18)*k,(CARDY+122)*k,15*k,'#6E6E73')
  else:
   wd=txt(p,price,(x+18)*k,(CARDY+146)*k,50*k,'#0D0D0D',weight='Semibold',tracking=-k);txt(p,'/ month',(x+18)*k+wd+8*k,(CARDY+174)*k,14*k,'#6E6E73')
  rr(p,((x+18)*k,(CARDY+222)*k,(x+CARDW-18)*k,(CARDY+266)*k),'#0D0D0D',22*k);txt(p,btn+'  ›',(x+CARDW/2)*k,(CARDY+235)*k,14*k,'white',True,'Medium')
  y=CARDY+292
  if every:
   diamond(p,(x+26)*k,(y+9)*k,6*k,'#0D0D0D');txt(p,every,(x+50)*k,y*k,14*k,'#0D0D0D',weight='Semibold');d.line([((x+18)*k,(y+32)*k),((x+CARDW-18)*k,(y+32)*k)],fill='#ECECEE',width=k);y+=58
  for f_ in feats:
   ls=wrapsf(f_,14*k,(CARDW-72)*k);line(p,[((x+20)*k,(y+9)*k),((x+25)*k,(y+14)*k),((x+34)*k,(y+3)*k)],'#0D0D0D',round(1.6*k))
   if 'Codex tasks' in f_:CODEX_ROW['box']=(x+12,y-8,x+CARDW-12,y+26)
   for li,l_ in enumerate(ls):txt(p,l_,(x+54)*k,(y+li*22)*k,14*k,'#1D1D1F')
   y+=35+22*(len(ls)-1)
 return p
def price(t,S,at):
 im=Image.new('RGBA',(W,H),BG);pay_=at('price','paying',.85);hund=at('price','$100',1.13);month=at('price','month',1.69);cdx=at('price','Codex,',2.65)
 e=ease(t/.3)
 if e<=0:return im
 page=pricing_page();vw,vh=1000,740
 full=(228,150,1772,150+1544*vh/vw);px=CARDX[3];pro=(px+CARDW/2-290,CARDY-16,px+CARDW/2+290,CARDY-16+580*vh/vw);pro2=(pro[0],pro[1]+118,pro[2],pro[3]+118)
 z=smooth((t-pay_+.1)/.6);z2=smooth((t-(cdx-.55))/.45);box=[lerp(lerp(full[i],pro[i],z),pro2[i],z2) for i in range(4)]
 # slow drift while wide
 crop=page.crop(tuple(round(v*K) for v in box)).resize((vw,vh),Image.Resampling.LANCZOS);sc=vw/(box[2]-box[0])
 def X(x):return (x-box[0])*sc
 def Y(y):return (y-box[1])*sc
 # cards arrive left to right in the wide shot
 for ci in range(4):
  a=1-ease((t-.18-ci*.09)/.3)
  if a>0:lay=blank(vw,vh);ImageDraw.Draw(lay).rectangle((X(CARDX[ci]-4),Y(CARDY-4),X(CARDX[ci]+CARDW+4),vh),fill=(255,255,255,int(255*a)));crop.alpha_composite(lay)
 # Pro price counts up to land on "$100"
 v=ease((t-(hund-.22))/.34);val=round(100*v);s=f'${val}';n=50*sc;wd=txt(crop,s,X(px+18),Y(CARDY+146),n,'#0D0D0D',weight='Semibold',tracking=-sc)
 mcol='#0D0D0D' if month<=t<month+.5 else '#6E6E73';txt(crop,'/ month',X(px+18)+wd+8*sc,Y(CARDY+174),14*sc,mcol,weight='Semibold' if mcol=='#0D0D0D' else 'Regular')
 if t>=hund-.02:
  a=t-hund+.02;u=ease(a/.25);lay=blank(vw,vh);ImageDraw.Draw(lay).rounded_rectangle((X(px+8),Y(CARDY+112),X(px+CARDW-8),Y(CARDY+206)),10*sc,outline=(255,59,48,int(230*u)),width=max(2,round(3*sc)));crop.alpha_composite(lay)
 if t>=cdx-.05 and 'box' in CODEX_ROW:
  a=t-cdx+.05;u=ease(a/.25);b=CODEX_ROW['box'];lay=blank(vw,vh);ImageDraw.Draw(lay).rounded_rectangle((X(b[0]),Y(b[1]),X(b[0])+(X(b[2])-X(b[0]))*u,Y(b[3])),8*sc,fill=(255,214,10,95));crop.alpha_composite(lay)
 motion(crop,t,points=[(pay_+.2,820,640),(hund+.25,X(px+CARDW/2)+40,Y(CARDY+250)),(cdx-.5,X(px+CARDW/2)+40,Y(CARDY+250)),(cdx+.1,X(px+CARDW-60),Y(CARDY+292+58+35*2+18)+0)],end=9)
 win=window(vw,vh+52,url='chatgpt.com/pricing',r=16);win.alpha_composite(crop,(0,53));win=clip(win,16)
 place(im,win,40,110+24*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 return im

# ---------- free (split): every model, free ----------
def free(t,S,at,w=940,h=560):
 p=blank(w,h);rr(p,(0,0,w-1,h-1),'#0E0E10',20);fr=at('free','free',2.79)-.1
 p.alpha_composite(tile('Freebuff',44),(30,22));txm(p,'Models',90,44,28,TFG,'Semibold');txm(p,'100 Freebucks every day',w-30,44,20,TMU,right=True)
 sel=int(max(0,t-.75)/.24)%6 if t<fr else -1
 for i,(tn,nm,hrs) in enumerate(MODELS):
  a=t-.1-i*.09
  if a<0:continue
  v=ease(a/.26);y=86+i*78;row=blank(w-40,70);fa=t-fr-i*.06;on=i==sel or fa>0
  rr(row,(0,0,w-41,69),'#1D1D22' if on else '#151518',16,FGL if on else '#232328',2 if on else 1);row.alpha_composite(tile(tn,50),(14,10));txm(row,nm,84,35,30,TFG,'Medium')
  cx,cy=w-40-40,35;ImageDraw.Draw(row).ellipse((cx-14,cy-14,cx+14,cy+14),outline=FGL if on else '#4A4A52',width=3)
  if on:
   k=spring(fa/.24) if fa>0 else 1;r_=8*max(.05,k);ImageDraw.Draw(row).ellipse((cx-r_,cy-r_,cx+r_,cy+r_),fill=FGL)
  place(p,row,20+24*(1-v),y,opacity=v)
 return clip(p,20)

# ---------- ads (full): the terminal while it generates, with the real ad-card format ----------
def ads(t,S,at):
 im=Image.new('RGBA',(W,H),BG);look=at('ads','looking',.40);ad=at('ads','ads',.90)-.13;these=at('ads','these',1.42)-.13;gen=at('ads','generating.',2.20)
 e=ease(t/.28)
 if e<=0:return im
 w,h=1000,880;tm=term(w,h,'freebuff — zsh');y=66
 diamond(tm,38,y+15,11,FGL);txt(tm,'freebuff',60,y,26,TFG,weight='Bold',mono=True);txt(tm,'GLM 5.3 Flash · ~/my-app',60+mono(26,'Bold').getlength('freebuff')+18,y+4,20,TMU,mono=True)
 txt(tm,'›',28,y+58,28,FGL,mono=True);txt(tm,'add google login to my app',60,y+53,24,TFG,mono=True)
 hov=t>=look
 c1=adcard(w-56,*ADS[0],hover=hov,n=30);v=ease((t-.12)/.3);place(tm,c1,28,y+110+14*(1-v),opacity=v)
 if t>=ad:
  a=t-ad;v=spring(a/.28);c2=adcard(w-56,*ADS[1],n=30);place(tm,c2,28,y+297+30*(1-ease(a/.25)),scale=.94+.06*max(.05,v),opacity=min(1,a*8))
 if t>=these:
  a=t-these;v=spring(a/.28);c3=adcard(w-56,*ADS[2],inline=True,n=30);place(tm,c3,28,y+484+30*(1-ease(a/.25)),scale=.94+.06*max(.05,v),opacity=min(1,a*8))
 # generating line: spinner, elapsed counter, streaming dots
 gy=h-166;g=t>=gen;spinner(tm,44,gy+16,12,t,FGL,5);s='Generating';txt(tm,s,72,gy,26,FGL if g else TFG,weight='Bold' if g else 'Regular',mono=True);dx=72+mono(26,'Bold' if g else 'Regular').getlength(s)+8
 for q in range(1+int(t*4)%3):ImageDraw.Draw(tm).ellipse((dx+q*14,gy+22,dx+q*14+5,gy+27),fill=TMU)
 el=f'{4+t:4.1f}s · esc to stop';txt(tm,el,w-44-mono(20).getlength(el),gy+4,20,TMU,mono=True)
 if g:
  u=ease((t-gen)/.25);lay=blank(w,h);ImageDraw.Draw(lay).rounded_rectangle((18,gy-14,w-18,gy+50),10,outline=(84,169,103,int(220*u)),width=3);tm.alpha_composite(lay)
 rr(tm,(28,h-96,w-28,h-28),'#141418',14,'#2A2A30',1);txt(tm,'Type a message — / for skills, @ for files',52,h-76,21,'#5C5C66',mono=True)
 motion(tm,t,points=[(.05,820,640),(look-.03,700,y+215),(these+.1,700,y+215),(these+.6,760,y+400)],end=9)
 place(im,clip(tm,16),40,96+24*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 return im

# ---------- hours (split): five hours of GPT-5.6 Luna, every day ----------
def hours(t,S,at,w=940,h=560):
 p=blank(w,h);rr(p,(0,0,w-1,h-1),'white',20);five=at('hours','five',.99)-.1;gpt=at('hours','GPT',1.75)-.13;ev=at('hours','every',3.59)-.1;day=at('hours','day,',4.15)
 a=t-gpt
 if a>=0:
  v=spring(a/.28);place(p,tile('OpenAI',120),40,36,scale=max(.05,v),opacity=min(1,a*9),sh=True);la=ease((a-.08)/.25);txt(p,'GPT-5.6 Luna',184,52+8*(1-la),40,(29,29,31,int(255*la)),weight='Semibold');txt(p,'OpenAI · on Freebuff',184,104+8*(1-la),24,(110,110,115,int(255*la)))
 else:
  pulse=.55+.45*math.sin(t*5);ImageDraw.Draw(p).rounded_rectangle((42,38,158,154),34,outline=(190,190,196,int(255*pulse)),width=3)
 # big counter
 v=ease((t-five)/.4);n=5*v;s=f'{n:.0f}' if v>=1 else f'{n:.1f}';wd=txt(p,s,w-270-(tw(s,150,'Bold')-tw('5',150,'Bold')),14,150,DEEP if t>=five else '#C7C7CC',weight='Bold');txt(p,'hrs',w-168,84,54,INK,weight='Semibold');txt(p,'per day',w-168,142,24,GRAY)
 # 24 hour strip
 x0,y0,cw,gap=40,220,30,6
 for i in range(24):
  fill='#EEEEF0'
  if t<five and int(t/.045)%24==i:fill='#CFE9D6'
  fa=t-five-i*.07
  if i<5 and fa>0:fill=DEEP
  x=x0+i*(cw+gap);k=1+.25*math.sin(min(1,max(0,fa/.25))*math.pi) if i<5 and fa>0 else 1
  rr(p,(x,y0-44*(k-1),x+cw,y0+88),fill,9)
 for hh,lab in [(0,'0h'),(6,'6h'),(12,'12h'),(18,'18h'),(23,'24h')]:txt(p,lab,x0+hh*(cw+gap)+cw/2,y0+100,18,'#8E8E93',True)
 # freebucks refill
 if t>=ev:
  a=t-ev;e=ease(a/.28);row=blank(w-80,150);rr(row,(0,0,w-81,149),'#F5F5F7',24)
  cx,cy=64,75;ang=a*300;ImageDraw.Draw(row).arc((cx-26,cy-26,cx+26,cy+26),ang,ang+290,fill=DEEP,width=6)
  hx=cx+26*math.cos(math.radians(ang+290));hy=cy+26*math.sin(math.radians(ang+290));ImageDraw.Draw(row).ellipse((hx-8,hy-8,hx+8,hy+8),fill=DEEP)
  fillv=ease((t-ev-.1)/.9);txt(row,'Freebucks',120,22,28,INK,weight='Semibold');s=f'{round(100*fillv)} / 100';txt(row,s,w-80-30-tw(s,28,'Semibold'),22,28,DEEP,weight='Semibold')
  rr(row,(120,76,w-110,100),'#E1E1E6',12);rr(row,(120,76,120+max(24,(w-230)*fillv),100),DEEP,12);txt(row,'Refills every day at midnight Pacific',120,108,23,GRAY)
  place(p,row,40,376+16*(1-e),opacity=e)
  if t>=day:
   b=t-day;k=math.sin(min(1,b/.3)*math.pi);lay=blank(w,h);ImageDraw.Draw(lay).rounded_rectangle((36,372,w-36,530),26,outline=(30,142,62,int(255*k)),width=4);p.alpha_composite(lay)
 return clip(p,20)

# ---------- glm (full): free hours per day, by model ----------
def glm(t,S,at):
 im=Image.new('RGBA',(W,H),BG);tw20=at('glm','20',.33)-.12;fl=at('glm','Flash.',2.43)
 e=ease(t/.28)
 if e<=0:return im
 w,h=960,790;c=blank(w,h);rr(c,(0,0,w-1,h-1),'white',30);txt(c,'Free hours per day, by model',44,36,36,INK,weight='Bold')
 for i,(tn,nm,hrs) in enumerate(MODELS):
  last=i==5;y=112+i*104;t0=(.12+i*.07) if not last else tw20;a=t-t0
  if a<0 and not last:continue
  ia=ease((t-.12-i*.07)/.25);row=blank(w-60,96)
  if last and t>=tw20:rr(row,(0,0,w-61,95),'#EAF6EE',22,DEEP,3)
  row.alpha_composite(tile(tn,68),(14,14));txt(row,nm,100,8,30,INK,weight='Semibold')
  v=ease(max(0,a)/(.7 if last else .45));bw=(w-60-100-170)*hrs/20*v;rr(row,(100,54,100+max(16,bw),78),DEEP if last else '#B9DDC3',12)
  s=f'{round(hrs*v)} hrs';n=44 if last else 28;txt(row,s,w-60-20-tw(s,n,'Bold'),(22 if last else 32),n,DEEP if last else INK,weight='Bold')
  k=1+(.05*math.sin(min(1,max(0,(t-fl)/.3))*math.pi) if last and t>=fl else 0)
  place(c,row,30+20*(1-ia),y,scale=k,opacity=ia)
 place(im,c,60,96+24*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 return im

# ---------- smart (split): not the frontier shelf ----------
def crown(size,col='#F5B700'):
 c=blank(size,size);d=ImageDraw.Draw(c);s=size;d.polygon([(s*.08,s*.78),(s*.04,s*.30),(s*.30,s*.52),(s*.5,s*.18),(s*.70,s*.52),(s*.96,s*.30),(s*.92,s*.78)],fill=col);d.rounded_rectangle((s*.08,s*.74,s*.92,s*.88),s*.04,fill='#D99A00');return c
def smart(t,S,at,w=940,h=560):
 p=blank(w,h);no=at('smart','not',.86)-.1;sm=at('smart','smartest',1.34)-.13;fr=at('smart','frontier',1.80)
 # podium
 e=ease(t/.3);top=blank(420,300);rr(top,(0,0,419,340),'#1D1D1F',24);low=blank(440,170);rr(low,(0,0,439,220),'#2C2C2E',24)
 place(p,top,40,h-300*e,sh=True);place(p,low,470,h-170*e,sh=True)
 for i,n in enumerate(['Claude','ChatGPT']):
  a=t-.12-i*.12
  if a<0:continue
  v=spring(a/.28);x=70+i*190;place(p,tile(n,160),x,h-300-150-200*(1-ease(a/.24)),scale=max(.05,.7+.3*v),opacity=min(1,a*8),sh=True)
  if t>=sm:
   b=t-sm-i*.08
   if b>0:place(p,crown(96),x+32,h-300-150-84-160*(1-ease(b/.22)),scale=max(.05,spring(b/.26)),opacity=min(1,b*9),rot=-8+16*i)
 fe=ease((t-fr)/.25)
 if fe>0:txt(p,'Frontier',250,h-300+36,40,(255,255,255,int(255*fe)),True,'Bold')
 for i,n in enumerate(['DeepSeek','Zai','MiMo']):
  a=t-no-i*.1
  if a<0:continue
  v=spring(a/.28);x=486+i*140;place(p,tile(n,120),x,h-170-112-200*(1-ease(a/.24)),scale=max(.05,.7+.3*v),opacity=min(1,a*8),sh=True)
 fe=ease((t-no-.2)/.25)
 if fe>0:txt(p,'Free on Freebuff',714,h-170+40,32,(255,255,255,int(255*fe)),True,'Bold');p.alpha_composite(tile('Freebuff',40),(714-tw('Free on Freebuff',32,'Bold')/2-54,h-170+36))
 return p

# ---------- crazy (full): what the paid agents cost per year, from freebuff.com ----------
YEAR=[('Devin','Devin',2400),('ClaudeCode','Claude Code',1200),('Cursor','Cursor',720),('Codex','Codex',240),('OpenCode','OpenCode',120),('Freebuff','Freebuff',0)]
def crazy(t,S,at):
 im=Image.new('RGBA',(W,H),BG);pc=at('crazy','100%',1.07)-.13;ins=at('crazy','insane.',2.35)
 e=ease(t/.28)
 if e<=0:return im
 w,h=960,800;c=blank(w,h);rr(c,(0,0,w-1,h-1),'white',30);txt(c,'Cost per year',44,36,36,INK,weight='Bold')
 shake=math.sin((t-ins)*50)*10*math.exp(-(t-ins)*6) if t>=ins else 0
 for i,(tn,nm,cost) in enumerate(YEAR):
  last=i==5;y=112+i*108;a=t-(.1+i*.09)
  if a<0:continue
  ia=ease(a/.25);row=blank(w-60,100);on=last and t>=pc
  if on:rr(row,(0,0,w-61,99),'#EAF6EE',22,DEEP,3)
  row.alpha_composite(tile(tn,68),(14,16));dim=t>=pc and not last;txt(row,nm,100,12,26,'#9A9AA0' if dim else INK,weight='Semibold')
  v=ease((a-.05)/.55);bw=(w-60-100-230)*cost/2400*v
  if cost:rr(row,(100,56,100+max(16,bw),80),'#F2B8B5' if dim else '#FF6259',12)
  s=f'${round(cost*v):,} / yr';n=44 if on else 28;col=DEEP if last else ('#9A9AA0' if dim else INK);x=w-60-20-tw(s,n,'Bold');txt(row,s,x,(22 if on else 34),n,col,weight='Bold')
  if dim:
   u=ease((t-pc-i*.05)/.2);ImageDraw.Draw(row).line([(x-4,50),(x-4+(tw(s,n,'Bold')+8)*u,50)],fill='#9A9AA0',width=3)
  k=1+(.06*math.sin(min(1,max(0,(t-pc)/.32))*math.pi) if on else 0)
  place(c,row,30+20*(1-ia)+(shake if not last else 0),y,scale=k,opacity=ia)
 place(im,c,60,96+24*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 return im

# ---------- cta (full) ----------
def cta(t,S,at):
 im=Image.new('RGBA',(W,H),BG);k=at('cta','"Install"',.63);ts=max(.12,k-.3);post=k+.62
 p=ig.render(t,keyword='INSTALL',type_start=ts,type_duration=.4,post_at=post)
 motion(p,t,points=[(0,597,385),(post-.3,813,364),(post-.05,813,364),(post+.4,850,274)],clicks=[post],end=post+.9)
 e=ease(t/.28);place(im,p,90,330+24*(1-e),scale=1.08,opacity=e,sh=True)
 fe=spring((t-.05)/.3);place(im,tile('Freebuff',150),465,120,scale=max(.05,fe),opacity=min(1,t*8),sh=True)
 return im

# ---------- dispatch ----------
def graphics(b,t,S,at):
 name=b['name'];im=Image.new('RGBA',(W,H),BG)
 full={'hook':hook,'pay':pay,'price':price,'ads':ads,'glm':glm,'crazy':crazy,'cta':cta}
 if name in full:return full[name](t,S,at)
 if name=='called':return called(t,S,at)
 if name=='how':place(im,how(t,S,at),70,104,opacity=ease(t/.2))
 elif name=='agent':enter(im,agent(t,S,at),70,104,t,sh=False)
 elif name=='free':enter(im,free(t,S,at),70,104,t)
 elif name=='hours':enter(im,hours(t,S,at),70,104,t)
 elif name=='smart':place(im,smart(t,S,at),70,104,opacity=ease(t/.3))
 return im
