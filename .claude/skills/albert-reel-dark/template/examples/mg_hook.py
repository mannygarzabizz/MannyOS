"""Hook: Claude empties a machine gun into the Salesforce tile.  (Albert: "have Claude have a machine gun,
and full auto with bullet holes into the most well known software logo")

"AI just killed all software."

No face. The official Salesforce app icon (white tile, blue cloud) sits on the right with its name under it; the
Claude tile slides in on the left already shouldering an SMG. The gun levels during "AI just", then goes FULL AUTO
from "killed" (13 rounds/s) through "all": every round = 2-frame muzzle flash + tracer + recoil jitter + ejected brass
+ a hole punched IN the tile (drawn on the tile so it rides the jolt) + blue chips + a 2-frame camera kick. The last
round lands on "software": the tile breaks into three shards that fall under gravity and the name tumbles off.

Pattern from examples/gun_hook.py (Laya reel, accepted). Sound: mix.py stacks audio/sources/mg-round.wav per round.
render(t, at) -> 1080x1920 RGBA in scene coordinates (UI y 120..930, captions sit below at CAPY).
`python3 examples/mg_hook.py` writes examples/mg_hook_strip.jpg.
"""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
from brand import tile_salesforce,tile_claude,SF_BLUE

JS=360                      # Salesforce tile size
JX=650                      # Salesforce tile left at rest
QS=280;QX=36                # Claude tile
GY=800                      # ground line both tiles stand on
G=2600.0                    # px/s^2
RATE=.075                   # seconds between rounds (about 13 rounds/s)
BLUE=(31,189,254)

# hit points inside the Salesforce tile (tile coordinates), spread so the holes never stack
HITS=[(118,150),(250,120),(176,236),(292,250),(96,268),(214,180),(146,92),(262,196),(120,206),(200,290),(300,150),(160,150),(236,262),(90,120)]

def shot_times(at):
    """Full auto from 'killed' to 'software'; the last round is the one that breaks the tile."""
    k=at('hook','killed',.68);s=at('hook','software.',1.36);L=.05
    t0=k-L;last=s-L;T=[];x=t0
    while x<last-.045:T.append(round(x,4));x+=RATE
    T.append(round(last,4));return T

@lru_cache(None)
def gun():
    """Flat SMG silhouette, muzzle to the right. Canvas 380x190; grip pivot near (130,130)."""
    q=3;im=blank(380*q,190*q);d=ImageDraw.Draw(im);k=q;ink='#3A3A40';dk='#66666E'   # dark mode: gunmetal, not ink (ink vanishes on #0A0A0B)
    def P_(pts,fill=ink):d.polygon([(x*k,y*k) for x,y in pts],fill=fill)
    # stock (collapsible, with a cut-out) and buffer tube
    d.rounded_rectangle((6*k,58*k,80*k,72*k),radius=5*k,fill=ink)
    P_([(6,72),(26,72),(20,108),(4,108)]);d.rounded_rectangle((4*k,100*k,44*k,112*k),radius=5*k,fill=ink)
    # receiver
    d.rounded_rectangle((62*k,48*k,300*k,102*k),radius=10*k,fill=ink)
    # handguard + barrel + muzzle
    d.rounded_rectangle((250*k,56*k,332*k,94*k),radius=8*k,fill=ink)
    for i in range(4):d.rounded_rectangle(((262+i*17)*k,64*k,(272+i*17)*k,86*k),radius=3*k,fill=dk)     # vent slots
    d.rounded_rectangle((330*k,66*k,376*k,84*k),radius=4*k,fill=ink);d.rounded_rectangle((356*k,60*k,378*k,90*k),radius=5*k,fill='#2A2A2E')
    # sights, charging handle, ejection port, mag release
    d.rectangle((326*k,38*k,336*k,58*k),fill=ink);d.rectangle((90*k,34*k,112*k,50*k),fill=ink);d.rectangle((96*k,28*k,106*k,36*k),fill=ink)
    d.rounded_rectangle((176*k,58*k,236*k,74*k),radius=4*k,fill=dk);d.rounded_rectangle((130*k,36*k,166*k,48*k),radius=4*k,fill=ink)
    for i in range(5):d.line([((70+i*9)*k,56*k),((66+i*9)*k,94*k)],fill=dk,width=3*k)                       # serrations
    # pistol grip, trigger guard, trigger
    P_([(112,100),(166,100),(150,176),(96,176)]);d.rounded_rectangle((94*k,166*k,150*k,182*k),radius=7*k,fill=ink)
    d.rounded_rectangle((160*k,98*k,222*k,140*k),radius=16*k,outline=ink,width=8*k);d.line([(190*k,104*k),(184*k,126*k)],fill=ink,width=6*k)
    # magazine, curved forward
    P_([(226,100),(268,100),(258,186),(214,186)]);d.rounded_rectangle((214*k,178*k,262*k,189*k),radius=4*k,fill=dk)
    for i in range(4):d.line([((232+i*8)*k,110*k),((226+i*8)*k,176*k)],fill=dk,width=2*k)
    return im.resize((380,190),Image.Resampling.LANCZOS)

