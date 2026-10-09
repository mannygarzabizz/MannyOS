#!/usr/bin/env python3
# short3 "codex plugin": split-screen tutorial, WHITE style, less-text cards.
# Cards only where no screen window: VS hook (claude vs openai), merge card,
# checkmark DONE, best-of-both-worlds, calendar CTA. Screen windows are overlaid
# in compose (6.30-15.35, 15.35-26.70, 27.95-34.60); band shows decorative bg there.
import json, html, sys
A="#f0813f"; AD="rgba(240,129,63,0.45)"; GL="rgba(240,129,63,0.16)"
RED="#ff5470"; REDD="rgba(255,84,112,0.5)"
d=json.load(open(sys.argv[1]))
WS=[w for w in d["words"] if w.get("type")!="spacing" and w.get("start") is not None]
TOTAL=round(WS[-1]["end"],2)+0.23

EXPECT={3:"Fiber",6:"GPT-5.6?",12:"choose.",13:"Both",14:"together.",15:"Just",
 87:"And",90:"done.",91:"Automatically,",96:"check",98:"Codex,",99:"go",107:"best",
 108:"solution",109:"every",112:"which",117:"best",119:"both",120:"worlds.",
 121:"I'm",126:"every",128:"day.",131:"tomorrow."}
for i,t in EXPECT.items():
    got=WS[i]["text"]
    assert got.lower().rstrip(",.!?")==t.lower().rstrip(",.!?"), f"anchor mismatch idx {i}: expected {t!r} got {got!r}"
def T(i): return round(WS[i]["start"],2)

clips=[]; tw=[]; bi=0
def beat(s,e,cls,inner_html,js_lines):
    global bi
    dur=max(0.5,e-s)
    clips.append(f'<div class="beat" id="beat{bi}" data-start="{s}" data-duration="{dur:.2f}" '
                 f'data-track-index="{bi+2}"><div class="inner {cls}" id="in{bi}">{inner_html}</div></div>')
    js=[f'tl.fromTo("#beat{bi}",{{opacity:0,y:26,scale:0.975}},{{opacity:1,y:0,scale:1,duration:0.18,ease:"power3.out"}},{s:.2f});']
    js+=js_lines
    js.append(f'tl.to("#beat{bi}",{{opacity:0,duration:0.15,ease:"power2.in"}},{e-0.15:.2f});')
    tw.append("\n      ".join(js)); bi+=1
def shake_js(target,t,amp=12):
    return (f'tl.fromTo("{target}",{{x:0}},{{keyframes:[{{x:-{amp},duration:0.04}},'
            f'{{x:{amp-3},duration:0.04}},{{x:-{amp//2},duration:0.04}},{{x:0,duration:0.04}}]}},{t:.2f});')

# ---- B0: VS hook — claude logo slam vs openai logo slam ----
s,e=0.0,T(7)
h=( f'<div class="hookwrap" id="hw0"><div class="qmark" id="qm">?</div><div class="vsrow">'
    f'<img src="assets/logos/claude.svg" class="vslogo" id="lc"/>'
    f'<div class="vs" id="vs0">VS</div>'
    f'<img src="assets/logos/openai.svg" class="vslogo" id="lo"/></div></div>')
js=[
 f'tl.fromTo("#qm",{{opacity:0,scale:2.6,rotate:14}},{{opacity:1,scale:1,rotate:0,duration:0.24,ease:"power4.out"}},0.10);',
 shake_js("#hw0",0.26,8),
 f'tl.to("#qm",{{opacity:0,scale:0.5,y:-50,duration:0.18,ease:"power2.in"}},{T(3)-0.10:.2f});',
 f'tl.fromTo("#lc",{{opacity:0,scale:2.2,rotate:-12}},{{opacity:1,scale:1,rotate:0,duration:0.26,ease:"power4.out"}},{max(0.05,T(3)-0.06):.2f});',
 shake_js("#hw0",T(3)+0.16,9),
 f'tl.fromTo("#lo",{{opacity:0,scale:2.2,rotate:12}},{{opacity:1,scale:1,rotate:0,duration:0.26,ease:"power4.out"}},{T(6):.2f});',
 shake_js("#hw0",T(6)+0.16,9),
 f'tl.fromTo("#vs0",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.24,ease:"back.out(2.4)"}},{T(6)+0.35:.2f});']
