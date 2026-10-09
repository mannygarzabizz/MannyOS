"""ACCEPTED full scenes.py of the "AI killed software" reel (22 Sep 2026, v8 after eight revision rounds). Reference + importable.
In a project the parts live in parts/ (hook.py, shootout.py, fcpage.py, macbook.py); here they are the sibling examples
mg_hook.py, shootout.py, article_zoom.py, macbook.py.

Scenes for the "AI killed software" reel (22 Sep 2026).

Every surface is recreated with Pillow - no screenshots. Product-true material:
  * Salesforce tile = the official Salesforce iOS app icon (App Store artwork)
  * $4.6 trillion   = Foundation Capital, "AI leads a service as software paradigm shift" (Chen & Gupta, 19 Apr 2024):
                      "The push towards services represents a $4.6 trillion opportunity." - recreated in parts/fcpage.py
  * $750 billion    = spoken (no single public source found; nearest: Gartner worldwide software $1.23T for 2025)
  * every other number on screen is spoken ($1B "billion-dollar", 6x) - no invented amounts anywhere (the accounting
    table uses skeleton bars where amounts would be)

Scene coordinates are the pre-TOP_SHIFT canvas: split graphics live in y 100..700 (panel 940x560 at (70,104)),
full-screen UI in y 120..930 with the cinematic words underneath.
"""
from draw import *
import sys,math,random
import numpy as np
sys.path.insert(0,str(P/'helpers'));sys.path.insert(0,str(P/'parts'))
import instagram_comment,pointer_motion
try:import hook as _hook_part
except ImportError:import mg_hook as _hook_part
import shootout as _shootout_part
try:import fcpage as _fc_part
except ImportError:import article_zoom as _fc_part
from brand import *
from brand import _ring,_mask
from macbook import macbook,desktop,wifi

LEAD=.13
MONO='/System/Library/Fonts/SFNSMono.ttf'
GREEN_D='#1E8E3E';SOFT_GREY='#8E8E93'

def enter0(im,obj,x,y,t,sh=True):
    """Entrance already part-way in at t=0, so a cut into a beat is never blank."""
    e=ease((t+.09)/.32);place(im,obj,x,y+22*(1-e),.96+.04*e,e,sh)

def pop(v):return spring(max(0,min(1,v)))
def card(w=940,h=560,fill='white',r=30):return panel(w,h,fill,r)
def clamp(v):return max(0,min(1,v))

# ---------------------------------------------------------------- 1. hook (full) ---------------
def hook(t,at):return _hook_part.render(t,at)

# ---------------------------------------------------------------- 2 + 3. the shell game: Claude, top hat on, shuffles the cups
@lru_cache(None)
def _cup(w=160,h=150):
    """A shaded cup: vertical gradient body, lighter rim band, soft specular, darker foot."""
    q=3;im=blank(w*q,h*q);body=blank(w*q,h*q);d=ImageDraw.Draw(body)
    for yy in range(h*q):                                            # gradient ink, darker at the foot
        u=yy/(h*q);g=round(lerp(58,20,u**.9));d.line([(0,yy),(w*q,yy)],fill=(g,g,g+3,255))
    m=Image.new('L',(w*q,h*q));dm=ImageDraw.Draw(m)
    dm.polygon([(w*.25*q,h*.12*q),(w*.75*q,h*.12*q),(w*.94*q,h*.92*q),(w*.06*q,h*.92*q)],fill=255)
    dm.rounded_rectangle((w*.21*q,0,w*.79*q,h*.22*q),radius=h*.11*q,fill=255);dm.rounded_rectangle((0,h*.82*q,w*q-1,h*q-1),radius=h*.09*q,fill=255)
    body.putalpha(m);im.alpha_composite(body)
    d=ImageDraw.Draw(im);d.rounded_rectangle((w*.21*q,0,w*.79*q,h*.20*q),radius=h*.10*q,fill=(70,70,76,255))     # rim band
    d.rounded_rectangle((w*.24*q,h*.05*q,w*.76*q,h*.11*q),radius=h*.03*q,fill=(92,92,98,255))
    hl=blank(w*q,h*q);ImageDraw.Draw(hl).line([(w*.30*q,h*.26*q),(w*.13*q,h*.84*q)],fill=(255,255,255,46),width=8*q);hl=hl.filter(ImageFilter.GaussianBlur(4*q));im.alpha_composite(hl)
    d.rounded_rectangle((0,h*.86*q,w*q-1,h*q-1),radius=h*.08*q,fill=(16,16,18,255))                                # foot
    return im.resize((w,h),Image.Resampling.LANCZOS)

CX=[230,470,710];TY=480;CW,CH=160,150;QS_=150;QY_=160          # cup centres, table line, cup size, Claude tile size / top
ARM='#D97757';HAND='#C4653F'
def _bez(p0,p1,p2,u):return ((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1])

def _track(t,phases):
    """Continuous position from a list of (t0,t1,fn) phases: inside a phase fn(t); between phases a smooth blend from
    the previous phase's end to the next phase's start; before the first / after the last: held."""
    for i,(t0,t1,fn) in enumerate(phases):
        if t0<=t<=t1:return fn(t)
        if t<t0:
            if i==0:return fn(t0)
            p0,p1,f0=phases[i-1];a=f0(p1);b=fn(t0);u=smooth((t-p1)/max(1e-3,t0-p1));return (lerp(a[0],b[0],u),lerp(a[1],b[1],u))
    t0,t1,fn=phases[-1];return fn(t1)

def cupsgame(T,at,Wd):
    """One choreography for both beats, in combined time T (worry starts at 0, hidden at Wd). Returns the state dict.
    Shuffles: both hands, one cup each (they cross). "never": right hand lifts the Salesforce cup - empty. "in": throws
    it right. "begin": left hand throws the middle cup left. "actually": left hand throws the last cup. Right hand rests
    on the hat (wiggle), takes it off right after "else"; the money is on his head; left hand: ta-da."""
    L=.13
    w_never=at('worry','never',1.67)-L;w_in=at('worry','in',1.95)-L;w_begin=at('worry','begin',2.71)-L;w_soft=at('worry','software',2.11)-L
    h_act=Wd+at('hidden','actually',.25)-L;h_else=Wd+at('hidden','else',1.11)-L;h_sight=Wd+at('hidden','sight.',1.81)-L
    S1=(.42,.82);S2=(.94,1.34);top=lambda x,y:(x,y+8)
    def arc(t,t0,t1,a,b,up):
        u=smooth((t-t0)/(t1-t0));return lerp(CX[a],CX[b],u),TY-CH-(34*math.sin(u*math.pi) if up else 0)
    # ---- cups: each a position track + lift/throw ------------------------------------------------
    def rest(slot):return lambda t:(CX[slot],TY-CH)
    cupsP={'A':[(0,S1[0],rest(1)),(S1[0],S1[1],lambda t:arc(t,*S1,1,0,True)),(S1[1],S2[0],rest(0)),(S2[0],S2[1],lambda t:arc(t,*S2,0,2,True)),(S2[1],99,rest(2))],
           'B':[(0,S1[0],rest(0)),(S1[0],S1[1],lambda t:arc(t,*S1,0,1,False)),(S1[1],99,rest(1))],
           'C':[(0,S2[0],rest(2)),(S2[0],S2[1],lambda t:arc(t,*S2,2,0,False)),(S2[1],99,rest(0))]}
    throws={'A':(w_in,1,120),'B':(w_begin,-1,0),'C':(h_act,-1,0)}                # (time, side, pre-lift)
    cups={}
    for k in 'ABC':
        x,y=_track(T,cupsP[k]);lift=0;rot=0;op=1;flying=False
        if k=='A' and T>w_never:lift=ease((T-w_never)/.28)*120+6*math.sin(T*5.5)*min(1,(T-w_never)/.3)
        t0,side,pre=throws[k]
        if T>=t0:
            u=T-t0;grab=.10
            if u<grab:lift=lift+ease(u/grab)*26
            else:
                v=u-grab;flying=True;x=x+side*1500*v;y=y-lift-26-900*v+1900*v*v;rot=side*-420*v;op=max(0,1-v/.45);lift=0
        if op<=0:continue
        cups[k]=(x,y-lift,rot,op,flying,lift)
    def cuptop(k):
        def f(t):
            st=cups.get(k)
            if st is None:return (CX[0],TY-CH+8)
            return (st[0],st[1]+8)
        return f
    # ---- hands ------------------------------------------------------------------------------------
    sy=QY_+QS_*.62;Lsh=(470-QS_/2+6,sy);Rsh=(470+QS_/2-6,sy)
    Lrest=lambda t:(Lsh[0]-60+4*math.sin(t*2.1),sy+120);Rrest=lambda t:(Rsh[0]+60+4*math.sin(t*2.3+1),sy+120)
    hu=ease((T-(h_else+.02))/.16) if T>h_else+.02 else 0
    wait=w_in+.9<T<h_else+.02;wig=4*math.sin(T*14) if wait else 0
    hat=(130*hu,-50*hu,-28*hu+wig);hatpos=lambda t:(470+62+130*hu+2*wig,QY_-70-50*hu+1.5*wig)
    def follow(k,side):                                                             # hand rides the throw for 0.12 s
        t0=throws[k][0]+.10
        def f(t):
            st=cups.get(k);v=t-t0
            if st is None or v<0:return cuptop(k)(t)
            return (st[0]-side*40,st[1]+30)
        return f
    L_ph=[(0,.25,Lrest),(S1[0],S1[1],cuptop('B')),(S2[0],S2[1],cuptop('A')),(S2[1]+.15,w_begin-.3,Lrest),
          (w_begin-.08,w_begin+.10,cuptop('B')),(w_begin+.10,w_begin+.22,follow('B',-1)),(w_begin+.55,h_act-.3,Lrest),
          (h_act-.08,h_act+.10,cuptop('C')),(h_act+.10,h_act+.22,follow('C',-1)),(h_act+.6,h_else+.1,Lrest),
          (h_else+.3,99,lambda t:(470-150-20*math.sin((t-h_else)*9),QY_-10-8*math.sin((t-h_else)*9)))]   # ta-da
    R_ph=[(0,.25,Rrest),(S1[0],S1[1],cuptop('A')),(S2[0],S2[1],cuptop('C')),(S2[1]+.15,w_never-.25,Rrest),
          (w_never-.1,w_in+.10,cuptop('A')),(w_in+.10,w_in+.22,follow('A',1)),(w_in+.75,99,hatpos)]
    hands={'L':_track(T,L_ph),'R':_track(T,R_ph)}
    cash=pop((T-(h_else+.05))/.20) if T>h_else+.05 else 0
    wob=(math.sin(clamp((T-w_soft)/.3)*math.pi) if T>w_soft else 0)+(math.sin(clamp((T-h_sight)/.35)*math.pi) if T>h_sight else 0)+(.25*math.sin(T*7) if wait else 0)
    pulse=math.sin(clamp((T-h_sight)/.4)*math.pi) if T>h_sight else 0
    return dict(cups=cups,hands=hands,hat=hat,cash=cash,wob=wob,pulse=pulse,shoulders=(Lsh,Rsh))

