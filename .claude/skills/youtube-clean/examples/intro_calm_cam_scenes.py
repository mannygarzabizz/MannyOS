"""00-intro — Jev YouTube video. Every scene runs on ABSOLUTE section time T (word onsets straight from transcript.json).
Copy/numbers come from P/research (x-launch-post.md, x-profile.md, facts.md). Light-mode recreations, no screenshots of the desktop."""
import json,math,re
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import ImageFilter
from draw import *
import layout as L, captions, emoji
import editorial_caption as editorial
from pointer_motion import motion

HERE=Path(__file__).resolve().parent;RA=HERE.parent.parent/'research/assets'
_T=json.load(open(HERE/'transcript.json'));WORDS=_T['words'] if isinstance(_T,dict) else _T
def _bare(s):return re.sub(r'[^a-z0-9$%]','',s.lower())
def Wt(word,after=0.,nth=0):
 ww=[w['start'] for w in WORDS if _bare(w['text'])==_bare(word) and w['start']>=after-.005]
 if len(ww)<=nth:raise KeyError(word)
 return ww[nth]
LEAD=.13

# rev 4 (Albert: calmer, ~50/50, "only when it actually needs a visual"): 'cam' = presenter full screen with a lower-third caption.
MODES=[(0,'split'),(.27,'full:hidden'),(5.5,'cam'),(7.85,'full:hidden'),(17.2,'cam'),(25.45,'full:hidden'),(31.2,'cam'),(40.95,'split')]
FACE_CX=[(1.5,981),(4.5,986),(7.5,981),(10.5,969),(13.5,973),(16.5,1004),(19.5,1025),(22.5,987),(25.5,940),(28.5,948),(31.5,988),(34.5,1018),(37.5,1012),(40.5,998),(43.5,1007),(46.5,999),(49.5,989),(52.5,1016)]
CINE_BEATS={'xpost','built'}
CINE_Y=925
editorial.special.update({'DIOGO':'Diogo','ALMEIDA':'Almeida','X':'X','CHATGPT':'ChatGPT'})
def edit_groups(G):
 # "VIRAL 33 MILLION" + "VIEWS"  ->  "VIRAL" + "33 MILLION VIEWS" (payoff group)
 i=next(k for k,g in enumerate(G) if g['text']=='VIRAL 33 MILLION');a,b=G[i],G[i+1];ws=a['words']+b['words'];t33=ws[1]['entry_frame']/30
 G[i:i+2]=[dict(a,text='VIRAL',end=t33,words=ws[:1]),dict(a,text='33 MILLION VIEWS',start=t33,end=b['end'],words=ws[1:])]
 # groups spoken while Albert is still full screen would sit under the camera picture: drop them
 G=[g for g in G if not (g['scene']=='xpost' and g['start']<7.95) and not (g['scene']=='built' and g['start']<25.6)]
 seen=set()
 for g in G:
  g['big']=118
  if g['scene'] not in seen:g['cap']=True;seen.add(g['scene'])
  tx=g['text']
  if tx.startswith('33 MILLION'):g['big']=150;g['color']='#1E8E3E'
  if 'ALMEIDA' in tx or 'INVENTED' in tx:g['big']=130
 return G

# ink key phrases on the white ground (runner-side)
CAPTIONS=[
 dict(beat='nocust',text='0 customers',words=['any','customer'],end=2.3,y=915,size=84,area='full',emph={'0':'red'}),
 dict(beat='getin',text="Let's get into it",start=-.1,stagger=.07,end=.62,y=540,size=84,emph={'into':'italic','it':'italic'}),
]
# white lower-third key phrases over the full-screen presenter ('cam'): (text, [word onsets' spoken words], after, end, emoji-free unless it adds something)
CAM_CAPS=[
 dict(text='How is this even a thing?',on=['How','is','this','even','a','thing?'],after=5.8,end=7.2),
 dict(text="Here's the weird part",on=["here's",'the','weird','part,'],after=17.4,end=18.8),
 dict(text="Can't write an email ✉️",on=["can't",'write','an','email.','email.'],after=19.9,end=21.62),
 dict(text='Cannot write code',on=['cannot','write','code,'],after=21.7,end=23.3),
 dict(text="Can't even say hello 👋",on=["can't",'even','say','hello.','hello.'],after=23.4,end=24.95),
 dict(text='Extremely useful',on=['extremely','useful.'],after=34.2,end=35.75),
 dict(text='Not really technical?',on=['not','really','technical,'],after=36.1,end=37.7),
]
for c in CAM_CAPS:
 c['times']=[Wt(w,c['after'])-LEAD for w in c['on']];c['start']=min(c['times'])
