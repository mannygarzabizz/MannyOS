"""Scenes for the Opus 5.5 / CLAUDE.md reel (23 Sep 2026).

Every surface is recreated with Pillow - no screenshots. Product-true material and sources:
  * Dario Amodei / Sam Altman portraits: Wikimedia Commons, CC BY 2.0 (UK Prime Minister's Office 2023; TechCrunch SF 2019)
  * Claude / ChatGPT / Gemini tiles: the official App Store icons (iTunes Search API artwork) + the template's Claude tile
  * "Astra" = OpenAI's GPT-6 Astra (launched 3 Sep 2026, TechCrunch/CNBC); "Opus 5.5" = Claude Opus 5.5, announced
    22 Sep 2026 at anthropic.com/claude-opus-5-5: "performs at the level of Claude Fable 5.1 on most work and costs 40% less
    to run than Opus 5", "generates output more than 30% faster than Opus 5" - the three pills under the wordmark quote that page.
  * The Claude Code app window (parts/claudeapp.py) follows the app on Albert's own screen (sidebar, prompt field,
    "Fable 5.1 · Medium" model chip). The model picker lists Fable 5.1 / Opus 5.5 / Sonnet 5 / Haiku 4.5 - the current models.
  * Sub-agent model selection is real: code.claude.com/docs/en/sub-agents - a subagent's model comes from the per-invocation
    `model` parameter Claude passes when delegating, then the agent's `model` frontmatter (sonnet/opus/haiku/fable or a full id).
  * The CLAUDE.md lines on screen are the prompt Albert dictates plus the "rest of this prompt" he promises in the DM (this
    project's CLAUDE-md-prompt.md). No numbers on screen are invented: the only figures are the announcement's 40% / 30%.
  * Memes: Giphy 6f15PceJUw8WGlj4uu (The Office, "if you're like me") and the Pinterest Wolf of Wall Street dance GIF
    (celebration on "And boom") - both linked by Albert; played as 30 fps frame sequences in rounded cards.

Scene coordinates are the pre-TOP_SHIFT canvas: split graphics live in y 100..700 (panel 940x560 at (70,104)),
full-screen UI in y 120..930 with the cinematic words underneath.
"""
from draw import *
import sys,math,random
import numpy as np
sys.path.insert(0,str(P/'helpers'));sys.path.insert(0,str(P/'parts'))
import instagram_comment,pointer_motion
import bazooka as _hook_part
import claudeapp
from brand import *
from brand import _ring,_mask

LEAD=.13
GREEN_D='#1E8E3E';SOFT_GREY='#8E8E93'
_S={}                                                             # beats (name -> start/end), set by graphics()

def enter0(im,obj,x,y,t,sh=True):
    """Entrance already part-way in at t=0, so a cut into a beat is never blank."""
    e=ease((t+.09)/.32);place(im,obj,x,y+22*(1-e),.96+.04*e,e,sh)
def pop(v):return spring(max(0,min(1,v)))
def card(w=940,h=560,fill='white',r=30):return panel(w,h,fill,r)
def clamp(v):return max(0,min(1,v))
def typed(text,onsets,t,tail=.22):
    """Prefix of `text` typed word by word: word k's letters appear between onsets[k] and min(onsets[k+1], onsets[k]+tail)."""
    words=text.split(' ');out=[]
    for k,wd in enumerate(words):
        t0=onsets[k];t1=min(onsets[k+1],t0+tail) if k+1<len(onsets) else t0+tail
        if t<t0:break
        frac=1 if t>=t1 else (t-t0)/max(1e-6,t1-t0);n=max(1,round(len(wd)*frac));out.append(wd[:n])
        if n<len(wd):break
    return ' '.join(out)

# ---- GIF memes as 30 fps frame folders (assets/gif/<name>/NNN.jpg) ---------------------------------------------
@lru_cache(None)
def _gif_files(name):return sorted((P/'assets/gif'/name).glob('*.jpg'))
@lru_cache(maxsize=256)
def _gif_frame(name,i,w,crop=None):
    files=_gif_files(name);fr=Image.open(files[i%len(files)]).convert('RGBA')
    if crop:fr=fr.crop(tuple(round(v*fr.width) for v in crop))         # crop as fractions of the frame width
    if fr.width!=w:fr=fr.resize((w,round(fr.height*w/fr.width)),Image.Resampling.LANCZOS)
    m=Image.new('L',fr.size);ImageDraw.Draw(m).rounded_rectangle((0,0,fr.width-1,fr.height-1),26,fill=255);fr.putalpha(m);return fr
def gif_card(name,t,w,crop=None):return _gif_frame(name,int(max(0,t)*30),w,crop)

