"""services beat: the Foundation Capital article recreated -> camera push-in -> yellow highlighter on the source line.

"in services every single year."

The $4.6 trillion figure in the script is Foundation Capital's (Joanne Chen & Jaya Gupta, "AI leads a service as
software paradigm shift", 19 Apr 2024, also run by Forbes): "The push towards services represents a $4.6 trillion
opportunity." The page is drawn once at 2x from the live page as scraped 22 Sep 2026 (announcement bar, nav, the
PERSPECTIVES eyebrow, the H1, byline, tags, the italic lead and the first paragraph); the market-map hero image is
skipped - this is a recreation, not a capture. The Safari window carries the real URL, the camera pushes in with
smooth() and the highlighter sweeps "push towards services" on "services" and "$4.6 trillion opportunity" across
"every single year", the cursor riding the tip.

render(t, at) -> 1080x1920 RGBA, split-panel geometry (panel 940x560 at (70,104)).
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
K=2;PW,PH_=940,760;VW,VH=940,508
FC_INK='#0B0B0C';FC_MUTED='#5B5B60';FC_LINE='#E4E4E7';FC_NAVY='#0B1B45'
HL={}

def F(n,wt='Regular'):return sf(n*K,wt)
def _rich(im,segs,x,y,maxw,size=21,lh=33,color=FC_INK):
    """Word-wrapped rich text. segs: (text, style, hl_id). Records highlight boxes per line in HL."""
    d=ImageDraw.Draw(im);sp=F(size).getlength(' ')/K;cx=x;cy=y;runs={}
    for text,style,hid in segs:
        f=F(size,'Semibold') if style=='b' else F(size)
        for wd in text.split(' '):
            if not wd:continue
            ww=f.getlength(wd)/K
            if cx+ww>x+maxw and cx>x:cx=x;cy+=lh
            d.text((cx*K,cy*K),wd,font=f,fill=color,anchor='ls')
            if hid:
                key=(hid,cy);b=runs.get(key)
                runs[key]=[min(b[0],cx) if b else cx,cy-size*.80,max(b[2],cx+ww) if b else cx+ww,cy+size*.30]
            cx+=ww+sp
    for (hid,_),b in sorted(runs.items(),key=lambda kv:kv[0][1]):HL.setdefault(hid,[]).append(tuple(b))
    return cy+lh

def _italic(layer):
    """Fake italic: shear the rendered line 12 degrees (SF Pro has no italic axis in the system file)."""
    w,h=layer.size;sh=.2;return layer.transform((w+int(h*sh),h),Image.Transform.AFFINE,(1,sh,-h*sh,0,1,0),resample=Image.Resampling.BICUBIC)

@lru_cache(None)
def page():
    HL.clear();im=Image.new('RGBA',(PW*K,PH_*K),'white');d=ImageDraw.Draw(im)
    # ---- announcement bar + nav (as on the live page)
    d.rectangle((0,0,PW*K,26*K),fill=FC_NAVY)
    d.text(((PW/2)*K,13*K),'Congratulations to Cerebras on their IPO! We wrote their first term sheet in 2016.   Read More',font=F(11),fill='white',anchor='mm')
    # logo: mark + two-line wordmark
    d.rounded_rectangle((26*K,40*K,50*K,64*K),radius=5*K,fill=FC_INK);d.text((38*K,52*K),'F',font=F(15,'Bold'),fill='white',anchor='mm')
    d.text((58*K,46*K),'foundation',font=F(12,'Semibold'),fill=FC_INK,anchor='lm');d.text((58*K,60*K),'capital',font=F(12,'Semibold'),fill=FC_INK,anchor='lm')
    x=PW-30
    for lab in ['Credo','Ideas','Build','Practices ▾','Portfolio','Team ▾']:
        w_=F(13).getlength(lab)/K;x-=w_;d.text((x*K,53*K),lab,font=F(13),fill=FC_INK,anchor='lm');x-=26
    d.line([(0,80*K),(PW*K,80*K)],fill=FC_LINE,width=K)
    # ---- eyebrow pill
    rr(im,(30*K,112*K,138*K,134*K),None,11*K,'#C9C9CE',K);d=ImageDraw.Draw(im)
    d.text((44*K,123*K),'✦',font=F(11),fill=FC_MUTED,anchor='lm');d.text((60*K,123*K),'PERSPECTIVES',font=F(10,'Medium'),fill=FC_INK,anchor='lm')
    # ---- H1 (light, two lines, as on the page)
    d.text((28*K,196*K),'AI leads a service as software',font=F(50,'Light'),fill=FC_INK,anchor='ls')
    d.text((28*K,252*K),'paradigm shift',font=F(50,'Light'),fill=FC_INK,anchor='ls')
    # ---- byline row
    y=300;d.text((30*K,y*K),'POSTED APR 19, 2024',font=F(11,'Medium'),fill=FC_MUTED,anchor='ls')
    for i,(nm,col) in enumerate([('Joanne Chen','#C9A27E'),('Jaya Gupta','#8E9AA8')]):
        xx=30+i*160;d.ellipse((xx*K,(y+14)*K,(xx+30)*K,(y+44)*K),fill=col);d.text(((xx+38)*K,(y+29)*K),nm,font=F(13,'Medium'),fill=FC_INK,anchor='lm')
    d.text((30*K,(y+72)*K),'8 MIN READ',font=F(11,'Medium'),fill=FC_MUTED,anchor='ls')
    for i,tag in enumerate(['Enterprise','AI']):
        xx=140+i*100;w_=F(12).getlength(tag)/K+24;rr(im,(xx*K,(y+58)*K,(xx+w_)*K,(y+80)*K),None,11*K,'#C9C9CE',K);ImageDraw.Draw(im).text(((xx+w_/2)*K,(y+69)*K),tag,font=F(12),fill=FC_INK,anchor='mm')
    d=ImageDraw.Draw(im)
    for i,ic in enumerate(['✉','𝕏','@']):
        xx=PW-30-(2-i)*40;d.ellipse(((xx-14)*K,(y+54)*K,(xx+14)*K,(y+82)*K),outline='#C9C9CE',width=K);d.text((xx*K,(y+68)*K),ic,font=F(12),fill=FC_INK,anchor='mm')
    d.line([(30*K,(y+100)*K),((PW-30)*K,(y+100)*K)],fill=FC_LINE,width=K)
    # ---- the italic lead (the sourced sentence) - rendered on its own layer, sheared, then the highlight boxes recorded
    global LEADY;LEADY=y+124
    lay=Image.new('RGBA',(PW*K,60*K));_rich(lay,[('The push towards',None,None),('services',None,'svc'),('represents a',None,None),('$4.6 trillion opportunity.',None,'num')],30,40,PW-60,21,33,FC_INK)
    im.alpha_composite(_italic(lay),(0,(LEADY-40)*K))
    # highlight boxes were recorded in lay coordinates (y from 40); shift them to page coordinates
    for hid in ('svc','num'):HL[hid]=[(b[0]+2,b[1]+LEADY-40,b[2]+6,b[3]+LEADY-40) for b in HL[hid]]
    # ---- first paragraphs (real copy)
    yy=_rich(im,[('Past decades of automation were all about efficiency: a machine helped a human speed up a variety of tasks. The current decade is where efficiency takes an AI-fueled leap forward, and things get exponentially messier. Software once merely digitized and augmented human work and services, but in automation 2.0, bots become brains.',None,None)],30,LEADY+52,PW-60,19,30,'#2A2A2E')
    yy=_rich(im,[('AI companies are leading a transition from software as a service to service as software, turning the table on the very essence of SaaS. In the software business, a company may sell access to its platform or tool, but customers are still responsible for using that tool to achieve the desired outcome. In the services business, responsibility for achieving the desired outcome sits with the company selling the service. Instead of QuickBooks, you offer tax services—in this case, conducted by an AI accountant.',None,None)],30,yy+12,PW-60,19,30,'#2A2A2E')
    return im

def _cursor(im,x,y):
    pts=[(x,y),(x+5,y+44),(x+16,y+33),(x+27,y+51),(x+37,y+44),(x+27,y+27),(x+42,y+24)]
    ImageDraw.Draw(im).polygon(pts,fill='white',outline=INK,width=3)

def render(t,at):
    im=blank(W,H);pg=page()
    ts=at('services','services',.25);te=at('services','every',1.05);ty=at('services','year.',2.43)
    z0=.02;z=smooth((t-z0)/.50)                                       # push-in over the first half second
    Z=1.55;tw_,th=VW/Z,VH/Z
    wide=(0,0,VW,VH);tgt=(0,LEADY-th*.42,tw_,th)
    pre=14*smooth(t/.5)
    vx=lerp(wide[0],tgt[0],z);vy=lerp(wide[1]+pre,tgt[1],z);vw=lerp(wide[2],tgt[2],z);vh=lerp(wide[3],tgt[3],z)
    vy+=10*smooth((t-te)/1.4)                                         # slow tilt with the long second sweep
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
    tip1=sweep('svc',max(z0+.50,ts+.02),.30);tip2=sweep('num',te-.13,ty-te+.13)
    win=window(VW,VH+52,url='foundationcapital.com/ideas/ai-leads-a-service-as-software-paradigm-shift');m=Image.new('L',(VW,VH));ImageDraw.Draw(m).rounded_rectangle((0,-20,VW-1,VH-1),radius=16,fill=255)
    view.putalpha(m);win.alpha_composite(view,(0,52))
    tip=tip2 or tip1
    if tip:_cursor(win,min(VW-50,tip[0]+6),min(VH-10,tip[1]+52+4))
    e=ease((t+.09)/.32);place(im,win,70,104+22*(1-e),.96+.04*e,e,True)
    return im

if __name__=='__main__':
    DEF={'services':.25,'every':1.05,'year.':2.43}
    at=lambda n,w,d=0,nth=0:DEF.get(w,d)
    ts=[.02,.3,.55,.8,1.2,1.8,2.4];sheet=Image.new('RGB',(len(ts)*360,240),BG)
    for i,t in enumerate(ts):
        f=Image.new('RGBA',(W,H),BG);f.alpha_composite(render(t,at));sheet.paste(f.crop((0,80,1080,720)).resize((360,213)).convert('RGB'),(i*360,0))
    sheet.save(Path(__file__).with_name('article_zoom_strip.jpg'));print('article_zoom_strip.jpg')