beat(s,e,"hook",h,js)

# ---- B1: don't choose -> logos come TOGETHER with a + ----
s,e=T(7),T(15)
h=( f'<div class="hookwrap" id="hw1"><div class="orbwrap">'
    f'<div class="bloom" id="blm"></div>'
    f'<div class="orb" id="orb"><div class="oh l" id="ohl"><img src="assets/logos/claude.svg" class="vslogo" id="mc"/></div>'
    f'<div class="oh r" id="ohr"><img src="assets/logos/openai.svg" class="vslogo" id="mo"/></div></div>'
    f'<span class="bdot" id="bd0"></span><span class="bdot" id="bd1"></span><span class="bdot" id="bd2"></span><span class="bdot" id="bd3"></span><span class="bdot" id="bd4"></span><span class="bdot" id="bd5"></span><span class="bdot" id="bd6"></span><span class="bdot" id="bd7"></span><span class="bdot" id="bd8"></span><span class="bdot" id="bd9"></span></div></div>')
tsnap=T(13)
js=[
 f'tl.fromTo("#mc",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{s+0.10:.2f});',
 f'tl.fromTo("#mo",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{s+0.14:.2f});',
 # orbit: parent rotates a full revolution, logos counter-rotate to stay upright
 f'tl.fromTo("#orb",{{rotation:0}},{{rotation:360,duration:{tsnap-s-0.30:.2f},ease:"power1.inOut"}},{s+0.28:.2f});',
 f'tl.fromTo("#mc",{{rotation:0}},{{rotation:-360,duration:{tsnap-s-0.30:.2f},ease:"power1.inOut"}},{s+0.28:.2f});',
 f'tl.fromTo("#mo",{{rotation:0}},{{rotation:-360,duration:{tsnap-s-0.30:.2f},ease:"power1.inOut"}},{s+0.28:.2f});',
 # snap together on "Both" + burst + shake
 f'tl.to("#ohl",{{x:90,duration:0.16,ease:"power4.in"}},{tsnap:.2f});',
 f'tl.to("#ohr",{{x:-90,duration:0.16,ease:"power4.in"}},{tsnap:.2f});',
 shake_js("#hw1",tsnap+0.16,11),
 f'tl.fromTo("#bd0",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-17,y:103,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd1",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-127,y:-11,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd2",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:225,y:120,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd3",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-193,y:110,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd4",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-247,y:40,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd5",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:5,y:82,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd6",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-21,y:-102,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd7",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:221,y:76,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd8",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:227,y:3,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});tl.fromTo("#bd9",{{opacity:1,scale:0.4,x:0,y:0}},{{opacity:0,scale:1,x:-106,y:-82,duration:0.55,ease:"power2.out",immediateRender:false}},{tsnap+0.14:.2f});',
 # on "together": the fused pair does a fast celebratory spin + glow bloom behind
 f'tl.to("#orb",{{rotation:"+=360",duration:0.55,ease:"power2.inOut"}},{T(14):.2f});',
 f'tl.to("#mc",{{rotation:"-=360",duration:0.55,ease:"power2.inOut"}},{T(14):.2f});',
 f'tl.to("#mo",{{rotation:"-=360",duration:0.55,ease:"power2.inOut"}},{T(14):.2f});',
 f'tl.fromTo("#blm",{{opacity:0,scale:0.5}},{{opacity:1,scale:1.25,duration:0.45,ease:"power2.out",immediateRender:false}},{T(14):.2f});',
 f'tl.to("#hw1 .orbwrap",{{scale:1.05,yoyo:true,repeat:1,duration:0.14,ease:"sine.inOut"}},{T(14)+0.42:.2f});']