def _armdraw(c,sh,tgt,side):
    ctrl=(sh[0]+side*70,sh[1]+40);pts=[_bez(sh,ctrl,tgt,i/24) for i in range(25)]
    ImageDraw.Draw(c).line(pts,fill=ARM,width=24,joint='curve');ImageDraw.Draw(c).ellipse((sh[0]-12,sh[1]-12,sh[0]+12,sh[1]+12),fill=ARM)

def _draw_game(c,st):
    """Table board, Claude (tile + hat + both arms), the cups (with shadows) and the hands, in the right order."""
    sh=blank(940,120);ImageDraw.Draw(sh).rounded_rectangle((70,30,870,80),radius=20,fill=(0,0,0,40));c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)),(0,TY-20))
    rr(c,(60,TY-8,880,TY+30),'#D8D8DD',14);rr(c,(60,TY-8,880,TY+14),'#ECECEF',14)
    qx=470-QS_/2;qy=QY_;Lsh,Rsh=st['shoulders'];wob=st['wob']
    if st['cash']>0:
        m=emoji('💵',150);gl=blank(300,220);ImageDraw.Draw(gl).ellipse((40,30,260,190),fill=(52,199,89,round(70*st['cash'])));c.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)),(round(470-150),round(qy-m.height-40)))
        place(c,m,470-m.width/2,qy-m.height+40-24*st['cash'],.7+.3*st['cash'],st['cash'],True)
    place(c,tile_claude(QS_),qx,qy,1+.03*wob,1,True,rot=-2*wob)
    h=emoji('🎩',140);hx,hy,hr=st['hat']
    if abs(hx)+abs(hy)<2:
        hs=blank(220,60);ImageDraw.Draw(hs).ellipse((30,10,190,40),fill=(0,0,0,55));c.alpha_composite(hs.filter(ImageFilter.GaussianBlur(8)),(470-110,qy+14))
    place(c,h,470-h.width/2+hx,qy-h.height+42+hy,1,1,abs(hx)>2,rot=hr)
    _armdraw(c,Lsh,st['hands']['L'],-1);_armdraw(c,Rsh,st['hands']['R'],1)
    for k,(x,y,rot,op,flying,lift) in sorted(st['cups'].items(),key=lambda kv:kv[1][1]):
        cup=_cup()
        if not flying:
            cs=blank(240,70);ImageDraw.Draw(cs).ellipse((30,18,210,52),fill=(0,0,0,int(70*max(0,1-lift/180))));c.alpha_composite(cs.filter(ImageFilter.GaussianBlur(9)),(round(x-120),TY-46))
        lay=blank(CW+60,CH+60);lay.alpha_composite(cup,(30,30))
        if k=='A':lay.alpha_composite(tile_salesforce(76),(30+CW//2-38,30+44))
        place(c,lay,x-CW/2-30,y-30,1,op,False,rot=rot if flying else -8*lift/120*(1 if k=='A' else 0))
    for side,key in ((-1,'L'),(1,'R')):
        hx_,hy_=st['hands'][key];ImageDraw.Draw(c).ellipse((hx_-17,hy_-17,hx_+17,hy_+17),fill=HAND)
    if st['pulse']>0:
        k=st['pulse'];m=emoji('💵',150);x0,y0=470-m.width/2,QY_-m.height+40-24
        g=14+10*k;rr(c,(x0-g,y0-g,x0+m.width+g,y0+m.height+g),None,22,(52,199,89,round(255*min(1,k*2))),4)

def worry(t,at,S):
    im=blank(W,H);c=card();Wd=S['worry']['end']-S['worry']['start']
    _draw_game(c,cupsgame(t,at,Wd));enter0(im,c,70,104,t);return im

def hidden(t,at,S):
    """Same table, same choreography, continued (no re-entrance: the cut is invisible)."""
    im=blank(W,H);c=card();Wd=S['worry']['end']-S['worry']['start']
    _draw_game(c,cupsgame(t+Wd,at,Wd));place(im,c,70,104,1,1,True);return im

# ---------------------------------------------------------------- 4. spend (full): the US, its companies, $750,000,000,000
import json as _json
DIGITS='750000000000'
CITIES=[('New York',-74.0,40.7),('Los Angeles',-118.2,34.0),('Chicago',-87.6,41.9),('Houston',-95.4,29.8),('Miami',-80.2,25.8),('Seattle',-122.3,47.6),('Denver',-105.0,39.7),('Atlanta',-84.4,33.7),('Dallas',-96.8,32.8),('Boston',-71.1,42.4)]
MW,MH=420,274
def _proj(lon,lat):return ((lon+125)/(125-66)*MW,(50-lat)/(50-24)*MH)
@lru_cache(None)
def _usmap():
    """The contiguous United States from real geodata (PublicaMundi us-states.json), ink with white state lines."""
    d=_json.load(open(P/'assets/geo/us-states.json'));skip={'Alaska','Hawaii','Puerto Rico'};q=2
    im=blank(MW*q,MH*q);dr=ImageDraw.Draw(im);polys=[]
    for f in d['features']:
        if f['properties']['name'] in skip:continue
        g=f['geometry'];rings=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        for r in rings:polys.append([(x*q,y*q) for x,y in (_proj(a,b) for a,b in r[0])])
    for pl in polys:dr.polygon(pl,fill='#1D1D1F')
    for pl in polys:dr.line(pl+[pl[0]],fill='#F1F0EB',width=2)
    return im.resize((MW,MH),Image.Resampling.LANCZOS)

def spend(t,at):
    im=blank(W,H);w,h=940,650;c=card(w,h,'white',34);d=ImageDraw.Draw(c)
    tus=at('spend','US',.10)-LEAD;tco=at('spend','companies',.46)-LEAD;tr=at('spend','right',1.06)-LEAD;t750=at('spend','750',2.28);tb=at('spend','billion',3.48);ty=at('spend','year',4.68)-LEAD;tsw=at('spend','software.',5.12)-LEAD
    # the country draws in on "US" (left-to-right wipe), the companies pop up on real city coordinates on "companies"
    MX,MY=470,26;k=ease((t-tus+.1)/.4)
    if k>0:
        m=_usmap().copy();msk=Image.new('L',m.size,0);ImageDraw.Draw(msk).rectangle((0,0,round(MW*k),MH),fill=255);m.putalpha(Image.fromarray(np.minimum(np.array(m.getchannel('A')),np.array(msk))))
        c.alpha_composite(m,(MX,MY))
    for i,(nm,lon,lat) in enumerate(CITIES):
        u=t-(tco+i*.06)
        if u<0:continue
        px,py=_proj(lon,lat);s=pop(u/.28);b=Image.open(P/'assets/icons/fluent/office_building.png').convert('RGBA').resize((52,52),Image.Resampling.LANCZOS)
        place(c,b,MX+px-26,MY+py-46-14*(1-ease(u/.2)),max(.05,s),min(1,u*8),True)
    fs=pop((t-tus)/.28) if t>tus else 0
    if fs>0:place(c,emoji('🇺🇸',54),60,52,fs,min(1,(t-tus)/.08),False)
    d.text((130,80),'US companies',font=sf(46,'Semibold'),fill=INK,anchor='lm')
    # the counter: tiles flip in on "right now" already spinning, lock left->right across "seven hundred and fifty", the last zero on "billion"
    TW,TH,GAP,CW_=54,92,6,20;x=60;cy=372;fr=int(t*30);locks=[lerp(t750,tb,i/11) for i in range(12)];allin=t>=tb
    kick=pop((t-tb)/.3) if allin else 0;x0=x
    if t>tr:d.text((x,cy+26),'$',font=sf(72,'Bold'),fill=INK,anchor='ls')
    x+=58
    for i,ch in enumerate(DIGITS):
        if i in (3,6,9):
            if t>tr+.06+i*.04:d.text((x+2,cy+26),',',font=sf(62,'Bold'),fill=INK,anchor='ls')
            x+=CW_
        u=t-(tr+.06+i*.04)
        if u<0:x+=TW+GAP;continue
        sy=ease(u/.22);tile=blank(TW,TH);rr(tile,(0,0,TW-1,TH-1),'#1D1D1F',10);ImageDraw.Draw(tile).line([(0,TH/2),(TW,TH/2)],fill='#3A3A3F',width=2)
        locked=t>=locks[i]
        if not locked:
            kk=(fr*7+i*3)%10
            for dy,a in ((-18,80),(18,80),(0,230)):
                lay=blank(TW,TH);ImageDraw.Draw(lay).text((TW/2,TH/2+dy),str((kk+(1 if dy>0 else -1 if dy<0 else 0))%10),font=sf(58,'Bold'),fill=(255,255,255,a),anchor='mm');tile.alpha_composite(lay)
        else:
            ImageDraw.Draw(tile).text((TW/2,TH/2),ch,font=sf(60,'Bold'),fill='white',anchor='mm')
            if t-locks[i]<.07:lay=blank(TW,TH);rr(lay,(0,0,TW-1,TH-1),(255,255,255,130),10);tile.alpha_composite(lay)
        sc=1+(.10*math.sin(min(1,(t-locks[i])/.25)*math.pi) if locked else 0)+.04*math.sin(kick*math.pi)
        th_=max(2,round(TH*sy));tl=tile.resize((max(2,round(TW*sc)),max(2,round(th_*sc))),Image.Resampling.LANCZOS)
        c.alpha_composite(tl,(round(x+(TW-tl.width)/2),round(cy-tl.height/2)))
        x+=TW+GAP
    xe=x-GAP
    if allin:g=8+12*(1-pop((t-tb)/.24));rr(c,(x0-g-4,cy-TH/2-g-6,xe+g+4,cy+TH/2+g+6),None,22,INK,5)
    if t>ty:
        s_=pop((t-ty)/.26);pl=blank(190,64);rr(pl,(0,0,189,63),'#F0F0F3',32);ImageDraw.Draw(pl).text((95,32),'/ year',font=sf(32,'Semibold'),fill=INK,anchor='mm')
        place(c,pl,xe-190,cy+TH/2+30+10*(1-s_),.8+.2*s_,min(1,(t-ty)/.1),False)
    row=[tile_salesforce,lambda z:tile_icon('Notion',z,.70),lambda z:tile_app('Slack',z),lambda z:tile_app('HubSpot',z),tile_software]
    for i,fn in enumerate(row):
        u=t-(tsw+i*.06)
        if u<0:continue
        s_=pop(u/.28);place(c,fn(100),60+i*(100+22),512+30*(1-ease(u/.2)),.7+.3*s_,min(1,u/.08),True)
    if t>tsw:
        lay=blank(w,h);ImageDraw.Draw(lay).text((w-60,562),'software',font=sf(36,'Semibold'),fill=GRAY,anchor='rm');place(c,lay,0,0,1,ease((t-tsw)/.25),False)
    enter0(im,c,70,140,t);return im

# ---------------------------------------------------------------- 5. alot (split): a lot, until the other bar shoots off the top
def alot(t,at):
    im=blank(W,H);w,h=940,620;c=card(w,h);d=ImageDraw.Draw(c)
    tn=at('alot','not',1.16)-LEAD;tth=at('alot','this.',1.78)-LEAD
    FL=530;d.line([(60,FL),(880,FL)],fill='#DEDCD4',width=4)
    hA0=ease((t+.05)/.5)*360;shrink=ease((t-tn)/.35) if t>tn else 0;hA=lerp(hA0,54,shrink)
    xa=210;wa=190;rr(c,(xa,FL-hA,xa+wa,FL),INK,22)
    d=ImageDraw.Draw(c);d.text((xa+wa/2,FL+34),'software',font=sf(30,'Medium'),fill=GRAY,anchor='mm')
    d.text((xa+wa/2,FL-hA-36),'$750B',font=sf(48 if shrink<.5 else 40,'Bold'),fill=INK,anchor='mm')
    if t>tn:                                                     # the mystery bar creeps up from "not", shoots up on "this" and bounces off the top of the card
        u=t-tn;top=60;xb=560;wb=190                                # the bar's top stops at y=60: always inside the card
        if t>tth:
            v=t-tth;hB=(FL-top)*min(1,ease(v/.32))+(10*math.sin(v*18)*math.exp(-v*5) if v>.32 else 0)
        else:hB=ease(u/.6)*60
        rr(c,(xb,FL-hB,xb+wb,FL),'#C7C7CC',22)
        if hB>120:place(c,tile_q(96),xb+wb/2-48,FL-hB+36,1,1,False)
        d=ImageDraw.Draw(c);d.text((xb+wb/2,FL+34),'?',font=sf(30,'Semibold'),fill=GRAY,anchor='mm')
    enter0(im,c,70,104,t);return im

def _money(c,x,y,val,unit,col,big=190,pre='$'):
    """Right-aligned '$NNN B' on one baseline. Returns the left x."""
    d=ImageDraw.Draw(c);fu=sf(72,'Semibold');fn=sf(big,'Bold');fp=sf(big*.55,'Semibold');uw=fu.getlength(unit)
    d.text((x,y),unit,font=fu,fill=SOFT_GREY,anchor='rs');vx=x-uw-14
    d.text((vx,y),val,font=fn,fill=col,anchor='rs');vx-=fn.getlength(val)+8
    d.text((vx,y),pre,font=fp,fill=col,anchor='rs');return vx-fp.getlength(pre)

# ---------------------------------------------------------------- 6. six (full): software vs services on one axis
def six(t,at):
    im=blank(W,H);w=940
    tc=at('six','companies',.79)-LEAD;ts=at('six','six',2.03)-LEAD;tm=at('six','more,',2.63);t46=at('six','4.6',3.15);ttr=at('six','trillion',3.99);td=at('six','dollars',4.45)-LEAD
    grow=ease((t-tc)/.30) if t>tc else 0;h=round(lerp(330,660,grow));c=card(w,h,'white',34);bx0,bx1=60,w-60;full=bx1-bx0
    AX=5.0                                                        # shared axis, 0..$5T
    # ---- row A: software (fades back once the services number has landed - it is the small one now)
    rowA=blank(w,300);place(rowA,tile_software(112),60,58,1,1,True);d=ImageDraw.Draw(rowA)
    d.text((196,116),'Software',font=sf(50,'Semibold'),fill=INK,anchor='lm')
    _money(rowA,w-60,176,'750','B',INK,120)
    rr(rowA,(bx0,222,bx1,258),'#F0F0F3',18);pa=ease((t+.05)/.5);rr(rowA,(bx0,222,bx0+max(36,full*.75/AX*pa),258),INK,18)
    dim=smooth((t-(t46+.05))/(ttr-t46-.1)) if t>t46+.05 else 0;place(c,rowA,0,0,1,1-.5*dim,False)
    # ---- row B: services (the card grows for it)
    if t>tc:
        row=blank(w,330);place(row,tile_emoji('💼',112),60,20,1,1,True);dr=ImageDraw.Draw(row)
        dr.text((196,78),'Services',font=sf(50,'Semibold'),fill=INK,anchor='lm')
        if t>ts:                                                  # 6x chip springs on "six"
            s=pop((t-ts)/.26);ch=blank(120,60);rr(ch,(0,0,119,59),'#EAF6EE',30,GREEN,3);ImageDraw.Draw(ch).text((60,30),'6×',font=sf(34,'Bold'),fill=GREEN_D,anchor='mm')
            place(row,ch,196+sf(50,'Semibold').getlength('Services')+22,50+8*(1-s),.7+.3*s,min(1,(t-ts)/.08),False)
        if t>=tm:                                                 # counts up from "more", lands 4.6 on the number, T on "trillion"
            pv=smooth((t-tm)/(t46-tm));vb=4.6*pv;_money(row,w-60,138,f'{vb:.1f}',('T' if t>=ttr else ''),GREEN_D,120)
        rr(row,(bx0,184,bx1,220),'#F0F0F3',18)
        pb=(.75/AX)*(1-smooth((t-ts)/(ttr-ts)))+(4.6/AX)*smooth((t-ts)/(ttr-ts)) if t>ts else (.75/AX)*ease((t-tc)/.3)
        rr(row,(bx0,184,bx0+max(36,full*pb),220),GREEN,18)
        if t>ts:
            ph=((t-ts)%.8)/.8;px=bx0+18+(max(36,full*pb)-36)*ph;ImageDraw.Draw(row).ellipse((px-10,202-10,px+10,202+10),fill='white')
        if t46<t<ttr:                                             # a light sweeps along the bar while "trillion" is on its way
            sw=smooth((t-t46)/(ttr-t46));sx=bx0+(full*pb+140)*sw-140;lay=blank(w,300)
            for k in range(14):ImageDraw.Draw(lay).rectangle((sx+k*10,184,sx+k*10+10,220),fill=(255,255,255,round(150*math.sin(k/14*math.pi))))
            m=Image.new('L',(w,300));ImageDraw.Draw(m).rounded_rectangle((bx0,184,bx0+max(36,full*pb),220),radius=18,fill=255);lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel('A')),np.array(m))));row.alpha_composite(lay)
        if t>=ttr:                                                # green frame lands on "trillion"
            s=pop((t-ttr)/.24);fw=sf(120,'Bold').getlength('4.6')+sf(66,'Semibold').getlength('$')+8;x1_=w-60-sf(72,'Semibold').getlength('T')-14
            g=10+14*(1-s);rr(row,(x1_-fw-g-6,138-92-g,x1_+g+6,138+16+g),None,20,GREEN,5)
            gl=.5+.5*math.sin((t-ttr)*40);rr(row,(bx0,184,bx0+full*4.6/AX,220),(255,255,255,round(90*gl)),18)
        place(c,row,0,296+26*(1-grow),1,grow,False)
    # ---- shared axis ticks arrive one by one while "four point six" is said
    ay=h-100
    for k in range(6):
        u=t-(t46+.05+k*.14)
        if u<=0:continue
        e=ease(u/.2);xx=bx0+full*k/5;lay=blank(w,h);dl=ImageDraw.Draw(lay)
        dl.line([(xx,ay),(xx,ay+16*e)],fill='#C7C7CC',width=3)
        dl.text((min(max(xx,bx0+14),bx1-28),ay+40),f'${k}T' if k else '0',font=sf(27,'Medium'),fill='#8E8E93',anchor='mm')
        place(c,lay,0,0,1,e,False)
    if t>t46:ImageDraw.Draw(c).line([(bx0,ay),(bx0+full*ease((t-t46)/.8),ay)],fill='#C7C7CC',width=3)
    if t>td:                                                      # the source lands on "dollars"
        lay=blank(w,h);ImageDraw.Draw(lay).text((w/2,ay+78),'source: Foundation Capital, 2024',font=sf(25),fill='#AEAEB2',anchor='mm');place(c,lay,0,0,1,ease((t-td)/.25),False)
    enter0(im,c,70,140,t);return im

