"""Hook: Dario fires a bazooka at Sam.  (Albert, 23 Sep 2026: "an image of Dario on the left, and an image of Sam
Altman on the right. Inside square boxes. Claude icon on Dario and ChatGPT icon on Sam. Take one of the gun animations
we have used previously and include a bazooka instead. Have left Dario shoot right Sam. It should create an explosion
that takes the entire screen, as a clean transition."  v2: "Make him actually hold the bazooka, make it look better,
higher res, more engaging.")

"Claude just killed Astra."

No face. Two 380 px square photo boxes (Wikimedia Commons, CC BY 2.0: Dario Amodei 2023 by the UK Prime Minister's
Office; Sam Altman TechCrunch SF 2019 by TechCrunch) slide in from the sides, names under them, the Claude / ChatGPT app
tiles as corner badges. Dario's box HOLDS the launcher: two navy sleeves (his suit) reach out of the box, a hand on the
pistol grip and one on the forward grip, the tube across his chest below the chin (never across the face). The launcher
is drawn at 4x with shading (cylinder gradient on the tube, wooden heat guards, olive warhead with an ochre nose, optical
sight with a glint, sling swivels). It levels during "Claude just", fires on "killed" (backblast + muzzle flash + recoil +
launch sound), the rocket crosses on a smoke trail and hits Sam's box on "Astra": the box breaks into shards and a
fireball grows from the impact until it fills the whole 1080x1920 frame by the end of the beat. The next beat calls
explosion() with continued time so the fireball cools to smoke and clears fast (gone ~0.43 s in).

render(t, at) -> 1080x1920 RGBA in scene coordinates.  `python3 parts/bazooka.py` writes review/bazooka_strip.jpg + detail.
"""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
from brand import tile_claude,tile_app
import numpy as np
def clamp(v):return max(0,min(1,v))

BS=380                       # photo box size
DX,SX=20,680                 # box lefts (Dario, Sam)
BY=300                       # box top
GY=BY+BS                     # ground under the boxes
G=2600.0
FIRE_LEAD=.05
FLIGHT=.26
NAVY=(30,42,72);NAVY_L=(52,68,108);SKIN=(232,190,160);SKIN_D=(196,146,116)
PVX,PVY=200,95               # launcher pivot (pistol grip) in launcher coords

def times(at):
    fire=at('hook','killed',.60)-FIRE_LEAD
    hit=at('hook','Astra',.94)-FIRE_LEAD
    if hit-fire<FLIGHT:fire=hit-FLIGHT
    return fire,hit

@lru_cache(None)
def photo_box(who,size=BS):
    src={'dario':'assets/people/dario-sq.jpg','sam':'assets/people/sam-sq.jpg'}[who]
    im=Image.open(P/src).convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
    m=Image.new('L',(size,size));ImageDraw.Draw(m).rounded_rectangle((0,0,size-1,size-1),18,fill=255);im.putalpha(m)
    ring=blank(size,size);ImageDraw.Draw(ring).rounded_rectangle((0,0,size-1,size-1),18,outline=(0,0,0,40),width=2);im.alpha_composite(ring)
    return im

def _l3(a,b,c,u):
    if u<.5:v=u/.5;return tuple(round(a[i]+(b[i]-a[i])*v) for i in range(3))
    v=(u-.5)/.5;return tuple(round(b[i]+(c[i]-b[i])*v) for i in range(3))
def _grad_shape(im,poly_or_box,c_top,c_mid,c_bot,r=0,k=4):
    """Vertical 3-stop gradient clipped to a rounded rect (box) or a polygon, all in logical coords x k."""
    if isinstance(poly_or_box[0],tuple):pts=[(x*k,y*k) for x,y in poly_or_box];xs=[p[0] for p in pts];ys=[p[1] for p in pts];x0,y0,x1,y1=min(xs),min(ys),max(xs),max(ys)
    else:x0,y0,x1,y1=[v*k for v in poly_or_box];pts=None
    w,h=int(x1-x0)+1,int(y1-y0)+1;g=blank(w,h);gd=ImageDraw.Draw(g)
    for yy in range(h):gd.line([(0,yy),(w,yy)],fill=_l3(c_top,c_mid,c_bot,yy/max(1,h-1)))
    m=Image.new('L',(w,h))
    if pts:ImageDraw.Draw(m).polygon([(x-x0,y-y0) for x,y in pts],fill=255)
    else:ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r*k,fill=255)
    g.putalpha(m);im.alpha_composite(g,(int(x0),int(y0)))