# ---- shared props ---------------------------------------------------------------------------------------------
@lru_cache(None)
def doc_icon(w=120,h=150):
    """A CLAUDE.md document: white sheet with a folded corner, the terracotta asterisk and the file name."""
    q=3;im=blank(w*q,h*q);d=ImageDraw.Draw(im);k=q;f=22*k
    d.polygon([(0,0),(w*k-f,0),(w*k,f),(w*k,h*k),(0,h*k)],fill='white');d.polygon([(w*k-f,0),(w*k-f,f),(w*k,f)],fill='#E6E2D6')
    d.line([(0,0),(w*k-f,0),(w*k,f),(w*k,h*k-1),(0,h*k-1),(0,0)],fill='#D6D2C8',width=2*k)
    im=im.resize((w,h),Image.Resampling.LANCZOS);im.alpha_composite(claudeapp.asterisk(round(w*.34)),(round(w*.33),round(h*.24)))
    ImageDraw.Draw(im).text((w/2,h*.78),'CLAUDE.md',font=sf(15,'Semibold'),fill=INK,anchor='mm');return im

def chip(text,fill='#F1EFE9',fg=INK,n=22,weight='Semibold',icon=None,pad=18,h=48):
    f=sf(n,weight);w=f.getlength(text)+pad*2+(h-14+8 if icon is not None else 0);im=blank(round(w),h);rr(im,(0,0,w-1,h-1),fill,h/2)
    x=pad
    if icon is not None:im.alpha_composite(icon.resize((h-14,h-14),Image.Resampling.LANCZOS),(pad-4,7));x+=h-14+8
    ImageDraw.Draw(im).text((x,h/2),text,font=f,fill=fg,anchor='lm');return im

def sweep(c,t,t0=0,speed=520,band=170,alpha=70):
    """A soft diagonal light band gliding across a card from t0 on (keeps a waiting surface alive)."""
    if t<t0:return
    w,h=c.size;x=((t-t0)*speed)%(w+band*2+h)-band-h;lay=blank(w,h)
    ImageDraw.Draw(lay).polygon([(x,0),(x+band,0),(x+band+h*.6,h),(x+h*.6,h)],fill=(255,255,255,alpha));c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18)))
def usage_bar(im,x,y,w,h,val,col,t=None):
    rr(im,(x,y,x+w,y+h),'#ECEBE7',h/2)
    if val>0:rr(im,(x,y,x+max(h,w*val),y+h),col,h/2)

# ---------------------------------------------------------------- 1. hook (full): Dario bazookas Sam --------------
def hook(t,at):return _hook_part.render(t,at)

# ---------------------------------------------------------------- 2. opus (full): the tile drops ------------------
PILLS=['Sep 22, 2026','40% cheaper than Opus 5','30% faster output']    # anthropic.com/claude-opus-5-5, 22 Sep 2026
# ---------------------------------------------------------------- 2. opus (full): the tile drops ------------------
def opus(t,at):
    """v2 (Albert: "make the drop faster, there is a delay after the transition; remove the things under Claude Opus 5.5"):
    the tile is already falling as the smoke clears and LANDS ON "Opus" (squash, dust, kick, thud) - the landing writes the
    wordmark; "5.5" pops on its word; on "just" the tile jumps and lands a second time on "dropped". No pills."""
    im=blank(W,H)
    topus=at('opus','Opus',1.13)-LEAD;t55=at('opus','5.5',1.65)-LEAD;tjust=at('opus','just',2.41)-LEAD;tdrop=at('opus','dropped,',2.71)-.05
    GYL=560;TS=340;cx=W/2;y1=GYL-TS;g=ease((t-.15)/.35)
    if g>0:line(im,[(cx-460*g,GYL+6),(cx+460*g,GYL+6)],'#DEDCD4',3)
    d=ImageDraw.Draw(im);f=sf(92,'Bold');lab='Claude Opus';w1=f.getlength(lab);w2=f.getlength(' 5.5');x0=cx-(w1+w2)/2
    if t>topus:d.text((x0,670),reveal(lab,t-topus,.34),font=f,fill=INK,anchor='lm')
    if t>t55:
        sc=pop((t-t55)/.28);num=blank(270,130);ImageDraw.Draw(num).text((135,65),'5.5',font=f,fill=TERRA,anchor='mm')
        place(im,num,x0+w1+w2/2+f.getlength(' ')/2-135,670-65,max(.05,sc),min(1,sc*2),False)
    # first fall: free fall from above the frame, landing exactly on "Opus"
    TF=math.sqrt(2*(y1+400)/2600);tstart=topus-TF;land2=tdrop;jump=tjust
    if t<topus:y=-400+.5*2600*(t-tstart)**2 if t>tstart else -400;sq=0;landed=None
    elif t<jump:y=y1;landed=topus
    elif t<land2:                                                    # the jump: up 120 px and back down, landing on "dropped"
        u=(t-jump)/max(.12,land2-jump);y=y1-120*math.sin(math.pi*u);landed=None
    else:y=y1;landed=land2
    sqv=math.exp(-(t-landed)/.10)*math.cos((t-landed)*28) if landed is not None else 0
    sy=1-.16*sqv;sx=1+.12*sqv;tl=tile_claude(TS)
    if landed is None and jump<=t<land2:                             # shadow shrinks while it is in the air
        r=140-60*math.sin(math.pi*(t-jump)/max(.12,land2-jump));shd=blank(round(r*2+40),90);ImageDraw.Draw(shd).ellipse((20,30,r*2+20,70),fill=(0,0,0,60));im.alpha_composite(shd.filter(ImageFilter.GaussianBlur(12)),(round(cx-r-20),GYL-46))
    if sx!=1 or sy!=1:tl=tl.resize((max(1,round(TS*sx)),max(1,round(TS*sy))),Image.Resampling.LANCZOS)
    if y>-TS:place(im,tl,cx-tl.width/2,y+TS-tl.height,1,1,True)
    for tl_ in (topus,land2):                                        # dust puffs on both landings
        if t>=tl_:
            v=t-tl_
            for sgn in (-1,1):
                for k in range(3):
                    r=12+v*110+k*6;op=max(0,1-v/.34);px=cx+sgn*(TS/2+16+v*380+k*20);py=GYL-8-v*50-k*8
                    if op>0:
                        pf=blank(round(r*2+6),round(r*2+6));ImageDraw.Draw(pf).ellipse((3,3,r*2+3,r*2+3),fill=(190,186,178,round(140*op)));im.alpha_composite(pf.filter(ImageFilter.GaussianBlur(4)),(round(px-r),round(py-r)))
    hit=at('hook','Astra',.94)-.05;hd=_S['hook']['end']-_S['hook']['start']
    _hook_part.explosion(im,(hd-hit)+t)
    for tl_ in (topus,land2):
        if tl_<t<tl_+.07:out=blank(W,H);out.alpha_composite(im,(0,8));return out
    return im