# ---------------------------------------------------------------- 7. services (split): the source page
def services(t,at):return _fc_part.render(t,at)

# ---------------------------------------------------------------- 8. jobs (full): four service tiles land on their words
JOBS=[('Accountants,','office_worker','Accountants'),('lawyers,','judge','Lawyers'),('brokers,','man_in_tuxedo','Brokers'),('agencies.','artist','Agencies')]
def _jobs_layout(n,ts=280,gap=60):
    """Tile centres for n landed tiles: one centred, two in a row, then 2+1, then 2x2."""
    L,R=540-ts/2-gap/2,540+ts/2+gap/2;c1,c2,mid=310,650,480
    return [[(540,mid)],[(L,mid),(R,mid)],[(L,c1),(R,c1),(540,c2)],[(L,c1),(R,c1),(L,c2),(R,c2)]][max(1,min(4,n))-1]
def jobs(t,at):
    im=blank(W,H);ts=280
    ons=[at('jobs',wd,[.11,.83,1.43,2.09][i])-LEAD for i,(wd,_,_) in enumerate(JOBS)]
    ons[0]=min(ons[0],-.10)                                        # already landing on frame 0: a cut is never blank
    n=sum(1 for o in ons if t>=o)
    if n==0:n=1
    cur=_jobs_layout(n);prev=_jobs_layout(n-1) if n>1 else cur;k=ease((t-ons[n-1])/.26)
    for i,(wd,em,lab) in enumerate(JOBS):
        a=t-ons[i]
        if a<0:continue
        if i<n-1:cx,cy=lerp(prev[i][0],cur[i][0],k),lerp(prev[i][1],cur[i][1],k)
        else:cx,cy=cur[i]
        v=pop(a/.28);bob=math.sin(t*2.6+i)*6
        place(im,tile_fluent(em,ts),cx-ts/2,cy-ts/2-120*(1-ease(a/.22))+bob,max(.05,.7+.3*v),min(1,a*9),True)
        la=ease((a-.10)/.22)
        if la>0:
            lay=blank(W,H);ImageDraw.Draw(lay).text((cx,cy+ts/2+46+10*(1-la)),lab,font=sf(40,'Semibold'),fill=INK,anchor='mm');place(im,lay,0,0,1,la,False)
    return im