@lru_cache(maxsize=512)
def _cam_word(word,size):
 """One caption word, white SF Pro Semibold with a soft dark shadow, drawn as ONE string on its baseline."""
 if emoji.is_emoji(word):
  e=emoji.emoji(word,round(size*1.08));return e,e.width,None
 f=sf(size,'Semibold');b=f.getbbox(word,anchor='ls');pad=40;w,h=b[2]-b[0]+2*pad,b[3]-b[1]+2*pad
 shd=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]+4),word,font=f,anchor='ls',fill=(0,0,0,210));shd=shd.filter(ImageFilter.GaussianBlur(9))
 t2=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(t2).text((pad-b[0],pad-b[1]+2),word,font=f,anchor='ls',fill=(0,0,0,120));shd.alpha_composite(t2.filter(ImageFilter.GaussianBlur(2)))
 ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]),word,font=f,anchor='ls',fill='white');return shd,f.getlength(word),(b[0]-pad,b[1]-pad)
@lru_cache(None)
def _scrim():
 g=np.zeros((1080,1920,4),np.uint8);y=np.arange(1080);a=np.clip((y-640)/440,0,1)**1.6*120;g[...,3]=a[:,None].astype(np.uint8);return Image.fromarray(g,'RGBA')
def overlay(b,t,S,at,st):
 """Drawn ABOVE the presenter by the runner. Only while the card (nearly) fills the frame."""
 T=b['start']+t;k=smooth((st.w-1500)/400)*st.opacity
 if k<=0:return None
 live=[c for c in CAM_CAPS if c['start']<=T<c['end']]
 if not live:return None
 c=live[0];size=80;words=c['text'].split();gap=sf(size,'Semibold').getlength(' ');tiles=[_cam_word(w,size) for w in words]
 width=sum(a for _,a,_ in tiles)+gap*(len(words)-1);x=960-width/2;base=905;im=canvas()
 fo=smooth((c['end']-T)/.18)*k;sc=_scrim();im.alpha_composite(fade(sc,min(1,ease((T-c['start'])/.3))*fo))
 for (tile,adv,off),tw0 in zip(tiles,c['times']):
  e=ease((T-tw0)/.18)
  if e>0:
   px,py=(x,base-size*.36-tile.height/2) if off is None else (x+off[0],base+off[1])
   im.alpha_composite(fade(tile,e*fo),(round(px),round(py+8*(1-e))))
  x+=adv+gap
 return im

# ---------------------------------------------------------------- helpers
def T_(im,s,x,y,font,fill=INK,anchor='lm'):ImageDraw.Draw(im).text((x,y),s,font=font,fill=fill,anchor=anchor)
def fade(im,a):
 if a>=1:return im
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:int(v*max(0,a))));return im
def env(T,a,b,i=.28,o=.25):return ease((T-a)/i)*(1-smooth((T-(b-o))/o))
def circle_crop(src,d):
 im=src.resize((d*4,d*4),Image.Resampling.LANCZOS);m=Image.new('L',(d*4,d*4),0);ImageDraw.Draw(m).ellipse((0,0,d*4-1,d*4-1),fill=255)
 im.putalpha(m);return im.resize((d,d),Image.Resampling.LANCZOS)
@lru_cache(None)
def avatar(d):
 a=Image.open(RA/'almeida-avatar-profile.png').convert('RGB').crop((8,10,138,140));return circle_crop(a,d)
@lru_cache(None)
def verified(d):
 q=4;im=blank(d*q,d*q);dr=ImageDraw.Draw(im);c=d*q/2
 for i in range(8):
  a=i/8*2*math.pi;r=d*q*.19;dr.ellipse((c+math.cos(a)*d*q*.30-r,c+math.sin(a)*d*q*.30-r,c+math.cos(a)*d*q*.30+r,c+math.sin(a)*d*q*.30+r),fill='#1D9BF0')
 dr.ellipse((c-d*q*.34,c-d*q*.34,c+d*q*.34,c+d*q*.34),fill='#1D9BF0')
 dr.line([(c-d*q*.17,c+d*q*.01),(c-d*q*.04,c+d*q*.14),(c+d*q*.19,c-d*q*.13)],fill='white',width=round(d*q*.09),joint='curve')
 return im.resize((d,d),Image.Resampling.LANCZOS)
