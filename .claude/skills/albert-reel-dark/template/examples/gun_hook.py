"""ACCEPTED (Laya reel, 21 Sep 2026 - Albert: "THIS REEL WAS SO GOOD").
Hook: the unrevealed "?" model shoots up the Jev tile.  Pattern = "tile does something physical to tile".

Reuse: swap tile_jev / tile_q for any two brand tiles, keep shot_times() tied to at() word onsets (one round per
stressed word, a burst on the run-up, the LAST round on the rival's name -> the tile breaks). Sound lives in
examples/laya_mix.py (gunshot.wav -15/-17/-19 dB + whoosh on the break). Captions: payoff word own group, big + green.

"Someone just released a free and open source version of Jev,"

No face. The official TypeSafe/Jev tile sits on the right; the ink "?" tile slides in on the left with a
pistol already levelled. One round per stressed word (released / free / open / source), then a three-round
burst across "version of", and the last round lands on "Jev": the tile breaks into three shards that fall
under gravity. Every round = muzzle flash (2 frames) + tracer + recoil + ejected brass + a hole punched in
the tile + magenta chips off the back. Holes are drawn ON the tile so they ride its jolt.

render(t, at) -> 1080x1920 RGBA in scene coordinates (UI y 120..930, captions sit below at CAPY).
`python3 examples/gun_hook.py` writes examples/gun_hook_strip.jpg.
"""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
from brand import tile_jev,tile_q,PINK

JS=360                      # Jev tile size
JX,JY=650,300               # Jev tile top-left at rest
QS=280;QX,QY=36,420         # "?" tile
GY=800                      # ground line both tiles stand on
MUZ=(QX+QS+232,QY+QS/2-47)  # muzzle tip at rest (gun levelled)
G=2600.0                    # px/s^2

# hit points inside the Jev tile (tile coordinates), spread so the holes never stack
HITS=[(100,128),(258,104),(164,246),(286,260),(76,272),(205,170),(128,66),(183,188)]

def shot_times(at):
    r=at('hook','released',.56);f=at('hook','free',1.12);o=at('hook','open',1.56);s=at('hook','source',1.78)
    v=at('hook','version',2.02);of=at('hook','of',2.30);j=at('hook','Jev,',2.50)
    L=.05
    return [r-L,f-L,o-L,s-L,v-L,(v+of)/2-L,of-L,j-L]

@lru_cache(None)
def gun():
    """Clean pistol silhouette, muzzle to the right. Canvas 300x190, grip pivot near (70,120)."""
    q=3;im=blank(300*q,190*q);d=ImageDraw.Draw(im);k=q
    ink='#111113'
    def P_(pts,fill=ink):d.polygon([(x*k,y*k) for x,y in pts],fill=fill)
    # slide + barrel
    d.rounded_rectangle((38*k,30*k,286*k,74*k),radius=9*k,fill=ink)
    d.rounded_rectangle((270*k,40*k,298*k,64*k),radius=5*k,fill='#2A2A2E')       # muzzle crown
    # frame under the slide
    P_([(52,70),(214,70),(206,96),(60,96)])
    # trigger guard
    d.rounded_rectangle((118*k,88*k,178*k,134*k),radius=17*k,outline=ink,width=9*k)
    d.line([(146*k,96*k),(140*k,118*k)],fill=ink,width=6*k)                      # trigger
    # grip, raked back
    P_([(54,84),(124,84),(108,182),(34,182)])
    d.rounded_rectangle((30*k,166*k,112*k,188*k),radius=8*k,fill=ink)
    # details: ejection port, slide serrations, sights
    d.rounded_rectangle((150*k,37*k,206*k,52*k),radius=4*k,fill='#3A3A3F')
    for i in range(5):d.line([((58+i*9)*k,38*k),((54+i*9)*k,66*k)],fill='#3A3A3F',width=3*k)
    d.rectangle((262*k,22*k,274*k,32*k),fill=ink);d.rectangle((48*k,20*k,66*k,32*k),fill=ink)
    return im.resize((300,190),Image.Resampling.LANCZOS)

def flash(size,seed):
    """Star muzzle flash: orange body, yellow middle, white core."""
    rnd=random.Random(seed);q=3;S=size*q;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2
    for col,sc in (('#FF7A1A',1.0),('#FFC933',.68),('#FFFFFF',.36)):
        pts=[];n=9
        for i in range(n*2):
            a=i/(n*2)*2*math.pi+rnd.uniform(-.08,.08)
            r=(c*sc)*(1.0 if i%2==0 else .40)*rnd.uniform(.82,1.0)
            # stretch forward (to the right)
            pts.append((c+r*math.cos(a)*(1.35 if math.cos(a)>0 else .7),c+r*math.sin(a)*.78))
        d.polygon(pts,fill=col)
    return im.resize((size,size),Image.Resampling.LANCZOS)