# ---------------------------------------------------------------- 3. solves (split): the issue inside the frontier models
FRONTIER=[('Claude',lambda z:tile_claude(z)),('ChatGPT',lambda z:tile_app('ChatGPT-app',z)),('Gemini',lambda z:tile_app('Gemini',z))]
def solves(t,at):
    im=blank(W,H);c=card();tmass=at('solves','massive',.71)-LEAD;tiss=at('solves','issue',1.11)-LEAD;tfr=at('solves','frontier',1.87)-LEAD;tmod=at('solves','models.',2.37)-LEAD
    TS=150;xs=[190,470,750];d=ImageDraw.Draw(c)
    fill=smooth((t-tmass)/.32) if t>tmass else 0;val=.35+.65*fill;limit=val>.92
    shake=(math.sin((t-tiss)*48)*7*max(0,1-(t-tiss)/.32)) if t>tiss else 0
    for i,(nm,fn) in enumerate(FRONTIER):
        e=pop((t+.12-i*.07)/.3);hop=0
        for th in (tfr,tmod):
            if t>th+i*.06:hop+=math.sin(math.pi*clamp((t-th-i*.06)/.3))*24
        place(c,fn(TS),xs[i]-TS/2+shake*(1 if i%2 else -1)*.4,70-hop,max(.05,e),min(1,e*2),True)
        d=ImageDraw.Draw(c);d.text((xs[i],262),nm,font=sf(26,'Semibold'),fill=INK,anchor='mm')
        usage_bar(c,xs[i]-130+shake,318,260,20,val,RED if limit else '#8E8E93')
        lab='Limit reached' if limit else 'Usage';d.text((xs[i]+shake,372),lab,font=sf(22,'Semibold' if limit else 'Regular'),fill=RED if limit else GRAY,anchor='mm')
    if limit and t>tiss:                                                # red frame springs around the whole row on "issue", then breathes
        s=pop((t-tiss)/.26);br=1+.012*math.sin((t-tiss)*7);fr=blank(940,560);rr(fr,(40,30,900,410),None,26,RED,5);place(c,fr,0,0,(.97+.03*s)*br,min(1,s*2),False)
        sweep(c,t,tiss+.3)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 4. likeme (full): the meme + the limit banner ---------
