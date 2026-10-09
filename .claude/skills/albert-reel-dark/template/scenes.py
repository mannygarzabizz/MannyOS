"""All scene visuals. Recreated UI (no screenshots), real brand marks, Apple-styled chrome.
Every timestamp is local to the beat. Illustrative UI only: no real downloads, posts or agent runs."""
from draw import *
import sys,numpy as np
from PIL import ImageColor
sys.path.insert(0,str(P/'helpers'))
from pointer_motion import motion
import instagram_comment as ig
ig.font=lambda n:sf(n)

# ---------- helpers ----------
def gradient(w,h,c1,c2,vertical=True):
 rgb=lambda c:ImageColor.getrgb(c)[:3] if isinstance(c,str) else tuple(c)[:3]
 a=np.array(rgb(c1),float);b=np.array(rgb(c2),float)
 t=np.linspace(0,1,h if vertical else w)
 arr=a[None,:]+(b-a)[None,:]*t[:,None]
 arr=np.repeat(arr[:,None,:],w,1) if vertical else np.repeat(arr[None,:,:],h,0)
 return Image.fromarray(arr.astype('uint8'),'RGB').convert('RGBA')
def clip(p,r=16):
 m=Image.new('L',p.size);ImageDraw.Draw(m).rounded_rectangle((0,0,p.width-1,p.height-1),r,fill=255)
 p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel('A')),np.array(m))));return p
def bezier(p0,p1,p2,n=40):return [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in np.linspace(0,1,n)]
def device(im,x,y,w,h,color,t=1):
 """Front-on iPhone: colored body, tinted wallpaper screen, Dynamic Island."""
 e=ease(t)
 if e<=0:return
 q=3;p=blank(w*q,h*q);d=ImageDraw.Draw(p);r=w*q*.19
 d.rounded_rectangle((0,0,w*q-1,h*q-1),r,fill=color)
 dark=tuple(max(0,int(c*.72)) for c in ImageColor.getrgb(color));d.rounded_rectangle((0,0,w*q-1,h*q-1),r,outline=dark,width=q)
 inset=w*q*.055;scr=gradient(round(w*q-2*inset),round(h*q-2*inset),color,'#1C1C1E')
 tint=tuple(int(c*.55+30) for c in ImageColor.getrgb(color));scr=gradient(round(w*q-2*inset),round(h*q-2*inset),tint,dark)
 m=Image.new('L',scr.size);ImageDraw.Draw(m).rounded_rectangle((0,0,scr.width-1,scr.height-1),r*.78,fill=255);scr.putalpha(m);p.alpha_composite(scr,(round(inset),round(inset)))
 d.rounded_rectangle((w*q*.36,h*q*.045,w*q*.64,h*q*.075),h*q*.02,fill='#0B0B0D')
 p=p.resize((w,h),Image.Resampling.LANCZOS);place(im,p,x,y+14*(1-e),opacity=e)

# ---------- generic "AI slop" sites ----------
@lru_cache(None)
def slop(k,w=560,h=340):
 p=window(w,h,url=['unlock-future.ai','revolutionize.app','nextgen-solutions.io'][k],bar=42,r=14);b=43
 if k==0:
  p.alpha_composite(gradient(w,h-b,'#6C4BD6','#B08CF4'),(0,b))
  txt(p,'Unlock the future',w/2,b+52,36,'white',True,'Bold');txt(p,'of your business.',w/2,b+96,36,'white',True,'Bold')
  txt(p,'Powerful solutions. Limitless possibilities.',w/2,b+152,17,'#EDE6FF',True)
  pill(p,'Get started',w/2-84,b+192,168,44,'white','#6C4BD6',17,'Semibold')
  for i in range(3):rr(p,(w/2-190+i*135,b+258,w/2-70+i*135,b+300),(255,255,255,70),10)
 elif k==1:
  p.alpha_composite(gradient(w,h-b,'#0B1020','#141C38'),(0,b))
  g=blank(w,h-b);ImageDraw.Draw(g).ellipse((w*.55,-60,w*1.2,220),fill=(26,214,193,90));g=g.filter(ImageFilter.GaussianBlur(40));p.alpha_composite(g,(0,b))
  txt(p,'Revolutionize',w/2,b+50,40,'white',True,'Bold');txt(p,'your workflow.',w/2,b+98,40,'#1AD6C1',True,'Bold')
  txt(p,'AI-powered. Cutting-edge. Seamless.',w/2,b+156,17,'#9AA3B8',True)
  pill(p,'Start free trial',w/2-92,b+196,184,44,'#1AD6C1','#0B1020',17,'Semibold')
  for i in range(3):rr(p,(w/2-190+i*135,b+262,w/2-70+i*135,b+300),(255,255,255,22),10)
 else:
  ImageDraw.Draw(p).rectangle((0,b,w,h),fill='#FFF6EE')
  txt(p,'Next-gen solutions',w/2,b+50,38,'#FF7A1A',True,'Bold');txt(p,'for modern teams.',w/2,b+96,38,'#1D1D1F',True,'Bold')
  txt(p,'Scale faster with our all-in-one platform.',w/2,b+152,17,'#8A7F76',True)
  pill(p,'Book a demo',w/2-80,b+192,160,44,'#FF7A1A','white',17,'Semibold')
  for i in range(3):rr(p,(w/2-190+i*135,b+258,w/2-70+i*135,b+300),'#FFE3CC',10)
 return clip(p,14)