@lru_cache(None)
def bazooka():
    """RPG-7-style launcher with shading, muzzle to the right. Logical canvas 520x150 drawn at 4x; pivot (200,95); muzzle (516,70)."""
    k=4;im=blank(520*k,150*k);d=ImageDraw.Draw(im)
    _grad_shape(im,[(60,50),(60,90),(6,104),(6,36)],(78,78,88),(40,40,46),(12,12,15),0,k)          # rear venturi
    _grad_shape(im,(58,50,404,90),(84,84,94),(42,42,48),(12,12,15),9,k)                            # tube
    d.line([(70*k,56*k),(398*k,56*k)],fill=(120,120,132,140),width=2*k)
    for x in (88,120):d.rounded_rectangle((x*k,46*k,(x+8)*k,94*k),radius=2*k,fill=(20,20,24))
    _grad_shape(im,(150,52,250,88),(150,104,64),(104,68,40),(58,36,22),6,k)                        # wooden heat guards
    _grad_shape(im,(286,52,322,88),(150,104,64),(104,68,40),(58,36,22),6,k)
    for x in (165,185,205,225):d.line([(x*k,56*k),(x*k,84*k)],fill=(70,44,26,120),width=k)
    d.rectangle((262*k,28*k,278*k,52*k),fill=(22,22,26));_grad_shape(im,(236,18,300,34),(74,74,84),(40,40,46),(16,16,19),4,k)   # optical sight
    d.ellipse((240*k,21*k,250*k,31*k),fill=(120,170,220));d.ellipse((242*k,23*k,246*k,27*k),fill=(220,240,255))
    _grad_shape(im,[(190,90),(230,90),(220,142),(178,142)],(48,48,54),(26,26,30),(10,10,12),0,k)    # pistol grip
    d.rounded_rectangle((176*k,134*k,222*k,148*k),radius=5*k,fill=(30,30,34))
    d.rounded_rectangle((232*k,92*k,292*k,118*k),radius=12*k,outline=(22,22,26),width=7*k);d.line([(257*k,98*k),(252*k,114*k)],fill=(22,22,26),width=5*k)
    _grad_shape(im,[(330,90),(368,90),(362,126),(324,126)],(48,48,54),(26,26,30),(10,10,12),0,k)    # forward grip
    for x in (100,380):d.ellipse(((x-5)*k,88*k,(x+5)*k,98*k),outline=(90,90,100),width=2*k)        # sling swivels
    _grad_shape(im,[(392,42),(462,54),(462,86),(392,98)],(120,150,104),(70,98,64),(34,52,32),0,k)   # warhead
    _grad_shape(im,[(462,54),(516,70),(462,86)],(214,172,90),(160,116,50),(96,66,26),0,k)          # ochre nose
    d.rectangle((392*k,38*k,404*k,102*k),fill=(40,40,46));d.line([(396*k,50*k),(456*k,58*k)],fill=(170,200,150,150),width=2*k)
    d.ellipse((456*k,58*k,470*k,82*k),fill=(50,70,46))
    return im.resize((520,150),Image.Resampling.LANCZOS)

@lru_cache(None)
def rocket():
    k=4;im=blank(150*k,50*k);d=ImageDraw.Draw(im)
    _grad_shape(im,[(0,17),(60,11),(60,39),(0,33)],(96,96,108),(58,58,66),(24,24,28),0,k)
    _grad_shape(im,[(60,8),(120,16),(120,34),(60,42)],(120,150,104),(70,98,64),(34,52,32),0,k)
    _grad_shape(im,[(120,16),(148,25),(120,34)],(214,172,90),(160,116,50),(96,66,26),0,k)
    d.polygon([(0,18*k),(-14*k,4*k),(16*k,18*k)],fill=(60,60,68));d.polygon([(0,32*k),(-14*k,46*k),(16*k,32*k)],fill=(40,40,46))
    return im.resize((150,50),Image.Resampling.LANCZOS)