DAYS=['M','T','W','T','F','S','S']
# ---------------------------------------------------------------- 4. likeme (full): the meme + Claude flips the limit off
LIKEME_CROP=(0,50/480,1,320/480)                                     # 16:9 window of the Office GIF: face kept, Peacock mark cut
TER_H=(217,119,87);TER_D=(190,96,60);TER_L=(236,152,120);TER_O=(150,72,42)
@lru_cache(None)
def fist(ext):
    """Drawn terracotta fist giving the finger (v6: "make the middle finger smaller"). Canvas 220x270 at 4x: a rounded fist,
    four folded knuckles on top, a short thick middle finger rising from the second knuckle (ext 0..1), the thumb wrapped in
    front, a wrist stub under it. Outline = every shape drawn once in the dark tone 3 px larger, then in terracotta."""
    k=4;im=blank(220*k,270*k);d=ImageDraw.Draw(im);L=12+90*ext;top=112-L
    shapes=[((30,112,190,214),42),((84,top,124,168),20),((34,94,80,142),20),((118,96,160,142),19),((156,108,192,150),16),((22,146,102,190),22)]
    for (x0,y0,x1,y1),r in shapes:d.rounded_rectangle(((x0-3)*k,(y0-3)*k,(x1+3)*k,(y1+3)*k),radius=(r+3)*k,fill=TER_O)
    for (x0,y0,x1,y1),r in shapes:d.rounded_rectangle((x0*k,y0*k,x1*k,y1*k),radius=r*k,fill=TER_H)
    for x,y0,y1 in ((82,114,146),(120,114,148),(158,120,150)):d.line([(x*k,y0*k),(x*k,y1*k)],fill=TER_O,width=3*k)    # creases between knuckles
    d.arc((26*k,146*k,100*k,190*k),start=200,end=340,fill=TER_O,width=3*k)                                        # thumb crease
    if ext>.45:
        for yy in (top+34,top+66):d.arc((88*k,(yy-6)*k,120*k,(yy+6)*k),start=200,end=340,fill=TER_O,width=3*k)   # knuckle creases
        d.rounded_rectangle((92*k,(top+10)*k,100*k,(top+78)*k),radius=4*k,fill=TER_L)                              # highlight
    sh=blank(220*k,270*k);ImageDraw.Draw(sh).rounded_rectangle((34*k,190*k,186*k,214*k),radius=22*k,fill=TER_D+(80,));im.alpha_composite(sh)
    return im.resize((220,270),Image.Resampling.LANCZOS)
def likeme(t,at):
    """v4 (Albert: "make the fuck finger smaller and him hold it out to the right of him with an arm"): the Claude tile sits
    under the meme; on "usage" a terracotta arm extends out to his right with a closed fist, on "limit" the middle finger
    flicks up (spring), the arm pumps on "one" and "day", pumps higher and wags on "reset". Hand at 0.6x, fully below the card."""
    im=blank(W,H);tus=at('likeme','usage',1.73)-LEAD;tlim=at('likeme','limit',2.05)-LEAD;tone=at('likeme','one',2.47)-LEAD;tday=at('likeme','day',2.69)-LEAD;treset=at('likeme','reset.',3.29)-LEAD
    g=gif_card('likeme',t,940,LIKEME_CROP);e=pop((t+.12)/.34);place(im,g,70,120+16*(1-e),max(.05,.94+.06*e),min(1,e*2),True)
    TS=160;tx,ty=400,830
    rise=pop((t-tus)/.36) if t>tus else 0;ext=pop((t-tlim)/.26) if t>tlim else 0
    pump=0
    for tp,h in ((tone,16),(tday,16),(treset,28)):
        if t>tp:pump+=h*math.sin(math.pi*clamp((t-tp)/.28))
    wag=(math.sin((t-treset)*20)*10*max(0,1-(t-treset)/.55)) if t>treset else 0
    rock=(math.sin((t-tone)*11)*4*max(0,1-(t-tone)/.7)) if t>tone else 0
    if rise>0:                                                       # a short arm out to the right, the hand at its end
        sc=.62;hd=fist(round(ext*20)/20);hd=hd.resize((round(hd.width*sc),round(hd.height*sc)),Image.Resampling.LANCZOS)
        ax=tx+TS+24+96*rise;ay=ty+TS*.62-TS*.16*rise-pump
        p0=(tx+TS-10,ty+TS*.58);p1=((p0[0]+ax)/2,p0[1]+36-40*rise);pts=_hook_part._bez(p0,p1,(ax,ay),48)
        d_=ImageDraw.Draw(im)
        for r,col in ((14.5,TER_O),(13,TER_H)):                      # a smooth tube: overlapping discs along the curve; 1.5 px outline like the hand's
            for (px,py) in pts:d_.ellipse((px-r,py-r,px+r,py+r),fill=col)
        place(im,hd,ax-110*sc,ay-198*sc,1,1,False,rot=wag*(.5+.5*ext))   # the fist sits on top of the arm's end
    place(im,tile_claude(TS),tx,ty+6*math.sin(t*4)*(1-rise),1,1,True,rot=rock)
    return im
