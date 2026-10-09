"""ACCEPTED full scenes.py of the Laya reel (21 Sep 2026) - Albert: "THIS REEL WAS SO GOOD". Reference + importable.
In a project the three big scenes live in parts/ (hook.py, macbook.py, readme_zoom.py); here they are the sibling
examples gun_hook.py, macbook.py, readme_zoom.py.

Scenes for the Laya reel (script says "Naya"; the real project is Laya - see README).

Every surface is recreated with Pillow - no screenshots. Product-true material:
  * Jev tile      = TypeSafe's own apple-touch-icon from typesafe.ai
  * Laya mark     = redrawn from the project's logo-mark.svg; tagline "DECISIONS, NOT TEXT" is theirs
  * numbers       = github.com/NandhaKishorM/laya README (5.2k stars, 468 forks, Apache-2.0, v0.3.4,
                    billing 0.94 / urgency 1.84 / churn 0.892 example, 0.362 -> 0.766 fine-tuned,
                    "Honest limits" copy) and the two spoken latencies (250 ms, 30 ms)

Scene coordinates are the pre-TOP_SHIFT canvas: split graphics live in y 100..700, full-screen UI in
y 120..930 with the cinematic words underneath.
"""
from draw import *
import sys,math,random
import numpy as np
sys.path.insert(0,str(P/'helpers'));sys.path.insert(0,str(P/'parts'));sys.path.insert(0,str(P/'examples'))
import instagram_comment
try:import hook as _hook_part
except ImportError:import gun_hook as _hook_part
import readme_zoom as _readme_part
from brand import *
from macbook import macbook,desktop,wifi

LEAD=.13
MONO='/System/Library/Fonts/SFNSMono.ttf'
GREEN_D='#1E8E3E'

def enter0(im,obj,x,y,t,sh=True):
    """Entrance already part-way in at t=0, so a cut into a beat is never blank."""
    e=ease((t+.09)/.32);place(im,obj,x,y+22*(1-e),.96+.04*e,e,sh)

def pop(v):return spring(max(0,min(1,v)))

def card(w=940,h=560,fill='white',r=30):return panel(w,h,fill,r)

# ---------------------------------------------------------------- 1. hook (full) ---------------
def hook(t,at):return _hook_part.render(t,at)

# ---------------------------------------------------------------- 2. faster (split) ------------
def faster(t,at):
    im=blank(W,H);c=card();d=ImageDraw.Draw(c)
    tf=at('faster','faster.',1.23)-LEAD
    x0,x1,ts=56,846,116                       # lane start, finish line, tile size (card coordinates)
    lanes=[150,372]
    # finish: checkered column through both lanes
    for r_ in range(28):
        for cc in range(2):
            if (r_+cc)%2==0:d.rectangle((x1+cc*15,70+r_*15,x1+cc*15+14,70+r_*15+14),fill='#1D1D1F')
    for y in lanes:
        d.line([(x0,y+ts+14),(x1-8,y+ts+14)],fill='#E5E5EA',width=4)
        for k in range(9):                                      # distance ticks
            xx=x0+k*(x1-x0)/8;d.line([(xx,y+ts+14),(xx,y+ts+26)],fill='#D8D8DD',width=3)
    # Jev crawls for the whole beat
    jx=x0+150*smooth(t/1.9)
    # "?" accelerates and reaches the line just before "faster"
    p=smooth((t-.10)/(tf-.10))**1.7;qx=x0+(x1-ts-x0)*p
    sp=max(0,min(1,(t-.10)/(tf-.10)));v=0 if t>tf else sp**.9
    lay=blank(c.width,c.height)
    for k in range(5):                                          # speed streaks
        ln=(60+34*k)*v*1.6;yy=lanes[1]+16+k*21
        if ln>4:ImageDraw.Draw(lay).line([(qx-ln-8,yy),(qx-8,yy)],fill=(29,29,31,round(150*v)),width=5)
    c.alpha_composite(lay)
    place(c,tile_jev(ts),jx,lanes[0],1,1,True)
    b=pop((t-tf)/.26) if t>tf else 0
    place(c,tile_q(ts),qx,lanes[1]-10*math.sin(min(1,max(0,(t-tf)/.26))*math.pi),1+.06*math.sin(min(1,max(0,(t-tf)/.26))*math.pi),1,True)
    if t>tf:                                                     # finish: green check lands on the line
        s=pop((t-tf)/.26);checkmark(c,x1+15,lanes[1]+ts/2,round(30*s),GREEN)
    txt(c,'Jev',x0,lanes[0]-52,34,GRAY,weight='Medium')
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 3. possible (split) ----------
def _lens(im,alt,cx,cy,r):
    """Magnifier: inside the glass the ALT layer shows, 1.18x, clipped to the circle."""
    z=1.18;src=alt.crop((round(cx-r/z),round(cy-r/z),round(cx+r/z),round(cy+r/z))).resize((2*r,2*r),Image.Resampling.LANCZOS)
    m=Image.new('L',(2*r*2,2*r*2));ImageDraw.Draw(m).ellipse((0,0,4*r-1,4*r-1),fill=255);m=m.resize((2*r,2*r),Image.Resampling.LANCZOS)
    glass=Image.new('RGBA',(2*r,2*r),'white');glass.alpha_composite(src);glass.putalpha(m)
    # handle first (under the ring)
    a=math.radians(42);hx0,hy0=cx+math.cos(a)*(r+4),cy+math.sin(a)*(r+4);hx1,hy1=cx+math.cos(a)*(r+150),cy+math.sin(a)*(r+150)
    d=ImageDraw.Draw(im);d.line([(hx0,hy0),(hx1,hy1)],fill='#1D1D1F',width=30)
    d.ellipse((hx1-15,hy1-15,hx1+15,hy1+15),fill='#1D1D1F')
    im.alpha_composite(shadow(2*r,2*r,r,16,40,8),(round(cx-r)-60,round(cy-r)-60))
    im.alpha_composite(glass,(round(cx-r),round(cy-r)))
    d=ImageDraw.Draw(im);d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#1D1D1F',width=13)
    d.arc((cx-r+24,cy-r+24,cx+r-24,cy+r-24),205,250,fill=(255,255,255,210),width=9)