def _bez(p0,p1,p2,n=32):return [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in np.linspace(0,1,n)]
def arm(im,p0,p2,bend,hand_r=16):
    """A suit sleeve from the box edge p0 to the grip p2 (quadratic bend), with a hand at the end."""
    p1=((p0[0]+p2[0])/2+bend[0],(p0[1]+p2[1])/2+bend[1]);pts=_bez(p0,p1,p2)
    line(im,pts,NAVY,28);line(im,pts[:-2],NAVY_L,9)
    d=ImageDraw.Draw(im);x,y=p2;d.ellipse((x-hand_r,y-hand_r,x+hand_r,y+hand_r),fill=SKIN,outline=SKIN_D,width=3)
    d.ellipse((x-hand_r*.55,y-hand_r*.2,x+hand_r*.15,y+hand_r*.55),fill=SKIN_D)

def flash(size,seed,stretch=1.35):
    rnd=random.Random(seed);q=3;S=size*q;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2
    for col,sc in (('#FF7A1A',1.0),('#FFC933',.68),('#FFFFFF',.36)):
        pts=[];n=10
        for i in range(n*2):
            a=i/(n*2)*2*math.pi+rnd.uniform(-.08,.08);r=(c*sc)*(1.0 if i%2==0 else .42)*rnd.uniform(.82,1.0)
            pts.append((c+r*math.cos(a)*(stretch if math.cos(a)>0 else .7),c+r*math.sin(a)*.78))
        d.polygon(pts,fill=col)
    return im.resize((size,size),Image.Resampling.LANCZOS)

_k=BS/360
SHARDS=[([(0,0),(BS,0),(BS,140*_k),(200*_k,190*_k),(0,110*_k)],(520,-700,-190)),
        ([(0,110*_k),(200*_k,190*_k),(160*_k,BS),(0,BS)],(-260,-420,150)),
        ([(200*_k,190*_k),(BS,140*_k),(BS,BS),(160*_k,BS)],(720,-380,-260)),
        ([(120*_k,0),(240*_k,0),(200*_k,190*_k),(140*_k,150*_k)],(180,-900,320))]
@lru_cache(None)
def shard(i):
    src=photo_box('sam');m=Image.new('L',(BS,BS));ImageDraw.Draw(m).polygon(SHARDS[i][0],fill=255)
    im=src.copy();im.putalpha(Image.fromarray(np.minimum(np.array(src.getchannel('A')),np.array(m))));return im

@lru_cache(None)
def _blob(seed):
    rnd=random.Random(seed);return [(rnd.uniform(0,2*math.pi),rnd.uniform(.55,1.0),rnd.uniform(.35,.6)) for _ in range(7)]

def explosion(im,u,cx=SX+BS/2,cy=BY+BS/2):
    """Fireball centred on the impact, drawn at 1/4 resolution and blurred. u = seconds since impact.
    0-.42 s: grows to cover the whole frame; .42-.62 s cools to grey smoke; gone by .87 s."""
    if u<0 or u>.9:return
    q=4;w,h=im.width//q,im.height//q;lay=blank(w,h);d=ImageDraw.Draw(lay)
    R=1900*smooth(u/.42);cool=clamp((u-.42)/.20);fade=1-clamp((u-.52)/.34)
    def col(hot,smoke):return tuple(round(lerp(a,b,cool)) for a,b in zip(hot,smoke))
    rings=[(1.00,col((70,44,34),(120,118,116))),(.82,col((255,106,0),(150,148,146))),(.62,col((255,178,40),(176,174,172))),(.40,col((255,236,150),(200,198,196))),(.22,col((255,255,255),(214,212,210)))]
    for k,(sc,c) in enumerate(rings):
        a=round(255*fade*(1 if k else .96))
        for (ang,rad,ecc) in _blob(k*11+3):
            r=R*sc*rad/q;ox=math.cos(ang)*R*sc*.28/q;oy=math.sin(ang)*R*sc*.28/q
            d.ellipse((cx/q+ox-r,cy/q+oy-r*(.85+ecc*.3),cx/q+ox+r,cy/q+oy+r*(.85+ecc*.3)),fill=c+(a,))
        r=R*sc/q;d.ellipse((cx/q-r,cy/q-r*.92,cx/q+r,cy/q+r*.92),fill=c+(a,))
    lay=lay.filter(ImageFilter.GaussianBlur(3+6*cool)).resize(im.size,Image.Resampling.BILINEAR)
    im.alpha_composite(lay)
    if u<.30:
        r=200+2200*ease(u/.30);ring=blank(im.width,im.height);ImageDraw.Draw(ring).ellipse((cx-r,cy-r*.9,cx+r,cy+r*.9),outline=(255,255,255,round(200*(1-u/.30))),width=round(26*(1-u/.30))+3)
        im.alpha_composite(ring.filter(ImageFilter.GaussianBlur(4)))
    if u<.16:
        fl=Image.new('RGBA',im.size,(255,250,235,round(235*(1-u/.16))));im.alpha_composite(fl)