beat(s,e,"hook",h,js)

# ---- screens cover 6.30-15.35 and 15.35-26.70: no cards, decorative bg only ----

# ---- B2: DONE checkmark (26.70-27.95) ----
s,e=T(87)-0.04,T(91)-0.05
h=( f'<div class="hookwrap" id="hw2"><div class="ckwrap">'
    f'<svg viewBox="0 0 120 120" class="cksvg"><circle cx="60" cy="60" r="52" fill="none" '
    f'stroke="{AD}" stroke-width="8"/><path id="ckp" d="M35 62 L53 80 L86 44" fill="none" '
    f'stroke="{A}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" '
    f'stroke-dasharray="76" stroke-dashoffset="76"/></svg></div></div>')
js=[
 f'tl.fromTo("#hw2 .ckwrap",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.26,ease:"back.out(2)"}},{s+0.06:.2f});',
 f'tl.fromTo("#ckp",{{attr:{{"stroke-dashoffset":76}}}},{{attr:{{"stroke-dashoffset":0}},duration:0.4,ease:"power2.out"}},{T(90)-0.1:.2f});',
 f'tl.to("#hw2 .ckwrap",{{scale:1.1,yoyo:true,repeat:1,duration:0.1}},{T(90)+0.28:.2f});']
beat(s,e,"hook",h,js)

# ---- B2b: Claude <-> Codex back-and-forth ping-pong ----
s,e=T(91)-0.05,T(112)-0.04
h=( f'<div class="hookwrap" id="hwbf"><div class="bfwrap">'
    f'<div class="bfrow">'
    f'<img src="assets/logos/claude.svg" class="vslogo sm" id="bfc"/>'
    f'<div class="bftrack" id="bft"><span class="bfball" id="bfb"></span>'
    f'<div class="bfcheck" id="bfk"><svg viewBox="0 0 60 60" width="86" height="86">'
    f'<circle cx="30" cy="30" r="27" fill="{A}"/>'
    f'<path d="M17 31 L26 40 L43 21" fill="none" stroke="#fff" stroke-width="6" '
    f'stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>'
    f'<img src="assets/logos/openai.svg" class="vslogo sm" id="bfo"/>'
    f'</div></div></div>')
t0=T(96)  # ping-pong starts on "check"
legs=5; leg=0.55
js=[
 f'tl.fromTo("#bfc",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:0.32,ease:"power3.out"}},{s+0.10:.2f});',
 f'tl.fromTo("#bfo",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.32,ease:"power3.out"}},{s+0.16:.2f});',
 f'tl.fromTo("#bft",{{opacity:0,scaleX:0.4}},{{opacity:1,scaleX:1,duration:0.28,ease:"power3.out"}},{s+0.30:.2f});',
 f'tl.fromTo("#bfb",{{opacity:0}},{{opacity:1,duration:0.15,immediateRender:false}},{t0-0.05:.2f});',
 f'tl.fromTo("#bfb",{{x:-215}},{{x:215,duration:{leg},repeat:{legs-1},yoyo:true,ease:"power1.inOut"}},{t0:.2f});',
 "".join(f'tl.to("#{ "bfo" if k%2==0 else "bfc"}",{{scale:1.13,yoyo:true,repeat:1,duration:0.11,ease:"power2.out"}},{t0+(k+1)*leg-0.06:.2f});' for k in range(legs)),
 f'tl.to("#bfb",{{opacity:0,duration:0.15}},{T(108)-0.05:.2f});',
 f'tl.fromTo("#bfk",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(2.2)"}},{T(108):.2f});',
 f'tl.to("#hwbf .bfrow",{{scale:1.05,yoyo:true,repeat:1,duration:0.14,ease:"sine.inOut"}},{T(109):.2f});']