# ---------------------------------------------------------------- 9. why (split): the question
@lru_cache(None)
def think(size):
    """Apple 🤔 upscaled to 4K on green (from the 19 Sep reel); matte = the glyph's own alpha from the 160 px strike."""
    f=ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc',160);raw=Image.new('RGBA',(240,240));ImageDraw.Draw(raw).text((120,120),'🤔',font=f,embedded_color=True,anchor='mm')
    col=np.array(Image.open(P/'assets/emoji/think-4k.png').convert('RGB').resize((2160,2160),Image.Resampling.LANCZOS)).astype(float)
    col[...,1]=np.minimum(col[...,1],np.maximum(col[...,0],col[...,2]))
    alpha=raw.crop((30,5,210,185)).getchannel('A').resize((2160,2160),Image.Resampling.LANCZOS).filter(ImageFilter.MinFilter(13)).filter(ImageFilter.GaussianBlur(2))
    im=Image.fromarray(col.astype('uint8'),'RGB').convert('RGBA');im.putalpha(alpha);im=im.crop(im.getbbox());return im.resize((size,round(size*im.height/im.width)),Image.Resampling.LANCZOS)

def why(t,at):
    """"And why is that?": the 🤔 pops in, rocks while he asks, hops on "why", shakes on "that?"; question marks spring in around it."""
    im=blank(W,H);c=card();tw_=at('why','why',.25)-LEAD;tth=at('why','that?',.75)
    for k in range(7):                                            # question marks around the face
        t0=.04+k*.09
        if t<t0:continue
        a=t-t0;e=spring(a/.3);ang=-2.6+k*.87;r=250+16*math.sin(a*3+k);x=470+math.cos(ang)*r*1.35;y=280+math.sin(ang)*r*.7-a*12
        q=blank(120,140);ImageDraw.Draw(q).text((60,70),'?',font=sf(84+(k%3)*16,'Bold'),fill=['#D97757','#1D1D1F','#AEAEB2'][k%3],anchor='mm')
        place(c,q,x-60,y-70,max(.05,min(1.1,e)),min(1,e*2)*.95,False,rot=(k%2*2-1)*14+5*math.sin(t*6+k))
    e=spring((t+.04)/.3);rock=math.sin(t*5.2)*7*min(1,t*2);hop=math.sin(clamp((t-tw_)/.32)*math.pi)
    shake=12*math.sin((t-tth)*46)*max(0,1-(t-tth)/.34) if t>=tth else 0
    f_=think(380);place(c,f_,470-f_.width/2+shake*.6,300-f_.height/2-hop*40,max(.05,min(1.08,e))*(1+.08*hop),min(1,(t+.04)*10),False,rot=rock+shake)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 10. tool (split): the accounting tool gets its tabs closed, one after another