def _rot(px,py,dx_,dy_,a):return px+dx_*math.cos(a)+dy_*math.sin(a),py-dx_*math.sin(a)+dy_*math.cos(a)

def render(t,at):
    im=blank(W,H);fire,hit=times(at)
    e=ease((t+.18)/.36);dx=DX-520*(1-e);sx=SX+520*(1-e)
    u=t-hit;hitnow=u>=0
    kick=(math.exp(-u/.10)*14 if 0<=u<.5 else 0);rec=(math.exp(-(t-fire)/.07) if 0<=t-fire<.5 else 0)
    line(im,[(20,GY+8),(1060,GY+8)],'#DEDCD4',3)
    # ---- Dario: box, badge, then the launcher held by two sleeves out of the box
    rx=dx-10*rec
    place(im,photo_box('dario'),rx,BY,1,1,True,rot=1.2*rec)
    ImageDraw.Draw(im).text((rx+BS/2,GY+62),'Dario Amodei',font=sf(44,'Semibold'),fill=INK,anchor='mm')
    place(im,tile_claude(116),rx+BS-76,BY-40,1,1,True)                    # badge on the top-right corner, clear of the arms
    bz=bazooka();lift=(1-ease((t-.02)/.42))*-22;ang=lift+7*rec;a=math.radians(ang)
    bx,by=rx+BS*.60,BY+BS*.83                             # grip pivot at chest height, below the chin
    grip_rear=_rot(bx,by,0,22,a);grip_front=_rot(bx,by,345-PVX,112-PVY,a)
    arm(im,(rx+BS-8,BY+BS*.68),grip_rear,(30,40))
    br=bz.rotate(ang,resample=Image.Resampling.BICUBIC,expand=True,center=(PVX,PVY));ox=(br.width-bz.width)/2;oy=(br.height-bz.height)/2
    im.alpha_composite(br,(round(bx-PVX-ox),round(by-PVY-oy)))
    arm(im,(rx+BS-8,BY+BS*.86),grip_front,(50,30))
    mx,my=_rot(bx,by,516-PVX,70-PVY,a);rx_,ry_=_rot(bx,by,8-PVX,70-PVY,a)
    # ---- Sam
    tx_,ty_=SX+BS/2,BY+BS/2
    if not hitnow:
        bob=math.sin(t*5.5)*3
        place(im,photo_box('sam'),sx,BY+bob,1,1,True)
        ImageDraw.Draw(im).text((sx+BS/2,GY+62),'Sam Altman',font=sf(44,'Semibold'),fill=INK,anchor='mm')
        place(im,tile_app('ChatGPT-app',116),sx+BS-76,BY+BS-76+bob,1,1,True)
    else:
        for i,(poly,(vx,vy,w)) in enumerate(SHARDS):
            x=SX+vx*u;y=BY+vy*u+.5*G*u*u
            place(im,shard(i),x,y,1,max(0,1-max(0,u-.25)/.35),False,rot=w*u)
        lu=max(0,1-u/.30)
        if lu>0:
            lab=blank(380,90);ImageDraw.Draw(lab).text((190,45),'Sam Altman',font=sf(44,'Semibold'),fill=INK,anchor='mm')
            place(im,lab,SX+BS/2-190,GY+62-45+60*u*u*8,1,lu,False,rot=-40*u)
        place(im,tile_app('ChatGPT-app',116),SX+BS-76+300*u,BY+BS-76-500*u+.5*G*u*u,1,max(0,1-u/.5),False,rot=-520*u)
    # ---- launch: backblast + muzzle flash + rocket on a smoke trail
    f=t-fire
    if 0<=f<FLIGHT+.02:
        if f<.10:
            sz=round(260*(1-f/.10*.5));place(im,flash(sz,1),mx+10-sz*.3,my-sz/2,1,1)
            bb=flash(round(sz*.9),2).transpose(Image.Transpose.FLIP_LEFT_RIGHT);place(im,bb,rx_-sz*.6,ry_-sz*.45,1,.9)
        p=clamp(f/FLIGHT);rxp=mx+(SX+40-mx)*p;ryp=my+(ty_-my)*p
        for k in range(10):
            pp=p-k*.09
            if pp<0:continue
            px=mx+(SX+40-mx)*pp;py=my+(ty_-my)*pp;age=(p-pp)*FLIGHT;r=10+age*140
            sm=blank(round(r*2+4),round(r*2+4));ImageDraw.Draw(sm).ellipse((2,2,r*2+2,r*2+2),fill=(150,150,154,round(150*max(0,1-age/.5))));im.alpha_composite(sm.filter(ImageFilter.GaussianBlur(3)),(round(px-r),round(py-r-age*40)))
        rk=rocket().rotate(math.degrees(math.atan2(-(ty_-my),SX+40-mx)),resample=Image.Resampling.BICUBIC,expand=True)
        fl=flash(60,5);place(im,fl,rxp-70,ryp-30,1,1);im.alpha_composite(rk,(round(rxp-rk.width/2+40),round(ryp-rk.height/2)))
    # ---- impact: chips, then the fireball that takes the whole frame
    if hitnow:
        rnd=random.Random(9)
        for c in range(16):
            a_=rnd.uniform(-1.3,1.3);v=rnd.uniform(500,1300);sz=rnd.uniform(8,20)
            cx_=tx_+math.cos(a_)*v*u*(1 if c%3 else -.5);cy_=ty_+math.sin(a_)*v*u-220*u+.5*G*u*u
            if u<.7:
                ch=blank(44,44);ImageDraw.Draw(ch).polygon([(6,8),(6+sz,4),(10+sz,8+sz*.8),(4,6+sz)],fill=['#1D1D1F','#5A3A2A','#F2F2F5'][c%3])
                place(im,ch,cx_-22,cy_-22,1,max(0,1-u/.7),False,rot=rnd.uniform(-700,700)*u)
        explosion(im,u)
    if kick:
        rnd=random.Random(int(u*60));out=blank(W,H);out.alpha_composite(im,(round(rnd.uniform(-kick,kick)),round(rnd.uniform(-kick,kick))));return out
    return im

if __name__=='__main__':
    DEF={'killed':.60,'Astra':.94}
    at=lambda n,w,d=0,nth=0:DEF.get(w,d)
    ts=[.0,.30,.55,.60,.68,.80,.90,.96,1.04,1.14,1.24,1.32]
    sheet=Image.new('RGB',(6*360,2*640),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.resize((360,640)).convert('RGB'),((i%6)*360,(i//6)*640))
    out=Path(__file__).resolve().parents[1]/'review/bazooka_strip.jpg';sheet.save(out);print(out)
    big=Image.new('RGBA',(W,H),BG);big.alpha_composite(render(.40,at));big.crop((0,250,1080,850)).convert('RGB').save(out.with_name('bazooka_closeup.jpg'))
    big=Image.new('RGBA',(W,H),BG);big.alpha_composite(render(.62,at));big.crop((0,250,1080,850)).convert('RGB').save(out.with_name('bazooka_fire.jpg'));print('closeups')