beat(s,e,"hook",h,js)

# ---- B3: best of both worlds — logos + plus again, warm pop ----
s,e=T(112)-0.04,T(121)-0.06
h=( f'<div class="hookwrap" id="hw3"><div class="vsrow tight">'
    f'<img src="assets/logos/claude.svg" class="vslogo sm" id="wc"/>'
    f'<div class="plus" id="pl2">+</div>'
    f'<img src="assets/logos/openai.svg" class="vslogo sm" id="wo"/></div></div>')
js=[
 f'tl.fromTo("#wc",{{opacity:0,y:36}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{T(117)-0.15:.2f});',
 f'tl.fromTo("#wo",{{opacity:0,y:36}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{T(117)-0.05:.2f});',
 f'tl.fromTo("#pl2",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.26,ease:"back.out(2.2)"}},{T(119):.2f});',
 f'tl.to("#hw3 .vsrow",{{scale:1.07,yoyo:true,repeat:1,duration:0.12,ease:"sine.inOut"}},{T(120):.2f});']
beat(s,e,"hook",h,js)

# ---- B4: CTA calendar ----
s,e=T(121)-0.06,TOTAL
days="".join(f'<span class="day" id="dy{k}">{n}</span>' for k,n in enumerate(["M","T","W","T","F","S","S"]))
h=( f'<div class="hookwrap" id="hw4"><div class="calwrap">'
    f'<div class="days" id="dw">{days}</div></div></div>')
js=[
 "".join(f'tl.fromTo("#dy{k}",{{opacity:0,scale:0.4,y:20}},{{opacity:1,scale:1,y:0,duration:0.2,ease:"back.out(2.4)"}},{T(126)+k*0.09:.2f});' for k in range(7)),
 "".join(f'tl.to("#dy{k}",{{background:"{A}",color:"#1a0e06",duration:0.12}},{T(126)+0.15+k*0.09:.2f});' for k in range(7))]
beat(s,e,"cal",h,js)

# ---- decorative bg (white) ----
NP=22
parts_html="".join(f'<span class="pt" id="pt{k}" style="left:{(k*131+40)%1040}px;top:{(k*97+30)%760}px;width:{5+(k%3)*3}px;height:{5+(k%3)*3}px;opacity:{0.12+0.2*((k*7)%5)/5:.2f}"></span>' for k in range(NP))
streaks_html="".join(f'<span class="stk" id="stk{k}" style="top:{120+k*230}px"></span>' for k in range(3))
bg=['tl.to("#glow",{x:120,y:30,scale:1.15,duration:6,yoyo:true,repeat:9,ease:"sine.inOut"},0);',
    'tl.to("#grid",{backgroundPosition:"0px 110px",duration:6,ease:"none",repeat:9},0);']
for k in range(NP):
    dur=4+(k%5)
    bg.append(f'tl.to("#pt{k}",{{y:-{120+(k%4)*60},duration:{dur},ease:"none",repeat:{int(60/dur)+1}}},0);')
    bg.append(f'tl.to("#pt{k}",{{opacity:0,duration:{dur},yoyo:true,repeat:{int(60/dur)+1},ease:"sine.inOut"}},0);')
for k in range(3):
    bg.append(f'tl.fromTo("#stk{k}",{{x:-1200}},{{x:1200,duration:{5+k*2},ease:"none",repeat:9}},{k*1.5});')

