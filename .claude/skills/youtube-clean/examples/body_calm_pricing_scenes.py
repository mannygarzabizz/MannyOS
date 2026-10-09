"""03-why-so-cheap (50 s, body). Everything is recreated; no screen share.
 0.0- 6.1 split  ChatGPT-style chat window streaming an answer word by word
 6.1-15.0 full   two-lane race (chat model still typing vs Jev done in 114 ms) + 70 ms..500 ms range bar
15.0-18.9 full   typesafe.ai launch post, "Frontiers, Old and New" table: push-in on the Cost cell, $0.042 counts up, red frame, highlighter
18.9-28.9 split  price table (official pricing pages, see sources.md): input + multiples, then output column, Jev flips to FREE, token counter dies
28.9-40.2 full   50,000,000 reviews -> Jev receipt ~$20 vs normal-model receipt "thousands"
40.2-50.1 split  recap rows, then "can't hallucinate" key phrase, clean exit
All timing is section-absolute (T) and comes from transcript.json via at()."""
from draw import *
import layout as L, captions, emoji
import random
import numpy as np
from pathlib import Path
from pointer_motion import motion
HERE=Path(__file__).resolve().parent;PR=HERE.parent.parent
MODES=[(0,'cam'),(14.55,'full'),(40.12,'cam')]   # calm cut: ~50 % cam / ~50 % visuals
FACE_CX=[(1.0,1035),(3.0,1040),(5.0,1035),(7.0,1037),(9.0,1042),(11.0,1031),(13.0,1014),(15.0,998),(17.0,976),(19.0,994),(21.0,1012),(23.0,1002),(25.0,1027),(27.0,1031),(29.0,1005),(31.0,986),(33.0,970),(35.0,970),(37.0,988),(39.0,1004),(41.0,1018),(43.0,1046),(45.0,1041),(47.0,1026),(49.0,1050)]
CAPTIONS=[
 dict(beat='b04',text='Four cents 💰',words=['four','cents',1.3],end=2.2,y=935,size=76,area='full',emph={'cents':'green'}),
 dict(beat='b07',text='About 20 bucks 💸',words=['about','20','bucks.',2.95],end=3.3,y=965,size=76,area='full',emph={'20':'green','bucks':'green'}),
]
GOLD='#FFB800';PALE='#F5F5F7'
@lru_cache(None)
def inter(n,weight='Regular'):
 f=ImageFont.truetype(str(PR/'lib/assets/fonts/Inter.ttf'),int(n));f.set_variation_by_name(weight);return f
@lru_cache(None)
def logo_ts(size):
 q=4;t=Image.new('RGBA',(size*q,size*q),'#F386A1');m=Image.open(PR/'research/assets/logo-typesafe.png').convert('RGBA');k=round(size*q*.68);m=m.resize((round(k*m.width/m.height),k),Image.Resampling.LANCZOS)
 t.alpha_composite(m,((size*q-m.width)//2,(size*q-m.height)//2));return clip(t.resize((size,size),Image.Resampling.LANCZOS),round(size*.22))
def T_(im,s,x,y,f,fill=INK,anchor='lm'):ImageDraw.Draw(im).text((round(x),round(y)),s,font=f,fill=fill,anchor=anchor)
def fade(im,a):
 if a>=1:return im
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:int(v*max(0,a))));return im
def win(t0,t1,T,d=.3):return ease((T-t0)/d)*(1-smooth((T-t1)/d))
_AT={}
def A(S,at,beat,word,default,nth=0):
 k=(beat,word,nth)
 if k not in _AT:_AT[k]=S[beat]['start']+at(beat,word,default,nth)
 return _AT[k]

# ================= 1. chat window (split) =================
ANSWER=("This review is mostly positive. The customer mentions that the package arrived late, which is a negative point about shipping, but they go on to say that the product works great, which suggests they are satisfied overall. So I would classify the sentiment as positive, with a minor complaint about the delivery time. If you want, I can also break this down into separate scores for product quality, shipping speed and overall satisfaction, or rewrite the review in a more neutral tone so that it is easier to compare with the other reviews in your table. Just let me know which of these options would be the most useful for you and I will get started right away").split()
STREAM0,RATE=1.17,7.5
def nwords(T):return max(0.,(T-STREAM0)*RATE)
@lru_cache(None)
def answer_layout(size,width):
 f=sf(size);sp=f.getlength(' ');x=0;line=0;pos=[]
 for w_ in ANSWER:
  wl=f.getlength(w_)
  if x+wl>width and x>0:x=0;line+=1
  pos.append((x,line));x+=wl+sp
 return pos
def draw_stream(im,x0,y0,size,width,lh,T,first_line=0,max_lines=99,color=INK):
 pos=answer_layout(size,width);n=nwords(T);f=sf(size);last=None
 for i,(w_,(x,ln)) in enumerate(zip(ANSWER,pos)):
  a=min(1.,(n-i)/.9)
  if a<=0:break
  if ln<first_line or ln>=first_line+max_lines:continue
  c=tuple(int(lerp(170,v,a)) for v in (29,29,31))+(int(255*a),)
  T_(im,w_,x0+x,y0+(ln-first_line)*lh,f,c,'ls');last=(x0+x+f.getlength(w_),y0+(ln-first_line)*lh)
 if last:
  r=size*.30*(.85+.15*math.sin(T*9));ImageDraw.Draw(im).ellipse((last[0]+10,last[1]-size*.36-r,last[0]+10+2*r,last[1]-size*.36+r),fill=INK)
 return pos