# ---------------------------------------------------------------- 5. but (split): Opus 5.5 drains the bar, the giga brain
@lru_cache(None)
def brain(size):return Image.open(P/'assets/icons/fluent/brain.png').convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
def but(t,at):
    """v5 (Albert: "when I say 'if you do this' then show this only" - the Tenor "think about it, use your brain" GIF):
    tile + bar drain + check as before, then on "if" the whole panel becomes the meme (square GIF cover-cropped to the
    940x560 panel, rounded corners); nothing else is shown with it."""
    im=blank(W,H);c=card();topus=at('but','Opus',.37)-LEAD;tsolve=at('but','solve',1.41)-LEAD;tit=at('but','it',1.71)-LEAD;tif=at('but','if',1.97)-LEAD
    t55=at('but','5.5',.79)-LEAD;tcan=at('but','can',1.21)-LEAD
    d=ImageDraw.Draw(c);e=pop((t-topus)/.3) if t>topus else 0
    bounce=1+.14*math.sin(math.pi*clamp((t-t55)/.3)) if t>t55 else 1;hop=math.sin(math.pi*clamp((t-tcan)/.32))*30 if t>tcan else 0
    if e>0:place(c,tile_claude(170),70,90-hop,max(.05,e)*bounce,min(1,e*2),True);d=ImageDraw.Draw(c);d.text((155,300),'Opus 5.5',font=sf(30,'Semibold'),fill=INK,anchor='mm')
    dr=smooth((t-tsolve)/.42) if t>tsolve else 0;val=(1-.86*dr)*(1-.025*(1+math.sin(t*9))*(1-dr));col=RED if val>.6 else GREEN
    d.text((300,120),'Usage limit',font=sf(26,'Semibold'),fill=INK,anchor='lm')
    usage_bar(c,300,150,580,28,val,col)
    if t>tit:sc=pop((t-tit)/.26);checkmark(c,300+580*.14+40,164,round(18*sc),GREEN)
    if t>tif:                                                        # the meme takes the whole panel
        u=t-tif;sc=pop(u/.3);fr=_gif_frame('usebrain',int(u*30),940)
        ch=round(560*fr.width/940);fr=fr.crop((0,(fr.height-ch)//2-40,fr.width,(fr.height-ch)//2-40+ch))
        m_=Image.new('L',fr.size);ImageDraw.Draw(m_).rounded_rectangle((0,0,fr.width-1,fr.height-1),30,fill=255);fr.putalpha(m_)
        place(c,fr,0,0,max(.05,.94+.06*sc),min(1,u/.08),False)
    enter0(im,c,70,104,t);return im
# ---------------------------------------------------------------- 6. create (split): the file appears in Claude Code ----
def create(t,at):
    im=blank(W,H);tcl=at('create','CLAUDE.md',.67)-LEAD;tfile=at('create','file',1.49)-LEAD
    ed={'tab':t>tcl,'tab_pop':pop((t-tcl)/.3),'lines':[],'typing':None,'caret':t>tfile-.1,'size':24}
    w=claudeapp.app(940,560,t,ed)
    pointer_motion.motion(w,t,points=[(0,420,300),(.22,80,64),(.30,80,64),(tcl+.1,260,120),(tfile-.05,330,168),(tfile+.15,330,168),(tfile+.7,360,190)],clicks=[.26,tfile],end=tfile+.9)
    enter0(im,w,70,104,t);return im

# ---------------------------------------------------------------- 7-9. the CLAUDE.md gets written -------------------------
L1='Never do the work yourself.';L2='Always dispatch a sub-agent.';L3="Don't always use Fable.";L4='Use Opus 5.5 for easier tasks.'
REST=[('# Model routing','h'),('- Fable 5.1: architecture, hard bugs, review',''),('- Opus 5.5: edits, tests, docs, refactors',''),
      ('- Haiku 4.5: lookups and summaries',''),('- Pass `model` on every Agent call',''),('# Delegation','h'),
      ('- One sub-agent per task, plan first',''),('- Run independent sub-agents in parallel',''),('- Read the report, never the files','')]
def write1(t,at):
    im=blank(W,H);o1=[at('write1',w_,d_)-LEAD for w_,d_ in (('"Never',.55),('do',.77),('the',.91),('work',1.01),('yourself.',1.19))]
    o2=[at('write1',w_,d_)-LEAD for w_,d_ in (('Always',1.79),('dispatch',2.21),('a',2.69),('sub-agent."',2.79))];tsub=o2[-1]
    p1=typed(L1,o1,t);p2=typed(L2,o2,t)
    ed={'tab':True,'tab_pop':1,'size':30,'lines':[],'typing':None,'caret':True}
    if len(p1)<len(L1):ed['typing']=(L1,p1,'q')
    else:
        ed['lines']=[(L1,'q')]
        if t>o2[0]:ed['typing']=(L2,p2,'q')
    w=claudeapp.app(940,810,t,ed)
    if t>tsub:                                                           # a sub-agent chip pops next to the line
        s=pop((t-tsub)/.28);ch=chip('sub-agent',TERRA,'white',22,'Semibold',tile_claude(40),16,46);place(w,ch,600,208+8*(1-s)+5*math.sin((t-tsub)*5),max(.05,s),min(1,s*3),True)
    enter0(im,w,70,120,t);return im

def _picker(t,at):
    tuse=at('write2','Use',2.41,1)-LEAD;topus=at('write2','Opus',2.69)-LEAD;t55=at('write2','5.5',3.15)-.05   # nth=1: the first 'use' is in "Don't always use Fable"
    op=ease((t-tuse)/.22) if t>tuse else 0
    if t>t55:op=1-ease((t-t55)/.18)
    hover=1 if t>t55-.22 else (0 if t>tuse+.14 else None)
    return {'open':op,'hover':hover,'chosen':'Opus 5.5' if t>t55 else None,'chip':'Opus 5.5' if t>t55 else 'Fable 5.1'},tuse,topus,t55
def write2(t,at):
    im=blank(W,H);o3=[at('write2',w_,d_)-LEAD for w_,d_ in (('"Don\'t',.93),('always',1.17),('use',1.55),('Fable.',1.79))]
    o4=[at('write2',w_,d_,n_)-LEAD for w_,d_,n_ in (('Use',2.41,1),('Opus',2.69,0),('5.5',3.15,0),('for',3.71,0),('easier',3.89,0),('tasks."',4.29,0))]
    p3=typed(L3,o3,t);p4=typed(L4,o4,t);pk,tuse,topus,t55=_picker(t,at)
    ed={'tab':True,'tab_pop':1,'size':24,'lines':[(L1,'q'),(L2,'q')],'typing':None,'caret':True,'picker':pk}
    if len(p3)<len(L3):ed['typing']=(L3,p3,'q')
    else:
        ed['lines'].append((L3,'q'))
        if t>o4[0]:ed['typing']=(L4,p4,'q')
    w=claudeapp.app(940,560,t,ed);teas=o4[4]
    if t>teas:                                                           # banner: the model change is confirmed
        u=t-teas;e2=ease(u/.3);nb=blank(330,84);rr(nb,(0,0,329,83),(255,255,255,240),18,'#E3DFD6',2);nb.alpha_composite(tile_claude(44),(16,20))
        ImageDraw.Draw(nb).text((74,30),'Model changed',font=sf(18,'Semibold'),fill=INK,anchor='lm');ImageDraw.Draw(nb).text((74,56),'Sub-agents default to Opus 5.5',font=sf(15),fill='#3A3A3C',anchor='lm')
        checkmark(nb,300,42,round(12*pop(u/.3)),GREEN);place(w,nb,940-346+40*(1-e2),330,1,e2,True)
    cx,cy=846,536;rx,ry=749,369                                          # model chip centre, "Opus 5.5" row centre (window coords)
    pointer_motion.motion(w,t,points=[(tuse-1.85,720,290),(tuse-1.35,560,410),(tuse-.85,680,470),(tuse-.4,600,500),(tuse-.05,cx,cy),(tuse+.12,cx,cy),(tuse+.34,rx,315),(t55-.28,rx,315),(t55-.08,rx,ry),(t55+.12,rx,ry),(teas,700,250),(teas+.55,790,372),(teas+1.2,700,300)],clicks=[tuse,t55],end=teas+1.3)
    enter0(im,w,70,104,t);return im

def rest(t,at):
    im=blank(W,H);tinc=at('rest','include',.71)-LEAD;tcl=at('rest','CLAUDE.md',2.15)-LEAD
    lines=[(L1,'q'),(L2,'q'),(L3,'q'),(L4,'q')];n=0
    if t>tinc:n=min(len(REST),int((t-tinc)/.11)+1);lines+=REST[:n]
    size=24;lh=round(size*1.55);vis=9;scroll=max(0,len(lines)-vis)*lh;tas=at('rest','as',2.85)-LEAD
    if t>tas:scroll*=1-smooth((t-tas)/.45)
    ed={'tab':True,'tab_pop':1,'size':size,'lines':lines,'typing':None,'caret':n<len(REST),'scroll':scroll,'saved':pop((t-tcl)/.3) if t>tcl else 0}
    w=claudeapp.app(940,560,t,ed)
    if t>tcl:                                                            # save wash: a green band slides down the editor
        u=clamp((t-tcl)/.45);wash=blank(700,360);yy=-90+u*450;ImageDraw.Draw(wash).rectangle((0,yy,700,yy+90),fill=(52,199,89,round(60*(1-u*.7))));w.alpha_composite(wash.filter(ImageFilter.GaussianBlur(14)),(230,98))
    if 0<n<len(REST):                                                    # paste flash on the newest line
        u=(t-tinc)%.11;fl=blank(700,lh);rr(fl,(0,0,699,lh-1),(217,119,87,round(70*(1-u/.11))),6);w.alpha_composite(fl,(230,98+round(lh*.7-scroll+(len(lines)-1)*lh-lh/2)))
    enter0(im,w,70,104,t);return im

# ---------------------------------------------------------------- 10. boom (full): celebration, then how it works ----------
TASKS=[('Fix the login bug','Opus 5.5'),('Design the schema','Fable 5.1'),('Write the tests','Opus 5.5')]
def _agent_card(task,model,flip,w=280,h=170):
    c=blank(w,h);rr(c,(0,0,w-1,h-1),'white',22,'#E3E3E6',2);c.alpha_composite(tile_claude(40),(20,18));d=ImageDraw.Draw(c)
    d.text((72,38),'sub-agent',font=sf(20,'Semibold'),fill=INK,anchor='lm');d.text((20,84),task,font=sf(21),fill='#3A3A3C',anchor='lm')
    green=model=='Opus 5.5';ch=chip(model,GREEN if green else INK,'white',20,'Semibold',None,16,40)
    if flip<1:ch=ch.resize((ch.width,max(1,round(ch.height*abs(math.cos(math.pi*flip))))),Image.Resampling.LANCZOS)
    c.alpha_composite(ch,(20,132-ch.height//2-20+20));return c
def boom(t,at):
    im=blank(W,H);tboom=at('boom','boom,',.24)-LEAD;tmeans=at('boom','means',1.48)-LEAD;tcl=at('boom','Claude',1.84)-LEAD;tnow=at('boom','now',2.18)-LEAD
    tnot=at('boom','not',2.36)-LEAD;talw=at('boom','always',2.66)-LEAD;tfab=at('boom','Fable',3.44)-LEAD;tnow2=at('boom','now.',3.76)-LEAD
    # before "boom": the file card waits, wobbling
    if t<tmeans+.3:
        e=pop((t+.1)/.3);di=doc_icon(150,188);place(im,di,W/2-75,380+6*math.sin(t*6),max(.05,e),1 if t<tboom else max(0,1-(t-tboom)/.15),True)
    if tboom<t<tmeans+.35:                                               # the celebration meme bursts in, then flies up and out
        u=t-tboom;s=pop(u/.3);fly=ease((t-tmeans)/.32) if t>tmeans else 0
        g=gif_card('celebrate',u,940);place(im,g,70,120-900*fly+14*(1-s),max(.05,.9+.1*s),min(1,s*2)*(1-fly*.6),True)
        rnd=random.Random(3)
        for k in range(28):                                              # confetti
            a=rnd.uniform(-math.pi,0);v=rnd.uniform(500,1300);col=[TERRA,INK,GREEN,'#0A84FF','#FFC933'][k%5];sz=rnd.uniform(10,20)
            x=W/2+math.cos(a)*v*u;y=420+math.sin(a)*v*u+.5*2200*u*u;op=max(0,1-u/.9)
            if op>0 and 110<y<960:
                pc=blank(30,30);ImageDraw.Draw(pc).rectangle((8,10,8+sz,10+sz*.55),fill=col);place(im,pc,x-15,y-15,1,op,False,rot=rnd.uniform(-500,500)*u)
    tdg=min(tcl-.05,tmeans+.12)
    if t>tdg:                                                            # the diagram: Claude + CLAUDE.md dispatches three sub-agents
        s=pop((t-tdg)/.3);place(im,tile_claude(170),W/2-85,150+10*(1-s),max(.05,s),min(1,s*2),True)
        ch=chip('CLAUDE.md','#F1EFE9',INK,22,'Semibold',claudeapp.asterisk(30),16,46);place(im,ch,W/2+100,212,max(.05,s),min(1,s*2),True)
        xs=[80,400,720];ts=[tnow,tnot,talw]
        for i,(task,model) in enumerate(TASKS):
            if t<ts[i]:continue
            u=t-ts[i];ln=ease(u/.26);x=xs[i]+140
            P0,P1,P2,P3=(W/2,335),(W/2,445),(x,400),(x,510)           # cubic S-curve (Albert: "make those curvy")
            pts=[((1-v)**3*P0[0]+3*(1-v)**2*v*P1[0]+3*(1-v)*v*v*P2[0]+v**3*P3[0],(1-v)**3*P0[1]+3*(1-v)**2*v*P1[1]+3*(1-v)*v*v*P2[1]+v**3*P3[1]) for v in np.linspace(0,ln,40)]
            if len(pts)>1:line(im,pts,'#C7C7CC',5)
            if u>.16:
                s2=pop((u-.16)/.28);flip=1 if model=='Fable 5.1' or t<tfab else clamp((t-tfab-i*.06)/.24)
                shown='Fable 5.1' if flip<.5 else model
                ac=_agent_card(task,shown,1 if flip>=1 or flip<=0 else (flip if flip>.5 else 1-flip));place(im,ac,xs[i],510+10*(1-s2),max(.05,.92+.08*s2),min(1,s2*2),True)
                if model=='Opus 5.5' and t>tnow2:                        # green pulse on the changed chips
                    p=clamp((t-tnow2-i*.05)/.4);ring=blank(320,90);rr(ring,(6,6,313,83),None,30,GREEN,round(6*(1-p))+1);place(im,ring,xs[i]-2,600,1+.12*p,1-p,False)
    return im

# ---------------------------------------------------------------- 11. determine (split): each task gets its model ----------
def determine(t,at):
    im=blank(W,H);c=card();tdet=at('determine','determine',.41)-LEAD;tits=at('determine','itself',.77)-LEAD;tmod=at('determine','model',1.47)-LEAD;tuse=at('determine','use.',1.99)-LEAD
    d=ImageDraw.Draw(c);c.alpha_composite(tile_claude(48),(40,36));d.text((104,60),'Sub-agents',font=sf(30,'Bold'),fill=INK,anchor='lm')
    locks=[tdet,tits,tmod];names=['Fable 5.1','Opus 5.5','Sonnet 5','Haiku 4.5']
    for i,(task,model) in enumerate(TASKS):
        e=ease((t+.1-i*.08)/.3);y=130+i*128
        row=blank(860,108);rr(row,(0,0,859,107),'#FAFAF8',22,'#ECEBE7',2);rd=ImageDraw.Draw(row);row.alpha_composite(tile_claude(44),(24,32))
        rd.text((88,54),task,font=sf(28,'Medium'),fill=INK,anchor='lm')
        locked=t>locks[i]
        if locked:
            s=pop((t-locks[i])/.28);green=model=='Opus 5.5';ch=chip(model,GREEN if green else INK,'white',24,'Semibold',None,20,50)
            place(row,ch,820-ch.width,29+6*(1-s),max(.05,.9+.1*s),1,False)
            if t>tuse:s2=pop((t-tuse-i*.05)/.26);checkmark(row,838,54,round(14*s2),GREEN)
        else:
            nm=names[int(t*15+i)%4];ch=chip(nm,'#F1EFE9',SOFT_GREY,24,'Semibold',None,20,50);place(row,ch,820-ch.width,29,1,.9,False)
        place(c,row,40,y+16*(1-e),1,e,False)
    sweep(c,t,.2,420,150,55)
    enter0(im,c,70,104,t);return im

# ---------------------------------------------------------------- 12. cta (split) ------------------------------------------
def cta(t,at):
    im=blank(W,H);tcl=at('cta','CLAUDE.md,',1.55)-LEAD;tcm=at('cta','comment',2.37)-LEAD;tand=at('cta','and',3.11)-LEAD;tsend=at('cta','send',3.37)-LEAD;tfree=at('cta','free',4.59)-LEAD
    obj=instagram_comment.render(t,keyword='SAVE',viewer='you',type_start=tcm,type_duration=.34,post_at=tand)
    if t>tfree:
        s=pop((t-tfree)/.26);hm=blank(60,60);ImageDraw.Draw(hm).polygon([(30+16*math.sin(a)**3*28/32,30-(13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a))*28/32) for a in [i/64*2*math.pi for i in range(65)]],fill='#ED4956')
        place(obj,hm,843-30,167-30,max(.05,s),1,False)
    tex=at('cta','exactly',.53)-LEAD;tfoc=tcm-.55
    pointer_motion.motion(obj,t,points=[(.35,600,300),(tfoc-.5,600,300),(tfoc-.05,400,360),(tfoc+.12,400,360),(tand-.35,813,364),(tand-.05,813,364),(tand+.4,850,300),(tfree-.05,843,167),(tfree+.12,843,167),(tfree+.6,880,120)],clicks=[tfoc,tand,tfree],end=tfree+.8)
    if tfoc<t<tand:ImageDraw.Draw(obj).rounded_rectangle((91,319,869,402),radius=41,outline='#262626',width=2)   # field focused
    e=ease((t+.09)/.30);place(im,obj,90,110+18*(1-e),.96+.04*e,e,True)
    # REJECTED 25 Sep 2026 ("Remove this too"): no link chip in the CTA - copy only the comment UI above. See SKILL.md rule 20.
    if t>tex:                                                            # the CLAUDE.md chip slides in on "exactly", goes blue on "send"
        u=t-tex;s_=ease(u/.5);w,h=700,74;ch=blank(w+200,h);sent=t>tsend
        rr(ch,(0,0,w-1,h-1),'white',37,'#0A84FF' if sent else '#E3E3E6',3 if sent else 2)
        ch.alpha_composite(claudeapp.asterisk(36),(24,19))
        label='CLAUDE.md · the full prompt';ImageDraw.Draw(ch).text((80,37),reveal(label,t-tex-.1,tcl-tex),font=sf(30,'Medium'),fill=INK,anchor='lm')
        fly=clamp((t-tsend-.3)/.5) if sent else 0;px,py=w-52+fly*260,37-fly*90;col='#0A84FF' if sent else '#C7C7CC';k=1+.25*math.sin(clamp((t-tsend)/.25)*math.pi) if sent else 1
        if fly<1:ImageDraw.Draw(ch).polygon([(px-16*k,py-13*k),(px+18*k,py),(px-16*k,py+13*k),(px-8*k,py)],fill=col)
        fl=6*math.sin((t-tcl)*5.2) if t>tcl else 0
        place(im,ch,(W-w)/2,575+70*(1-s_)+fl,.94+.06*s_,min(1,u/.12),True)
    return im

FN={'hook':hook,'opus':opus,'solves':solves,'likeme':likeme,'but':but,'create':create,'write1':write1,'write2':write2,'rest':rest,'boom':boom,'determine':determine,'cta':cta}
def graphics(b,t,S,at):
    _S.update(S);return FN[b['name']](t,at)
