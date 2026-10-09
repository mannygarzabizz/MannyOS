"""next beat: Claude shoots up a wall of SaaS icons.  (Albert: "Have Claude shoot again. But this time on a bunch of
saas icons like salesforce notion etc.")

"The next billion-dollar companies won't be AI software companies."

Claude slides in on the left with the SMG (same prop as the hook); six official app icons (Salesforce, Notion, Slack,
HubSpot, Zoom, Dropbox) stack into a 3x2 wall on "billion-dollar companies". Full auto from "won't": three rounds per
tile, sweeping the wall left->right and top->bottom; a tile breaks into shards on its third round, and the last tile
breaks on "companies". Gun aims at each target; every round = flash + tracer + hole on the tile + chips + brass +
camera kick. Reuses gun/flash/hole from parts/hook.py.
"""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from draw import *
from brand import tile_claude,tile_app
import numpy as np
from mg_hook import gun,flash,hole,RATE
def pop(v):return spring(max(0,min(1,v)))

APPS=['Salesforce','Notion','Slack','HubSpot','Zoom','Dropbox']
TS=150;COLS=[540,720,900];ROWS=[464,644];GY=800;QS=240;QX=30;G=2600.0
POS=[(COLS[i%3],ROWS[i//3]) for i in range(6)]
HITS=[(46,52),(104,92),(74,116)]                      # three hit points per tile

def shot_times(at):
    """Full auto from "won't" to "companies": 18 rounds, three per tile; the last one breaks the last tile."""
    a=at('next',"won't",1.39)-.05;b=at('next','companies',2.73,1)-.05
    n=6*3;return [a+(b-a)*k/(n-1) for k in range(n)]
def break_times(at):
    T=shot_times(at);return [T[3*k+2] for k in range(6)]

@lru_cache(None)
def holed(app,n):
    im=tile_app(app,TS).copy();a=im.getchannel('A');d=ImageDraw.Draw(im)
    for hx,hy in HITS[:n]:hole(d,hx,hy,11)
    im.putalpha(a);return im
SHARDS=[([(0,0),(TS,0),(TS,55),(80,76),(0,44)],(240,-520,-160)),([(0,44),(80,76),(64,TS),(0,TS)],(-140,-360,130)),([(80,76),(TS,55),(TS,TS),(64,TS)],(360,-300,-220))]
@lru_cache(None)
def shard(app,i):
    src=holed(app,3);m=Image.new('L',(TS,TS));ImageDraw.Draw(m).polygon(SHARDS[i][0],fill=255)
    im=src.copy();im.putalpha(Image.fromarray(np.minimum(np.array(src.getchannel('A')),np.array(m))));return im

def render(t,at):
    im=blank(W,H);T=shot_times(at);BR=break_times(at);fired=[s for s in T if t>=s];n=len(fired);last=t-fired[-1] if fired else 9
    tbd=at('next','billion-dollar',.33)-.13;firing=T[0]<=t<T[-1]+.03
    line(im,[(90,GY),(990,GY)],'#DEDCD4',3)
    # ---- Claude + gun (aims at the current target) ----------------------------------------------
    e=ease((t+.10)/.42);qx=QX-260*(1-e);rec=math.exp(-last/.06) if last<.4 else 0;qx-=8*rec
    place(im,tile_claude(QS),qx,GY-QS-6,1,1,True,rot=1.6*rec)
    lift=(1-ease((t-.05)/.40))*-38
    k=min(n,len(T))-1 if n else 0;tx0,ty0=POS[min(5,k//3)];aimx,aimy=tx0+HITS[k%3][0],ty0+HITS[k%3][1]
    gx=qx+QS-130-10*rec;gy=GY-6-QS/2-76;px,py=gx+130,gy+130
    aim=-math.degrees(math.atan2(aimy-py,aimx-px)) if n else 0
    ang=lift+aim*ease((t-(T[0]-.25))/.2)+6*rec+(1.2*math.sin(t*90) if firing else 0)
    g=gun();gr=g.rotate(ang,resample=Image.Resampling.BICUBIC,expand=True,center=(130,130));ox=(gr.width-g.width)/2;oy=(gr.height-g.height)/2
    im.alpha_composite(gr,(round(gx-ox),round(gy-oy)));rr(im,(gx+96,gy+104,gx+176,gy+156),TERRA,22)
    a=math.radians(ang);mvx,mvy=376-130,74-130;fmx=px+mvx*math.cos(a)+mvy*math.sin(a);fmy=py-mvx*math.sin(a)+mvy*math.cos(a)
    # ---- the wall of SaaS tiles -------------------------------------------------------------------
    for i,app in enumerate(APPS):
        x,y=POS[i];u=t-(tbd+i*.08)
        if u<0:continue
        hits=sum(1 for k2 in range(3) if t>=T[3*i+k2]);broken=t>=BR[i]
        if not broken:
            lh=t-T[3*i+hits-1] if hits else 9;jolt=math.exp(-lh/.08) if lh<.5 else 0
            place(im,holed(app,hits),x+14*jolt,y-(60*(1-ease(u/.22))),.7+.3*pop(u/.28) if u<.5 else 1,min(1,u*9),True,rot=-2.4*jolt*(1 if hits%2 else -1))
        else:
            ub=t-BR[i]
            for j,(poly,(vx,vy,w)) in enumerate(SHARDS):
                place(im,shard(app,j),x+vx*ub,y+vy*ub+.5*G*ub*ub,1,max(0,1-max(0,ub-.22)/.40),False,rot=w*ub)
    # ---- per-round effects ------------------------------------------------------------------------
    for k,s in enumerate(T):
        u=t-s
        if u<0:continue
        x,y=POS[k//3];hx,hy=HITS[k%3];tx,ty=x+hx,y+hy
        if u<.067:
            lay=blank(W,H);ImageDraw.Draw(lay).line([(fmx+30,fmy),(tx,ty)],fill=(255,214,120,220),width=7);ImageDraw.Draw(lay).line([(fmx+30,fmy),(tx,ty)],fill=(255,255,255,255),width=3);im.alpha_composite(lay)
        if u<.09:
            sz=round(190*(1-u/.09*.5));fl=flash(sz,k);place(im,fl,fmx+14-sz*.30,fmy-sz/2,1,1)
            sz2=round(110*(1-u/.09*.5));fl2=flash(sz2,k+40);place(im,fl2,tx-sz2/2,ty-sz2/2,1,.95)
        rnd=random.Random(k*31+5)
        for c in range(5):
            a2=rnd.uniform(-1.15,1.15);v=rnd.uniform(420,980);sz=rnd.uniform(7,15)
            cx=tx+math.cos(a2)*v*u*(1 if c%3 else -.45);cy=ty+math.sin(a2)*v*u-160*u+.5*G*u*u;op=max(0,1-u/.55)
            if op>0 and cy<900:
                ch=blank(40,40);ImageDraw.Draw(ch).polygon([(6,8),(6+sz,4),(10+sz,8+sz*.8),(4,6+sz)],fill='#F2F2F5' if c%2 else '#8E8E93');place(im,ch,cx-20,cy-20,1,op,False,rot=rnd.uniform(-600,600)*u)
        bx=fmx-190-rnd.uniform(120,260)*u;by=fmy-30-rnd.uniform(520,GY)*u+.5*G*u*u
        if u<.75 and by<775:
            br=blank(40,40);rr(br,(8,14,32,25),'#C9A24B',4);rr(br,(8,14,14,25),'#8D6E2C',3);place(im,br,bx-20,by-20,1,max(0,1-u/.75),False,rot=-900*u)
    if t>=T[-1]:
        u=t-T[-1]
        for i in range(4):
            uu=u-i*.05
            if uu>0:
                r=10+uu*70;lay=blank(W,H);ImageDraw.Draw(lay).ellipse((fmx+14+i*5-r,fmy-20-uu*150-r,fmx+14+i*5+r,fmy-20-uu*150+r),fill=(120,120,124,round(95*max(0,1-uu/.5))));im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    if last<.067:
        rnd=random.Random(n*17);out=blank(W,H);out.alpha_composite(im,(rnd.choice([-7,7]),rnd.choice([-5,5])));return out
    return im

if __name__=='__main__':
    DEF={"won't":1.39,'billion-dollar':.33};DEF2={('companies',1):2.73}
    def at(n,w,d=0,nth=0):return DEF2.get((w,nth),DEF.get(w,d))
    ts=[.15,.5,.9,1.4,1.7,2.0,2.4,2.75];sheet=Image.new('RGB',(4*540,2*450),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.crop((0,250,1080,1150)).resize((540,450)).convert('RGB'),((i%4)*540,(i//4)*450))
    sheet.save(Path(__file__).with_name('shootout_strip.jpg'));print('shootout_strip.jpg')