TABS=['Dashboard','Invoices','Expenses','Payroll','Taxes','Bank feed','Receipts','Reports','Clients','Settings']   # tabs of the shiney.ai accounting tool
def tool(t,at):
    im=blank(W,H);w,h=940,560;win=blank(w,h);rr(win,(0,0,w-1,h-1),'white',16)
    tn=at('tool','never',.85)-LEAD;tacc=at('tool','accounting.',2.81)-LEAD;N=len(TABS)
    closes=[lerp(tn,tacc,k/(N-1)) for k in range(N)];nc=sum(1 for c_ in closes if t>=c_);open_=TABS[nc:]
    rr(win,(0,0,w-1,70),'#EFEFF1',16);d=ImageDraw.Draw(win);d.rectangle((0,40,w-1,92),fill='#EFEFF1')
    for i,c_ in enumerate(['#FF5F57','#FEBC2E','#28C840']):d.ellipse((16+i*20,20,28+i*20,32),fill=c_)
    rr(win,(w/2-220,10,w/2+220,42),'#E1E1E4',9);d=ImageDraw.Draw(win);url='shiney.ai/'+(open_[0].lower().replace(' ','-') if open_ else '')
    d.text((w/2,26),url,font=sf(15),fill='#3A3A3C',anchor='mm')
    if open_:
        tw_=(w-24)/len(open_)
        for k,name in enumerate(open_):
            x0=12+k*tw_;act=k==0
            rr(win,(x0+2,54,x0+tw_-2,92),'white' if act else '#E2E2E6',8);d=ImageDraw.Draw(win)
            d.ellipse((x0+14,66,x0+28,80),fill=BLUE if act else '#AEAEB2')
            f=sf(16,'Medium' if act else 'Regular');lab=name if f.getlength(name)<tw_-72 else name[:max(1,int((tw_-72)/9))]+'…'
            d.text((x0+36,73),lab,font=f,fill=INK if act else GRAY,anchor='lm');d.text((x0+tw_-20,73),'×',font=sf(22),fill='#6E6E73',anchor='mm')
    d=ImageDraw.Draw(win);d.line([(0,92),(w,92)],fill='#D8D8DC',width=1)
    if open_:                                                          # the active tab's page: a skeleton, seeded by the tab
        name=open_[0];rnd=random.Random(TABS.index(name)*3);d.text((40,140),name,font=sf(34,'Bold'),fill=INK,anchor='lm');pill(win,'+ New',w-160,118,120,40,BLUE,'white',18)
        for r_ in range(5):
            y=196+r_*64;rr(win,(40,y+4,40+rnd.randint(160,380),y+22),'#E5E5EA',9);rr(win,(470,y+4,470+rnd.randint(80,180),y+22),'#E5E5EA',9)
            st=rnd.choice(['Paid','Due','Overdue']);col={'Paid':('#EAF6EE',GREEN_D),'Due':('#FFF4E0','#B25E00'),'Overdue':('#FDECEC','#C0392B')}[st]
            pw=sf(17,'Medium').getlength(st)+26;rr(win,(700,y,700+pw,y+28),col[0],14);ImageDraw.Draw(win).text((700+pw/2,y+14),st,font=sf(17,'Medium'),fill=col[1],anchor='mm')
            rr(win,(w-140,y+4,w-40,y+22),'#E5E5EA',9);ImageDraw.Draw(win).line([(40,y+48),(w-40,y+48)],fill='#F0F0F2',width=1)
        fl=t-closes[nc-1] if nc else 9
        if fl<.08:lay=blank(w,h);rr(lay,(0,92,w-1,h-1),(255,255,255,round(160*(1-fl/.08))),0);win.alpha_composite(lay)   # page swap flash
    else:d.text((w/2,330),'No open tabs',font=sf(28),fill='#AEAEB2',anchor='mm')
    pts=[(.30,700,400)]
    for k,tc in enumerate(closes):
        tw_=(w-24)/(N-k);pts+=[(tc-.06,12+tw_-20,73),(tc+.05,12+tw_-20,73)]
    pointer_motion.motion(win,t,points=pts,clicks=closes,end=tacc+.4)
    gone=ease((t-(tacc+.14))/.3) if t>tacc+.14 else 0                 # the empty window collapses after the last tab
    e=ease((t+.09)/.32);sc=(.96+.04*e)*(1-.92*gone)
    place(im,win,70,104+22*(1-e),sc,e*(1-gone),True)
    return im

# ---------------------------------------------------------------- 11. done (full): the MacBook - press one button, get "Complete"
TASKS=['Receipts categorised','Invoices reconciled','VAT return filed']
def _screen(t,at,w,h):
    s=desktop(w,h).copy()
    twant=at('done','want',.61)-LEAD;tacc=at('done','accounting',1.03)-LEAD;tdone=at('done','done',1.63)-LEAD;tthem=at('done','them.',2.21)-LEAD
    rr(s,(0,0,w,34),(255,255,255,120),0);s.alpha_composite(icon('Apple',20),(16,7))
    for k,(lab,wt) in enumerate([('Accounting','Bold'),('File','Regular'),('Edit','Regular'),('View','Regular')]):
        ImageDraw.Draw(s).text((50+[0,122,166,214][k],17),lab,font=sf(17,wt),fill='#1D1D1F',anchor='lm')
    ImageDraw.Draw(s).text((w-18,17),'Tue 22 Sep  09:41',font=sf(17,'Medium'),fill='#1D1D1F',anchor='rm')
    wifi(s,w-212,17,on=True);rr(s,(w-262,9,w-232,25),None,5,'#1D1D1F',2);rr(s,(w-259,12,w-240,22),'#1D1D1F',2)
    ww,wh=w-150,h-150;tx,ty=75,58;win=blank(ww,wh);rr(win,(0,0,ww-1,wh-1),'white',16);rr(win,(0,0,ww-1,50),'#F0F0F2',16);ImageDraw.Draw(win).rectangle((0,34,ww-1,50),fill='#F0F0F2')
    for i,cc in enumerate(['#FF5F57','#FEBC2E','#28C840']):ImageDraw.Draw(win).ellipse((18+i*24,17,32+i*24,31),fill=cc)
    win.alpha_composite(tile_claude(28),(ww//2-80,11));ImageDraw.Draw(win).text((ww/2-44,25),'Accounting',font=sf(19,'Medium'),fill='#3A3A3C',anchor='lm')
    d=ImageDraw.Draw(win);d.text((36,104),'September books',font=sf(30,'Bold'),fill=INK,anchor='lm')
    for i,lab in enumerate(TASKS):                                    # rows tick after the press
        y=190+i*54;td=tacc+.14+i*.15;on=t>td
        if on:checkmark(win,52,y,round(13*pop((t-td)/.24)),GREEN)
        else:ImageDraw.Draw(win).ellipse((39,y-13,65,y+13),outline='#C7C7CC',width=3)
        ImageDraw.Draw(win).text((84,y),lab,font=sf(24,'Medium' if on else 'Regular'),fill=INK if on else '#3A3A3C',anchor='lm')
    bx,by,bw,bh=ww-36-330,wh-36-72,330,72;pressed=tacc<=t<tacc+.12;busy=tacc+.12<=t<tdone;ps=.96 if pressed else 1
    btn=blank(bw,bh);rr(btn,(0,0,bw-1,bh-1),'#B9633F' if pressed else TERRA,36)
    if busy:                                                          # spinner while it works
        a=(t-tacc)*720;ImageDraw.Draw(btn).arc((22,18,58,54),a,a+250,fill='white',width=5);ImageDraw.Draw(btn).text((bw/2+18,bh/2),'Working…',font=sf(26,'Semibold'),fill='white',anchor='mm')
    else:ImageDraw.Draw(btn).text((bw/2,bh/2),'Do my accounting',font=sf(26,'Semibold'),fill='white',anchor='mm')
    place(win,btn,bx,by,ps,1,True)
    if t>tdone:                                                       # the sheet: big check, "Complete"
        u=t-tdone;e=ease(u/.3);lay=blank(ww,wh);rr(lay,(0,0,ww-1,wh-1),(0,0,0,round(80*e)),16);win.alpha_composite(lay)
        sh=blank(420,270);rr(sh,(0,0,419,269),'white',22);checkmark(sh,210,88,round(48*pop(u/.4)),GREEN)
        ImageDraw.Draw(sh).text((210,166),'Complete',font=sf(34,'Semibold'),fill=INK,anchor='mm');ImageDraw.Draw(sh).text((210,204),'Accounting done for you',font=sf(20),fill=GRAY,anchor='mm')
        pill(sh,'OK',150,228,120,34,'#0060C0' if t>tthem else BLUE,'white',18)
        lift=ease((t-tthem-.06)/.25) if t>tthem+.06 else 0
        place(win,sh,(ww-420)/2,(wh-270)/2-30*(1-e)-40*lift,.9+.1*e,e*(1-lift),True)
    pointer_motion.motion(win,t,points=[(.30,ww-40,120),(tacc-.05,bx+bw/2+24,by+bh/2+8),(tacc+.16,bx+bw/2+24,by+bh/2+8),(tthem-.05,ww/2+8,(wh-270)/2+245),(tthem+.12,ww/2+8,(wh-270)/2+245),(tthem+.6,ww/2+120,(wh-270)/2+330)],clicks=[tacc,tthem],end=tthem+.8)
    e=ease((t-.18)/.28);place(s,win,tx,ty+14*(1-e),.97+.03*e,e,True)
    if t>tthem+.1:                                                    # notification banner after OK
        u=t-tthem-.1;e2=ease(u/.3);nb=blank(330,84);rr(nb,(0,0,329,83),(255,255,255,235),18);nb.alpha_composite(tile_claude(44),(16,20))
        ImageDraw.Draw(nb).text((74,30),'Claude',font=sf(18,'Semibold'),fill=INK,anchor='lm');ImageDraw.Draw(nb).text((74,56),'Books closed · report sent',font=sf(17),fill='#3A3A3C',anchor='lm')
        place(s,nb,w-346+40*(1-e2),42,1,e2,True)
    dk=[('Claude',tile_claude),('ChatGPT',lambda z:apptile('ChatGPT',z)),('Notion',lambda z:apptile('Notion',z)),('Software',tile_software)]
    dz=54;dwid=len(dk)*(dz+14)+14;dx=(w-dwid)//2;dy=h-dz-22
    rr(s,(dx,dy-8,dx+dwid,dy+dz+8),(255,255,255,150),20)
    for k,(nm,fn) in enumerate(dk):
        yy=dy
        if nm=='Claude':
            u=t-twant
            if u<0:continue
            yy=dy-(abs(math.sin(u*9.5))*46*math.exp(-u*2.6) if u<1.4 else 0)-60*(1-ease(u/.16))
            ImageDraw.Draw(s).ellipse((dx+14+k*(dz+14)+dz/2-3,dy+dz+1,dx+14+k*(dz+14)+dz/2+3,dy+dz+7),fill='#1D1D1F')
        s.alpha_composite(fn(dz),(dx+14+k*(dz+14),round(yy)))
    return s

def done(t,at):
    im=blank(W,H);mw=940;op=.12+.88*ease((t+.06)/.46)
    sw,sh=mw-36,round((mw-36)*.628);lit=clamp((t-.22)/.2)
    scr=_screen(t,at,sw,sh)
    if lit<1:scr=Image.blend(Image.new('RGBA',scr.size,'#050506'),scr,lit)
    mb=macbook(mw,scr,op);place(im,mb,(W-mb.width)//2,150+(1-ease((t+.09)/.32))*26,1,1,False)
    return im

# ---------------------------------------------------------------- 12. humans (split): a lot of humans, then not
@lru_cache(None)
def _person(size,col):
    q=3;im=blank(size*q,size*q);d=ImageDraw.Draw(im);S=size*q
    d.ellipse((0,0,S-1,S-1),fill='#E9E9EC');d.ellipse((S*.33,S*.16,S*.67,S*.50),fill=col)
    d.ellipse((S*.14,S*.54,S*.86,S*1.26),fill=col);m=Image.new('L',(S,S));ImageDraw.Draw(m).ellipse((0,0,S-1,S-1),fill=255);im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(m))))
    return im.resize((size,size),Image.Resampling.LANCZOS)