def possible(t,at):
    im=blank(W,H);base=card();alt=card();ts=260;tx,ty=(940-ts)//2,(560-ts)//2-6
    rnd=random.Random(4)
    for k in range(9):                                          # question marks drifting up around the tile
        a0=.04+k*.075;u=t-a0
        if u<=0:continue
        side=-1 if k%2 else 1;x=470+side*rnd.uniform(215,400);y=rnd.uniform(120,470)-u*38
        n=rnd.choice([54,70,92]);col=rnd.choice(['#1D1D1F','#8E8E93',PINK,'#C7C7CC'])
        q=blank(140,140);ImageDraw.Draw(q).text((70,70),'?',font=sf(n,'Bold'),fill=col,anchor='mm')
        for L in (base,alt):place(L,q,x-70,y-70,.5+.5*pop(u/.28),min(1,u/.12),False,rot=side*(8+6*math.sin(u*4+k)))
    w=1+.035*math.sin(t*9)
    place(base,tile_q(ts),tx,ty,w,1,True);place(alt,tile_laya(ts),tx,ty,w,1,True)
    tp=at('possible','possible?',.79)
    # lens sweeps in from the upper left and settles over the tile just before "possible"
    p=smooth((t+.05)/(tp-.02));cx=lerp(150,tx+ts*.80,p)+8*math.sin(t*5)*(1 if p>=1 else 0);cy=lerp(120,ty+ts*.76,p)+6*math.cos(t*4.2)*(1 if p>=1 else 0)
    _lens(base,alt,cx,cy,92)
    enter0(im,base,70,104,t);return im

# ---------------------------------------------------------------- 4. naya / Laya reveal (split)
def naya(t,at):
    im=blank(W,H);c=card();ts=200;cx=470;ty=36
    tl=at('naya','Laya,',.57)-LEAD;f0=tl-.16                   # flip finishes ON the name
    p=max(0,min(1,(t-f0)/.22));sx=abs(math.cos(math.pi*p));tile=(tile_q if p<.5 else tile_laya)(ts)
    wob=1+.04*math.sin(t*14)*(1 if t<f0 else 0)
    tw_=max(2,round(ts*sx*wob));tl_=tile.resize((tw_,round(ts*wob)),Image.Resampling.LANCZOS)
    c.alpha_composite(shadow(tw_,tl_.height),(round(cx-tw_/2)-60,round(ty+(ts-tl_.height)/2)-60))
    c.alpha_composite(tl_,(round(cx-tw_/2),round(ty+(ts-tl_.height)/2)))
    u=t-tl
    if u>0:
        s=pop(u/.26);wm=blank(560,190);ImageDraw.Draw(wm).text((280,95),'laya',font=sf(150,'Bold'),fill='#111113',anchor='mm')
        place(c,wm,cx-280,232,.9+.1*s,min(1,u/.10),False)
    if u>.10:
        lay=blank(940,560);tracked(lay,'DECISIONS, NOT TEXT',cx,438,27,'#6E6E73',7.5);place(c,lay,0,8*(1-ease((u-.10)/.2)),1,ease((u-.10)/.2),False)
    pills=[('gh','NandhaKishorM/laya',330),('star','5.2k',150),(None,'Apache-2.0',190)]
    tot=sum(w for _,_,w in pills)+2*16;x=cx-tot/2
    for k,(ic,s_,w) in enumerate(pills):
        uu=u-.16-k*.07
        if uu>0:
            e=ease(uu/.22);pl=blank(w,56);rr(pl,(0,0,w-1,55),'#F5F5F7',28,'#E3E3E6',2);ox=22
            if ic=='gh':pl.alpha_composite(icon('lobe-github',30),(18,13));ox=58
            if ic=='star':
                pts=[(34+15*math.cos(-math.pi/2+i*math.pi/5)*(1 if i%2==0 else .45),28+15*math.sin(-math.pi/2+i*math.pi/5)*(1 if i%2==0 else .45)) for i in range(10)]
                ImageDraw.Draw(pl).polygon(pts,fill='#E3B341');ox=58
            ImageDraw.Draw(pl).text((ox,28),s_,font=sf(25,'Medium'),fill=INK,anchor='lm')
            place(c,pl,x,474+14*(1-e),1,e,False)
        x+=w+16
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 5. local (full): the MacBook --
TERM=[('cmd','pip install laya'),('ok','Successfully installed laya-0.3.4'),('cmd','python triage.py'),
      ('kv',('department','billing','0.94')),('kv',('urgency','1.84 / 2.0','')),('kv',('churn_risk','0.892','')),
      ('done','ran on this Mac - no cloud call')]