def hole(d,x,y,r=15):
    """Bullet hole: dark core, scorched ring, short cracks."""
    rnd=random.Random(int(x*7+y*13))
    for i in range(6):
        a=rnd.uniform(0,2*math.pi);l=rnd.uniform(r*1.5,r*2.7)
        d.line([(x+math.cos(a)*r*.8,y+math.sin(a)*r*.8),(x+math.cos(a)*l,y+math.sin(a)*l)],fill=(40,10,32,255),width=3)
    d.ellipse((x-r-5,y-r-5,x+r+5,y+r+5),fill=(150,40,118,255))
    d.ellipse((x-r,y-r,x+r,y+r),fill=(24,20,24,255))
    d.ellipse((x-r+5,y-r+4,x+r-7,y+r-8),fill=(8,8,10,255))

def holed_tile(n):
    im=tile_jev(JS).copy();a=im.getchannel('A');d=ImageDraw.Draw(im)
    for hx,hy in HITS[:n]:hole(d,hx,hy)
    im.putalpha(a);return im
_holed={}
def holed(n):
    if n not in _holed:_holed[n]=holed_tile(n)
    return _holed[n]

# three shards for the break: polygons in tile coordinates, with launch velocity and spin
SHARDS=[([(0,0),(JS,0),(JS,130),(192,184),(0,104)],(260,-520,-150)),
        ([(0,104),(192,184),(152,JS),(0,JS)],(-120,-380,120)),
        ([(192,184),(JS,130),(JS,JS),(152,JS)],(380,-300,-210))]
_sh={}
def shard(i):
    if i not in _sh:
        src=holed(len(HITS));m=Image.new('L',(JS,JS));ImageDraw.Draw(m).polygon(SHARDS[i][0],fill=255)
        im=src.copy();im.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(src.getchannel('A')),__import__('numpy').array(m))))
        _sh[i]=im
    return _sh[i]