def flash(size,seed):
    """Star muzzle flash: orange body, yellow middle, white core, stretched forward."""
    rnd=random.Random(seed);q=3;S=size*q;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2
    for col,sc in (('#FF7A1A',1.0),('#FFC933',.68),('#FFFFFF',.36)):
        pts=[];n=9
        for i in range(n*2):
            a=i/(n*2)*2*math.pi+rnd.uniform(-.08,.08)
            r=(c*sc)*(1.0 if i%2==0 else .40)*rnd.uniform(.82,1.0)
            pts.append((c+r*math.cos(a)*(1.35 if math.cos(a)>0 else .7),c+r*math.sin(a)*.78))
        d.polygon(pts,fill=col)
    return im.resize((size,size),Image.Resampling.LANCZOS)

def hole(d,x,y,r=14):
    """Bullet hole: dark core, scorched steel-blue ring, short cracks (reads on the white ground and on the cloud)."""
    rnd=random.Random(int(x*7+y*13))
    for i in range(6):
        a=rnd.uniform(0,2*math.pi);l=rnd.uniform(r*1.5,r*2.7)
        d.line([(x+math.cos(a)*r*.8,y+math.sin(a)*r*.8),(x+math.cos(a)*l,y+math.sin(a)*l)],fill=(30,44,60,255),width=3)
    d.ellipse((x-r-5,y-r-5,x+r+5,y+r+5),fill=(72,104,134,255))
    d.ellipse((x-r,y-r,x+r,y+r),fill=(24,26,30,255))
    d.ellipse((x-r+5,y-r+4,x+r-7,y+r-8),fill=(8,8,10,255))

def holed_tile(n):
    im=tile_salesforce(JS).copy();a=im.getchannel('A');d=ImageDraw.Draw(im)
    for hx,hy in HITS[:n]:hole(d,hx,hy)
    im.putalpha(a);return im
_holed={}
def holed(n):
    n=min(n,len(HITS))
    if n not in _holed:_holed[n]=holed_tile(n)
    return _holed[n]

# three shards for the break: polygons in tile coordinates, with launch velocity and spin
SHARDS=[([(0,0),(JS,0),(JS,130),(192,184),(0,104)],(260,-520,-150)),
        ([(0,104),(192,184),(152,JS),(0,JS)],(-120,-380,120)),
        ([(192,184),(JS,130),(JS,JS),(152,JS)],(380,-300,-210))]
_sh={}
def shard(i):
    if i not in _sh:
        import numpy as np
        src=holed(len(HITS));m=Image.new('L',(JS,JS));ImageDraw.Draw(m).polygon(SHARDS[i][0],fill=255)
        im=src.copy();im.putalpha(Image.fromarray(np.minimum(np.array(src.getchannel('A')),np.array(m))))
        _sh[i]=im
    return _sh[i]

