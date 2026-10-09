"""ACCEPTED (Laya reel, 21 Sep 2026). The pricing_zoom recipe applied to a GitHub repo / README.
Reuse: scrape the live repo (firecrawl) -> put the REAL copy in page() -> mark the sentences to highlight with an
hl id in the _rich() segments -> sweep(hid, t0, dur) on the spoken keywords. Main column + About sidebar keeps the
text column narrow enough that a 1.42x push-in makes 21-unit body text ~30 px on screen.

problem beat: the real GitHub README, recreated -> camera push-in -> yellow highlighter on the exact lines.

"The only problem is that the base model isn't good at everything,"

Albert's favourite move (pricing_zoom recipe): the whole page is drawn once at 2x and cached, a Safari window
carries the real URL, the camera pushes in with smooth() just before "base model", and the highlighter sweeps
  1. the bold lead of the first "Honest limits" bullet on "base model"
  2. "Laya is a fast base to specialise, not a zero-shot decision engine." on "isn't good"
All copy and numbers are from github.com/NandhaKishorM/laya as scraped 21 Sep 2026 (5.2k stars, 468 forks,
35 watching, 7 releases, v0.3.4, Apache-2.0, the three "Honest limits" bullets). Sections between the intro and
"Honest limits" are skipped - this is a recreation of the page, not a capture.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
K=2;PW,PH_=940,1130;VW,VH=940,708
GH_BLUE='#0969DA';GH_INK='#1F2328';GH_MUTED='#59636E';GH_LINE='#D1D9E0';GH_BTN='#F6F8FA'
MONO='/System/Library/Fonts/SFNSMono.ttf'
HL={}                                                              # id -> list of boxes (page units)

def F(n,wt='Regular'):return sf(n*K,wt)
def _btn(d,im,x,y,w,label,count,star=False):
    rr(im,(x*K,y*K,(x+w)*K,(y+32)*K),GH_BTN,6*K,GH_LINE,K)
    ox=x+12
    if star:
        pts=[((ox+8+8*math.cos(-math.pi/2+i*math.pi/5)*(1 if i%2==0 else .45))*K,(y+16+8*math.sin(-math.pi/2+i*math.pi/5)*(1 if i%2==0 else .45))*K) for i in range(10)]
        d.line(pts+[pts[0]],fill=GH_MUTED,width=K+1,joint='curve')
    else:
        for (ax,ay) in ((ox+4,y+9),(ox+12,y+9),(ox+8,y+23)):d.ellipse(((ax-2.5)*K,(ay-2.5)*K,(ax+2.5)*K,(ay+2.5)*K),outline=GH_MUTED,width=K)
        d.line([((ox+4)*K,(y+11)*K),((ox+4)*K,(y+15)*K),((ox+12)*K,(y+15)*K),((ox+12)*K,(y+11)*K)],fill=GH_MUTED,width=K);d.line([((ox+8)*K,(y+15)*K),((ox+8)*K,(y+21)*K)],fill=GH_MUTED,width=K)
    d.text(((ox+24)*K,(y+16)*K),label,font=F(14,'Medium'),fill=GH_INK,anchor='lm')
    lw=F(14,'Medium').getlength(label)/K;cx=ox+24+lw+10
    cw=F(12,'Medium').getlength(count)/K+14;rr(im,(cx*K,(y+7)*K,(cx+cw)*K,(y+25)*K),'#E6EAEF',9*K)
    d.text(((cx+cw/2)*K,(y+16)*K),count,font=F(12,'Medium'),fill=GH_INK,anchor='mm')

def _rich(im,segs,x,y,maxw,size=21,lh=33):
    """Word-wrapped rich text. segs: (text, style, hl_id). Records highlight boxes per line in HL."""
    d=ImageDraw.Draw(im);sp=F(size).getlength(' ')/K;cx=x;cy=y;runs={}
    for text,style,hid in segs:
        f=F(size,'Semibold') if style=='b' else (ImageFont.truetype(MONO,round(size*.9*K)) if style=='code' else F(size))
        for wd in text.split(' '):
            if not wd:continue
            ww=f.getlength(wd)/K
            if cx+ww>x+maxw and cx>x:cx=x;cy+=lh
            if style=='code':rr(im,((cx-4)*K,(cy-size*.62)*K,(cx+ww+4)*K,(cy+size*.42)*K),'#EFF1F3',5*K);d=ImageDraw.Draw(im)
            d.text((cx*K,cy*K),wd,font=f,fill=GH_INK,anchor='ls')
            if hid:
                key=(hid,cy);b=runs.get(key)
                runs[key]=[min(b[0],cx) if b else cx,cy-size*.80,max(b[2],cx+ww) if b else cx+ww,cy+size*.30]
            cx+=ww+sp
    for (hid,_),b in sorted(runs.items(),key=lambda kv:kv[0][1]):HL.setdefault(hid,[]).append(tuple(b))
    return cy+lh

@lru_cache(None)
def page():
    HL.clear();im=Image.new('RGBA',(PW*K,PH_*K),'white');d=ImageDraw.Draw(im)
    # ---- header
    im.alpha_composite(icon('lobe-github',32*K),(24*K,16*K))
    x=72;d.text((x*K,32*K),'NandhaKishorM',font=F(16),fill=GH_BLUE,anchor='lm');x+=F(16).getlength('NandhaKishorM')/K+8
    d.text((x*K,32*K),'/',font=F(16),fill=GH_MUTED,anchor='lm');x+=14
    d.text((x*K,32*K),'laya',font=F(16,'Bold'),fill=GH_BLUE,anchor='lm');x+=F(16,'Bold').getlength('laya')/K+12
    rr(im,(x*K,21*K,(x+54)*K,43*K),None,11*K,GH_LINE,K);d=ImageDraw.Draw(im);d.text(((x+27)*K,32*K),'Public',font=F(12,'Medium'),fill=GH_MUTED,anchor='mm')
    _btn(d,im,PW-24-118-10-106,16,106,'Fork','468');_btn(d,im,PW-24-118,16,118,'Star','5.2k',True);d=ImageDraw.Draw(im)
    # ---- tabs
    tx=24
    for i,lab in enumerate(['Code','Issues','Pull requests','Actions','Security','Insights']):
        wl=F(14,'Semibold' if i==0 else 'Regular').getlength(lab)/K
        d.text((tx*K,88*K),lab,font=F(14,'Semibold' if i==0 else 'Regular'),fill=GH_INK if i==0 else GH_MUTED,anchor='lm')
        if i==0:d.rectangle(((tx-8)*K,109*K,(tx+wl+8)*K,112*K),fill='#FD8C73')
        tx+=wl+34
    d.line([(0,112*K),(PW*K,112*K)],fill=GH_LINE,width=K)
    # ---- README box (main column) + About sidebar
    mx0,mx1=24,648;rr(im,(mx0*K,136*K,mx1*K,(PH_-20)*K),'white',8*K,GH_LINE,K);d=ImageDraw.Draw(im)
    d.text(((mx0+20)*K,160*K),'README',font=F(14,'Semibold'),fill=GH_INK,anchor='lm');d.rectangle(((mx0+12)*K,181*K,(mx0+84)*K,184*K),fill='#FD8C73')
    d.text(((mx0+112)*K,160*K),'Apache-2.0 license',font=F(14),fill=GH_MUTED,anchor='lm');d.line([(mx0*K,184*K),(mx1*K,184*K)],fill=GH_LINE,width=K)
    logo=Image.open(P/'assets/brand/laya-logo-lockup.png').convert('RGBA');lh_=92;logo=logo.resize((round(logo.width*lh_*K/logo.height),lh_*K),Image.Resampling.LANCZOS)
    im.alpha_composite(logo,((mx0+28)*K,206*K))
    tx0=mx0+32;tw_=mx1-mx0-64
    y=_rich(im,[('Multilingual, non-autoregressive System 1 decision engine.','b',None),
                ('Typed decisions over 100+ languages in a single forward pass - 33 ms - trained with reinforcement learning against strictly proper scoring rules (RLCD).','r',None)],tx0,338,tw_,19,30)
    d=ImageDraw.Draw(im);bx=tx0
    for lab,val,col in (('pypi','v0.3.4','#F37626'),('license','Apache 2.0','#3FB950'),('model','convaiinnovations/laya','#2A78D6')):
        lw=F(12).getlength(lab)/K+14;vw=F(12).getlength(val)/K+14
        rr(im,(bx*K,(y-8)*K,(bx+lw+vw)*K,(y+14)*K),'#555D66',4*K);rr(im,((bx+lw)*K,(y-8)*K,(bx+lw+vw)*K,(y+14)*K),col,4*K);d=ImageDraw.Draw(im)
        d.rectangle(((bx+lw)*K,(y-8)*K,(bx+lw+6)*K,(y+14)*K),fill=col)
        d.text(((bx+lw/2)*K,(y+3)*K),lab,font=F(12),fill='white',anchor='mm');d.text(((bx+lw+vw/2)*K,(y+3)*K),val,font=F(12),fill='white',anchor='mm');bx+=lw+vw+8
    y+=62
    d.text((tx0*K,y*K),'Honest limits',font=F(26,'Semibold'),fill=GH_INK,anchor='ls');d.line([(tx0*K,(y+14)*K),((mx1-32)*K,(y+14)*K)],fill=GH_LINE,width=K)
    global H2Y;H2Y=y-30
    y+=58
    bullets=[[('The base checkpoints are near chance on typed-decisions zero-shot','b','lead'),
              ('- 0.362 and 0.352 against a 0.318 random baseline and a 0.461 majority-class baseline. The 0.766 figure comes from the checkpoint fine-tuned on that benchmark\'s own training split.','r',None),
              ('Laya is a fast base to specialise, not a zero-shot decision engine.','r','key')],
             [('Ordinal','r',None),('score','code',None),('questions are the weakest primitive (SST-5 0.372).','r',None)],
             [('laya','code',None),('collapses outside English;','r',None),('laya-multilingual','code',None),('is weaker on English. Route, or pick deliberately.','r',None)]]
    for segs in bullets:
        d=ImageDraw.Draw(im);d.ellipse(((tx0+6)*K,(y-10)*K,(tx0+13)*K,(y-3)*K),fill=GH_INK)
        y=_rich(im,segs,tx0+30,y,tw_-30,21,33)+14
    # ---- sidebar
    sx=680;d=ImageDraw.Draw(im);d.text((sx*K,160*K),'About',font=F(16,'Semibold'),fill=GH_INK,anchor='lm')
    yy=_rich(im,[('No description, website, or topics provided.','r',None)],sx,200,230,15,23)
    rows=['Readme','Apache-2.0 license','5.2k stars','35 watching','468 forks']
    for i,lab in enumerate(rows):
        d=ImageDraw.Draw(im);cy=yy+18+i*34;d.ellipse((sx*K,(cy-7)*K,(sx+14)*K,(cy+7)*K),outline=GH_MUTED,width=K+1)
        d.text(((sx+26)*K,cy*K),lab,font=F(15,'Semibold' if lab[0].isdigit() else 'Regular'),fill=GH_MUTED,anchor='lm')
    cy=yy+18+len(rows)*34+22;d.line([(sx*K,cy*K),((PW-24)*K,cy*K)],fill=GH_LINE,width=K)
    d.text((sx*K,(cy+30)*K),'Releases',font=F(16,'Semibold'),fill=GH_INK,anchor='lm');rr(im,((sx+78)*K,(cy+20)*K,(sx+104)*K,(cy+40)*K),'#E6EAEF',10*K);ImageDraw.Draw(im).text(((sx+91)*K,(cy+30)*K),'7',font=F(12,'Medium'),fill=GH_INK,anchor='mm')
    d=ImageDraw.Draw(im);d.text((sx*K,(cy+66)*K),'v0.3.4',font=F(15,'Semibold'),fill=GH_INK,anchor='lm')
    rr(im,((sx+62)*K,(cy+55)*K,(sx+118)*K,(cy+77)*K),None,11*K,'#1A7F37',K);ImageDraw.Draw(im).text(((sx+90)*K,(cy+66)*K),'Latest',font=F(12,'Medium'),fill='#1A7F37',anchor='mm')
    return im

def _cursor(im,x,y):
    pts=[(x,y),(x+5,y+44),(x+16,y+33),(x+27,y+51),(x+37,y+44),(x+27,y+27),(x+42,y+24)]
    ImageDraw.Draw(im).polygon(pts,fill='white',outline=INK,width=3)

def render(t,at):
    im=blank(W,H);pg=page()
    tb=at('problem','base',.99);ti=at('problem',"isn't",1.65)
    z0=tb-.13-.42;z=smooth((t-z0)/.60)                                  # push-in finishes just before "base"
    Z=1.42;tw_,th=VW/Z,VH/Z
    wide=(0,0,VW,VH);tgt=(2,H2Y-22,tw_,th)
    # a small settle-scroll in the wide shot keeps the page alive before the push-in
    pre=18*smooth(t/.5)
    vx=lerp(wide[0],tgt[0],z);vy=lerp(wide[1]+pre,tgt[1],z);vw=lerp(wide[2],tgt[2],z);vh=lerp(wide[3],tgt[3],z)
    # after the push-in the camera keeps tilting down with the highlighter
    vy+=16*smooth((t-(ti-.13))/.7)
    view=pg.crop((round(vx*K),round(vy*K),round((vx+vw)*K),round((vy+vh)*K))).resize((VW,VH),Image.Resampling.LANCZOS)
    s=VW/vw
    def sweep(hid,t0,dur):
        boxes=HL.get(hid,[]);tot=sum(b[2]-b[0] for b in boxes);done=max(0,min(1,(t-t0)/dur))*tot;tip=None
        for b in boxes:
            if done<=0:break
            ln=b[2]-b[0];k=min(ln,done);done-=k
            X0,Y0,X1,Y1=(b[0]-3-vx)*s,(b[1]-vy)*s,(b[0]+k+3-vx)*s,(b[3]-vy)*s
            rr(view,(X0,Y0,X1,Y1),(255,214,10,95),4);tip=(X1,(Y0+Y1)/2)
        return tip
    tip1=sweep('lead',tb-.13,.42);tip2=sweep('key',ti-.13,.62)
    win=window(VW,VH+52,url='github.com/NandhaKishorM/laya');m=Image.new('L',(VW,VH));ImageDraw.Draw(m).rounded_rectangle((0,-20,VW-1,VH-1),radius=16,fill=255)
    view.putalpha(m);win.alpha_composite(view,(0,52))
    # cursor rides the active highlighter tip
    tip=tip2 or tip1
    if tip:_cursor(win,min(VW-50,tip[0]+6),min(VH-10,tip[1]+52+4))
    e=ease((t+.09)/.32);place(im,win,70,130+22*(1-e),.96+.04*e,e,True)
    return im

if __name__=='__main__':
    DEF={'base':.99,"isn't":1.65}
    at=lambda n,w,d=0,nth=0:DEF.get(w,d)
    ts=[.1,.6,.9,1.2,1.7,2.1,2.6];sheet=Image.new('RGB',(len(ts)*360,330),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.crop((0,100,1080,1090)).resize((360,330)).convert('RGB'),(i*360,0))
    sheet.save(Path(__file__).with_name('readme_zoom_strip.jpg'));print('readme_zoom_strip.jpg')