def render(t,at):
    im=blank(W,H);d=ImageDraw.Draw(im);T=shot_times(at);fired=[s for s in T if t>=s];n=len(fired)
    last=t-fired[-1] if fired else 9;brk=T[-1];broken=t>=brk

    # ---- ground line both tiles stand on --------------------------------------------------------
    line(im,[(90,GY),(990,GY)],'#DEDCD4',3)

    # ---- "?" tile + gun ---------------------------------------------------------------------------
    e=ease((t+.10)/.42);qx=QX-260*(1-e)
    rec=math.exp(-last/.07) if last<.4 else 0          # recoil envelope per round
    qx-=10*rec
    # tile leans back a touch with each round, stands on the ground line
    place(im,tile_q(QS),qx,QY+70-QS+QS,1,1,True,rot=2.2*rec) if False else None
    tq=tile_q(QS);place(im,tq,qx,GY-QS-6,1,1,True,rot=2.0*rec)
    # gun: raised from -38deg to level while sliding in, kicks up on each round
    lift=(1-ease((t-.05)/.40))*-38
    ang=lift+13*rec
    g=gun();gx=qx+QS-96-16*rec;gy=GY-QS-6+QS/2-92
    gr=g.rotate(ang,resample=Image.Resampling.BICUBIC,expand=True,center=(70,120))
    # rotate(expand) shifts origin: compensate so the grip pivot stays put
    ox=(gr.width-g.width)/2;oy=(gr.height-g.height)/2
    im.alpha_composite(gr,(round(gx-ox),round(gy-oy)))
    # little hand-nub so the tile visibly holds the grip
    rr(im,(gx+30,gy+96,gx+118,gy+150),'#1D1D1F',22)
    mzx=gx-ox+gr.width/2+math.cos(math.radians(-ang))*(298-150)-math.sin(math.radians(-ang))*(52-95)
    mzy=gy-oy+gr.height/2+math.sin(math.radians(-ang))*(298-150)+math.cos(math.radians(-ang))*(52-95)
    # at the instant of fire the gun is level: use the level muzzle for flash + tracer so they line up
    fmx,fmy=qx+QS-96+298,GY-QS-6+QS/2-92+52

    # ---- Jev tile -----------------------------------------------------------------------------------
    jolt=math.exp(-last/.09) if last<.5 else 0
    bob=math.sin(t*5.2)*3*(0 if n else 1)
    if not broken:
        jx=JX+20*jolt;jy=GY-JS-6+bob
        place(im,holed(n),jx,jy,1,1,True,rot=-3.2*jolt*(1 if n%2 else -1))
        # label
        a=1.0
        d=ImageDraw.Draw(im);d.text((JX+JS/2+20*jolt,GY+58),'Jev',font=sf(54,'Semibold'),fill=INK,anchor='mm')
    else:
        u=t-brk
        for i,(poly,(vx,vy,w)) in enumerate(SHARDS):
            x=JX+vx*u;y=GY-JS-6+vy*u+.5*G*u*u
            place(im,shard(i),x,y,1,max(0,1-max(0,u-.22)/.40),False,rot=w*u)
        d=ImageDraw.Draw(im)
        lu=max(0,1-u/.30)
        if lu>0:
            lab=blank(200,90);ImageDraw.Draw(lab).text((100,45),'Jev',font=sf(54,'Semibold'),fill=INK,anchor='mm')
            place(im,lab,JX+JS/2-100,GY+58-45+60*u*u*8,1,lu,False,rot=-40*u)

    # ---- per-round effects -----------------------------------------------------------------------
    for k,s in enumerate(T):
        u=t-s
        if u<0:continue
        hx,hy=HITS[k];tx=JX+hx;ty=GY-JS-6+hy
        # tracer: 2 frames
        if u<.067:
            lay=blank(W,H);ImageDraw.Draw(lay).line([(fmx+40,fmy),(tx,ty)],fill=(255,214,120,220),width=7)
            ImageDraw.Draw(lay).line([(fmx+40,fmy),(tx,ty)],fill=(255,255,255,255),width=3);im.alpha_composite(lay)
        # muzzle flash: 2-3 frames, big then small
        if u<.10:
            sz=round(190*(1-u/.10*.55));fl=flash(sz,k);place(im,fl,fmx+18-sz*.30,fmy-sz/2,1,1)
        # impact spark on the tile
        if u<.10:
            sz=round(120*(1-u/.10*.5));fl=flash(sz,k+40);place(im,fl,tx-sz/2,ty-sz/2,1,.95)
        # magenta chips off the tile
        rnd=random.Random(k*31+5)
        for c in range(7):
            a=rnd.uniform(-1.15,1.15);v=rnd.uniform(420,980);sz=rnd.uniform(7,17)
            cx=tx+math.cos(a)*v*u*(1 if c%3 else -.45);cy=ty+math.sin(a)*v*u-160*u+.5*G*u*u
            op=max(0,1-u/.55)
            if op>0 and cy<900:
                ch=blank(40,40);ImageDraw.Draw(ch).polygon([(6,8),(6+sz,4),(10+sz,8+sz*.8),(4,6+sz)],fill=PINK if c%2 else '#171717')
                place(im,ch,cx-20,cy-20,1,op,False,rot=rnd.uniform(-600,600)*u)
        # brass: ejects up and back from the port
        bx=fmx-150-rnd.uniform(140,260)*u;by=fmy-30-rnd.uniform(560,GY)*u+.5*G*u*u
        if u<.75 and by<775:
            br=blank(40,40);rr(br,(8,14,32,25),'#C9A24B',4);rr(br,(8,14,14,25),'#8D6E2C',3)
            place(im,br,bx-20,by-20,1,max(0,1-u/.75),False,rot=-900*u)
    # smoke curl from the muzzle after the last round
    if broken:
        u=t-brk
        for i in range(4):
            uu=u-i*.05
            if uu>0:
                r=10+uu*70;lay=blank(W,H)
                ImageDraw.Draw(lay).ellipse((mzx+14+i*5-r,mzy-20-uu*150-r,mzx+14+i*5+r,mzy-20-uu*150+r),fill=(120,120,124,round(95*max(0,1-uu/.5))))
                im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    if last<.067:                                   # 2-frame camera kick on every round
        rnd=random.Random(n*17);out=blank(W,H);out.alpha_composite(im,(rnd.choice([-7,7]),rnd.choice([-5,5])));return out
    return im

if __name__=='__main__':
    DEF={'released':.56,'free':1.12,'open':1.56,'source':1.78,'version':2.02,'of':2.30,'Jev,':2.50}
    at=lambda n,w,d=0,nth=0:DEF.get(w,d)
    ts=[.15,.53,.60,1.12,1.80,2.30,2.47,2.62]
    sheet=Image.new('RGB',(len(ts)*360,300),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.crop((0,250,1080,1150)).resize((360,300)).convert('RGB'),(i*360,0))
    sheet.save(Path(__file__).with_name('gun_hook_strip.jpg'));print('gun_hook_strip.jpg')