CW,CH=1050,690
@lru_cache(None)
def chat_static():
 w=window(CW,CH,url='chatgpt.com',r=16);bar=53
 T_(w,'ChatGPT',34,bar+40,sf(26,'Semibold'));line(w,[(142,bar+36),(149,bar+43),(156,bar+36)],GRAY,3)
 rr(w,(40,CH-104,CW-40,CH-34),'white',35,'#D9D9DE',2);T_(w,'Ask anything',76,CH-69,sf(24),'#8E8E93')
 ImageDraw.Draw(w).ellipse((CW-104,CH-93,CW-56,CH-45),fill=INK);rr(w,(CW-89,CH-78,CW-71,CH-60),'white',4)
 return clip(w,16)
def chat(T,S,at):
 im=canvas();a=win(.15,5.85,T,.3)
 if a<=0:return im
 w=chat_static().copy();bar=53
 u=ease((T-.3)/.3)
 if u>0:
  b=blank(700,132);rr(b,(0,0,699,131),'#F1F1F3',32);T_(b,'Is this review positive or negative?',34,44,sf(30));T_(b,'“Arrived late, but works great.”',34,90,sf(30),GRAY)
  place(w,b,CW-40-700,bar+78+14*(1-u),opacity=u)
 v=ease((T-.95)/.25)
 if v>0:
  ic=blank(52,52);ImageDraw.Draw(ic).ellipse((0,0,51,51),fill='white',outline='#D9D9DE',width=2);ic.alpha_composite(icon('openai',30),(11,11));place(w,ic,40,bar+246,opacity=v)
  draw_stream(w,112,bar+284,32,CW-112-60,48,T)
 e=ease((T-.15)/.3);place(im,w,100,102+24*(1-e),scale=.96+.04*e,opacity=a,sh=True)
 return im

# ================= 2. race + latency range (full) =================
LX0,LX1=140,1780
DOTS=[92,138,176,228,262,305,351,418,466]   # illustrative requests inside the published 70-500 ms range (no values shown)
def race(T,S,at):
 im=canvas();a=win(6.2,14.45,T,.3)
 if a<=0:return im
 lay=canvas();jev=A(S,at,'b02','Jev,',1.6)-.13;resp=A(S,at,'b02','responds',3.95)-.13;t70=A(S,at,'b02','70',5.1)-.13;thalf=A(S,at,'b02','half',6.1)-.13;alw=A(S,at,'b02','always,',7.1)-.13;within=A(S,at,'b02','within',4.4)-.13
 OFF=80*(1-smooth((T-(within-.45))/.45))
 # lane A: chat model, still typing
 e=ease((T-6.25)/.3)
 if e>0:
  c=blank(LX1-LX0,270);rr(c,(0,0,c.width-1,269),PALE,32)
  ic=blank(76,76);ImageDraw.Draw(ic).ellipse((0,0,75,75),fill='white');ic.alpha_composite(icon('openai',44),(16,16));c.alpha_composite(ic,(36,38))
  T_(c,'Chat model',132,58,sf(46,'Semibold'));T_(c,'one token at a time',132,108,sf(30),GRAY)
  pos=answer_layout(34,730);cur=pos[min(len(pos)-1,int(nwords(T)))][1];draw_stream(c,600,80,34,730,48,T,first_line=max(0,cur-3),max_lines=4)
  T_(c,f'{T-STREAM0:.1f} s',c.width-48,112,sf(64,'Semibold',mono=True),INK,'rm')
  dots='still typing'+'.'*(1+int(T*3)%3);T_(c,dots,c.width-48,182,sf(30),GRAY,'rm')
  T_(c,'LLMs: 3 to 329 seconds',132,226,sf(28),GRAY)
  place(lay,c,LX0,80+OFF+20*(1-e),opacity=e)
 # lane B: Jev
 e=ease((T-6.5)/.3)
 if e>0:
  c=blank(LX1-LX0,250);done=T>=resp+.3;rr(c,(0,0,c.width-1,249),'#EEF8F0' if done else PALE,32)
  c.alpha_composite(logo_ts(76),(36,38));T_(c,'Jev',132,58,sf(46,'Semibold'));T_(c,'all outputs in a single query',132,108,sf(30),GRAY)
  v=ease((T-resp)/.3);ms=round(114*v)
  T_(c,f'{ms} ms',c.width-48,112,sf(64,'Semibold',mono=True),GREEN if done else INK,'rm')
  if done:
   u=spring((T-resp-.3)/.3);chip=blank(600,96);rr(chip,(0,0,599,95),'white',22,'#CFE8D5',2);T_(chip,'sentiment',30,48,sf(34,mono=True),GRAY);T_(chip,'positive',268,48,sf(36,'Semibold',mono=True),INK);checkmark(chip,548,48,22,GREEN)
   place(c,chip,660,66,scale=.85+.15*u,opacity=min(1,(T-resp-.3)*8));T_(c,'done',c.width-48,182,sf(30,'Semibold'),GREEN,'rm')
  else:T_(c,'waiting',c.width-48,182,sf(30),GRAY,'rm')
  T_(c,'0.114 s in TypeSafe’s demo',132,210,sf(28),GRAY)
  pj_=spring((T-jev)/.3) if T>=jev else 1;place(lay,c,LX0,380+OFF+20*(1-e),scale=.97+.03*pj_ if T>=jev else .97,opacity=e*(1 if T>=jev else .55))
 # range bar 0..500 ms
 e=ease((T-within)/.3)
 if e>0:
  x0,x1,y=220,1340,800;X=lambda ms:x0+(x1-x0)*ms/500
  r=canvas();T_(r,'End-to-end response time',(x0+x1)/2+60,874,sf(36,'Medium'),GRAY,'mm');rr(r,(x0,y-5,x1,y+5),'#E3E3E6',5)
  g=smooth((T-t70-.1)/(max(.3,thalf-t70)))
  if g>0:rr(r,(X(70),y-9,X(70)+max(18,(X(500)-X(70))*g),y+9),GREEN,9)
  for ms,tt,lab,sub in [(70,t70,'70 ms',None),(500,thalf,'500 ms','half a second')]:
   u=spring((T-tt)/.3)
   if T>=tt:
    ImageDraw.Draw(r).ellipse((X(ms)-15,y-15,X(ms)+15,y+15),fill='white',outline=GREEN,width=6)
    lb=blank(320,120);T_(lb,lab,160,40,sf(50,'Bold'),INK,'mm')
    if sub:T_(lb,sub,160,94,sf(30),GRAY,'mm')
    place(r,lb,min(X(ms)-160,1500-320),y+26,scale=.8+.2*u,opacity=min(1,(T-tt)*8))
  for i,ms in enumerate([114]+DOTS):
   tt=(resp+.75) if i==0 else alw+(i-1)*.07
   if T<tt or T<within+.3:continue
   u=ease((T-tt)/.22);yy=y-46-60*(1-u);col=INK if i==0 else '#0F6B2B'
   ImageDraw.Draw(r).ellipse((X(ms)-9,yy-9,X(ms)+9,yy+9),fill=col)
   if i==0:line(r,[(X(ms),yy+9),(X(ms),y-10)],INK,3);T_(r,'114 ms',X(ms),yy-38,sf(34,'Semibold'),INK,'mm')
  place(lay,r,0,16*(1-e),opacity=e)
 place(im,lay,0,0,opacity=a);return im