COLS=['#5B6CFF','#D97757','#2FB350','#1FBDFE','#B25E00','#8E8E93','#E551BA','#F5B700','#1D1D1F','#0A84FF','#C0392B','#6E6E73']
def humans(t,at):
    im=blank(W,H);c=card();d=ImageDraw.Draw(c);w,h=940,560
    tnow=at('humans','now,',.58)-LEAD;tneed=at('humans','needed',1.24)-LEAD;thum=at('humans','humans,',2.20)-LEAD;tnot=at('humans','not',3.14)-LEAD;tany=at('humans','anymore.',3.28)-LEAD
    # timeline: "until now"
    d.line([(60,96),(880,96)],fill='#E5E5EA',width=4);p=smooth((t+.05)/max(.3,tnow+.05));d.line([(60,96),(60+820*p,96)],fill=INK,width=4)
    d.ellipse((60+820*p-10,86,60+820*p+10,106),fill=INK)
    if t>tnow:
        s=pop((t-tnow)/.26);lay=blank(w,h);ImageDraw.Draw(lay).text((880,60),'now',font=sf(28,'Semibold'),fill=INK,anchor='rm');place(c,lay,0,8*(1-s),1,s,False)
    d=ImageDraw.Draw(c);d.text((60,60),'until',font=sf(28,'Medium'),fill=GRAY,anchor='lm')
    # avatars fill a 6x2 grid between "needed" and "humans"
    sz=100;gx=[92+i*128 for i in range(6)];gy=[170,320];gone=ease((t-tnot)/.3) if t>tnot else 0
    for i in range(12):
        u=t-(tneed+i*((thum-tneed)/11))
        if u<0:continue
        s=pop(u/.26);x=gx[i%6];y=gy[i//6];fall=gone*(240+i*8)*gone
        pr=_person(sz,COLS[i]) if gone<.5 else _person(sz,'#C7C7CC')
        place(c,pr,x,y+fall,max(.05,s)*(1-.3*gone),max(0,min(1,u*8))*(1-gone),True,rot=gone*(-20+i*4))
    if t>tany:
        s=pop((t-tany)/.28);place(c,tile_claude(170),470-85,240-85,s,min(1,(t-tany)/.08),True)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- the company figure (shared by next + service)
@lru_cache(None)
def _head(size,face='smile',badge='AI'):
    """White squircle head with a drawn face and a small badge."""
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill='white');d=ImageDraw.Draw(im);lw=max(3,round(size*.035))
    ex,ey,r=size*.33,size*.44,size*.055
    if face=='dead':
        for cx in (ex,size-ex):
            d.line([(cx-r*1.7,ey-r*1.7),(cx+r*1.7,ey+r*1.7)],fill=INK,width=lw);d.line([(cx-r*1.7,ey+r*1.7),(cx+r*1.7,ey-r*1.7)],fill=INK,width=lw)
        d.arc((size*.34,size*.66,size*.66,size*.92),200,340,fill=INK,width=lw)
        d.ellipse((size*.52,size*.70,size*.62,size*.84),fill='#E8707A')
    else:
        for cx in (ex,size-ex):d.ellipse((cx-r,ey-r,cx+r,ey+r),fill=INK)
        d.arc((size*.32,size*.50,size*.68,size*.80),15,165,fill=INK,width=lw)
    if badge:
        rr(im,(size*.60,size*.08,size*.92,size*.27),'#1D1D1F',size*.05);ImageDraw.Draw(im).text((size*.76,size*.175),badge,font=sf(size*.11,'Bold'),fill='white',anchor='mm')
    return _ring(_mask(im,size),size)

@lru_cache(None)
def _maskface(w=190,h=230):
    """A smiling service-company mask on a stick (masquerade style)."""
    q=2;im=blank(w*q,(h+120)*q);d=ImageDraw.Draw(im)
    d.line([(w*.62*q,h*.86*q),(w*.86*q,(h+112)*q)],fill=INK,width=10*q)
    d.ellipse((0,0,w*q-1,h*q-1),fill='#FFF6EC',outline=INK,width=4*q)
    for cx in (.33,.67):d.ellipse(((cx*w-.09*w)*q,(.36*h)*q,(cx*w+.09*w)*q,(.36*h+.09*w*1.3)*q),fill=INK)
    d.arc((.24*w*q,.48*h*q,.76*w*q,.86*h*q),15,165,fill=INK,width=5*q)
    for cx in (.20,.80):d.ellipse(((cx*w-.07*w)*q,(.60*h)*q,(cx*w+.07*w)*q,(.60*h+.10*w)*q),fill='#F6C1B5')
    return im.resize((w,h+120),Image.Resampling.LANCZOS)

def _figure(head,walk=0,arm=None,col=INK,W_=460,H_=560):
    """Figure layer: head on a torso with two legs; the right arm can reach a point (holding something). Feet at (W_/2, H_-10)."""
    im=blank(W_,H_);d=ImageDraw.Draw(im);cx=W_/2;fy=H_-10;tw,th=150,170;top=fy-330
    sw=22*math.sin(walk) if walk else 0
    for k,(lx,ex) in enumerate(((cx-40,cx-40+sw),(cx+40,cx+40-sw))):
        d.line([(lx,top+th-14),(ex,fy-8)],fill=col,width=28);d.rounded_rectangle((ex-26,fy-18,ex+30,fy+2),radius=9,fill=col)
    rr(im,(cx-tw/2,top,cx+tw/2,top+th),col,46)
    lx,ly=cx-tw/2+14,top+34;d.line([(lx,ly),(lx-34+8*math.sin(walk*1.3),ly+120)],fill=col,width=26)
    rx,ry=cx+tw/2-14,top+34
    if arm is None:d.line([(rx,ry),(rx+34-8*math.sin(walk*1.3),ry+120)],fill=col,width=26)
    else:d.line([(rx,ry),arm],fill=col,width=26);d.ellipse((arm[0]-16,arm[1]-16,arm[0]+16,arm[1]+16),fill=col)
    hs=head.width;im.alpha_composite(head,(round(cx-hs/2),round(top-hs+12)))
    return im

def place_pivot(im,obj,px,py,pivot,rot=0,opacity=1):
    """Place obj so that its pivot point (obj coords) lands on (px,py) after rotating by rot degrees."""
    if rot:
        ow,oh=obj.size;r=obj.rotate(rot,resample=Image.Resampling.BICUBIC,expand=True)
        a=math.radians(rot);dx,dy=pivot[0]-ow/2,pivot[1]-oh/2
        nx=dx*math.cos(a)+dy*math.sin(a);ny=-dx*math.sin(a)+dy*math.cos(a)
        place(im,r,px-(r.width/2+nx),py-(r.height/2+ny),1,opacity,False)
    else:place(im,obj,px-pivot[0],py-pivot[1],1,opacity,False)

@lru_cache(None)
def _grave(w=230,h=250):
    q=2;im=blank(w*q,h*q);d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w*q-1,h*q-1),radius=w*q*.42,fill='#C7C7CC',outline='#8E8E93',width=3*q);d.rectangle((0,h*q*.6,w*q-1,h*q-1),fill='#C7C7CC')
    d.line([(0,h*q-2*q),(w*q,h*q-2*q)],fill='#8E8E93',width=3*q)
    d.text((w*q/2,h*q*.40),'R.I.P.',font=sf(44*q,'Bold'),fill='#3A3A3C',anchor='mm');d.text((w*q/2,h*q*.66),'AI software',font=sf(22*q,'Medium'),fill='#5A5A5E',anchor='mm');d.text((w*q/2,h*q*.80),'company',font=sf(22*q,'Medium'),fill='#5A5A5E',anchor='mm')
    return im.resize((w,h),Image.Resampling.LANCZOS)

