"""The Claude Code desktop app, recreated with Pillow (Albert: "for creating the CLAUDE.md file mimic the UI of Claude").

Reference: the app as it looks on Albert's own screen (OBS capture of 23 Sep 2026): a warm off-white sidebar
(New / Artifacts / Routines / Customize, project groups underneath, "Albert · Max" at the bottom), a white main pane,
the prompt field "Type / for commands" with a "+" and a model chip ("Fable 5.1 · Medium") at the bottom right,
the terracotta asterisk mark. Nothing is a screenshot; the file editor is our own reading of a CLAUDE.md open in it.

app(w,h,t,editor) -> RGBA window. `editor` is a dict:
  lines   list of (text, style) already typed  ('h' heading, 'q' quoted rule, '' plain, 'k' code)
  typing  (full text, shown prefix, style) for the line being typed, or None
  tab     True when the CLAUDE.md tab exists;  tab_pop 0..1 spring for its entrance
  caret   True/False
  scroll  pixels the editor content is scrolled up
  picker  None or dict(open=0..1, hover=index, chosen='Opus 5.5'|None, chip='Fable 5.1')
  saved   0..1 green check on the tab
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
from brand import tile_claude

SIDE='#F5F3EE';INKS='#2B2A27';MUTED='#7A776F';LINE_='#E8E5DE';TERRA_='#D97757';CODE_BG='#F6F4EF'
MODELS=[('Fable 5.1','Most capable'),('Opus 5.5','Fable-level, 40% cheaper'),('Sonnet 5','Fast everyday work'),('Haiku 4.5','Quick lookups')]

def asterisk(size,color=TERRA_):
    q=4;im=blank(size*q,size*q);d=ImageDraw.Draw(im);c=size*q/2
    for k in range(4):
        a=k*math.pi/4;d.line([(c-math.cos(a)*c*.86,c-math.sin(a)*c*.86),(c+math.cos(a)*c*.86,c+math.sin(a)*c*.86)],fill=color,width=round(size*q*.18))
    return im.resize((size,size),Image.Resampling.LANCZOS)

def _sidebar(im,sw,h):
    d=ImageDraw.Draw(im);rr(im,(0,0,sw,h),SIDE,0)
    for i,c in enumerate(['#FF5F57','#FEBC2E','#28C840']):d.ellipse((18+i*20,17,30+i*20,29),fill=c)
    y=64
    for k,(glyph,lab) in enumerate([('+','New'),('◫','Artifacts'),('◷','Routines'),('✧','Customize')]):
        d.text((26,y),glyph,font=sf(19,'Medium'),fill=MUTED,anchor='lm');d.text((54,y),lab,font=sf(19,'Medium' if k==0 else 'Regular'),fill=INKS,anchor='lm');y+=34
    y+=22
    for lab in ['Routines','Delivery','Content Machine','ContentHouse']:
        d.text((26,y),lab,font=sf(16,'Medium'),fill=MUTED,anchor='lm');d.text((sw-22,y),'›',font=sf(18),fill=MUTED,anchor='rm');y+=30
    d.ellipse((20,h-40,44,h-16),fill='#D9D6CE');d.text((32,h-28),'A',font=sf(14,'Semibold'),fill=INKS,anchor='mm')
    d.text((54,h-28),'Albert',font=sf(16,'Medium'),fill=INKS,anchor='lm');d.text((112,h-28),'Max',font=sf(13),fill=MUTED,anchor='lm')

def _line_text(d,x,y,text,style,size,mono):
    if style=='h':d.text((x,y),text,font=sf(size,'Bold'),fill=INKS,anchor='lm')
    elif style=='q':
        d.text((x,y),text,font=sf(size,'Medium',True),fill=INKS,anchor='lm')
    elif style=='k':
        w=mono.getlength(text);rr_=(x-6,y-size*.62,x+w+6,y+size*.62);ImageDraw.Draw(d._image).rounded_rectangle(rr_,6,fill=CODE_BG);d.text((x,y),text,font=mono,fill='#B84A2E',anchor='lm')
    else:d.text((x,y),text,font=sf(size,'Regular',True),fill=INKS,anchor='lm')

def app(w,h,t,ed):
    im=blank(w,h);rr(im,(0,0,w-1,h-1),'white',16);sw=round(w*.19);_sidebar(im,sw,h);d=ImageDraw.Draw(im)
    d.line([(sw,0),(sw,h)],fill=LINE_,width=1)
    mx=sw;mw=w-sw
    # top bar: project chip + title
    d.text((mx+26,26),'⌂',font=sf(18),fill=MUTED,anchor='lm')
    rr(im,(mx+52,12,mx+52+118,40),'#F1EFE9',8);d.text((mx+111,26),'ContentHouse',font=sf(14,'Medium'),fill=INKS,anchor='mm')
    d.text((mx+190,26),'Opus 5.5 workflow',font=sf(15,'Medium'),fill=INKS,anchor='lm')
    # editor tab strip
    ty=64
    if ed.get('tab'):
        s=ed.get('tab_pop',1);tw_=178*s;tx=mx+26
        rr(im,(tx,ty-16,tx+tw_,ty+16),'#F1EFE9',9)
        if s>.6:
            im.alpha_composite(asterisk(16),(round(tx+12),ty-8));d.text((tx+36,ty),'CLAUDE.md',font=sf(16,'Semibold'),fill=INKS,anchor='lm')
            sv=ed.get('saved',0)
            if sv>0:checkmark(im,tx+tw_-18,ty,round(9*sv),GREEN)
            else:d.ellipse((tx+tw_-24,ty-5,tx+tw_-14,ty+5),fill='#C9C5BC')
    # editor body
    ex,ey=mx+26,ty+34;eh=h-ey-92;ew=mw-52;size=ed.get('size',24);lh=round(size*1.55);mono=sf(size-1,'Regular',True)
    body=blank(ew,eh);bd=ImageDraw.Draw(body);bd._image=body
    y=lh*.7-ed.get('scroll',0);n=1
    def gutter(yy):bd.text((28,yy),str(n),font=sf(size-6,'Regular',True),fill='#C4C0B6',anchor='rm')
    for text,style in ed.get('lines',[]):
        if -lh<y<eh+lh:
            gutter(y);_line_text(bd,52,y,text,style,size,mono)
        y+=lh;n+=1
    typ=ed.get('typing')
    if typ:
        text,s_,style=typ
        gutter(y);_line_text(bd,52,y,s_,style,size,mono)
        f=sf(size,'Bold' if style=='h' else ('Medium' if style=='q' else 'Regular'),style!='h' and style!='q' or True)
        cx=52+sf(size,'Medium',True).getlength(s_) if style!='k' else 52+mono.getlength(s_)
        if ed.get('caret',True) and int(t*3)%2==0:bd.rectangle((cx+3,y-size*.6,cx+6,y+size*.6),fill=TERRA_)
    elif ed.get('caret',False) and int(t*3)%2==0:
        gutter(y);bd.rectangle((52,y-size*.6,55,y+size*.6),fill=TERRA_)
    bd.line([(44,0),(44,eh)],fill=LINE_,width=1)
    im.alpha_composite(body,(ex,ey))
    # prompt field at the bottom
    py=h-70;rr(im,(mx+26,py-30,w-26,py+30),'white',14,'#DDD9D0',2)
    d.text((mx+48,py),'Type / for commands',font=sf(16),fill='#A5A198',anchor='lm')
    d.text((mx+44,py+46),'+',font=sf(18),fill=MUTED,anchor='lm');d.text((mx+72,py+46),'Auto',font=sf(14),fill=MUTED,anchor='lm')
    # model chip (bottom right) + picker
    pk=ed.get('picker') or {};chip=pk.get('chip','Fable 5.1')
    cw=sf(15,'Medium').getlength(chip)+sf(13).getlength('Medium')+44;cx0=w-26-cw
    rr(im,(cx0,py+32,cx0+cw,py+60),'#F1EFE9' if pk.get('open',0)<.5 else '#E7E4DC',9)
    d.text((cx0+14,py+46),chip,font=sf(15,'Medium'),fill=INKS,anchor='lm');d.text((cx0+14+sf(15,'Medium').getlength(chip)+8,py+46),'Medium',font=sf(13),fill=MUTED,anchor='lm')
    op=pk.get('open',0)
    if op>0:
        e=ease(op);ph=len(MODELS)*54+16;pw=330;px=w-26-pw;pyy=py+24-ph
        pop_=blank(pw,ph);rr(pop_,(0,0,pw-1,ph-1),'white',14,'#E3DFD6',2);pd=ImageDraw.Draw(pop_)
        for i,(nm,desc) in enumerate(MODELS):
            yy=8+i*54
            if pk.get('hover')==i:rr(pop_,(8,yy,pw-8,yy+50),'#F1EFE9',10)
            pd.text((22,yy+18),nm,font=sf(17,'Semibold'),fill=INKS,anchor='lm');pd.text((22,yy+38),desc,font=sf(13),fill=MUTED,anchor='lm')
            cur=(pk.get('chosen') or chip)==nm
            if cur:pd.text((pw-22,yy+25),'✓',font=sf(18,'Semibold'),fill=TERRA_,anchor='rm')
        place(im,pop_,px,pyy+12*(1-e),.96+.04*e,e,True)
    return im

if __name__=='__main__':
    ed={'tab':True,'tab_pop':1,'lines':[('Never do the work yourself.','q'),('Always dispatch a sub-agent.','q')],'typing':("Don't always use Fable.","Don't always u",'q'),'picker':{'open':1,'hover':1,'chip':'Fable 5.1'}}
    im=Image.new('RGBA',(1080,1920),BG);im.alpha_composite(app(940,560,.2,ed),(70,104));im.alpha_composite(app(940,810,.2,dict(ed,size=30)),(70,700))
    out=Path(__file__).resolve().parents[1]/'review/claudeapp.jpg';im.convert('RGB').save(out);print(out)