# ================= 3. typesafe.ai launch post, push-in on the Cost row (full) =================
K=3;PW,PH=1600,1260;TX=(200,420,910,1400);FS=17
ROWS=[('Sampling',[[('b','Sequential.'),('r',' Generates one token at a time, each')],[('r','conditioned on the last.')]],[[('b','Parallel.'),('r',' Generates all outputs in a single query.')],[('r','Incredibly efficient and hardware-aware.')]]),
 ('Cost',[[('r','Input tokens: from $0.20 to $10 / MTok.')],[('r','Output tokens: ~5x more expensive than input tokens.')]],'JEVCOST'),
 ('Speed',[[('b','End-to-end response time is 3 to 329 seconds')],[('r','for frontier models. Fast enough for interfacing with')],[('r','humans, but a big bottleneck when integrated in code.')]],[[('b','End-to-end response time is 70ms-500ms'),('r',' for')],[('r','TypeSafe. This can range from 40x-200x faster for the')],[('r','same levels of frontier intelligence for System One')],[('r','shaped queries.')]]),
 ('Confidence',[[('r','Even if prompted for a confidence estimate, models')],[('r','tend to be overconfident and inconsistent.')]],[[('r','Always communicates confidence and uncertainty')],[('r','with every output. Calibrated: higher confidence')],[('r','means higher accuracy.')]])]