CSS=f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#fff;font-family:"Montserrat","Inter",sans-serif}}
#root{{position:relative;width:1080px;height:1920px}}
#bgz{{position:absolute;top:0;left:0;width:1080px;height:864px;overflow:hidden}}
#grid{{position:absolute;inset:-40px;background-image:linear-gradient(rgba(240,129,63,0.14) 1px,transparent 1px),linear-gradient(90deg,rgba(240,129,63,0.14) 1px,transparent 1px);background-size:110px 110px}}
#glow{{position:absolute;top:120px;left:280px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(240,129,63,0.13),transparent 65%);filter:blur(22px)}}
.pt{{position:absolute;border-radius:50%;background:{A};box-shadow:0 0 12px {A}}}
.stk{{position:absolute;left:0;width:520px;height:2px;background:linear-gradient(90deg,transparent,{A},transparent);opacity:0.3}}
.beat{{position:absolute;top:0;left:0;width:1080px;height:864px}}
.inner{{position:absolute;top:55px;left:64px;right:64px;height:700px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.hookwrap{{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.accw{{color:{A};text-shadow:0 0 26px {GL}}}
.vsrow{{display:flex;align-items:center;gap:56px}}
.vsrow.tight{{gap:40px}}
.vslogo{{height:280px;width:280px;object-fit:contain;filter:drop-shadow(0 6px 24px rgba(0,0,0,0.18))}}
.vslogo.sm{{height:230px;width:230px}}
.vs{{color:#141414;font-size:110px;font-weight:900;letter-spacing:-2px}}
.plus{{color:{A};font-size:170px;font-weight:900;line-height:1;text-shadow:0 0 30px {GL}}}
.ckwrap{{width:400px;height:400px}}
.cksvg{{width:100%;height:100%;filter:drop-shadow(0 0 24px {GL})}}
.calwrap{{display:flex;flex-direction:column;align-items:center;gap:44px}}

.qmark{{position:absolute;color:{A};font-size:340px;font-weight:900;text-shadow:0 0 60px {GL};line-height:1}}
.orbwrap{{position:relative;display:flex;align-items:center;justify-content:center;width:100%;height:100%}}
.bloom{{position:absolute;width:560px;height:560px;border-radius:50%;background:radial-gradient(circle,rgba(240,129,63,0.30),transparent 62%);opacity:0}}
.orb{{position:relative;width:640px;height:230px}}
.oh{{position:absolute;top:50%;margin-top:-115px}}
.oh.l{{left:0}}.oh.r{{right:0}}
.oh .vslogo{{height:230px;width:230px}}
.bdot{{position:absolute;left:50%;top:50%;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:{A};box-shadow:0 0 14px {A};opacity:0}}
.bfwrap{{display:flex;align-items:center;justify-content:center;width:100%}}
.bfrow{{display:flex;align-items:center;gap:34px}}
.bftrack{{position:relative;width:460px;height:10px;border-radius:5px;background:rgba(240,129,63,0.18);display:flex;align-items:center;justify-content:center}}
.bfball{{position:absolute;left:50%;top:50%;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;background:{A};box-shadow:0 0 26px {A};opacity:0}}
.bfcheck{{opacity:0;filter:drop-shadow(0 0 18px {GL})}}
.days{{display:flex;gap:18px}}
.day{{width:118px;height:130px;border-radius:22px;background:rgba(240,129,63,0.07);border:3px solid {AD};color:#141414;font-size:56px;font-weight:900;display:flex;align-items:center;justify-content:center}}
.tmr{{font-size:104px;font-weight:900;letter-spacing:-2px}}
'''
HTML=('<!doctype html><html lang="en"><head><meta charset="UTF-8"/>'
 '<meta name="viewport" content="width=1080, height=1920"/>'
 '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'
 f'<style>{CSS}</style></head><body>'
 f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.2f}" data-width="1080" data-height="1920">'
 f'<div id="bgz" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="0"><div id="grid"></div><div id="glow"></div>{streaks_html}{parts_html}</div>'
 +"".join(clips)+
 '</div><script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});\n'
 +"\n".join(bg)+"\n"+"\n".join(tw)+
 '\nwindow.__timelines["main"]=tl;</script></body></html>')
open("index.html","w").write(HTML)
print(f"short3: {bi} beats, total {TOTAL}s")