# ---------- scythe + Claude icon ----------
@lru_cache(None)
def scythe():
 q=4;w,h=360,540;im=blank(w*q,h*q);d=ImageDraw.Draw(im)
 snath=[(150,530),(158,380),(172,200),(190,70)]
 sm=[(x*q,y*q) for x,y in snath];d.line(sm,fill='#5C3D22',width=15*q,joint='curve');d.line([(x-4*q,y) for x,y in sm],fill='#8C6239',width=5*q,joint='curve')
 d.line([(140*q,335*q),(112*q,352*q)],fill='#4A2F18',width=12*q);d.line([(178*q,178*q),(150*q,195*q)],fill='#4A2F18',width=12*q)
 outer=bezier((192,72),(60,30),(18,240),60);inner=bezier((18,240),(96,118),(190,104),60)
 poly=[(x*q,y*q) for x,y in outer+inner]
 d.polygon(poly,fill='#D8DBE0');d.line(poly+[poly[0]],fill='#6F757D',width=2*q,joint='curve')
 d.line([(x*q,y*q) for x,y in outer],fill='#F7F8FA',width=6*q,joint='curve')
 d.line([(x*q,y*q) for x,y in bezier((150,84),(95,122),(60,190),30)],fill='#B6BAC0',width=2*q,joint='curve')
 d.rounded_rectangle((178*q,62*q,206*q,112*q),6*q,fill='#26262A')
 return im.resize((w,h),Image.Resampling.LANCZOS)