SPOT={}
@lru_cache(None)
def blog_page():
 k=K;p=Image.new('RGBA',(PW*k,PH*k),'#FEFEFE');d=ImageDraw.Draw(p)
 def t(s,x,y,n,wt='Regular',fill='#1E1E1E',anchor='ls'):d.text((round(x*k),round(y*k)),s,font=inter(n*k,wt),fill=fill,anchor=anchor);return inter(n*k,wt).getlength(s)/k
 for s,x,anc in [('TypeSafe AI',0,'l'),('Manifesto',742,'l'),('Our Team',842,'l'),('Join Waitlist',PW,'r')]:
  wl=inter(16*k,'Medium').getlength(s)/k+16;xa=x if anc=='l' else x-wl;d.rectangle((xa*k,0,(xa+wl)*k,30*k),fill='#E4E4E4');t(s,xa+8,21,16,'Medium')
 t('∵ Back',200,92,16,'Medium');t('Company News',200,150,15,'Medium','#6B6B6B');t('Sep 15, 2026',330,150,15,'Regular','#6B6B6B')
 t('Introducing System One Models & Jev',198,222,56,'Medium','#111111');d.text((200*k,262*k),'Diogo Almeida, founder, TypeSafe',font=ny(19*k,'Regular',italic=True),fill='#1E1E1E',anchor='ls')
 t('Frontiers, Old and New',200,352,34,'Medium','#111111')
 y=392;d.line([(TX[0]*k,y*k),(TX[3]*k,y*k)],fill='#1E1E1E',width=k);t('Existing LLMs',TX[1]+16,y+32,FS,'Bold');t('System One + Jev',TX[2]+16,y+32,FS,'Bold');y+=52
 for name,left,right in ROWS:
  d.line([(TX[0]*k,y*k),(TX[3]*k,y*k)],fill='#D8D8D8',width=k);t(name,TX[0],y+34,FS,'Regular','#1E1E1E')
  n=max(len(left),3 if right=='JEVCOST' else len(right))
  for col,cell in ((1,left),(2,right)):
   if cell=='JEVCOST':
    SPOT['y']=y;SPOT['x']=TX[2]+16;SPOT['pre']=t('Input tokens: ',TX[2]+16,y+34,FS);t('($42 per billion tokens).',TX[2]+16,y+60,FS);t('Output tokens: FREE (too cheap to meter).',TX[2]+16,y+86,FS);continue
   for li,runs in enumerate(cell):
    x=TX[col]+16
    for kind,s in runs:x+=t(s,x,y+34+li*26,FS,'Bold' if kind=='b' else 'Regular')
  y+=34+n*26+6
 d.line([(TX[0]*k,y*k),(TX[3]*k,y*k)],fill='#D8D8D8',width=k)
 return p
VW,VH=1420,700
def pricepage(T,S,at):
 im=canvas();a=win(14.8,18.62,T,.28)
 if a<=0:return im
 page=blog_page();inp=A(S,at,'b04','input',.29);four=A(S,at,'b04','four',.91)-.13;mil=A(S,at,'b04','million',1.77)-.13
 sy=SPOT['y'];full=(110,300,1490,300+1380*VH/VW);cw=540;tgt=(TX[2]-6,sy-52,TX[2]-18+cw,sy-52+cw*VH/VW)
 z=smooth((T-(inp-.12))/.6);drift=(T-14.8)*5*(1-z);box=[lerp(full[i]+(drift if i in(1,3) else 0),tgt[i],z) for i in range(4)]
 crop=page.crop(tuple(round(v*K) for v in box)).resize((VW,VH),Image.Resampling.LANCZOS);sc=VW/(box[2]-box[0])
 X=lambda x:(x-box[0])*sc
 Y=lambda y:(y-box[1])*sc
 # rows arrive top to bottom in the wide shot (white covers fading off)
 # live number: counts up and lands on "four"
 v=ease((T-(four-.34))/.34);val=.042 if T<inp-.12 else .042*v;f=inter(FS*sc,'Bold' if v>=1 else 'Regular');s=f'${val:.3f}';nx=X(SPOT['x']+SPOT['pre']);by=Y(sy+34)
 T_(crop,s,nx,by,f,'#1E1E1E','ls');wn=f.getlength(s);fr=inter(FS*sc);T_(crop,' / MTok',nx+wn,by,fr,'#1E1E1E','ls');wm=fr.getlength(' / MTok')
 cut=lerp(444,1120,ease((T-15.05)/.75))
 if cut<1120 and Y(cut)<VH:ImageDraw.Draw(crop).rectangle((0,max(0,Y(cut)),VW,VH),fill='#FEFEFE')
 if T>=four-.02:
  u=ease((T-four+.02)/.25);lay=blank(VW,VH);ImageDraw.Draw(lay).rounded_rectangle((nx-3*sc,by-21*sc,nx+wn+wm+8*sc,by+9*sc),6*sc,outline=(255,59,48,int(235*u)),width=max(2,round(1.2*sc)));crop.alpha_composite(lay)
 if T>=mil:
  u=ease((T-mil)/.3);x_a=X(SPOT['x'])-5*sc;x_b=nx+wn+wm+5*sc
  rr(crop,(x_a,by-18*sc,x_a+(x_b-x_a)*u,by+6*sc),HILITE,4*sc)
 motion(crop,T,points=[(inp+.1,1180,560),(four+.1,nx+wn+wm+70,by+46),(mil-.25,nx+wn+wm+70,by+46),(mil+.35,nx+wn+wm+40,by+30)],end=18.7)
 w=window(VW,VH+52,url='typesafe.ai/blog/introducing-system-one-models-and-jev',r=16);w.alpha_composite(crop,(0,53));w=clip(w,16)
 e=ease((T-14.8)/.3);place(im,w,90,72+24*(1-e),scale=.96+.04*e,opacity=a,sh=True)
 return im