# ---------------------------------------------------------------- 13. next (full): Claude shoots up the SaaS wall
def next_(t,at):return _shootout_part.render(t,at)

# ---------------------------------------------------------------- 14. service (split): search "accountant near me" - the AI company is listed as a service
FIRMS=[('Smith & Co Accountants','Accountants · Open'),('Northwind Bookkeeping','Bookkeeping · Open')]
def _stars(d,x,y,n=5,col='#FBBC05',r=8):
    for i in range(n):
        cx=x+i*(r*2+4);pts=[(cx+r*math.cos(-math.pi/2+k*math.pi/5)*(1 if k%2==0 else .45),y+r*math.sin(-math.pi/2+k*math.pi/5)*(1 if k%2==0 else .45)) for k in range(10)]
        d.polygon(pts,fill=col)
def service(t,at):
    im=blank(W,H);w,h=940,560;win=window(w,h,url='google.com/search?q=accountant+near+me');d=ImageDraw.Draw(win)
    tsw=at('service','software',.98)-LEAD;tcm=at('service','companies',1.36)-LEAD;tact=at('service','acting',2.08)-LEAD;tas=at('service','as',2.60)-LEAD;tsv=at('service','service',2.78)-LEAD;tco=at('service','companies',3.18,1)-LEAD
    x=40
    for ch,col in zip('Google',['#4285F4','#EA4335','#FBBC05','#4285F4','#34A853','#EA4335']):d.text((x,94),ch,font=sf(40,'Bold'),fill=col,anchor='lm');x+=sf(40,'Bold').getlength(ch)-1
    rr(win,(210,70,w-40,118),'white',24,'#DFE1E5',2);d=ImageDraw.Draw(win);q='accountant near me';s_=reveal(q,t-.05,.70);d.text((238,94),s_,font=sf(22),fill=INK,anchor='lm')
    if len(s_)<len(q) or int(t*3)%2==0:cx_=238+sf(22).getlength(s_)+3;d.rectangle((cx_,82,cx_+2,106),fill=INK)
    d.ellipse((w-86,82,w-64,104),outline='#4285F4',width=3);d.line([(w-66,102),(w-56,112)],fill='#4285F4',width=3)
    if .12<t<tsw:                                                     # autocomplete dropdown while typing
        sug=['accountant near me','accountant near me open now','accountant near me reviews','accountant near me for small business']
        e=min(1,(t-.12)/.15)*min(1,(tsw-t)/.12);dd=blank(w-250,190);rr(dd,(0,0,w-251,189),'white',18,'#DFE1E5',2);dr=ImageDraw.Draw(dd)
        for i,sg in enumerate(sug):
            if t<.12+i*.14:continue
            shown=reveal(sg,t-.12-i*.14,.30);dr.ellipse((22,26+i*42,34,38+i*42),outline='#9AA0A6',width=2);dr.text((48,32+i*42),shown,font=sf(20),fill=INK if i==0 else '#3C4043',anchor='lm')
        place(win,dd,210,124+6*(1-e),1,e,True)
    if t>tsw:
        tx=214;e=ease((t-tsw)/.25);lay=blank(w,h);dl=ImageDraw.Draw(lay)
        for i,lab in enumerate(['All','Maps','Images','News','Videos']):
            dl.text((tx,148),lab,font=sf(18,'Medium' if i==0 else 'Regular'),fill='#1A73E8' if i==0 else '#5F6368',anchor='lm')
            if i==0:dl.line([(tx-4,164),(tx+sf(18,'Medium').getlength(lab)+4,164)],fill='#1A73E8',width=3)
            tx+=sf(18).getlength(lab)+34
        dl.line([(0,174),(w,174)],fill='#EBEBEB',width=1);place(win,lay,0,0,1,e,False)
    if t>tcm-.05:
        e=ease((t-tcm+.05)/.25);lay=blank(w,h);ImageDraw.Draw(lay).text((40,206),'Businesses',font=sf(24,'Semibold'),fill=INK,anchor='lm');place(win,lay,0,6*(1-e),1,e,False)
    ins=ease((t-tact)/.32) if t>tact else 0;rowh=96;y0=236
    def _row(nm,ic,sub,ai=False):
        row=blank(w-80,84);rr(row,(0,0,w-81,83),('#EAF6EE' if t>tas else '#F8F9FA') if ai else 'white',16,(GREEN if t>tas else '#E3E3E6') if ai else '#EBEBEB',2)
        if ai:place(row,tile_claude(60),12,12,1,1,True)
        else:row.alpha_composite(Image.open(P/'assets/icons/fluent'/f'{ic}.png').convert('RGBA').resize((58,58),Image.Resampling.LANCZOS),(13,13))
        dr=ImageDraw.Draw(row);dr.text((88,26),nm,font=sf(24,'Semibold'),fill=INK,anchor='lm');_stars(dr,90,58)
        if ai:
            dr.text((196,58),'AI ·',font=sf(18),fill='#5F6368',anchor='lm');cx0=196+sf(18).getlength('AI · ')
            on=t>tsv;pw=sf(18,'Medium').getlength('Accounting service')+20
            rr(row,(cx0-4,46,cx0+pw-4,70),'#D9F2E1' if on else '#F1F3F4',12);ImageDraw.Draw(row).text((cx0+pw/2-4,58),'Accounting service',font=sf(18,'Medium'),fill=GREEN_D if on else '#5F6368',anchor='mm')
            ImageDraw.Draw(row).text((cx0+pw+8,58),'· Open now',font=sf(18),fill='#5F6368',anchor='lm')
            booked=t>tco;bw=140;bx=w-80-bw-16;rr(row,(bx,22,bx+bw,62),GREEN if booked else '#1A73E8',20);ImageDraw.Draw(row).text((bx+bw/2,42),'Booked ✓' if booked else 'Book',font=sf(20,'Semibold'),fill='white',anchor='mm')
        else:
            dr.text((196,58),sub,font=sf(18),fill='#5F6368',anchor='lm');bw=140;bx=w-80-bw-16;rr(row,(bx,22,bx+bw,62),'#F1F3F4',20);dr=ImageDraw.Draw(row);dr.text((bx+bw/2,42),'Website',font=sf(20,'Medium'),fill='#3C4043',anchor='mm')
        return row
    for i,(nm,sub) in enumerate(FIRMS):
        u=t-(tcm+i*.1)
        if u<0:continue
        e=ease(u/.25);place(win,_row(nm,'office_building',sub),40,y0+i*rowh+rowh*ins+8*(1-e),1,e*(1-.4*ins),False)
    if ins>0:place(win,_row('Shiney.ai Accounting',None,'',True),40,y0-24*(1-ins),1,ins,False)
    bx=40+(w-80-140-16)+70;by=y0+42
    pointer_motion.motion(win,t,points=[(tact+.15,600,470),(tco-.06,bx,by),(tco+.14,bx,by),(tco+.7,bx+40,by+60)],clicks=[tco],end=tco+.9)
    e=ease((t+.09)/.32);place(im,win,70,104+22*(1-e),.96+.04*e,e,True)
    return im

# ---------------------------------------------------------------- 15. skills (split): what you already know
SKILLS=['Bookkeeping','Copywriting','Sales calls','Design','Recruiting','Legal research','Marketing','Customer support','Scheduling']
PICK=[0,1,2]
def skills(t,at):
    im=blank(W,H);c=card();d=ImageDraw.Draw(c);w,h=940,560
    tsk=at('skills','skills',2.33)-LEAD;tk=[tsk,at('skills','that',2.77)-LEAD,at('skills','know',3.15)-LEAD]   # picks on skills / that / know: ~0.4 s apart
    d.text((60,72),'Skills you already have',font=sf(36,'Semibold'),fill=INK,anchor='lm')
    x,y=60,130;f=sf(29,'Medium');centres={}
    for i,lab in enumerate(SKILLS):
        cw=f.getlength(lab)+96
        if x+cw>w-60:x=60;y+=96
        u=t-(.12+i*.13);on=any(i==PICK[k] and t>tk[k] for k in range(3));centres[i]=(x+cw/2,y+38)
        if u>0:
            s=pop(u/.26);ch=blank(round(cw)+8,76)
            rr(ch,(0,0,cw-1,75),'#EAF6EE' if on else '#F5F5F7',38,GREEN if on else '#E3E3E6',3 if on else 2)
            if on:
                k=next(k for k in range(3) if i==PICK[k]);checkmark(ch,38,38,round(15*pop((t-tk[k])/.24)),GREEN)
            else:ImageDraw.Draw(ch).ellipse((24,24,52,52),outline='#C7C7CC',width=3)
            ImageDraw.Draw(ch).text((66,38),lab,font=f,fill=INK if on else '#3A3A3C',anchor='lm')
            wob=1+.04*math.sin(clamp((t-tsk)/.3)*math.pi) if t>tsk else 1
            place(c,ch,x,y+10*(1-s),(.8+.2*s)*wob,min(1,u/.1),False)
        x+=cw+16
    # the cursor tours the chips and presses the three that get picked
    p0=(centres[PICK[0]][0]-40,centres[PICK[0]][1]+6);p1=(centres[PICK[1]][0]-40,centres[PICK[1]][1]+6);p2=(centres[PICK[2]][0]-40,centres[PICK[2]][1]+6)
    pointer_motion.motion(c,t,points=[(1.30,760,470),(tk[0]-.08,*p0),(tk[0]+.16,*p0),(tk[1]-.08,*p1),(tk[1]+.16,*p1),(tk[2]-.08,*p2),(tk[2]+.40,p2[0]+30,p2[1]+70)],clicks=tk,end=tk[2]+.6)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 16. turn (full): the shop opens