PIV=(166,290)
@lru_cache(None)
def reaper(angle,tilt=0,size=150):
 """Claude app icon 'holding' the scythe; rotation about the grip pivot."""
 c=blank(1120,1120);s=scythe();sc=1.32;s=s.resize((round(s.width*sc),round(s.height*sc)),Image.Resampling.LANCZOS);c.alpha_composite(s,(560-round(PIV[0]*sc),560-round(PIV[1]*sc)))
 c=c.rotate(angle,resample=Image.Resampling.BICUBIC,center=(560,560))
 ic=apptile('Claude',size)
 if tilt:ic=ic.rotate(tilt,resample=Image.Resampling.BICUBIC,expand=True)
 sh=shadow(ic.width,ic.height,r=size*.22,blur=10,alpha=40,dy=8);c.alpha_composite(sh,(560-ic.width//2-60,560-ic.height//2-60))
 c.alpha_composite(ic,(560-ic.width//2,560-ic.height//2));return c
def split_halves(card):
 w,h=card.size;out=[]
 for poly in [[(0,0),(w*.90,0),(w*.10,h),(0,h)],[(w*.90,0),(w,0),(w,h),(w*.10,h)]]:
  m=Image.new('L',card.size);ImageDraw.Draw(m).polygon(poly,fill=255);piece=card.copy();piece.putalpha(Image.fromarray(np.minimum(np.array(card.getchannel('A')),np.array(m))));out.append(piece)
 return out
def hook(t,S,at):
 im=Image.new('RGBA',(W,H),BG)
 cw,ch=620,376;cards=[(0,50,150,-3),(1,410,412,2),(2,120,676,-2)]
 ts=[at('hook','kills',.94),1.50,at('hook','slop',2.16)]
 def rot_pt(px,py,cx,cy,deg):
  a=math.radians(deg);dx,dy=px-cx,py-cy;return (cx+dx*math.cos(a)+dy*math.sin(a),cy-dx*math.sin(a)+dy*math.cos(a))
 for k,x,y,rot in cards:
  card=slop(k,cw,ch);e=ease((t-.02-k*.07)/.32);a=t-ts[k]
  if a<0:place(im,card,x+40*(1-e),y,scale=.97+.03*e,opacity=e,sh=True,rot=rot)
  elif a<.8:
   L,R=split_halves(card);f=ease(a/.5);g=a*a*1400;op=max(0,1-a/.66)
   place(im,R,x+130*f,y-70*f+g*.8,opacity=op,rot=rot-9*f)
   place(im,L,x-100*f,y+30*f+g,opacity=op,rot=rot+7*f)
  if 0<=a<.2:
   cx,cy=x+cw/2,y+ch/2;p0=rot_pt(x+cw*.92,y-30,cx,cy,rot);p1=rot_pt(x+cw*.08,y+ch+30,cx,cy,rot)
   lay=blank(W,H);ImageDraw.Draw(lay).line([p0,p1],fill=(217,119,87,int(235*(1-a/.2))),width=26);lay=lay.filter(ImageFilter.GaussianBlur(10));im.alpha_composite(lay)
   ImageDraw.Draw(im).line([p0,p1],fill=(255,255,255,int(255*(1-a/.2))),width=6)
 anchors=[(x+cw-30,y-30) for k,x,y,r in cards]
 route=[(0,-300,200)]
 for k,(ax,ay) in enumerate(anchors):route+=[(ts[k]-.22,ax,ay),(ts[k]+.10,ax-90,ay+120)]
 route+=[(ts[2]+.55,560,560)]
 def pos(tt):
  if tt<=route[0][0]:return route[0][1:]
  for (a,x0,y0),(b,x1,y1) in zip(route,route[1:]):
   if tt<=b:u=smooth((tt-a)/max(.001,b-a));return (lerp(x0,x1,u),lerp(y0,y1,u))
  return route[-1][1:]
 px,py=pos(t);ang=70;tilt=-14
 for k in range(3):
  u=(t-(ts[k]-.16))/.24
  if 0<=u<1:ang=lerp(70,-80,smooth(u));tilt=lerp(-14,12,smooth(u))
  elif t>=ts[k]+.08 and (k==2 or t<ts[k+1]-.16):
   v=smooth((t-ts[k]-.08)/.35);ang=lerp(-80,70 if k<2 else 25,v);tilt=lerp(12,-14 if k<2 else 0,v)
 if t>ts[2]+.55:py+=math.sin((t-ts[2]-.55)*4)*4
 e0=ease(t/.3);r=reaper(round(ang),round(tilt),190);place(im,r,px-560,py-560,opacity=e0)
 return im

# ---------- product recreations ----------
@lru_cache(None)
def hero(name,w=900,h=520,state=1.0):
 """Recreated hero sections at 900x520, then resized by caller."""
 p=blank(900,520);d=ImageDraw.Draw(p)
 if name=='Apple':
  d.rectangle((0,0,900,520),fill='#FFFFFF');d.rectangle((0,0,900,48),fill='#F5F5F7')
  items=['Store','Mac','iPad','iPhone','Watch','AirPods','TV & Home','Support']
  txt(p,'\uf8ff',34,12,22,'#1D1D1F');x=104;gap=(748-sum(tw(i,15) for i in items))/(len(items)+1)
  for i in items:x+=gap;txt(p,i,x,16,15,'#3A3A3C');x+=tw(i,15)
  d.ellipse((850,17,861,28),outline='#3A3A3C',width=2);d.line([(860,27),(866,33)],fill='#3A3A3C',width=2)
  d.rounded_rectangle((878,20,890,33),2,outline='#3A3A3C',width=2);d.arc((880,13,888,23),180,360,fill='#3A3A3C',width=2)
  txt(p,'iPhone',450,84,66,INK,True,'Semibold');txt(p,'Designed to be loved.',450,166,27,'#1D1D1F',True)
  txt(p,'Learn more ›',382,214,19,BLUE,True);txt(p,'Buy ›',518,214,19,BLUE,True)
  cols=['#2F3236','#B9CDE8','#EAD9CF','#CFE3D0','#D9D0EC'];pw,ph=98,200
  for i,c in enumerate(cols):device(p,450-2.5*(pw+22)+i*(pw+22)+11,270,pw,ph,c,state*3-i*.15)
 elif name=='Notion':
  d.rectangle((0,0,900,520),fill='#FFFFFF');p.alpha_composite(icon('Notion',30),(28,14));txt(p,'Notion',66,15,22,INK,weight='Semibold')
  for i,s in enumerate(['Product','Download','Solutions','Resources','Pricing']):txt(p,s,190+i*100,20,15,'#37352F')
  pill(p,'Get Notion free',722,10,150,36,'#0075DE','white',15,'Semibold');txt(p,'Log in',655,20,15,'#37352F')
  txt(p,'The AI workspace',450,112,60,INK,True,font=ny(60,'Bold'));txt(p,'that works for you.',450,186,60,INK,True,font=ny(60,'Bold'))
  txt(p,'One place where teams find every answer, automate the busywork, and get projects done.',450,272,19,'#5B5955',True)
  pill(p,'Get Notion free',330,322,168,50,'#0075DE','white',18,'Semibold');pill(p,'Request a demo',518,322,168,50,'#F1F0EE','#37352F',18,'Semibold')
  for i,c in enumerate(['#FFD9D3','#FFF1C2','#DDEBFF']):
   e=ease(state*3-i*.2);rr(p,(160+i*200,420+12*(1-e),340+i*200,520),c,12);rr(p,(176+i*200,440+12*(1-e),300+i*200,452),(0,0,0,40),6);rr(p,(176+i*200,462+12*(1-e),260+i*200,472),(0,0,0,30),5)
 elif name=='Duolingo':
  d.rectangle((0,0,900,520),fill='#FFFFFF');txt(p,'duolingo',34,18,36,'#58CC02',weight='Heavy',tracking=-1);txt(p,'SITE LANGUAGE: ENGLISH',660,28,14,'#AFAFAF',weight='Bold')
  ow=icon('Duolingo',300).copy();m=squircle_mask(300);ow.putalpha(Image.fromarray(np.minimum(np.array(ow.getchannel('A')),np.array(m))))
  e=ease(state*3);place(p,ow,80,110+12*(1-e),opacity=e)
  for i,s in enumerate(['The free, fun, and','effective way to','learn a language!']):txt(p,s,640,150+i*46,36,'#4B4B4B',True,'Bold')
  pill(p,'GET STARTED',470,318,340,54,'#58CC02','white',18,'Heavy');pill(p,'I ALREADY HAVE AN ACCOUNT',470,388,340,54,'white','#1CB0F6',16,'Heavy','#E5E5E5')
 elif name=='After':
  d.rectangle((0,0,900,520),fill='#FBFBFD');txt(p,'site.com',36,20,24,INK,weight='Semibold')
  for i,s in enumerate(['Product','Workspace','Pricing','Company']):txt(p,s,470+i*95,24,15,'#3A3A3C')
  pill(p,'Get started',778,14,96,34,BLUE,'white',14,'Medium')
  e=ease(state*2.2);txt(p,'Simple tools.',450,96+20*(1-e),64,INK,True,'Semibold');txt(p,'Serious work.',450,168+20*(1-e),64,INK,True,'Semibold')
  e2=ease(state*2.2-.25);txt(p,'A calm workspace for everything your team is building.',450,258,21,'#6E6E73',True)
  pill(p,'Try it free',372,310,156,48,BLUE,'white',18,'Medium');txt(p,'Learn more ›',600,325,18,BLUE)
  for i,s in enumerate(['Plan','Design','Ship']):
   e3=ease(state*3-.6-i*.2)
   if e3>0:dy=16*(1-e3);rr(p,(130+i*220,400+dy,330+i*220,520+dy),'white',16,'#E5E5EA',1);txt(p,s,150+i*220,420+dy,20,INK,weight='Semibold');rr(p,(150+i*220,458+dy,300+i*220,466+dy),'#E5E5EA',4);rr(p,(150+i*220,478+dy,262+i*220,486+dy),'#E5E5EA',4)
 out=p.resize((w,h),Image.Resampling.LANCZOS) if (w,h)!=(900,520) else p
 return out
def herowin(name,w,h,t=1.0,url=None):
 b=44;p=window(w,h,url=url or {'Apple':'apple.com','Notion':'notion.com','Duolingo':'duolingo.com','After':'site.com'}[name],bar=b,r=14)
 p.alpha_composite(hero(name,w,h-b-1,round(min(1,max(0,t))*20)/20),(0,b+1));return clip(p,14)

# ---------- Refero recreations ----------
def refero_nav(p,crumb='Styles'):
 p.alpha_composite(icon('Refero',30),(26,60));txt(p,'/',66,62,20,'#9A9A9E');txt(p,crumb,84,62,20,INK,weight='Medium')
 txt(p,'Log in',p.width-176,64,16,'#3A3A3C');pill(p,'Sign up',p.width-118,56,88,34,INK,'white',15,'Medium')
def refero_home(t,w=940,h=560):
 p=window(w,h,url='styles.refero.design');refero_nav(p)
 e=ease((t-.12)/.32);txt(p,'High-quality DESIGN.md',w/2,150+18*(1-e),46,(29,29,31,int(255*e)),True,font=ny(46,'Medium'));txt(p,'examples for AI agents',w/2,206+18*(1-e),46,(29,29,31,int(255*e)),True,font=ny(46,'Medium'))
 e=ease((t-.28)/.32);txt(p,'Style references extracted from the world’s best-designed products.',w/2,278+14*(1-e),18,(110,110,115,int(255*e)),True)
 e=ease((t-.42)/.32)
 if e>0:
  f=blank(600,56);rr(f,(0,0,599,55),'white',14,'#D9D9DE',1);txt(f,'Search styles…',22,17,18,'#9A9A9E');pill(f,'Search',492,9,96,38,INK,'white',15,'Medium');place(p,f,170,338+14*(1-e),opacity=e)
 for i,n in enumerate(['Apple','Notion','Duolingo']):
  e=ease((t-.55-i*.08)/.3)
  if e>0:
   c=blank(280,150);rr(c,(0,0,279,149),'white',12,'#E5E5EA',1);c.alpha_composite(hero(n,256,110),(12,12));place(p,c,50+i*300,428+16*(1-e),opacity=e)
 return clip(p,16)
def stylecard(name,w=280,h=200,sel=False):
 c=blank(w,h);rr(c,(0,0,w-1,h-1),'white',12,BLUE if sel else '#E5E5EA',3 if sel else 1)
 if name in ('Apple','Notion','Duolingo'):c.alpha_composite(hero(name,w-24,round((w-24)*.6)),(12,12));c.alpha_composite(apptile(name,26),(14,h-38));txt(c,name,50,h-36,16,INK,weight='Medium')
 else:
  col={'Linear':'#0B0B0F','Stripe':'#635BFF','Vercel':'#111111'}[name];rr(c,(12,12,w-12,round((w-24)*.6)+12),col,8);txt(c,name,50,h-36,16,INK,weight='Medium');rr(c,(14,h-38,40,h-12),col,7)
  rr(c,(34,44,w-60,56),(255,255,255,200),4);rr(c,(34,66,w-110,76),(255,255,255,120),4)
 return c
def refero_gallery(t,pick=None,w=940,h=440):
 p=window(w,h,url='styles.refero.design');refero_nav(p)
 names=['Apple','Notion','Duolingo'];sel=pick is not None and t>=pick
 order=[1,2,0] if sel else [0,1,2]   # selected card is composited last so it sits on top, fully opaque
 for i in order:
  n=names[i];x=40+i*295;y=140;e=ease((t-i*.06)/.3);card=stylecard(n,280,200,sel and n=='Apple')
  if sel:
   f=ease((t-pick)/.42)
   if n=='Apple':place(p,card,x+(w/2-140-x)*f,y+(150-y)*f,scale=1+.36*f,opacity=e,sh=f>.2)
   else:place(p,card,x,y,opacity=e*(1-.82*f))
  else:place(p,card,x,y+18*(1-e),opacity=e)
 if pick is not None:motion(p,t,points=[(0,760,400),(pick-.2,182,176),(pick-.02,182,176),(pick+.5,150,150)],clicks=[pick],end=pick+.9)
 return clip(p,16)

# ---------- claude/chatgpt comparison ----------
def chatwin(name,t,w=455,h=560,send_at=1.0,thumb_at=1.35,dup_at=None):
 cream=name=='Claude';p=window(w,h,title=name,fill='#FAF9F5' if cream else 'white',bar=44,r=14)
 p.alpha_composite(apptile(name,22),(w/2-tw(name,15,'Semibold')/2-30,11))
 f=blank(w-40,62);rr(f,(0,0,w-41,61),'white' if cream else '#F4F4F4',16,'#E3DFD6' if cream else '#E5E5EA',1)
 txt(f,reveal('Design a website for my business.',t-.1,.8),20,20,17,INK)
 ImageDraw.Draw(f).ellipse((w-40-52,13,w-40-16,49),fill=(TERRA if cream else INK) if t>.9 else ('#E8DFD4' if cream else '#D1D1D6'))
 txt(f,'↑',w-40-34,19,20,'white',True,'Bold');place(p,f,20,56)
 if t>=thumb_at:
  a=t-thumb_at;txt(p,'Here’s a landing page for your business:',22,138,15,'#6E6E73' if not cream else '#7A7268')
  base=slop(0 if cream else 1,400,242)
  if dup_at is not None and t>=dup_at:
   for j in [3,2,1]:
    e=ease((t-dup_at-(3-j)*.12)/.3);place(p,base,27+j*8*e,172+j*26*e,scale=1-j*.03*e,opacity=e*(1-j*.15),sh=True)
  e=ease(a/.34);place(p,base,27,172+16*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 return clip(p,14)
def generic(t,S,at):
 p=blank(940,560);dup=at('generic','every',3.73)
 place(p,chatwin('Claude',t,thumb_at=1.30,dup_at=dup),0,0,sh=True);place(p,chatwin('ChatGPT',t-.12,thumb_at=1.40,dup_at=dup+.15),485,0,sh=True)
 return p



PALETTES=[('#6C4BD6','#B08CF4'),('#0E7C86','#3FC1C9'),('#F26A2E','#FFB170'),('#C13584','#F77FB0'),('#1F5FD1','#6FA6FF'),('#1E9E5A','#7BD69B'),('#D3302F','#FF8A80'),('#3B3F8F','#8A8FE0'),('#8C5A2B','#D9A066'),('#0F766E','#5EEAD4'),('#7C3AED','#C4B5FD'),('#B45309','#FCD34D')]
HEADS=['Unlock the future','Revolutionize','Next-gen solutions','Empower your team','Scale without limits','Innovate faster','Transform your','Elevate every','Seamless growth','Smarter workflows','Reimagine your','Build the future']
SUBS=['of your business.','your workflow.','for modern teams.','with AI today.','starting today.','than ever before.','digital presence.','customer journey.','for your brand.','made simple.','online experience.','together.']
@lru_cache(None)
def slop_color(i,w=360,h=220):
 """Same generic hero layout, different color per card."""
 c1,c2=PALETTES[i%len(PALETTES)];p=window(w,h,url=f'{HEADS[i%12].split()[0].lower()}-site.com',bar=28,r=12);b=29
 p.alpha_composite(gradient(w,h-b,c1,c2),(0,b))
 txt(p,HEADS[i%12],w/2,b+30,23,'white',True,'Bold');txt(p,SUBS[i%12],w/2,b+58,23,'white',True,'Bold')
 txt(p,'Powerful solutions. Limitless possibilities.',w/2,b+94,11,'#F3F0FF',True)
 pill(p,'Get started',w/2-52,b+118,104,28,'white',c1,11,'Semibold')
 for k in range(3):rr(p,(w/2-120+k*85,b+160,w/2-45+k*85,b+184),(255,255,255,70),7)
 return clip(p,12)
# ---------- full-screen: Claude and ChatGPT spit out generic sites ----------
def generic_full(t,S,at):
 im=Image.new('RGBA',(W,H),BG)
 tc,tg=at('generic','Claude',.65),at('generic','ChatGPT',1.07);mk=at('generic','making',1.75);end=S['generic']['end']-S['generic']['start']
 # shared prompt above the two assistants
 e=ease(t/.3)
 if e>0:
  f=blank(700,74);rr(f,(0,0,699,73),'white',22,'#E0DDD6',1);txt(f,reveal('Design a website for my business.',t-.08,.7),28,23,24,INK)
  place(im,f,190,150+16*(1-e),opacity=e,sh=True)
 icons=[('Claude',420,tc),('ChatGPT',660,tg)];cy=380;size=170
 # cards: alternate sides, one every .16 s from 'making'
 cards=[]
 k=0;tt=mk
 while tt<end-.05 and k<16:
  cards.append((k%2,tt,k//2));tt+=.16;k+=1
 for side,t0,n in cards:
  a=t-t0
  if a<0:continue
  u=ease(a/.55);sx=icons[side][1];dirn=-1 if side==0 else 1
  lx=(230 if side==0 else 850)+dirn*n*3;ly=770-n*16
  x=lerp(sx,lx,u);y=lerp(cy,ly,u)-150*math.sin(math.pi*u)*(1-u*.4);rot=lerp(0,dirn*-(5+n*1.3),u)
  card=slop_color(n*2+side);sc=lerp(.22,1,u)
  place(im,card,x-180,y-110,scale=sc,opacity=min(1,a*6),sh=u>.3,rot=rot)
 for name,cx,t0 in icons:
  e=spring(max(0,t-t0)/.35)
  if e<=0:continue
  # squash on every spit from this icon
  sq=1
  for side,tt,n in cards:
   if (side==0)==(name=='Claude') and 0<=t-tt<.14:sq=1-.09*math.sin((t-tt)/.14*math.pi)
  place(im,apptile(name,size),cx-size/2,cy-size/2,scale=max(.05,e)*sq,opacity=min(1,e*2),sh=True)
 return im

# ---------- Safari tabs ----------
def tabs(t,S,at,w=940,h=560):
 p=window(w,h,bar=52,r=16);names=['Apple','Notion','Duolingo'];ons=[.05,at('explain','site',.75)-.2,at('explain','done',1.1)-.15]
 shown=[i for i,o in enumerate(ons) if t>=o];active=shown[-1] if shown else 0
 x=110
 for i,n in enumerate(names):
  if i not in shown:continue
  e=ease((t-ons[i])/.25);tw_=228;tab=blank(tw_,34);rr(tab,(0,0,tw_-1,33),'white' if i==active else '#ECECEE',8,'#DADADE',1)
  tab.alpha_composite(icon(n,18) if n!='Duolingo' else apptile('Duolingo',18),(14,8));txt(tab,{'Apple':'Apple','Notion':'Notion – The AI workspace','Duolingo':'Duolingo'}[n],42,9,14,INK)
  place(p,tab,x+12*(1-e),9,opacity=e);x+=tw_+8
 a=t-ons[active];e=ease(a/.28);p.alpha_composite(hero(names[active],w,h-53,min(1,a+.4)).crop((0,0,w,h-53)),(0,53)) if e>=1 else place(p,hero(names[active],w,h-53,min(1,a+.4)),0,53+14*(1-e),opacity=e)
 return clip(p,16)

# ---------- wireframe -> design (investment) ----------
def wireframe(t,w=940,h=560):
 """Layout being designed: blocks pop in staggered, a blue selection frame with handles hops between them."""
 p=window(w,h,url='apple.com',bar=44,r=14);b=45;g='#E5E5EA';d=ImageDraw.Draw(p)
 d.rectangle((0,b,w,b+48),fill='#F2F2F4')
 blocks=[(30,b+16,52,b+34,5)]+[(112+i*95,b+18,168+i*95,b+30,5) for i in range(8)]
 blocks+=[(w/2-120,b+92,w/2+120,b+150,12),(w/2-150,b+176,w/2+150,b+198,8),(w/2-90,b+222,w/2-20,b+238,6),(w/2+20,b+222,w/2+70,b+238,6)]
 blocks+=[(240+i*92,b+272,314+i*92,b+520,18) for i in range(5)]
 for i,(x0,y0,x1,y1,r) in enumerate(blocks):
  e=spring(max(0,t-.04-i*.04)/.3)
  if e<=0:continue
  cx,cy=(x0+x1)/2,(y0+y1)/2;hw,hh=(x1-x0)/2*e,(y1-y0)/2*e
  rr(p,(cx-hw,cy-hh,cx+hw,cy+hh),g,r*e)
 # selection frame hops across the major elements while the layout is still being designed
 hops=[9,10,14,16,11,12,9];step=.24;k=int(t/step)
 if k<len(hops) and t>=.35 and t-.04-hops[k]*.04>.12:
  x0,y0,x1,y1,_=blocks[hops[k]];pad=6;u=ease((t-k*step)/.12)
  if u>0:
   d.rectangle((x0-pad,y0-pad,x1+pad,y1+pad),outline=(0,113,227,int(255*u)),width=2)
   for hx in (x0-pad,x1+pad):
    for hy in (y0-pad,y1+pad):d.rectangle((hx-4,hy-4,hx+4,hy+4),fill='white',outline=(0,113,227,int(255*u)),width=2)
   lab=f'{round(x1-x0)} × {round(y1-y0)}';tw_=tw(lab,13,'Medium');rr(p,((x0+x1)/2-tw_/2-8,y1+pad+6,(x0+x1)/2+tw_/2+8,y1+pad+26),(0,113,227,int(255*u)),4);txt(p,lab,(x0+x1)/2,y1+pad+9,13,(255,255,255,int(255*u)),True,'Medium')
 return clip(p,14)
def investment(t,S,at,w=940,h=560):
 wf=wireframe(t,w,h);fin=herowin('Apple',w,h,1.0)
 sweep=at('investment','millions',1.87);u=ease((t-sweep)/.9)
 p=blank(w,h);place(p,wf,0,0)
 if u>0:
  xx=round(w*u);m=Image.new('L',(w,h));ImageDraw.Draw(m).rectangle((0,0,xx,h),fill=255);m=m.filter(ImageFilter.GaussianBlur(6))
  f=fin.copy();f.putalpha(Image.fromarray(np.minimum(np.array(f.getchannel('A')),np.array(m))));p.alpha_composite(f)
  if u<1:line(p,[(xx,46),(xx,h-2)],BLUE,3)
 return p

# ---------- dock (brands) ----------
def dock(t,S,at):
 im=Image.new('RGBA',(W,H),BG);names=['Apple','Notion','Duolingo'];ons=[max(0,at('brands',n,.5+i*.65)-.13) for i,n in enumerate(names)]
 shown=[i for i,o in enumerate(ons) if t>=o];active=shown[-1] if shown else None
 # preview window above the dock for the current brand
 if active is not None:
  a=t-ons[active];e=ease(a/.3);win=herowin(names[active],760,440,a+.2);place(im,win,160+(30 if active==2 else -30 if active==0 else 0)*(1-e),90+24*(1-e),scale=.96+.04*e,opacity=e,sh=True)
 bar=blank(700,150);rr(bar,(0,0,699,149),(255,255,255,190),34,(0,0,0,28),1);e=ease(t/.3);place(im,bar,190,640+30*(1-e),opacity=e,sh=True)
 xs=[320,540,760]
 for i,n in enumerate(names):
  s=1.0;lift=0
  if i in shown:
   a=t-ons[i];s=1+.42*spring(a/.26) if (i==active) else 1.12;lift=(40*spring(a/.26)) if i==active else 8
  tile=apptile(n,150);place(im,tile,xs[i]-75+(150-150*s)/2*0,715-75-lift-(150*s-150)/2,scale=s,opacity=e,sh=i in shown)
  if i in shown:ImageDraw.Draw(im).ellipse((xs[i]-4,777,xs[i]+4,785),fill='#3A3A3C')
 return im

# ---------- DESIGN.md file (document) ----------
@lru_cache(None)
def docicon(size=260,lines=0):
 q=3;w,h=size,round(size*1.28);im=blank(w*q,h*q);d=ImageDraw.Draw(im);f=round(w*.16)*q
 d.rounded_rectangle((0,0,w*q-1,h*q-1),round(w*.04)*q,fill='white',outline='#C9C9CE',width=q)
 d.polygon([(w*q-f,0),(w*q,f),(w*q-f,f)],fill='#E9E9EC');d.line([(w*q-f,0),(w*q-f,f),(w*q,f)],fill='#C9C9CE',width=q)
 rows=[('#',BLUE,.55),('##',BLUE,.4),('-',INK,.7),('-',INK,.62),('-',INK,.66),('##',BLUE,.36),('-',INK,.58),('-',INK,.5)]
 if size>=60:
  for i,(k,c,fr) in enumerate(rows[:lines]):
   y=(h*.18+i*h*.078)*q;lx=w*.085*q;bh=h*.027*q
   if k!='-':d.rounded_rectangle((lx,y,lx+len(k)*w*.03*q,y+bh),q,fill=c);lx+=(len(k)*w*.03+w*.03)*q
   d.rounded_rectangle((lx,y,lx+(w*.83*q-lx)*fr,y+bh),q,fill='#3A3A3C' if c==INK else '#8FBFF3')
  d.rounded_rectangle((w*q*.30,h*q-h*.126*q,w*q*.70,h*q-h*.054*q),round(w*.02)*q,fill='#EEEEF0');d.text((w*q/2,h*q-h*.09*q),'MD',font=sf(round(w*.05)*q,'Bold'),fill='#6E6E73',anchor='mm')
 else:
  for i in range(min(lines,4)):d.rounded_rectangle((w*.15*q,(h*.25+i*h*.15)*q,w*.7*q,(h*.25+i*h*.15+h*.06)*q),q,fill='#8FBFF3' if i==0 else '#9A9A9E')
 return im.resize((w,h),Image.Resampling.LANCZOS)
def document(t,S,at):
 im=Image.new('RGBA',(W,H),BG);saved=at('document','saved',.52);named=at('document','design.md',1.96)
 names=['Apple','Notion','Duolingo'];starts=[(260,250),(540,250),(820,250)]
 u=ease((t-saved)/.55)
 for i,n in enumerate(names):
  e=ease((t-i*.06)/.25);x0,y0=starts[i];x=lerp(x0,540,u);y=lerp(y0,520,u);s=lerp(1,.25,u)
  if u<1:place(im,apptile(n,190),x-95,y-95,scale=s,opacity=e*(1-u*.9),sh=True)
 if u>0:
  lines=min(8,max(0,int((t-saved-.35)/.12)));lines=8 if t-saved>1.4 else lines
  s=.6+.4*spring((t-saved)/.5);ic=docicon(340,lines);place(im,ic,540-170,520-218,scale=s,opacity=min(1,u*1.5),sh=True)
 if t>=named:
  e=ease((t-named)/.25);lab=blank(330,58);rr(lab,(0,0,329,57),BLUE,9);txt(lab,'DESIGN.md',165,12,30,'white',True,'Medium');place(im,lab,375,760+12*(1-e),opacity=e)
 return im

# ---------- download (full) ----------
def download(t,S,at):
 im=Image.new('RGBA',(W,H),BG);click=.42
 c=blank(760,430);rr(c,(0,0,759,429),'white',22);c.alpha_composite(apptile('Apple',96),(40,40));txt(c,'Apple',160,44,46,INK,font=ny(46,'Medium'));txt(c,'DESIGN.md  ·  14 KB  ·  Light theme',160,110,18,'#6E6E73')
 line(c,[(40,168),(720,168)],'#EBEBEF',1)
 for i,(k,v) in enumerate([('Accent','#0071E3'),('Ink','#1D1D1F'),('Surface','#F5F5F7')]):
  rr(c,(40+i*228,190,254+i*228,286),v,14,'#E5E5EA',1);txt(c,k,50+i*228,296,15,'#6E6E73')
 pressed=t>=click;done=t>=click+.35
 if not done:
  s=1-.05*(1 if click<=t<click+.12 else 0);pill(c,'↓  Download',380-150*s,332,300*s,64,BLUE if not pressed else '#0060C0','white',22,'Semibold')
 else:
  e=ease((t-click-.35)/.25);pill(c,'✓  Downloaded',230,332,300,64,GREEN,'white',22,'Semibold')
 motion(c,t,points=[(0,690,120),(click-.16,395,364),(click-.02,395,364),(click+.55,470,300)],clicks=[click],end=1.3)
 e=ease(t/.3);place(im,c,160,170+20*(1-e),opacity=e,sh=True)
 if t>=click+.06:
  a=t-click-.06;u=smooth(a/.55);ic=docicon(120,8);x=lerp(540-60,700,u);y=lerp(510,640,u)-150*math.sin(math.pi*u);s=lerp(.4,1,u)
  place(im,ic,x,y,scale=s,opacity=min(1,a*6),sh=True)
 return im

# ---------- Claude agent ----------
def agent(t,S,at,w=940,h=560):
 p=window(w,h,title='Claude',fill='#FAF9F5',bar=44,r=14);p.alpha_composite(apptile('Claude',22),(w/2-tw('Claude',15,'Semibold')/2-30,11))
 send=at('agent','agent',1.1);steps=[('Reading DESIGN.md',send+.25),('Applying colors, type and spacing',send+.75),('Building pages',send+1.25)];prev=at('agent','beautiful',2.75)
 txt(p,'Good afternoon.',w/2,84,34,INK,True,font=ny(34,'Medium'))
 f=blank(w-60,150);rr(f,(0,0,w-61,149),'white',20,'#E3DFD6',1)
 e=ease(t/.3)
 if e>0:
  chip=blank(190,44);rr(chip,(0,0,189,43),'#F1EEE8',10,'#E3DFD6',1);chip.alpha_composite(docicon(22,3),(12,7));txt(chip,'DESIGN.md',44,12,16,INK,weight='Medium');place(f,chip,18,16+10*(1-e),opacity=e)
 txt(f,reveal('Build my website with this design.',t-.35,.8),20,78,20,INK)
 pressed=t>=send;ImageDraw.Draw(f).ellipse((w-60-66,94,w-60-22,138),fill='#B65F3E' if send<=t<send+.15 else TERRA if t>.3 else '#E8DFD4');txt(f,'↑',w-60-44,101,24,'white',True,'Bold')
 place(p,f,30,132)
 if pressed:
  y=316
  for i,(s,tt) in enumerate(steps):
   if t<tt-.2:continue
   e=ease((t-(tt-.2))/.25)
   if t>=tt+.4 or (i==2 and t>=prev):checkmark(p,52,y+i*44+12,11)
   else:
    d=ImageDraw.Draw(p);a=(t*540)%360;d.arc((42,y+i*44+2,62,y+i*44+22),a,a+250,fill=TERRA,width=3)
   txt(p,s,76,y+i*44+1+8*(1-e),18,(29,29,31,int(255*e)))
  if t>=prev:
   a=t-prev;e=ease(a/.3);win=herowin('After',470,300,a*1.1+.1);place(p,win,430,300+16*(1-e),opacity=e,sh=True)
 motion(p,t,points=[(0,700,470),(send-.16,w-30-44,257),(send-.02,w-30-44,257),(send+.5,w-30-140,380)],clicks=[send],end=send+1.0)
 return clip(p,14)

# ---------- transform flip ----------
def transform(t,S,at):
 im=Image.new('RGBA',(W,H),BG);flip=at('transform','this',2.35,nth=2);first=at('transform','this',1.2,nth=1)
 before=slop(0,780,470);x,y=150,150
 if t<flip:
  e=ease(t/.3);k=1-.06*math.sin(min(1,max(0,(t-first)/.25))*math.pi);place(im,before,x,y+18*(1-e),scale=(.97+.03*e)*k,opacity=e,sh=True)
 else:
  a=t-flip
  if a<.16:
   sx=max(.02,1-a/.16);b=before.resize((round(780*sx),470),Image.Resampling.LANCZOS);place(im,b,x+(780-b.width)/2,y,sh=True)
  else:
   u=a-.16;sx=min(1,spring(u/.32));aft=herowin('After',780,470,u*1.4+.15);b=aft.resize((max(2,round(780*sx)),470),Image.Resampling.LANCZOS);place(im,b,x+(780-b.width)/2,y,sh=True)
 return im

# ---------- app store list (free) ----------
def appstore(t,S,at):
 im=Image.new('RGBA',(W,H),BG);free=at('free','free',2.4)
 c=blank(820,560);rr(c,(0,0,819,559),'white',26)
 c.alpha_composite(apptile('Refero',56),(40,36));txt(c,'Styles',114,34,34,INK,weight='Bold');txt(c,'DESIGN.md references',114,78,17,'#6E6E73')
 line(c,[(40,122),(780,122)],'#EBEBEF',1)
 for i,n in enumerate(['Apple','Notion','Duolingo']):
  e=ease((t-.1-i*.12)/.3)
  if e<=0:continue
  row=blank(740,120);row.alpha_composite(apptile(n,92),(0,14));txt(row,n,116,26,26,INK,weight='Semibold');txt(row,'DESIGN.md  ·  '+['Light theme','Light theme','Playful'][i],116,64,17,'#6E6E73')
  s=1+.18*math.sin(min(1,max(0,(t-free-i*.08)/.3))*math.pi) if t>=free else 1
  pw,ph=112*s,40*s;pill(row,'GET',740-pw-4+(112-pw)/2*0,52-ph/2+20*0,pw,ph,'#EEEEF0' if t<free else BLUE,BLUE if t<free else 'white',18,'Bold')
  if t>=free:
   e2=ease((t-free-.15)/.25);txt(row,'Free',740-56-tw('Free',15,'Medium')/2,84+8*(1-e2),15,(110,110,115,int(255*e2)),weight='Medium')
  if i<2:line(row,[(116,119),(740,119)],'#EBEBEF',1)
  place(c,row,40,136+i*136+14*(1-e),opacity=e)
 e=ease(t/.3);place(im,c,130,120+20*(1-e),opacity=e,sh=True)
 return im

# ---------- available: typing the URL ----------
def available(t,S,at,w=940,h=560):
 """Show the site directly: the Refero styles home, already built, gently settling."""
 return refero_home(t+.55,w,h)

# ---------- comment CTA ----------
def cta(t,S,at):
 k=at('cta','design',1.25);ts=max(.2,k-.5);post=k+.4
 p=ig.render(t,keyword='DESIGN',type_start=ts,type_duration=.45,post_at=post)
 motion(p,t,points=[(0,597,385),(post-.3,813,364),(post-.05,813,364),(post+.4,850,274)],clicks=[post],end=post+.9)
 return p

# ---------- carousel (teach, full) ----------
def teach(t,S,at):
 im=Image.new('RGBA',(W,H),BG);love=at('teach','love',1.75);know=at('teach','know',1.39)
 names=['Apple','Notion','Duolingo'];cw,ch=620,380;gap=40
 # continuous eased slide: card i centered at ~ its onset
 stops=[0,at('teach','that',.7),know];u=0
 for i in range(1,3):u+=smooth((t-stops[i]+.1)/.45)
 x0=540-cw/2-u*(cw+gap)
 for i,n in enumerate(names):
  e=ease((t-i*.05)/.3);x=x0+i*(cw+gap);dist=abs(x+cw/2-540)/(cw+gap);s=1-.08*min(1,dist)
  place(im,herowin(n,cw,ch,t+.3),x,180,scale=s,opacity=e*(1-.35*min(1,dist)),sh=True)
  if t>=love:
   a=t-love-i*.05;v=spring(max(0,a)/.35)
   if a>0:h=heart(84);place(im,h,x+cw/2-42,180+ch*s+34,scale=max(.05,v),opacity=min(1,a*8))
 return im

# ---------- dispatch ----------
def graphics(b,t,S,at):
 name=b['name'];im=Image.new('RGBA',(W,H),BG)
 if name=='hook':return hook(t,S,at)
 if name=='generic':return generic_full(t,S,at)
 if name=='teach':return teach(t,S,at)
 if name=='brands':return dock(t,S,at)
 if name=='document':return document(t,S,at)
 if name=='download':return download(t,S,at)
 if name=='transform':return transform(t,S,at)
 if name=='free':return appstore(t,S,at)
 if name=='generic':enter(im,generic(t,S,at),70,104,t)
 elif name=='teach_intro':enter(im,refero_home(t,940,560),70,104,t)
 elif name=='explain':enter(im,tabs(t,S,at),70,104,t)
 elif name=='investment':enter(im,investment(t,S,at),70,104,t)
 elif name=='choose':enter(im,refero_gallery(t,at('choose','Apple',2.55)),70,150,t)
 elif name=='agent':enter(im,agent(t,S,at),70,104,t)
 elif name=='available':enter(im,available(t,S,at),70,104,t)
 elif name=='cta':enter(im,cta(t,S,at),90,170,t)
 return im