# ================= 4. price table (split): input + multiples, then output, FREE, dead counter =================
MODELS=[('Jev','TypeSafe AI',.042,None),('Gemini 2.5 Flash-Lite','Google',.10,.40),('GPT-5.6 Luna','OpenAI',.20,1.20),('GPT-5.6 Terra','OpenAI',2.00,12.00),('Claude Fable 5.1','Anthropic',10.00,50.00)]
TXP,TYP,TWP,THP=90,96,1070,700
def money(v):return f'${v:.3f}' if v<.1 else f'${v:.2f}'
def table(T,S,at):
 im=canvas();a=win(18.95,28.62,T,.3)
 if a<=0:return im
 put=A(S,at,'b04','put',2.67)-.13;big=A(S,at,'b04','big',4.93)-.13;dif=A(S,at,'b04','difference',5.39)-.13
 outp=A(S,at,'b05','output',.53)-.13;free=A(S,at,'b05','free',1.47)-.13;doesnt=A(S,at,'b05',"doesn't",2.91)-.13;count=A(S,at,'b05','count',4.21)-.13
 p=blank(TWP,THP);rr(p,(0,0,TWP-1,THP-1),'white',30,'#E3E3E6',2)
 T_(p,'API price per 1M tokens',40,52,sf(34,'Semibold'));T_(p,'official pricing pages · 18 Sep 2026',TWP-40,54,sf(24),GRAY,'rm')
 ph=smooth((T-(outp-.35))/.3)      # 0 = input/multiples view, 1 = output view
 T_(p,'Model',40,118,sf(26,'Medium'),GRAY);T_(p,'Input',560,118,sf(26,'Medium'),GRAY,'rm')
 if ph<1:T_(p,'vs Jev',600,118,sf(26,'Medium'),tuple([110,110,115,int(255*(1-ph))]))
 if ph>0:T_(p,'Output',TWP-60,118,sf(26,'Medium'),(110,110,115,int(255*ph)),'rm')
 mx=math.log10(10/.042)
 for i,(nm,prov,pin,pout) in enumerate(MODELS):
  y=146+i*108;e=ease((T-put-i*.11)/.3)
  if e<=0:continue
  r=blank(TWP-40,98);rr(r,(0,0,r.width-1,97),'#EEF8F0' if i==0 else PALE,22)
  x=28
  if i==0:r.alpha_composite(logo_ts(54),(24,22));x=96
  T_(r,nm,x,34,sf(31,'Semibold'));T_(r,prov,x,72,sf(24),GRAY)
  T_(r,money(pin),540,49,sf(36,'Semibold'),GREEN if i==0 else INK,'rm')
  if i and ph<1:
   g=ease((T-big-(i-1)*.09)/.4);ratio=pin/.042
   if g>0:
    bw=max(8,430*pin/10*g) ;rr(r,(580,37,580+bw,61),(255,59,48,int(255*(1-ph))),12)
    m=ease((T-dif-(i-1)*.09)/.25)
    if m>0:
     s=f'{ratio:.1f}×' if ratio<10 else f'{ratio:.0f}×';xx=580+bw+16
     if xx+tw(s,32,'Bold')>r.width-20:xx=580+bw-16-tw(s,32,'Bold');col=(255,255,255,int(255*m*(1-ph)))
     else:col=(255,59,48,int(255*m*(1-ph)))
     T_(r,s,xx,49,sf(32 if ratio<100 else 24,'Bold'),col)
  if ph>0:
   if i:
    o=ease((T-outp-(i-1)*.1)/.28)
    if o>0:T_(r,money(pout),r.width-40,49+8*(1-o),sf(36,'Semibold'),(29,29,31,int(255*o)),'rm')
   else:
    fl=ease((T-free)/.26)
    if fl<.5:
     pass
    else:
     s2=(fl-.5)*2;pl=blank(190,64);rr(pl,(0,0,189,63),GREEN,32);T_(pl,'FREE',95,32,sf(32,'Bold'),'white','mm');place(r,pl.resize((190,max(1,round(64*s2)))),r.width-36-190,49-32*s2)
     tc=ease((T-free-.45)/.3)
     if tc>0:T_(r,'too cheap to meter',r.width-244,49,sf(24),(110,110,115,int(255*tc)),'rm')
  place(p,r,20,y+16*(1-e),opacity=e)
 place(im,p,TXP,TYP,opacity=a,sh=True)
 # output-token counter under the table: ticks, then greys out and is struck through on "count"
 c0=free+.55;e=ease((T-c0)/.3)
 if e>0:
  dead=smooth((T-doesnt)/(max(.4,count-doesnt)));tick=min(T,doesnt+(count-doesnt)*.6);n=int(1204+(tick-c0)**1.15*3870*(1-.35*dead))
  c=blank(760,96);rr(c,(0,0,759,95),PALE,26);col=tuple(int(lerp(v,w_,dead)) for v,w_ in zip((29,29,31),(174,174,178)))
  T_(c,'Output tokens',32,48,sf(32,'Medium'),col);T_(c,f'{n:,}',728,48,sf(40,'Semibold',mono=True),col,'rm')
  s=ease((T-count)/.3)
  if s>0:line(c,[(24,50),(24+712*s,50)],RED,5)
  place(im,c,TXP+(TWP-760)/2,830+14*(1-e),opacity=e*a)
 st=im.crop((40,50,1210,1000));st=st.resize((round(st.width*1.06),round(st.height*1.06)),Image.Resampling.LANCZOS);out=canvas();out.alpha_composite(st,(285,8));return out