def _screen(t,at,w,h):
    s=desktop(w,h).copy();d=ImageDraw.Draw(s)
    tl=at('local','local',.47)-LEAD;tsys=at('local','system',.95)-LEAD;trun=at('local','run',2.33)-LEAD
    town=at('local','own',2.83)-LEAD;tcmp=at('local','computer.',3.05)-LEAD
    # menu bar
    rr(s,(0,0,w,34),(255,255,255,120),0)
    s.alpha_composite(icon('Apple',20),(16,7))
    for k,(lab,wt) in enumerate([('Terminal','Bold'),('Shell','Regular'),('Edit','Regular'),('View','Regular')]):
        ImageDraw.Draw(s).text((50+[0,92,152,202][k],17),lab,font=sf(17,wt),fill='#1D1D1F',anchor='lm')
    ImageDraw.Draw(s).text((w-18,17),'Mon 21 Sep  08:32',font=sf(17,'Medium'),fill='#1D1D1F',anchor='rm')
    wifi(s,w-212,17,on=t<town,k=max(0,min(1,(t-town)/.18)))
    rr(s,(w-262,9,w-232,25),None,5,'#1D1D1F',2);rr(s,(w-259,12,w-240,22),'#1D1D1F',2)
    # terminal window
    tw_,th=w-150,h-150;tx,ty=75,58
    win=blank(tw_,th);rr(win,(0,0,tw_-1,th-1),'#16161A',16);rr(win,(0,0,tw_-1,50),'#2A2A2F',16);ImageDraw.Draw(win).rectangle((0,34,tw_-1,50),fill='#2A2A2F')
    for i,cc in enumerate(['#FF5F57','#FEBC2E','#28C840']):ImageDraw.Draw(win).ellipse((18+i*24,17,32+i*24,31),fill=cc)
    win.alpha_composite(tile_laya(28),(tw_//2-92,11));ImageDraw.Draw(win).text((tw_/2-54,25),'laya - zsh',font=sf(19,'Medium'),fill='#B9B9BF',anchor='lm')
    dw=ImageDraw.Draw(win);f=ImageFont.truetype(MONO,30);fb=f;y=74;LH=46
    starts=[tsys-.05,tsys+.62,trun,trun+.42,trun+.54,trun+.66,tcmp]
    for (kind,val),st in zip(TERM,starts):
        if t<st:break
        u=t-st
        if kind=='cmd':
            dw.text((26,y),'$',font=f,fill='#28C840');s_=reveal(val,u,.40);dw.text((58,y),s_,font=f,fill='#F2F2F7')
            if u<.40 or (kind=='cmd' and t<starts[starts.index(st)+1] and int(t*3)%2==0):
                xx=58+f.getlength(s_);dw.rectangle((xx+2,y+2,xx+18,y+35),fill='#F2F2F7')
        elif kind=='ok':
            dw.text((26,y),val,font=f,fill='#8E8E93')
        elif kind=='kv':
            k_,v_,c_=val;dw.text((58,y),k_,font=f,fill='#8E8E93');dw.text((330,y),v_,font=f,fill='#F2F2F7')
            if c_:dw.text((560,y),c_,font=f,fill='#30D158')
        else:
            checkmark(win,40,y+19,14,'#30D158');dw.text((68,y),val,font=f,fill='#30D158')
        y+=LH
    e=ease((t-(tl+.10))/.28);place(s,win,tx,ty+14*(1-e),.97+.03*e,e,True)
    # dock: Laya drops in and bounces like a launching app on "local"
    dk=[('Claude',tile_claude),('ChatGPT',lambda z:apptile('ChatGPT',z)),('Notion',lambda z:apptile('Notion',z)),('Laya',tile_laya)]
    dz=54;dwid=len(dk)*(dz+14)+14;dx=(w-dwid)//2;dy=h-dz-22
    rr(s,(dx,dy-8,dx+dwid,dy+dz+8),(255,255,255,150),20)
    for k,(nm,fn) in enumerate(dk):
        yy=dy
        if nm=='Laya':
            u=t-tl
            if u<0:continue
            yy=dy-(abs(math.sin(u*9.5))*46*math.exp(-u*2.6) if u<1.4 else 0)-60*(1-ease(u/.16))
            ImageDraw.Draw(s).ellipse((dx+14+k*(dz+14)+dz/2-3,dy+dz+1,dx+14+k*(dz+14)+dz/2+3,dy+dz+7),fill='#1D1D1F')
        s.alpha_composite(fn(dz),(dx+14+k*(dz+14),round(yy)))
    return s

def local(t,at):
    im=blank(W,H);mw=940;op=.12+.88*ease((t+.06)/.46)          # lid opens, fully up by "local"
    sw,sh=mw-36,round((mw-36)*.628)
    lit=max(0,min(1,(t-.22)/.2))
    scr=_screen(t,at,sw,sh)
    if lit<1:scr=Image.blend(Image.new('RGBA',scr.size,'#050506'),scr,lit)
    mb=macbook(mw,scr,op);place(im,mb,(W-mb.width)//2,150+ (1-ease((t+.09)/.32))*26,1,1,False)
    return im

# ---------------------------------------------------------------- 6. nocode (split) ------------
CODE=[[('def ','#FF7AB2'),('route','#6BDFFF'),('(ticket):','#F2F2F7')],
      [('    team = ','#F2F2F7'),('classify','#6BDFFF'),('(ticket)','#F2F2F7')],
      [('    if ','#FF7AB2'),('team == ','#F2F2F7'),('"billing"','#FF8170'),(':','#F2F2F7')],
      [('        return ','#FF7AB2'),('refund','#6BDFFF'),('(ticket)','#F2F2F7')],
      [('    return ','#FF7AB2'),('escalate','#6BDFFF'),('(ticket)','#F2F2F7')]]
def nocode(t,at):
    im=blank(W,H);w,h=940,560;c=blank(w,h);rr(c,(0,0,w-1,h-1),'#1E1E21',26);rr(c,(0,0,w-1,70),'#2B2B2F',26);ImageDraw.Draw(c).rectangle((0,44,w-1,70),fill='#2B2B2F')
    d=ImageDraw.Draw(c)
    for i,cc in enumerate(['#FF5F57','#FEBC2E','#28C840']):d.ellipse((24+i*28,27,40+i*28,43),fill=cc)
    rr(c,(130,14,330,70),'#1E1E21',12);d=ImageDraw.Draw(c);d.rectangle((130,56,330,70),fill='#1E1E21');d.text((158,40),'handler.py',font=sf(24,'Medium'),fill='#D1D1D6',anchor='lm')
    # "Same as Jev": both tiles sit in the title bar, Jev pops on its name
    tj=at('nocode','Jev,',.49)-LEAD
    place(c,tile_laya(48),w-76,11,1,1,False)
    if t>tj:place(c,tile_jev(48),w-136,11,pop((t-tj)/.24),1,False)
    if t>tj+.04:d=ImageDraw.Draw(c);d.text((w-82,35),'=',font=sf(26,'Bold'),fill='#8E8E93',anchor='mm') if False else None
    f=ImageFont.truetype(MONO,31);tc=at('nocode','cannot',.97)-LEAD
    total=sum(len(s) for ln in CODE for s,_ in ln);shown=int(total*min(1,max(0,(t+.10)/.80)));y0=118;LH=78
    for li,ln in enumerate(CODE):
        y=y0+li*LH;d.text((34,y),str(li+1),font=f,fill='#5A5A60');x=96
        k=t-tc-li*.075;dead=k>0
        for s,col in ln:
            take=max(0,min(len(s),shown));shown-=take
            if take:d.text((x,y),s[:take],font=f,fill='#A0A0A8' if dead and k>.10 else col)
            x+=f.getlength(s)
        if dead:                                                # strike through the x-height middle, left to right
            bb=d.textbbox((0,0),'x',font=f);ym=y+(bb[1]+bb[3])/2;x_end=96+(x-96)*ease(k/.16)
            first=len(ln[0][0])-len(ln[0][0].lstrip());xs=96+f.getlength(' '*first)
            if x_end>xs:d.line([(xs-6,ym),(x_end+6,ym)],fill='#FF453A',width=3)
    if t<tc and int(t*3.2)%2==0:                                # caret while typing
        pass
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 7. speed (full) --------------
def _num(c,x,y,val,unit,col,big=150):
    """Right-aligned 'NNN ms' on one baseline."""
    d=ImageDraw.Draw(c);fu=sf(54,'Semibold');fn=sf(big,'Bold');uw=fu.getlength(unit)
    d.text((x,y),unit,font=fu,fill='#8E8E93',anchor='rs');d.text((x-uw-14,y),val,font=fn,fill=col,anchor='rs')
    return x-uw-14-fn.getlength(val)

def speed(t,at):
    im=blank(W,H);w=940
    t250=at('speed','250',1.17);ttk=at('speed','takes',.71);tthis=at('speed','this',3.19)-LEAD
    t30=at('speed','30',4.29);ttk2=at('speed','takes',3.93,1)
    grow=ease((t-tthis)/.30) if t>tthis else 0;h=round(lerp(440,750,grow))   # the card grows to take the Laya row
    c=card(w,h,'white',34);bx0,bx1=60,w-60;full=bx1-bx0
    # ---- row A: Jev
    place(c,tile_jev(112),60,58,1,1,True);d=ImageDraw.Draw(c)
    d.text((196,92),'Jev',font=sf(50,'Semibold'),fill=INK,anchor='lm');d.text((196,142),'cloud API',font=sf(28),fill=GRAY,anchor='lm')
    pa=smooth((t-(ttk-.12))/(t250-(ttk-.12)));va=round(250*pa)
    _num(c,w-60,176,str(va),'ms','#1D1D1F')
    rr(c,(bx0,222,bx1,258),'#F0F0F3',18)
    if pa>0:rr(c,(bx0,222,bx0+max(36,full*pa),258),PINK,18)
    if t>=t250:                                                  # red frame lands ON the spoken number
        s=pop((t-t250)/.24);fw=sf(150,'Bold').getlength('250');x1_=w-60-sf(54,'Semibold').getlength('ms')-14
        g=10+14*(1-s);rr(c,(x1_-fw-g-6,58-g+8,x1_+g+6,190+g),None,20,'#FF3B30',5)
        # real-time ping: the dot crosses the bar once every 250 ms
        ph=((t-t250)%.25)/.25;px=bx0+18+(full-36)*ph;ImageDraw.Draw(c).ellipse((px-11,240-11,px+11,240+11),fill='white')
    # ---- row B: Laya
    if t>tthis:
        e=grow;row=blank(w,300)
        place(row,tile_laya(112),60,20,1,1,True);dr=ImageDraw.Draw(row)
        dr.text((196,54),'Laya',font=sf(50,'Semibold'),fill=INK,anchor='lm');dr.text((196,104),'runs on your machine',font=sf(28),fill=GRAY,anchor='lm')
        pb=smooth((t-(ttk2-.10))/(t30-(ttk2-.10)));vb=round(30*pb)
        _num(row,w-60,138,str(vb),'ms',GREEN_D)
        rr(row,(bx0,184,bx1,220),'#F0F0F3',18)
        if pb>0:rr(row,(bx0,184,bx0+max(36,full*30/250*pb),220),GREEN,18)
        if t>=t30:
            s=pop((t-t30)/.24);fw=sf(150,'Bold').getlength('30');x1_=w-60-sf(54,'Semibold').getlength('ms')-14
            g=10+14*(1-s);rr(row,(x1_-fw-g-6,20-g+8,x1_+g+6,152+g),None,20,GREEN,5)
            gl=.5+.5*math.sin((t-t30)*40);rr(row,(bx0,184,bx0+full*30/250,220),(255,255,255,round(90*gl)),18)
        place(c,row,0,296+26*(1-e),1,e,False)
    # ---- shared axis rides the bottom edge; ticks arrive one by one through "milliseconds to respond"
    ay=h-118
    for k in range(6):
        u=t-(t250+.50+k*.12)
        if u<=0:continue
        e=ease(u/.2);xx=bx0+full*k/5;lay=blank(w,h);dl=ImageDraw.Draw(lay)
        dl.line([(xx,ay),(xx,ay+16*e)],fill='#C7C7CC',width=3)
        dl.text((min(max(xx,bx0+14),bx1-28),ay+46),f'{k*50}',font=sf(27,'Medium'),fill='#8E8E93',anchor='mm')
        place(c,lay,0,0,1,e,False)
    if t>t250+.50:ImageDraw.Draw(c).line([(bx0,ay),(bx0+full*ease((t-t250-.50)/.7),ay)],fill='#C7C7CC',width=3)
    if t>t250+1.25:
        lay=blank(w,h);ImageDraw.Draw(lay).text((w/2,ay+88),'milliseconds to respond',font=sf(25),fill='#AEAEB2',anchor='mm');place(c,lay,0,0,1,ease((t-t250-1.25)/.25),False)
    enter0(im,c,70,130,t);return im

# ---------------------------------------------------------------- 8. cloud (split) -------------
def _cloudshape(w,h,fill,edge):
    q=3;im=blank(w*q,h*q);d=ImageDraw.Draw(im)
    blobs=[(.26,.62,.22),(.45,.42,.27),(.68,.50,.24),(.80,.68,.18),(.52,.70,.24)]
    for pass_,(col,g) in enumerate(((edge,5*q),(fill,0))):
        for bx,by,br in blobs:
            r=br*w*q+g;d.ellipse((bx*w*q-r,by*h*q-r*.86,bx*w*q+r,by*h*q+r*.86),fill=col)
        d.rounded_rectangle((.10*w*q-g,.62*h*q-g*.4,.92*w*q+g,.92*h*q+g),radius=.15*h*q,fill=col)
    return im.resize((w,h),Image.Resampling.LANCZOS)

def _bez(p0,p1,p2,u):return ((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1])

def cloud(t,at):
    im=blank(W,H);c=card();w,h=940,560
    tl=at('cloud','local,',1.09)-LEAD;tn=at('cloud',"doesn't",1.71)-LEAD;tc=at('cloud','cloud',2.55)-LEAD;tb=at('cloud','back,',3.07)-LEAD
    # laptop with the Laya tile on its screen
    MW=430;sw,sh=MW-16,round((MW-16)*.628);scr=Image.new('RGBA',(sw,sh),'#F5F5F7')
    sc=pop((t-.18)/.3);place(scr,tile_laya(128),(sw-128)//2,(sh-128)//2,sc,1 if t>.18 else 0,True)
    if t>tl:                                                     # the whole round trip happens on the machine
        u=t-tl;spd=9.0 if t<tb else 15.0;a=u*spd;r=100;cx,cy=sw/2,sh/2
        lay=blank(sw,sh);dl=ImageDraw.Draw(lay)
        for k in range(18):
            aa=a-k*.12;op=round(255*(1-k/18)*min(1,u/.15));rad=9-k*.3
            dl.ellipse((cx+math.cos(aa)*r-rad,cy+math.sin(aa)*r*.92-rad,cx+math.cos(aa)*r+rad,cy+math.sin(aa)*r*.92+rad),fill=(52,199,89,op))
        scr.alpha_composite(lay)
    mb=macbook(MW,scr,1.0);mx,my=48,178;place(c,mb,mx,my,1,1,False);mcx=mx+mb.width/2
    gl=ease((t-tl)/.2) if t>tl else 0;lw=176
    rr(c,(mcx-lw/2,494,mcx+lw/2,542),(232,248,237,255) if gl>.5 else '#F2F2F4',24)
    d=ImageDraw.Draw(c);d.text((mcx+(15 if gl>.5 else 0),518),'local',font=sf(29,'Semibold'),fill=GREEN_D if gl>.5 else GRAY,anchor='mm')
    if gl>.5:checkmark(c,mcx-50,518,14,GREEN)
    # the cloud and the route to it
    away=smooth((t-tn-.25)/.7) if t>tn+.25 else 0
    cl=_cloudshape(370,236,'#EEF4FE','#CFDDF5');place(c,cl,540+24*away,30-18*away,1,(1-.72*away)*ease((t-.30)/.3),False)
    if t>.30:
        lay=blank(w,h);ImageDraw.Draw(lay).text((726+24*away,150-18*away),'cloud',font=sf(34,'Semibold'),fill='#5B7DB8',anchor='mm');place(c,lay,0,0,1,(1-.8*away)*ease((t-.35)/.3),False)
    p0,p1,p2=(mcx+30,my+6),(mcx+70,20),(590,150)
    drawn=ease((t-.45)/.45);gone=smooth((t-tn)/.6) if t>tn else 0   # un-draws from the laptop end on "doesn't"
    lay=blank(w,h);dl=ImageDraw.Draw(lay);N=30
    for k in range(N):
        u0=((k/N)+t*.10)%1;u1=u0+.55/N
        if u1>drawn or u0<gone or u1>1:continue
        dl.line([_bez(p0,p1,p2,u0),_bez(p0,p1,p2,u1)],fill='#A9B8D4',width=7)
    c.alpha_composite(lay)
    if t<tn and drawn>=1:                                        # Jev-style packet doing the slow round trip
        per=1.10;ph=((t-.9)%per)/per;u=ph*2 if ph<.5 else 2-ph*2;x,y=_bez(p0,p1,p2,smooth(u))
        ImageDraw.Draw(c).ellipse((x-17,y-17,x+17,y+17),fill=PINK,outline='white',width=5)
    elif t>=tn:
        u=t-tn;x,y=_bez(p0,p1,p2,max(gone,.02));k_=max(0,1-u/.6)
        if k_>0:ImageDraw.Draw(c).ellipse((x-17*k_,y-17*k_,x+17*k_,y+17*k_),fill=PINK)
    if t>tb:                                                     # "and back": nothing left to wait for
        s_=pop((t-tb)/.26);checkmark(c,mx+mb.width-40,my+4,round(32*s_),GREEN)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 9. muchfast (split) ----------
def muchfast(t,at):
    im=blank(W,H);c=card();w,h=940,560;cx,cy,R=470,470,350
    tf=at('muchfast','faster.',.88)-LEAD
    v=.10+.86*max(0,min(1,(t-.06)/(tf-.06)))**2.1
    if t>tf:u_=t-tf;v=.96+.035*math.exp(-u_*8)*math.sin(u_*34)+.004*math.sin(t*40)
    q=2;lay=blank(w*q,h*q);dl=ImageDraw.Draw(lay);box=((cx-R)*q,(cy-R)*q,(cx+R)*q,(cy+R)*q)
    dl.arc(box,180,360,fill='#EDEDF0',width=46*q)
    # fill arc: green deepens toward the top end
    seg=90;end=180+180*v
    for k in range(seg):
        a0=180+180*k/seg;a1=min(end,180+180*(k+1)/seg+.6)
        if a0>=end:break
        u=k/seg;col=(round(lerp(168,30,u)),round(lerp(230,160,u)),round(lerp(190,70,u)))
        dl.arc(box,a0,a1,fill=col,width=46*q)
    for k in range(11):                                          # ticks inside the arc
        a=math.radians(180+18*k);r0,r1=(R-72)*q,(R-46)*q if k%5 else (R-38)*q
        dl.line([(cx*q+math.cos(a)*r0,cy*q+math.sin(a)*r0),(cx*q+math.cos(a)*r1,cy*q+math.sin(a)*r1)],fill='#C7C7CC',width=5*q if k%5==0 else 3*q)
    # needle
    a=math.radians(180+180*v);nx,ny=cx*q+math.cos(a)*(R-84)*q,cy*q+math.sin(a)*(R-84)*q
    dl.line([(cx*q,cy*q),(nx,ny)],fill='#1D1D1F',width=12*q);dl.ellipse((nx-6*q,ny-6*q,nx+6*q,ny+6*q),fill='#1D1D1F')
    c.alpha_composite(lay.resize((w,h),Image.Resampling.LANCZOS))
    # Jev marks where the old needle sat; Laya is the hub
    aj=math.radians(180+180*.16);place(c,tile_jev(66),cx+math.cos(aj)*(R+6)-33,cy+math.sin(aj)*(R+6)-33-44,1,1,True)
    hub=tile_laya(128);place(c,hub,cx-64,cy-64,1+.05*math.sin(min(1,max(0,(t-tf)/.25))*math.pi),1,True)
    if t>tf:                                                     # speed ticks fly off the needle tip
        u=t-tf
        for k in range(5):
            aa=math.radians(180+180*v)+(-.22+k*.11);r0=R+34+u*150;r1=r0+30+10*k
            op=max(0,1-u/.42)
            if op>0:
                l2=blank(w,h);ImageDraw.Draw(l2).line([(cx+math.cos(aa)*r0,cy+math.sin(aa)*r0),(cx+math.cos(aa)*r1,cy+math.sin(aa)*r1)],fill=(30,142,62,round(255*op)),width=6);c.alpha_composite(l2)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 10. problem (full) -----------
def problem(t,at):return _readme_part.render(t,at)

# ---------------------------------------------------------------- 11. tuned (split) ------------
USE=['Support triage','Prompt guardrails','Moderation','Model routing']      # laya.*_questions() presets
def tuned(t,at):
    im=blank(W,H);c=card();w,h=940,560;d=ImageDraw.Draw(c)
    t0=at('tuned','tuned',.69)-LEAD;t1=at('tuned','trained',1.29)+.34;ts_=at('tuned','specific',1.81)-LEAD;te=at('tuned','cases.',2.53)-LEAD
    p=smooth((t-t0)/(t1-t0));val=.362+(.766-.362)*p
    d.text((56,112),f'{val:.3f}',font=sf(104,'Bold'),fill=GREEN_D if p>=1 else INK,anchor='ls')
    d.text((58,152),'typed-decisions accuracy',font=sf(25),fill=GRAY,anchor='ls')
    # chart
    x0,x1,y0,y1=58,520,500,210
    d.line([(x0,y0),(x1,y0)],fill='#E5E5EA',width=3)
    for k in range(1,4):d.line([(x0,y0-(y0-y1)*k/3),(x1,y0-(y0-y1)*k/3)],fill='#F2F2F4',width=2)
    def cy_(u):
        base=1-math.exp(-3.4*u);return y0-24-(y0-y1-40)*base/(1-math.exp(-3.4))+6*math.sin(u*23)*(1-u)
    # base level, dotted
    for k in range(0,46,2):d.line([(x0+k*10,cy_(0)),(x0+k*10+9,cy_(0))],fill='#D1D1D6',width=3)
    d.text((x1,cy_(0)+22),'base  0.362',font=sf(22,'Medium'),fill='#AEAEB2',anchor='rm')
    if p>0:
        pts=[(x0+(x1-x0)*u/80,cy_(u/80)) for u in range(0,int(80*p)+1)]
        if len(pts)>1:
            poly=pts+[(pts[-1][0],y0),(x0,y0)];lay=blank(w,h);ImageDraw.Draw(lay).polygon(poly,fill=(52,199,89,38));c.alpha_composite(lay)
            ImageDraw.Draw(c).line(pts,fill=GREEN,width=7,joint='curve')
        hx,hy=pts[-1];ImageDraw.Draw(c).ellipse((hx-12,hy-12,hx+12,hy+12),fill=GREEN,outline='white',width=4)
    else:
        ImageDraw.Draw(c).ellipse((x0-12,cy_(0)-12,x0+12,cy_(0)+12),fill='#AEAEB2',outline='white',width=4)
    if p>=1:
        e=ease((t-t1)/.2);lay=blank(w,h);ImageDraw.Draw(lay).text((x1,cy_(1)-30),'fine-tuned  0.766',font=sf(23,'Semibold'),fill=GREEN_D,anchor='rm');place(c,lay,0,0,1,e,False)
    # epoch ticker keeps the left side alive before and after the curve
    ep=min(4,int(max(0,t-t0)/(t1-t0)*4)+1) if t>t0 else 1
    d=ImageDraw.Draw(c);d.text((x0,y0+34),f'epoch {ep} / 4',font=sf(23,'Medium'),fill=GRAY,anchor='lm')
    for k in range(4):
        rr(c,(x0+150+k*34,y0+26,x0+176+k*34,y0+42),GREEN if (k<ep and t>t0) else '#E5E5EA',8)
    # use-case chips, picked one at a time across "specific use cases"
    step=(te-ts_)/3
    for k,lab in enumerate(USE):
        yy=96+k*104;u=t-(ts_+k*step);on=u>0;e0=ease((t-.10-k*.07)/.3)
        ch=blank(340,84);s=pop(u/.24) if on else 0
        rr(ch,(0,0,339,83),(232,248,237,255) if on else '#F7F7F8',24,GREEN if on else '#E3E3E6',3 if on else 2)
        if on:checkmark(ch,44,42,round(17*s),GREEN)
        else:ImageDraw.Draw(ch).ellipse((27,25,61,59),outline='#C7C7CC',width=3)
        ImageDraw.Draw(ch).text((80,42),lab,font=sf(28,'Semibold' if on else 'Medium'),fill=INK if on else GRAY,anchor='lm')
        place(c,ch,568,yy+12*(1-e0),1+.03*math.sin(min(1,max(0,u/.24))*math.pi) if on else 1,e0,False)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 12. claude (full) ------------
def claude(t,at):
    im=blank(W,H);tcl=at('claude','Claude.',1.13)-LEAD
    # tiles: Laya waits, Claude lands on its name
    ts=250;y=190
    e0=ease((t+.09)/.3);sl=ease((t-tcl)/.26) if t>tcl else 0
    place(im,tile_laya(ts),lerp((W-ts)/2,150,sl),y+22*(1-e0),1+.03*math.sin(t*7)*(1-sl),e0,True)
    if t>tcl:
        s=pop((t-tcl)/.26);place(im,tile_claude(ts),W-150-ts,y,.6+.4*s,min(1,(t-tcl)/.08),True)
        pl=blank(120,120);dp=ImageDraw.Draw(pl);dp.line([(60,24),(60,96)],fill='#1D1D1F',width=14);dp.line([(24,60),(96,60)],fill='#1D1D1F',width=14)
        place(im,pl,W/2-60,y+ts/2-60,s,1,False,rot=90*(1-s))
    else:
        # a dashed slot breathing where the partner will land keeps the right side alive
        pass
    # Claude prompt field, cream, typed from the first frame
    w,h=940,250;c=blank(w,h);rr(c,(0,0,w-1,h-1),'#FAF9F5',34,'#E6E2D6',2);d=ImageDraw.Draw(c)
    msg='Fine-tune Laya on my support tickets';s_=reveal(msg,t+.05,.85)
    d.text((44,70),s_,font=sf(40,'Medium'),fill='#2B2A27',anchor='lm')
    if len(s_)<len(msg) or int(t*3)%2==0:
        xx=44+sf(40,'Medium').getlength(s_);d.rectangle((xx+4,46,xx+8,94),fill=TERRA)
    rr(c,(40,150,250,208),'#F0EEE6',29);c.alpha_composite(icon('lobe-claudecode-color',34),(56,162));ImageDraw.Draw(c).text((100,179),'Claude Code',font=sf(24,'Medium'),fill='#5E5D59',anchor='lm')
    pr=t-(tcl+.12);r=34*(1-.12*math.sin(min(1,max(0,pr/.2))*math.pi)) if pr>0 else 34
    ImageDraw.Draw(c).ellipse((w-60-34-r,179-r,w-60-34+r,179+r),fill=TERRA if len(s_)>3 else '#E3DFD3')
    ax,ay=w-60-34,179;ImageDraw.Draw(c).line([(ax,ay+14),(ax,ay-14)],fill='white',width=6);ImageDraw.Draw(c).line([(ax-12,ay-3),(ax,ay-15),(ax+12,ay-3)],fill='white',width=6,joint='curve')
    enter0(im,c,70,540,t);return im

# ---------------------------------------------------------------- 13. cta (split) --------------
def cta(t,at):
    im=blank(W,H)
    obj=instagram_comment.render(t,keyword='FAST',viewer='you',type_start=at('cta','comment',1.29)-LEAD,type_duration=.34,
                                 post_at=at('cta','and',2.03)-LEAD)
    e=ease((t+.09)/.30);place(im,obj,90,150+18*(1-e),.96+.04*e,e,True)
    # REJECTED 25 Sep 2026 ("Remove this too"): no link chip in the CTA - copy only the comment UI above. See SKILL.md rule 20.
    # "the link": the real repo URL writes itself in under the comments, and goes blue on "send"
    tlk=at('cta','link',.45)-LEAD;tsd=at('cta','send',2.37)-LEAD
    if t>tlk:
        u=t-tlk;s_=pop(u/.26);w,h=700,72;ch=blank(w,h);sent=t>tsd
        rr(ch,(0,0,w-1,h-1),'white',36,'#0A84FF' if sent else '#E3E3E6',3 if sent else 2)
        ch.alpha_composite(icon('lobe-github',38),(22,17))
        url='github.com/NandhaKishorM/laya';ImageDraw.Draw(ch).text((78,36),reveal(url,u,.70),font=sf(31,'Medium'),fill=INK,anchor='lm')
        # paper plane
        px,py=w-52,36;col='#0A84FF' if sent else '#C7C7CC';k=1+.25*math.sin(min(1,max(0,(t-tsd)/.25))*math.pi) if sent else 1
        pts=[(px-16*k,py-13*k),(px+18*k,py),(px-16*k,py+13*k),(px-8*k,py)]
        ImageDraw.Draw(ch).polygon(pts,fill=col)
        place(im,ch,(W-w)/2,612+14*(1-s_),.94+.06*s_,min(1,u/.10),True)
    return im

FN={'hook':hook,'faster':faster,'possible':possible,'naya':naya,'local':local,'nocode':nocode,'speed':speed,
    'cloud':cloud,'muchfast':muchfast,'problem':problem,'tuned':tuned,'claude':claude,'cta':cta}
def graphics(b,t,S,at):return FN[b['name']](t,at)