def render(t,at):
    im=blank(W,H);d=ImageDraw.Draw(im);T=shot_times(at);fired=[s for s in T if t>=s];n=len(fired)
    last=t-fired[-1] if fired else 9;brk=T[-1];broken=t>=brk;firing=T[0]<=t<brk+.03

    # ---- ground line both tiles stand on --------------------------------------------------------
    line(im,[(90,GY),(990,GY)],LINE,3)

    # ---- Claude tile + gun ----------------------------------------------------------------------
    e=ease((t+.10)/.42);qx=QX-260*(1-e)
    rec=math.exp(-last/.06) if last<.4 else 0            # recoil envelope per round (fast, so full auto reads as jitter)
    qx-=8*rec
    tq=tile_claude(QS);place(im,tq,qx,GY-QS-6,1,1,True,rot=1.6*rec)
    lift=(1-ease((t-.05)/.40))*-38                        # raised from -38deg to level while sliding in
    ang=lift+6*rec+(1.2*math.sin(t*90) if firing else 0)  # constant shudder while the burst runs
    g=gun();gx=qx+QS-130-10*rec;gy=GY-6-QS/2-76
    gr=g.rotate(ang,resample=Image.Resampling.BICUBIC,expand=True,center=(130,130))
    ox=(gr.width-g.width)/2;oy=(gr.height-g.height)/2
    im.alpha_composite(gr,(round(gx-ox),round(gy-oy)))
    rr(im,(gx+96,gy+104,gx+176,gy+156),TERRA,22)          # Claude's hand on the grip
    fmx,fmy=qx+QS-130+376,GY-6-QS/2-76+74                 # level muzzle for flash + tracer

    # ---- Salesforce tile ------------------------------------------------------------------------
    jolt=math.exp(-last/.08) if last<.5 else 0
    bob=math.sin(t*5.2)*3*(0 if n else 1)
    if not broken:
        jx=JX+16*jolt;jy=GY-JS-6+bob
        place(im,holed(n),jx,jy,1,1,True,rot=-2.6*jolt*(1 if n%2 else -1))
        d=ImageDraw.Draw(im);d.text((JX+JS/2+16*jolt,GY+58),'Salesforce',font=sf(54,'Semibold'),fill=INK,anchor='mm')
    else:
        u=t-brk
        for i,(poly,(vx,vy,w)) in enumerate(SHARDS):
            x=JX+vx*u;y=GY-JS-6+vy*u+.5*G*u*u
            place(im,shard(i),x,y,1,max(0,1-max(0,u-.22)/.40),False,rot=w*u)
        lu=max(0,1-u/.30)
        if lu>0:
            lab=blank(360,90);ImageDraw.Draw(lab).text((180,45),'Salesforce',font=sf(54,'Semibold'),fill=INK,anchor='mm')
            place(im,lab,JX+JS/2-180,GY+58-45+60*u*u*8,1,lu,False,rot=-40*u)

    # ---- per-round effects ----------------------------------------------------------------------
    for k,s in enumerate(T):
        u=t-s
        if u<0:continue
        hx,hy=HITS[k%len(HITS)];tx=JX+hx;ty=GY-JS-6+hy
        if u<.067:                                        # tracer: 2 frames
            lay=blank(W,H);ImageDraw.Draw(lay).line([(fmx+40,fmy),(tx,ty)],fill=(255,214,120,220),width=7)
            ImageDraw.Draw(lay).line([(fmx+40,fmy),(tx,ty)],fill=(255,255,255,255),width=3);im.alpha_composite(lay)
        if u<.09:                                         # muzzle flash: 2-3 frames, big then small
            sz=round(200*(1-u/.09*.5));fl=flash(sz,k);place(im,fl,fmx+18-sz*.30,fmy-sz/2,1,1)
        if u<.09:                                         # impact spark on the tile
            sz=round(120*(1-u/.09*.5));fl=flash(sz,k+40);place(im,fl,tx-sz/2,ty-sz/2,1,.95)
        rnd=random.Random(k*31+5)
        for c in range(6):                                # blue + white chips off the tile
            a=rnd.uniform(-1.15,1.15);v=rnd.uniform(420,980);sz=rnd.uniform(7,17)
            cx=tx+math.cos(a)*v*u*(1 if c%3 else -.45);cy=ty+math.sin(a)*v*u-160*u+.5*G*u*u
            op=max(0,1-u/.55)
            if op>0 and cy<900:
                ch=blank(40,40);ImageDraw.Draw(ch).polygon([(6,8),(6+sz,4),(10+sz,8+sz*.8),(4,6+sz)],fill=BLUE if c%2 else '#F2F2F5',outline='#C7C7CC' if not c%2 else None)
                place(im,ch,cx-20,cy-20,1,op,False,rot=rnd.uniform(-600,600)*u)
        bx=fmx-190-rnd.uniform(120,260)*u;by=fmy-30-rnd.uniform(520,GY)*u+.5*G*u*u    # brass ejects up and back
        if u<.75 and by<775:
            br=blank(40,40);rr(br,(8,14,32,25),'#C9A24B',4);rr(br,(8,14,14,25),'#8D6E2C',3)
            place(im,br,bx-20,by-20,1,max(0,1-u/.75),False,rot=-900*u)
    if broken:                                            # smoke curl from the muzzle after the last round
        u=t-brk
        for i in range(4):
            uu=u-i*.05
            if uu>0:
                r=10+uu*70;lay=blank(W,H)
                ImageDraw.Draw(lay).ellipse((fmx+14+i*5-r,fmy-20-uu*150-r,fmx+14+i*5+r,fmy-20-uu*150+r),fill=(120,120,124,round(95*max(0,1-uu/.5))))
                im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    if last<.067:                                         # 2-frame camera kick on every round
        rnd=random.Random(n*17);out=blank(W,H);out.alpha_composite(im,(rnd.choice([-7,7]),rnd.choice([-5,5])));return out
    return im

if __name__=='__main__':
    DEF={'killed':.68,'software.':1.36}
    at=lambda n,w,d=0,nth=0:DEF.get(w,d)
    ts=[.12,.45,.66,.82,1.00,1.20,1.34,1.55]
    sheet=Image.new('RGB',(4*540,2*450),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.crop((0,250,1080,1150)).resize((540,450)).convert('RGB'),((i%4)*540,(i//4)*450))
    sheet.save(Path(__file__).with_name('mg_hook_strip.jpg'));print('mg_hook_strip.jpg')