# ================= 5. 50,000,000 reviews -> receipts (full) =================
REVIEWS=[(5,'Works great, arrived late.'),(4,'Good value for the price.'),(1,'Broke after two days.'),(5,'Exactly as described!'),(3,'Okay, but the box was dented.'),(5,'Best purchase this year.'),(2,'Too small, sent it back.'),(4,'Fast shipping, solid build.'),(5,'My kids love it.'),(1,'Never arrived. Refund please.'),(4,'Does what it says.'),(3,'Average. Nothing special.'),(5,'Would buy again.'),(2,'Stopped charging in a week.'),(4,'Nice, a bit loud though.'),(5,'Five stars, no notes.')]
def star(d,cx,cy,r,fill):
 pts=[]
 for i in range(10):
  a=-math.pi/2+i*math.pi/5;rad=r if i%2==0 else r*.45;pts.append((cx+rad*math.cos(a),cy+rad*math.sin(a)))
 d.polygon(pts,fill=fill)
@lru_cache(None)
def review_card(i):
 n,s=REVIEWS[i%len(REVIEWS)];q=2;c=blank(520*q,180*q);rr(c,(0,0,520*q-1,180*q-1),'white',30*q,'#E3E3E6',2*q);d=ImageDraw.Draw(c)
 for k in range(5):star(d,(52+k*46)*q,48*q,20*q,GOLD if k<n else '#E3E3E6')
 T_(c,s,32*q,108*q,sf(32*q),INK);T_(c,'verified buyer · site.com',32*q,148*q,sf(22*q),GRAY)
 return c.resize((520,180),Image.Resampling.LANCZOS)
SLOTS=[(150+c*550,335+r*195) for r in range(3) for c in range(3) if not (r==2 and c==2)]
ORDER=list(range(len(SLOTS)));random.Random(7).shuffle(ORDER)
def paper_jev(T,tot_t):
 pw,ph=440,460;p=blank(pw,ph);ImageDraw.Draw(p).rectangle((0,0,pw,ph),fill='white');yy=ph-66
 p.alpha_composite(logo_ts(40),(30,yy-20));T_(p,'Jev',82,yy,sf(30,'Bold'));T_(p,'receipt',pw-30,yy,sf(26),GRAY,'rm');yy-=46
 def dash(y):
  for k in range(0,pw-60,18):ImageDraw.Draw(p).line([(30+k,y),(30+k+9,y)],fill='#C7C7CC',width=2)
 dash(yy);yy-=50
 for l_,r_,col in [('Reviews','50,000,000',INK),('Input','$0.042 / MTok',INK),('Output','FREE',GREEN)]:
  T_(p,l_,30,yy,sf(27,'Medium'),INK);T_(p,r_,pw-30,yy,sf(26,'Semibold',mono=True),col,'rm');yy-=58
 yy+=14;dash(yy);yy-=62;T_(p,'Total',30,yy,sf(36,'Bold'))
 if T>=tot_t:
  v=spring((T-tot_t)/.28);t_=blank(260,90);T_(t_,'≈ $20',252,45,sf(58,'Bold'),GREEN,'rm');place(p,t_,pw-30-260,yy-45,scale=max(.05,v),opacity=min(1,(T-tot_t)*9))
 d=ImageDraw.Draw(p)
 for k in range(0,pw,26):d.polygon([(k,ph),(k+13,ph-14),(k+26,ph)],fill=(0,0,0,0))
 return p
def paper_llm(T,tot_t):
 pw,ph=440,1100;p=blank(pw,ph);ImageDraw.Draw(p).rectangle((0,0,pw,ph),fill='white');yy=ph-66
 T_(p,'Normal model',30,yy,sf(30,'Bold'));T_(p,'receipt',pw-30,yy,sf(26),GRAY,'rm');yy-=46
 def dash(y):
  for k in range(0,pw-60,18):ImageDraw.Draw(p).line([(30+k,y),(30+k+9,y)],fill='#C7C7CC',width=2)
 dash(yy);yy-=50
 for l_,r_ in [('Reviews','50,000,000'),('Input','$0.20–$10 / MTok'),('Output','~5× input price')]:
  T_(p,l_,30,yy,sf(27,'Medium'),INK);T_(p,r_,pw-30,yy,sf(26,'Semibold',mono=True),INK,'rm');yy-=58
 yy+=14;dash(yy);yy-=70;T_(p,'Total',30,yy,sf(36,'Bold'))
 if T>=tot_t:
  v=spring((T-tot_t)/.28);t_=blank(300,90);T_(t_,'$ thousands',292,45,sf(46,'Bold'),RED,'rm');place(p,t_,pw-30-300,yy-45,scale=max(.05,v),opacity=min(1,(T-tot_t)*9))
 yy-=70
 while yy>30:dash(yy);yy-=44
 d=ImageDraw.Draw(p)
 for k in range(0,pw,26):d.polygon([(k,ph),(k+13,ph-14),(k+26,ph)],fill=(0,0,0,0))
 return p,ph-(yy if False else 0)