def _awning(w,h,k):
    q=2;im=blank(w*q,h*q);d=ImageDraw.Draw(im);n=9;sw=w*q/n
    for i in range(n):d.polygon([(i*sw,0),((i+1)*sw,0),((i+1)*sw-6*q,h*q*.8),(i*sw+6*q,h*q*.8)],fill=TERRA if i%2==0 else '#F6E7DF')
    for i in range(n):d.ellipse((i*sw+6*q,h*q*.6,(i+1)*sw-6*q,h*q),fill=TERRA if i%2==0 else '#F6E7DF')
    im=im.resize((w,h),Image.Resampling.LANCZOS);hh=max(2,round(h*k));return im.resize((w,hh),Image.Resampling.LANCZOS) if k<1 else im

def turn(t,at):
    im=blank(W,H);d=ImageDraw.Draw(im)
    tturn=at('turn','turn',.22)-LEAD;tinto=at('turn','into',.68)-LEAD;tai=at('turn','AI-native',1.10)-LEAD;tsv=at('turn','service',1.72)-LEAD;tbus=at('turn','business.',2.08)-LEAD
    X0,Y0,FW,FH=110,250,860,600;lit=ease((t-tinto)/.4) if t>tinto else 0;glow=pop((t-tai)/.3) if t>tai else 0
    # facade
    rr(im,(X0,Y0,X0+FW,Y0+FH),'#ECECEF',34);rr(im,(X0,Y0+FH-30,X0+FW,Y0+FH),'#DEDCD4',16)
    line(im,[(60,Y0+FH),(1020,Y0+FH)],'#DEDCD4',3)
    # windows (light on with "into")
    for wx in (X0+70,X0+FW-70-230):
        wc=(255,236,190,255) if lit>0 else (214,222,232,255);win=blank(230,200);rr(win,(0,0,229,199),wc,18,'#C9C9CE',3)
        for k in range(1,3):ImageDraw.Draw(win).line([(0,k*66),(230,k*66)],fill='#C9C9CE',width=3)
        ImageDraw.Draw(win).line([(115,0),(115,200)],fill='#C9C9CE',width=3);place(im,win,wx,Y0+190,1,1,False)
        if lit>0:
            gl=blank(330,300);ImageDraw.Draw(gl).rounded_rectangle((50,50,280,250),radius=18,fill=(255,214,120,round(110*lit)));im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(24)),(wx-50,Y0+140))
    # door with the Claude tile as the shop's mark
    dx=X0+FW/2-110;rr(im,(dx,Y0+180,dx+220,Y0+FH-30),'#1D1D1F',22);rr(im,(dx+18,Y0+200,dx+202,Y0+FH-120),'#2C2C2E',14)
    rr(im,(dx+165,Y0+380,dx+185,Y0+392),'#C9A24B',6)
    if t>tai:
        gl=blank(300,300);ImageDraw.Draw(gl).ellipse((40,40,260,260),fill=(217,119,87,round(120*glow)));im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(30)),(round(dx-40),Y0+150))
    place(im,tile_claude(120),dx+50,Y0+240,.9+.1*glow if t>tai else .9,1,True)
    # sign board
    rr(im,(X0+40,Y0+40,X0+FW-40,Y0+150),'white',22,'#DEDCD4',3);d=ImageDraw.Draw(im)
    d.text((X0+FW/2,Y0+95),'Accounting, done for you',font=sf(56,'Bold'),fill=INK,anchor='mm')
    # the awning unrolls on "service"
    ak=ease((t-tsv)/.35) if t>tsv else 0
    if ak>0:aw=_awning(FW-40,120,ak);place(im,aw,X0+20,Y0+150,1,1,True)
    # the OPEN sign flips on "business"
    op=clamp((t-tbus)/.3);sx=abs(math.cos(math.pi*op));sg=blank(200,90)
    if op<.5:rr(sg,(0,0,199,89),'#F5F5F7',16,'#C9C9CE',3);ImageDraw.Draw(sg).text((100,45),'CLOSED',font=sf(34,'Bold'),fill='#8E8E93',anchor='mm')
    else:rr(sg,(0,0,199,89),'#1E8E3E',16);ImageDraw.Draw(sg).text((100,45),'OPEN',font=sf(38,'Bold'),fill='white',anchor='mm')
    sw_=max(2,round(200*sx));sg=sg.resize((sw_,90),Image.Resampling.LANCZOS);im.alpha_composite(sg,(round(dx+110-sw_/2),Y0+FH-230))
    d=ImageDraw.Draw(im);d.line([(dx+110,Y0+FH-260),(dx+110,Y0+FH-230)],fill='#8E8E93',width=3)
    # the three chosen skills fly in through the door on "turn"
    for k,i in enumerate(PICK):
        lab=SKILLS[i];u=t-(tturn+k*.10)
        if u<0 or u>.8:continue
        p=smooth(u/.6);f=sf(26,'Medium');cw=f.getlength(lab)+56;ch=blank(round(cw),60);rr(ch,(0,0,cw-1,59),'#EAF6EE',30,GREEN,2);ImageDraw.Draw(ch).text((cw/2,30),lab,font=f,fill=INK,anchor='mm')
        x=lerp(160+k*300,dx+110-cw/2,p);y=lerp(120,Y0+300,p)-120*math.sin(p*math.pi)
        place(im,ch,x,y,1-.5*p,1-max(0,(p-.7)/.3),False)
    return im

# ---------------------------------------------------------------- 17. cta (split) --------------
def cta(t,at):
    im=blank(W,H)
    tg=at('cta','guide',1.34)-LEAD;tcomp=at('cta','completely',.62)-LEAD;tcm=at('cta','comment',3.14)-LEAD;tand=at('cta','and',3.94)-LEAD;tsend=at('cta','send',4.32)-LEAD
    tyes=at('cta','you',4.82,2)-LEAD
    obj=instagram_comment.render(t,keyword='FREE',viewer='you',type_start=tcm,type_duration=.34,post_at=tand)
    if t>tyes:                                                     # the comment gets liked on "you"
        s=pop((t-tyes)/.26);hm=blank(60,60);ImageDraw.Draw(hm).polygon([(30+16*math.sin(a)**3*28/32,30-(13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a))*28/32) for a in [i/64*2*math.pi for i in range(65)]],fill='#ED4956')
        place(obj,hm,843-30,167-30,max(.05,s),1,False)
    pointer_motion.motion(obj,t,points=[(.35,600,300),(tand-.35,813,364),(tand-.05,813,364),(tand+.4,850,300),(tyes-.05,843,167),(tyes+.12,843,167),(tyes+.6,880,120)],clicks=[tand,tyes],end=tyes+.8)
    e=ease((t+.09)/.30);place(im,obj,90,120+18*(1-e),.96+.04*e,e,True)
    # REJECTED 25 Sep 2026 ("Remove this too"): no link chip in the CTA - copy only the comment UI above. See SKILL.md rule 20.
    # the guide chip writes itself under the comments and goes blue on "send"; the plane flies off
    if t>tcomp-.2:
        u=t-(tcomp-.2);s_=pop(u/.26);w,h=700,74;ch=blank(w+200,h);sent=t>tsend
        rr(ch,(0,0,w-1,h-1),'white',37,'#0A84FF' if sent else '#E3E3E6',3 if sent else 2)
        ch.alpha_composite(emoji('📘',40),(24,17))
        label='Free guide · your AI service business';ImageDraw.Draw(ch).text((80,37),reveal(label,t-tcomp+.05,tg-tcomp+.35),font=sf(30,'Medium'),fill=INK,anchor='lm')
        fly=clamp((t-tsend-.3)/.5) if sent else 0;px,py=w-52+fly*260,37-fly*90;col='#0A84FF' if sent else '#C7C7CC';k=1+.25*math.sin(clamp((t-tsend)/.25)*math.pi) if sent else 1
        if fly<1:ImageDraw.Draw(ch).polygon([(px-16*k,py-13*k),(px+18*k,py),(px-16*k,py+13*k),(px-8*k,py)],fill=col)
        fl=6*math.sin((t-tg)*5.2) if t>tg else 0                        # gentle float once written
        place(im,ch,(W-w)/2,590+14*(1-s_)+fl,.94+.06*s_,min(1,u/.10),True)
    return im

FN={'hook':hook,'worry':worry,'hidden':hidden,'spend':spend,'alot':alot,'six':six,'services':services,'jobs':jobs,'why':why,
    'tool':tool,'done':done,'humans':humans,'next':next_,'service':service,'skills':skills,'turn':turn,'cta':cta}
def graphics(b,t,S,at):return FN[b['name']](t,at,S) if b['name'] in ('worry','hidden') else FN[b['name']](t,at)