@lru_cache(None)
def affiliate(d):
 im=blank(d,d);rr(im,(0,0,d-1,d-1),'#E0349A',max(2,d//6));m=Image.open(RA/'logo-typesafe.png').convert('RGBA');k=d*.72/m.height
 m=m.resize((max(1,round(m.width*k)),max(1,round(m.height*k))),Image.Resampling.LANCZOS);s=Image.new('RGBA',m.size,'#1A0B14');s.putalpha(m.getchannel('A'));im.alpha_composite(s,((d-m.width)//2,(d-m.height)//2));return im
@lru_cache(None)
def gpt_tile(size):return apptile('ChatGPT',size)
def tile_ring(im,x,y,size):
 ImageDraw.Draw(im).rounded_rectangle((x,y,x+size,y+size),radius=size*.235,outline='#E3E3E6',width=2)

# ---------------------------------------------------------------- 1 numbers (0-5.75) full
def numbers(T):
 im=canvas();t200=Wt('200');tf=Wt('faster');t400=Wt('400');tc=Wt('cheaper');tg=Wt('ChatGPT.')
 out=1-smooth((T-5.42)/.26)
 if out<=0:return im
 mv=smooth((T-(t400-.42))/.4)            # 200x slides left and shrinks
 up=smooth((T-(tg-.42))/.4)              # both rise, ChatGPT row arrives
 def block(val,label,cx,cy,sc,landed,lab_a,color):
  lay=blank(1100,700);d=ImageDraw.Draw(lay);s=f'{val}×'
  d.text((550,280),s,font=sf(360,'Bold'),fill=color if landed else INK,anchor='mm')
  if lab_a>0:
   l2=blank(1100,160);ImageDraw.Draw(l2).text((550,80),label,font=sf(128,'Semibold'),fill=INK,anchor='mm');place(lay,l2,0,490+22*(1-lab_a),opacity=lab_a)
  w,h=lay.size;lay=lay.resize((round(w*sc),round(h*sc)),Image.Resampling.LANCZOS);return lay,cx-lay.width/2,cy-lay.height/2
 # 200x
 v=ease((T-(t200-LEAD-.52))/.55);a=ease((T-.3)/.25)
 if a>0:
  sc=lerp(1,.72,mv);cx=lerp(960,490,mv);cy=lerp(500,470,mv)-70*up
  lay,x,y=block(round(200*v),'faster',cx,cy,sc,v>=1,ease((T-(tf-LEAD))/.22),BLUE)
  # speed streaks behind the number while it counts
  if .02<v<1:
   st=canvas();d=ImageDraw.Draw(st)
   for i in range(7):
    yy=300+i*52;ph=(T*9+i*.37)%1;x0=200+ph*1300;d.rounded_rectangle((x0,yy,x0+220,yy+6),3,fill=(0,113,227,int(70*(1-abs(ph-.5)*2))))
   im.alpha_composite(st)
  place(im,lay,x,y,opacity=a*out)
 # 400x
 a=ease((T-(t400-.4))/.25)
 if a>0:
  v=ease((T-(t400-LEAD-.3))/.4);lay,x,y=block(round(400*v),'cheaper',1430,470-70*up+30*(1-a),.72,v>=1,ease((T-(tc-LEAD))/.22),GREEN)
  place(im,lay,x,y,opacity=a*out)
  if mv>0:
   ln=canvas();ImageDraw.Draw(ln).rounded_rectangle((944,300-70*up,948,640-70*up),2,fill=(227,227,230,int(255*mv*out)));im.alpha_composite(ln)
 # than ChatGPT
 a=spring((T-(tg-LEAD-.25))/.34) if T>tg-LEAD-.25 else 0
 if a>0:
  row=blank(900,190);tl=gpt_tile(150);row.alpha_composite(tl,(60,20));tile_ring(row,60,20,150)
  T_(row,'than ChatGPT',250,95,sf(92,'Semibold'),INK,'lm');wd=250+tw('than ChatGPT',92,'Semibold');r2=row.crop((40,0,min(900,int(wd)+20),190))
  place(im,r2,960-r2.width/2,760+40*(1-min(1,a)),scale=.9+.1*min(1.05,a),opacity=min(1,a)*out)
 return im

# ---------------------------------------------------------------- 3 xpost (7.08-13.0) full: light-mode X post, tilt, push-in on 33M Views
K=2;PGW,PGH=1100,900;COLX=250;COLW=600
XT='#0F1419';XG='#536471';XL='#EFF3F4';XB='#1D9BF0'
POST=["After co-inventing ChatGPT, I kept asking myself: why have superhuman","chat models not led to AGI?","",
 "I’ve spent the last 2 years in stealth building a new way to train models","(RLCD), and a new type of frontier AI model that we are releasing today:","Jev","",
 "• 20-200x faster","• 40-400x cheaper (w/ output tokens free)","• Frontier composable intelligence optimized for decisions","",
 "AFAICT the shortest path to AI-based economic revolution"]
TXY=126;LH=24;VIDY=TXY+len(POST)*LH+10;VIDH=round(COLW*9/16);METAY=VIDY+VIDH+30;ROWY=METAY+52
GEO={}
def xi(im,kind,x,y,k,col=XG):
 d=ImageDraw.Draw(im);w=max(2,round(1.7*k))
 def P(px,py):return (x+px*k,y+py*k)
 if kind=='reply':d.rounded_rectangle((*P(0,0),*P(20,16)),8*k,outline=col,width=w);d.polygon([P(5,15),P(5,21),P(11,15)],fill=col)
 elif kind=='repost':
  d.line([P(3,7),P(3,16),P(14,16)],fill=col,width=w);d.line([P(19,12),P(19,3),P(8,3)],fill=col,width=w);d.polygon([P(-1,8),P(7,8),P(3,3)],fill=col);d.polygon([P(15,11),P(23,11),P(19,16)],fill=col)
 elif kind=='like':
  pts=[]
  for i in range(60):
   a=i/60*2*math.pi;xx=16*math.sin(a)**3;yy=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a);pts.append(P(10+xx*.62,9-yy*.62))
  d.line(pts+[pts[0]],fill=col,width=w,joint='curve')
 elif kind=='bookmark':d.line([P(3,0),P(17,0),P(17,20),P(10,14),P(3,20),P(3,0)],fill=col,width=w,joint='curve')
 elif kind=='share':d.line([P(10,1),P(10,14)],fill=col,width=w);d.line([P(5,6),P(10,1),P(15,6)],fill=col,width=w,joint='curve');d.line([P(2,11),P(2,19),P(18,19),P(18,11)],fill=col,width=w,joint='curve')
@lru_cache(None)
def xpage():
 k=K;p=Image.new('RGBA',(PGW*k,PGH*k),'white');d=ImageDraw.Draw(p);x0=COLX
 d.line([((x0-16)*k,0),((x0-16)*k,PGH*k)],fill=XL,width=k);d.line([((x0+COLW+16)*k,0),((x0+COLW+16)*k,PGH*k)],fill=XL,width=k)
 # header: back arrow + Post
 d.line([((x0+4)*k,28*k),((x0+22)*k,28*k)],fill=XT,width=2*k);d.line([((x0+12)*k,20*k),((x0+4)*k,28*k),((x0+12)*k,36*k)],fill=XT,width=2*k,joint='curve')
 T_(p,'Post',(x0+54)*k,28*k,sf(20*k,'Bold'),XT)
 # author
 p.alpha_composite(avatar(44*k),(x0*k,62*k));nm='Diogo Almeida';T_(p,nm,(x0+56)*k,74*k,sf(16*k,'Bold'),XT);bx=x0+56+tw(nm,16,'Bold')+4
 p.alpha_composite(verified(20*k),(round(bx*k),64*k));p.alpha_composite(affiliate(16*k),(round((bx+24)*k),66*k))
 T_(p,'@CompleteSkeptic',(x0+56)*k,95*k,sf(15*k),XG);T_(p,'···',(x0+COLW-8)*k,74*k,sf(20*k,'Bold'),XG,'rm')
 # media card
 v=Image.open(RA/'launch-video-frame-talking-head.png').convert('RGB');vw=v.width;v=v.crop((70,0,70+352,198)).resize((COLW*k,VIDH*k),Image.Resampling.LANCZOS).convert('RGBA')
 v=clip(v,16*k);p.alpha_composite(v,(x0*k,VIDY*k))
 cx,cy=(x0+COLW/2)*k,(VIDY+VIDH/2)*k;r=30*k;d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=XB,outline='white',width=3*k);d.polygon([(cx-9*k,cy-13*k),(cx-9*k,cy+13*k),(cx+14*k,cy)],fill='white')
 rr(p,((x0+12)*k,(VIDY+VIDH-34)*k,(x0+62)*k,(VIDY+VIDH-12)*k),(0,0,0,170),5*k);T_(p,'2:56',(x0+37)*k,(VIDY+VIDH-23)*k,sf(13*k,'Medium'),'white','mm')
 # meta line (33M is drawn live)
 s='9:17 PM · Sep 15, 2026 · ';T_(p,s,x0*k,METAY*k,sf(15*k),XG);GEO['views_x']=x0+tw(s,15)
 d.line([(x0*k,(METAY+24)*k),((x0+COLW)*k,(METAY+24)*k)],fill=XL,width=k);d.line([(x0*k,(ROWY+28)*k),((x0+COLW)*k,(ROWY+28)*k)],fill=XL,width=k)
 for i,kind in enumerate(['reply','repost','like','bookmark']):xi(p,kind,(x0+8+i*150)*k,(ROWY-10)*k,k)
 xi(p,'share',(x0+COLW-30)*k,(ROWY-10)*k,k)
 return p
def fmt_views(v):
 if v>=33e6:return '33M'
 if v>=1e6:return f'{v/1e6:.1f}M'
 return f'{v/1e3:.0f}K'
def fmt_k(v,final):
 if v>=final:return (f'{final/1000:.1f}'.rstrip('0').rstrip('.'))+'K'
 return f'{v/1000:.1f}K' if v>=1000 else f'{int(v)}'
VW,VH=1240,640;WINX,WINY=340,56
def xpost(T):
 im=canvas();t0=7.9;tl=Wt('launched');tv=Wt('viral.');t33=Wt('33');tvw=Wt('views,')
 a=env(T,t0,13.0,.3,.22)
 if a<=0:return im
 page=xpage();asp=VH/VW
 def box(cx,cy,w):return (cx-w/2,cy-w*asp/2,cx+w/2,cy+w*asp/2)
 wide=box(COLX+COLW/2,0,720);wide=(wide[0],52,wide[2],52+720*asp)
 low=box(COLX+COLW/2,ROWY+40-760*asp/2,760);mx=GEO['views_x']+60;zoom=box(COLX+150,METAY+8,470)
 z1=smooth((T-(tv-.75))/.6);z2=smooth((T-(t33-.62))/.5);drift=min(60,(T-t0)*22)*(1-z1)
 bx=[lerp(lerp(wide[i],low[i],z1),zoom[i],z2) for i in range(4)];bx[1]+=drift;bx[3]+=drift
 crop=page.crop(tuple(round(v*K) for v in bx)).resize((VW,VH),Image.Resampling.LANCZOS);sc=VW/(bx[2]-bx[0])
 X=lambda x:(x-bx[0])*sc
 Y=lambda y:(y-bx[1])*sc
 # post text wipes in line by line from "launched"
 for i,l in enumerate(POST):
  if not l:continue
  u=ease((T-(tl-LEAD-.1)-i*.05)/.24)
  if u<=0:continue
  y=Y(TXY+i*LH+12)+8*sc*(1-u);lay=blank(VW,round(40*sc));x=X(COLX)
  if 'superhuman' in l:
   pre,post_=l.split('superhuman');T_(lay,pre,x,20*sc,sf(17*sc),XT);x2=x+sf(17*sc).getlength(pre);T_(lay,'superhuman',x2,20*sc,sf(17*sc,'Bold'),XT)
  else:T_(lay,l,x,20*sc,sf(17*sc,'Bold' if l=='Jev' else 'Regular'),XT)
  place(crop,lay,0,y-20*sc,opacity=u)
 # live counters
 cu=ease((T-(tv-LEAD))/.75)
 for i,(final) in enumerate([3500,12000,67000,55000]):
  T_(crop,fmt_k(final*cu,final),X(COLX+8+i*150+30),Y(ROWY),sf(14*sc),XG)
 vv=ease((T-(t33-LEAD-.62))/.62);vs=fmt_views(33e6*vv);fx=X(GEO['views_x']);fy=Y(METAY)
 # highlighter on "33M Views" on the word "views"
 hu=ease((T-(tvw-LEAD))/.3);wv=sf(15*sc,'Bold').getlength(vs);wall=wv+sf(15*sc).getlength(' Views')
 if hu>0:rr(crop,(fx-3*sc,fy-11*sc,fx-3*sc+(wall+8*sc)*hu,fy+11*sc),HILITE,4*sc)
 T_(crop,vs,fx,fy,sf(15*sc,'Bold'),XT);T_(crop,' Views',fx+wv,fy,sf(15*sc),XG)
 if T>=t33-LEAD:
  u=ease((T-(t33-LEAD))/.22);lay=blank(VW,VH);ImageDraw.Draw(lay).rounded_rectangle((fx-5*sc,fy-15*sc,fx+wall+8*sc,fy+15*sc),7*sc,outline=(255,59,48,int(235*u)),width=max(2,round(1.6*sc)));crop.alpha_composite(lay)
 motion(crop,T,points=[(tl+.9,1080,560),(tv-.2,980,430),(t33-.15,fx+wall+60*sc/2.9,fy+44),(12.9,fx+wall+70,fy+50)],end=12.8)
 win=window(VW,VH+52,url='x.com',r=16);win.alpha_composite(crop,(0,53));win=clip(win,16)
 e=ease((T-t0)/.3);place(im,win,WINX,WINY+26*(1-e),scale=.96+.04*e,opacity=a,sh=True)
 return im

# ---------------------------------------------------------------- 4 raised + nocust (13.0-17.32) full
def money(T):
 im=canvas();t40=Wt('$40');tw_=Wt('without');tcu=Wt('customer')
 a=env(T,13.0,17.32,.26,.24)
 if a<=0:return im
 card=blank(1500,620);rr(card,(0,0,1499,619),'#1D1D1F',44)
 v=ease((T-(t40-LEAD-.55))/.58);val=round(40_000_000*v);landed=v>=1
 lay=blank(1500,620);T_(lay,f'${val:,}',750,270,sf(210,'Bold'),'#30D158' if landed else 'white','mm')
 la=ease((T-(t40+.25))/.25)
 if la>0:
  l2=blank(1500,100);T_(l2,'seed round · led by DCVC',750,50,sf(46,'Medium'),'#A1A1A6','mm');place(lay,l2,0,420+14*(1-la),opacity=la)
 l3=blank(1500,90);ts=Image.open(RA/'logo-typesafe.png').convert('RGBA');k=54/ts.height;ts=ts.resize((round(ts.width*k),54),Image.Resampling.LANCZOS);wh=Image.new('RGBA',ts.size,'white');wh.putalpha(ts.getchannel('A'))
 wd=tw('TypeSafe AI',40,'Semibold');x0=750-(ts.width+16+wd)/2;l3.alpha_composite(wh,(round(x0),18));T_(l3,'TypeSafe AI',x0+ts.width+16,45,sf(40,'Semibold'),'white');lay.alpha_composite(l3,(0,50))
 card.alpha_composite(lay);e=ease((T-13.0)/.3)
 place(im,card,960-750,130+28*(1-e),opacity=a,sh=True)
 return im

# ---------------------------------------------------------------- 8 built (24.95-31.23) full: X profile card + ChatGPT tile
BIO=[('Sane + ',XT),('🌶',None),(' takes in an insane AI world... AI capabilities researcher: ',XT),('co-created RLHF/ChatGPT',XT,'hl'),(' @ ',XT),('@openai',XB),(' now trying to right the wrong ',XT),('🤭',None),(' (ceo ',XT),('@typesafeai',XB),(')',XT)]
def flow(im,toks,x,y,width,size,lh,weight='Regular'):
 """Tiny rich-text flow: coloured runs + Apple emoji, word wrap. Returns {tag:[boxes]} for tagged runs."""
 f=sf(size,weight);cx,cy=x,y;boxes={};sp=f.getlength(' ')
 for tk in toks:
  s,col=tk[0],tk[1];tag=tk[2] if len(tk)>2 else None
  if col is None:
   if cx+size>x+width:cx=x;cy+=lh
   emoji.place_emoji(im,s,cx,cy-size*.55,size*1.1);cx+=size*1.15;continue
  parts=re.findall(r'\s+|\S+',s)
  for p in parts:
   if p.isspace():cx+=sp*len(p);continue
   wl=f.getlength(p)
   if cx+wl>x+width:cx=x;cy+=lh
   T_(im,p,cx,cy,f,col)
   if tag:boxes.setdefault(tag,[]).append((cx,cy-lh/2+2,cx+wl+sp,cy+lh/2-2))
   cx+=wl
 return boxes,cy
PCW=880
@lru_cache(None)
def profile_card():
 w=PCW;bh=round(w*200/590);h=bh+372;p=blank(w,h);rr(p,(0,0,w-1,h-1),'white',28)
 ban=Image.open(RA/'almeida-banner.png').convert('RGBA').resize((w,bh),Image.Resampling.LANCZOS);p.alpha_composite(ban,(0,0))
 d=ImageDraw.Draw(p);ad=196;ax,ay=20,bh-118;d.ellipse((ax-8,ay-8,ax+ad+8,ay+ad+8),fill='white');p.alpha_composite(avatar(ad),(ax,ay))
 d.rectangle((ax+ad+10,bh,w,bh+10),fill='white')
 # buttons
 by=bh+22
 for i in range(2):
  bx=w-300+i*62;d.ellipse((bx,by,bx+48,by+48),outline='#CFD9DE',width=2)
 for j in range(3):d.ellipse((w-300+13+j*9,by+21,w-300+19+j*9,by+27),fill=XT)
 d.rounded_rectangle((w-238+13,by+15,w-238+35,by+31),4,outline=XT,width=2);d.line([(w-238+14,by+17),(w-238+24,by+25),(w-238+34,by+17)],fill=XT,width=2)
 rr(p,(w-160,by,w-28,by+48),'#0F1419',24);T_(p,'Follow',w-94,by+24,sf(21,'Bold'),'white','mm')
 ny_=bh+112;nm='Diogo Almeida';T_(p,nm,28,ny_,sf(32,'Heavy'),XT);bx=28+tw(nm,32,'Heavy')+8;p.alpha_composite(verified(34),(round(bx),ny_-17));p.alpha_composite(affiliate(26),(round(bx+40),ny_-13))
 T_(p,'@CompleteSkeptic',28,ny_+38,sf(23),XG)
 boxes,yy=flow(p,BIO,28,ny_+92,w-56,23,32);GEO['bio_hl']=boxes['hl']
 yy+=44;d.rounded_rectangle((28,yy-10,48,yy+10),3,outline=XG,width=2);d.line([(28,yy-3),(48,yy-3)],fill=XG,width=2);T_(p,'Joined October 2014',58,yy,sf(22),XG)
 yy+=42;x=28
 for n_,l_ in [('95','Following'),('106.8K','Followers')]:
  T_(p,n_,x,yy,sf(22,'Bold'),XT);x+=tw(n_,22,'Bold')+6;T_(p,l_,x,yy,sf(22),XG);x+=tw(l_,22)+28
 GEO['name_box']=(22,ny_-24,bx-2,ny_+56);GEO['av']=(ax,ay,ad);GEO['pc_h']=h
 return clip(p,28)
def built(T):
 im=canvas();a=env(T,25.45,31.23,.3,.24)
 if a<=0:return im
 tb=Wt('built');tguy=Wt('guy');tn=Wt('Diogo');tinv=Wt('invented');tg=Wt('ChatGPT.',29)
 card=profile_card().copy();h=GEO['pc_h']
 # name highlighter on "Diogo Almeida"
 u=ease((T-(tn-LEAD))/.35)
 if u>0:
  b=GEO['name_box'];hl=blank(*card.size);rr(hl,(b[0],b[1]+6,b[0]+(b[2]-b[0])*u,b[1]+44),HILITE,8);card.alpha_composite(hl)
 u=ease((T-(tinv-LEAD))/.4)
 if u>0:
  bs=GEO['bio_hl'];tot=sum(b[2]-b[0] for b in bs);run=tot*u;hl=blank(*card.size)
  for b in bs:
   wseg=b[2]-b[0];k=max(0,min(wseg,run));run-=wseg
   if k>0:rr(hl,(b[0]-3,b[1],b[0]+k,b[3]),HILITE,6)
  card.alpha_composite(hl)
 mv=smooth((T-(tinv-.5))/.45);x=lerp(520,230,mv);e=ease((T-25.5)/.32);pulse=1+.035*math.sin(min(1,max(0,(T-(tguy-LEAD))/.35))*math.pi)
 place(im,card,x,52+28*(1-e),scale=(.95+.05*e)*pulse,opacity=a*e,sh=True)
 # ring around the avatar on "this guy"
 g=ease((T-(tguy-LEAD))/.25)*(1-smooth((T-(tn+.9))/.3))
 if g>0:
  ax,ay,ad=GEO['av'];cx,cy=x+ax+ad/2,52+ay+ad/2;r=ad/2+14+10*(1-g);lay=canvas();ImageDraw.Draw(lay).ellipse((cx-r,cy-r,cx+r,cy+r),outline=(255,59,48,int(240*g*a)),width=6);im.alpha_composite(lay)
 # ChatGPT tile on the right
 s=spring((T-(tg-LEAD-.12))/.36) if T>tg-LEAD-.12 else 0;pre=ease((T-(tinv-LEAD))/.3)
 if pre>0:
  lay=canvas();d=ImageDraw.Draw(lay);d.line([(1100,400),(1270,400)],fill=(199,199,204,int(255*pre*a)),width=4)
  d.polygon([(1270,388),(1292,400),(1270,412)],fill=(199,199,204,int(255*pre*a)));im.alpha_composite(lay)
 if s>0:
  size=280;tl=gpt_tile(size).copy();tile_ring(tl,1,1,size-2);place(im,tl,1330,260,scale=max(.05,min(1.06,s)),opacity=min(1,s*2)*a,sh=True)
  l2=blank(500,70);T_(l2,'ChatGPT',250,35,sf(50,'Semibold'),INK,'mm');place(im,l2,1330+size/2-250,566,opacity=ease((T-tg)/.25)*a)
 return im

# ---------------------------------------------------------------- 11 agenda (40.04-52.44) split: four rows check in
ROWS=[('What this thing actually is','what','is,','🧩'),('Why it’s so fast','why','fast,','⚡'),('Where it lacks vs ChatGPT','where','ChatGPT,','gpt'),('How it changes what we build','why,','build.','🛠')]
def agenda(T):
 im=canvas()
 if T<40.1:return im
 tvid=Wt('video,');x0,y0,w=110,150,1030;lw=52.1
 ha=ease((T-(tvid-LEAD-.15))/.3)
 hd=blank(w,90);T_(hd,'In this video',0,45,ny(64,'Semibold'),INK);out_h=1-smooth((T-(lw-.2))/.3);place(im,hd,x0,y0-10+12*(1-ha),opacity=ha*out_h)
 for i,(lab,w_on,w_off,em) in enumerate(ROWS):
  ton=Wt(w_on,47. if i==3 else 41.1)-LEAD;tof=Wt(w_off,41.1)+.12;u=ease((T-ton)/.4)
  if u<=0:continue
  active=ton<=T<tof+.25;done=T>=tof;rh=150;row=blank(w,rh)
  rr(row,(0,0,w-1,rh-1),'#F5F5F7',32)
  if done:
   checkmark(row,76,rh/2,34,GREEN)
  else:
   ImageDraw.Draw(row).ellipse((42,rh/2-34,110,rh/2+34),fill=INK);T_(row,str(i+1),76,rh/2,sf(36,'Bold'),'white','mm')
  T_(row,lab,142,rh/2,sf(46,'Semibold'),INK if (active or not done) else '#3A3A3C')
  if em=='gpt':tl=gpt_tile(84);row.alpha_composite(tl,(w-130,rh//2-42));tile_ring(row,w-130,rh//2-42,84)
  else:emoji.place_emoji(row,em,w-88,rh/2,80,anchor='mm')
  o=smooth((T-(lw-.15))/.3)
  place(im,row,x0,y0+100+i*(rh+22)+14*(1-u),opacity=u*(1-o),sh=False)
 return im

def graphics(b,t,S,at):
 T=b['start']+t;n=b['name']
 if n=='numbers':return numbers(T)
 if n=='xpost':return xpost(T)
 if n in('raised','nocust'):return money(T)
 if n=='built':return built(T)
 if n in('agenda','nowaste'):return agenda(T)
 return None      # how / weird / email / code / hello / reason / useful / technical: Albert full screen ('cam'), captions via overlay()