PS=1.3
def printer(dst,X0,label,T,strip,logo=False,busy=True):
 w=520;x=60;cx=x+w/2;lay=blank(w+120,1000)
 if logo:lay.alpha_composite(logo_ts(48),(round(cx-62),10));T_(lay,label,cx-2,34,sf(34,'Semibold'))
 else:T_(lay,label,cx,34,sf(34,'Semibold'),INK,'mm')
 rr(lay,(x,74,x+w,128),'#1D1D1F',20);rr(lay,(x+30,104,x+w-30,118),'#000000',7)
 if strip is not None:place(lay,strip,cx-strip.width/2+(math.sin(T*38)*1.4 if busy else 0),114,sh=True)
 rr(lay,(x,74,x+w,114),'#1D1D1F',20);ImageDraw.Draw(lay).rectangle((x,94,x+w,114),fill='#1D1D1F')
 ImageDraw.Draw(lay).ellipse((x+w-60,86,x+w-44,102),fill=GREEN if (int(T*6)%2 or not busy) else '#2C2C2E')
 lay=lay.resize((round(lay.width*PS),round(lay.height*PS)),Image.Resampling.LANCZOS);dst.alpha_composite(lay,(round(X0-60*PS),150))
def reviews(T,S,at):
 im=canvas();a=win(28.9,39.86,T,.3)
 if a<=0:return im
 lay=canvas();fifty=A(S,at,'b06','50',2.43)-.13;say=A(S,at,'b06',"let's",1.39);b7=S['b07']['start'];scoring=A(S,at,'b07','scoring',1.02)-.13;twenty=A(S,at,'b07','20',2.72)-.13
 normal=A(S,at,'b08','normal',.35)-.13;thou=A(S,at,'b08','thousands',1.91)-.13
 sh=smooth((T-(b7-.05))/.45)      # header shrinks, cards leave
 v=ease((T-say)/(fifty-say));val=int(round(50_000_000*v/10)*10) if v<1 else 50_000_000
 hd=ease((T-say+.15)/.3)
 if hd>0:
  big=lerp(150,60,sh);yy=lerp(170,96,sh);h=blank(1500,300)
  if sh<.5:
   T_(h,f'{val:,}',750,120,sf(big,'Bold'),GREEN if v>=1 and sh==0 else INK,'mm');pr=ease((T-A(S,at,'b06','product',3.31)+.13)/.25)
   if pr>0:T_(h,'product reviews',750,120+big*.72,sf(lerp(44,30,sh),'Medium'),(110,110,115,int(255*pr*(1-sh*2))),'mm')
  else:T_(h,'50,000,000 product reviews',750,120,sf(big,'Bold'),INK,'mm')
  place(lay,h,lerp(210,63,sh),yy-120,opacity=hd)
 if sh<1:
  for k,si in enumerate(ORDER):
   t0=28.98+k*.1;e=spring((T-t0)/.3)
   if T<t0:continue
   x,y=SLOTS[si];swap=0;c=review_card(si*2);ph_=1
   o=(1-smooth((T-(b7-.05)-k*.02)/.3));sc_=(.6+.4*e)*(1 if ph_>=1 or swap==0 else .94+.06*ph_)
   place(lay,c,x,y+30*(1-o),scale=sc_,opacity=min(1,(T-t0)*8)*o,sh=True)
 if sh>0:
  pe=ease((T-b7-.2)/.3)
  if pe>0:
   l2=canvas();out=ease((T-scoring)/1.25);pj=paper_jev(T,twenty);vis=round(40+(pj.height-50)*out)
   printer(l2,100,'Jev',T,pj.crop((0,pj.height-vis,pj.width,pj.height)) if T>=scoring else None,True,busy=out<1)
   place(lay,l2,0,18*(1-pe),opacity=pe)
  pe=ease((T-b7-.35)/.3)
  if pe>0:
   l2=canvas();pl,_=paper_llm(T,thou);o1=ease((T-normal)/1.3);o2=max(0,T-thou-.3)*130;vis=round(40+480*o1+o2)
   vis=min(vis,pl.height);printer(l2,850,'Normal model',T,pl.crop((0,pl.height-vis,pl.width,pl.height)) if T>=normal else None,False,busy=T>=normal)
   place(lay,l2,0,18*(1-pe),opacity=pe*(.45+.55*ease((T-normal+.2)/.25)))
 place(im,lay,0,0,opacity=a);return im

