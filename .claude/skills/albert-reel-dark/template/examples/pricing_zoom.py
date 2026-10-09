"""ACCEPTED EXAMPLE (Freebuff reel, Sept 2026) — Albert: "that entire page was really sick".
Recreated web page + camera push-in + count-up + highlighter. Copy into a project next to draw.py and adapt.

The recipe (keep all five parts, they are what made it land):
 1. Build the WHOLE real page once, at 2x, from the live site's copy (scrape it first: plan names, prices, button labels,
    every feature line). `pricing_page()` is lru_cached, so per frame you only crop + resize. Never draw per-glyph tracking.
 2. Put it in a Safari `window()` with the real URL. The page is wider than the viewport, so the establishing shot already
    crops to the four cards (`full`), not the whole 2000 px page (that was unreadable).
 3. Cards arrive left to right in the wide shot (white covers fading off), so something moves before the zoom.
 4. CAMERA: `smooth()` push-in from `full` to the target card (`pro`) starting ~0.1 s before the verb ("paying"), 0.6 s long.
    The number is left OUT of the cached page and drawn live so it can count up and LAND on the spoken price, with a red
    rounded frame snapping round it. "/ month" darkens on its word. Scale every overlay by `sc` = viewport / crop width.
 5. Second move: tilt down (`pro2`) ~0.55 s before the second keyword and sweep a yellow highlighter (fill 255,214,10,95)
    left-to-right across the exact feature row (`CODEX_ROW['box']` is recorded while drawing the page). The cursor travels
    to the button, then to the highlighted row. One pop on the price landing, one on the highlight, whoosh on the push-in.
In render.py: beat in FULL, caption y ~1080 (the window ends at y=902).
"""
from draw import *
import sys,numpy as np
sys.path.insert(0,str(P/'helpers'))
from pointer_motion import motion
def clip(p,r=16):
 m=Image.new('L',p.size);ImageDraw.Draw(m).rounded_rectangle((0,0,p.width-1,p.height-1),r,fill=255)
 p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel('A')),np.array(m))));return p
def diamond(im,x,y,r,col):ImageDraw.Draw(im).polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=col)
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


if __name__=='__main__':
 # quick look: python3 examples/pricing_zoom.py  -> examples/pricing_zoom_strip.jpg
 at=lambda beat,word,default=0,nth=0:default
 ts=[.4,.9,1.4,2.0,2.7,3.2];sheet=Image.new('RGB',(len(ts)*270,480),'#DDD')
 for i,t in enumerate(ts):sheet.paste(price(t,{},at).convert('RGB').resize((270,480)),(i*270,0))
 sheet.save(Path(__file__).with_name('pricing_zoom_strip.jpg'));print('ok')