# ================= 6. recap rows + "can't hallucinate" (split) =================
RECAP=[('⚡','70–500 ms','every response'),('💰','$0.042','per 1M input tokens'),('✅','FREE','output tokens')]
def finale(T,S,at):
 im=canvas();hope=A(S,at,'b09','hope',.06);pw_=A(S,at,'b09','powerful.',2.89)-.13;b10=S['b10']['start']
 o=1-smooth((T-(b10-.12))/.3)
 if o>0:
  for i,(em,big,sub) in enumerate(RECAP):
   t0=hope+.1+i*.42;e=spring((T-t0)/.32)
   if T<t0:continue
   r=blank(900,136);hot=smooth((T-pw_-i*.08)/.2)*(1-smooth((T-pw_-.5-i*.08)/.3));rr(r,(0,0,899,135),tuple(int(lerp(v,w_,hot)) for v,w_ in zip((245,245,247),(226,243,230))),30)
   emoji.place_emoji(r,em,36,68,64,anchor='lm');T_(r,big,128,68,sf(48,'Bold'),GREEN if i==2 else INK);T_(r,sub,868,68,sf(30),GRAY,'rm')
   place(im,r,175,190+i*166+20*(1-min(1,e)),scale=.9+.1*e,opacity=min(1,(T-t0)*7)*o)
  captions.key_phrase(im,'Kind of powerful 💪',T,start=pw_-.45,end=b10-.1,y=800,size=84,emph={'powerful':'italic green'},word_times=[A(S,at,'b09','kind',2.45)-.13,A(S,at,'b09','of',2.71)-.13,pw_,pw_+.2])
 if T>=b10:
  nea=A(S,at,'b10','not',.52)-.13;one=A(S,at,'b10','one',1.52)-.13;cant=A(S,at,'b10',"can't",3.02)-.13;hal=A(S,at,'b10','hallucinate,',3.46)-.13;bigd=A(S,at,'b10','big',5.14)-.13;end=49.5
  captions.key_phrase(im,'Not even all 👀',T,start=nea,end=one-.05,y=520,size=84,word_times=[nea,A(S,at,'b10','even',.64)-.13,A(S,at,'b10','all,',.84)-.13,nea+.5])
  captions.key_phrase(im,'One of the first models',T,start=one,end=end,y=450,size=70,color=GRAY,word_times=[one,A(S,at,'b10','of',1.62)-.13,A(S,at,'b10','the',1.68)-.13,A(S,at,'b10','first',1.84)-.13,A(S,at,'b10','models',2.12)-.13])
  u=ease((T-bigd)/.35)
  if u>0 and T<end:
   fo=smooth((end-T)/.15);wd=captions._measure(["can't",'hallucinate'],84,{'hallucinate':'italic red'})[1];x0=625-wd/2-14;rr(im,(x0,598,x0+(wd+28)*u,642),(255,214,10,int(95*fo)),10)
  captions.key_phrase(im,"can't hallucinate",T,start=cant,end=end,y=590,size=84,emph={'hallucinate':'italic red'},word_times=[cant,hal])
 return im

def graphics(b,t,S,at):
 T=b['start']+t
 if T<14.8 or T>=40.2:return None          # cam: Albert full screen
 if T<18.9:return pricepage(T,S,at)
 if T<28.95:return table(T,S,at)
 return reviews(T,S,at)

# ---------- cam captions (copied from 00-intro: white SF Pro Semibold 80, soft shadow, bottom scrim) ----------
CAM_CAPS=[
 dict(beat='b01',text='One by one',times=[2.80,3.00,3.28],end=4.7),
 dict(beat='b02',text='70 ms to half a second',times=[11.22,11.40,12.02,12.22,12.54,12.68],end=14.15),
 dict(beat='b09',text='Kind of powerful',times=[42.68,42.94,43.12],end=43.95),
 dict(beat='b10',text="Can't hallucinate",times=[46.96,47.40],end=48.6),
]   # times = Scribe onsets from transcript.json (section seconds); led by 0.13 s below
for c_ in CAM_CAPS:c_['times']=[x-.13 for x in c_['times']];c_['start']=min(c_['times'])
@lru_cache(maxsize=512)
def _cam_word(word,size):
 f=sf(size,'Semibold');b=f.getbbox(word,anchor='ls');pad=40;w,h=b[2]-b[0]+2*pad,b[3]-b[1]+2*pad
 shd=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]+4),word,font=f,anchor='ls',fill=(0,0,0,210));shd=shd.filter(ImageFilter.GaussianBlur(9))
 t2=Image.new('RGBA',(w,h),(0,0,0,0));ImageDraw.Draw(t2).text((pad-b[0],pad-b[1]+2),word,font=f,anchor='ls',fill=(0,0,0,120));shd.alpha_composite(t2.filter(ImageFilter.GaussianBlur(2)))
 ImageDraw.Draw(shd).text((pad-b[0],pad-b[1]),word,font=f,anchor='ls',fill='white');return shd,f.getlength(word),(b[0]-pad,b[1]-pad)
@lru_cache(None)
def _scrim():
 g=np.zeros((1080,1920,4),np.uint8);y=np.arange(1080);a=np.clip((y-640)/440,0,1)**1.6*120;g[...,3]=a[:,None].astype(np.uint8);return Image.fromarray(g,'RGBA')
def overlay(b,t,S,at,st):
 T=b['start']+t;k=smooth((st.w-1500)/400)*st.opacity
 if k<=0:return None
 live=[c for c in CAM_CAPS if c['start']<=T<c['end']]
 if not live:return None
 c=live[0];size=80;words=c['text'].split();gap=sf(size,'Semibold').getlength(' ');tiles=[_cam_word(w,size) for w in words]
 width=sum(a for _,a,_ in tiles)+gap*(len(words)-1);x=960-width/2;base=905;im=canvas()
 fo=smooth((c['end']-T)/.18)*k;im.alpha_composite(fade(_scrim(),min(1,ease((T-c['start'])/.3))*fo))
 for (tile,adv,off),tw0 in zip(tiles,c['times']):
  e=ease((T-tw0)/.18)
  if e>0:im.alpha_composite(fade(tile,e*fo),(round(x+off[0]),round(base+off[1]+8*(1-e))))
  x+=adv+gap
 return im
