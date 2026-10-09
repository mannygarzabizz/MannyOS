#!/usr/bin/env python3
# short2 "Yoom": free Loom alternative reel. ORANGE theme, upgraded animation language:
# every card gets slam entrances + shockwave rings + impact shakes; staged sequences
# anchored per word (Loom strike, YOOM hero, feature pills + stopwatch, REC->STOP->
# UPLOAD->LINK flow, github repo, save bookmark, tool-tile burst + FREE stamp, calendar).
import json, html, sys
A="#f0813f"; AD="rgba(240,129,63,0.45)"; GL="rgba(240,129,63,0.16)"
RED="#ff5470"; REDD="rgba(255,84,112,0.5)"; GREY="#8b938e"; LOOM="#625DF5"
d=json.load(open(sys.argv[1]))
WS=[w for w in d["words"] if w.get("type")!="spacing" and w.get("start") is not None]
TOTAL=round(WS[-1]["end"],2)+0.23

EXPECT={6:"Loom",7:"anymore",11:"built",12:"Yoom.",13:"No",14:"subscription,",
 18:"free,",22:"open",23:"source,",27:"host",31:"ten",32:"minutes.",33:"You",
 37:"screen",38:"recording,",39:"stop",42:"done.",45:"upload",51:"link",55:"share",
 57:"anyone.",58:"The",59:"GitHub",63:"Yoom",64:"Public.",65:"Save",67:"video",
 71:"forget",73:"And",75:"rebuilding",79:"tools",81:"releasing",85:"free.",
 86:"Posting",87:"every",88:"single",89:"day.",93:"tomorrow."}
for i,t in EXPECT.items():
    got=WS[i]["text"]
    assert got.lower()==t.lower(), f"anchor mismatch idx {i}: expected {t!r} got {got!r}"
def T(i): return round(WS[i]["start"],2)
def esc(s): return html.escape(s)

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

_rid=[0]
def ring(color_cls=""):
    _rid[0]+=1
    return "", f"#rg{_rid[0]}"   # rings removed (user: no circle effect)
def ring_js(sel,t,sc=2.4):
    return ""
def shake_js(target,t,amp=13):
    return (f'tl.fromTo("{target}",{{x:0}},{{keyframes:[{{x:-{amp},duration:0.04}},'
            f'{{x:{amp-3},duration:0.04}},{{x:-{amp//2},duration:0.04}},{{x:0,duration:0.04}}]}},{t:.2f});')

# ---- B0: hook — Loom logo slams in, then SHATTERS like glass on "anymore" ----
s,e=0.0,T(8)
r1,r1s=ring(); r2,r2s=ring("red")
# shard grid: 3x3 cells, each split into 2 triangles -> 18 glass shards of the logo
import random
random.seed(7)
tsh=T(7)  # shatter moment
shards=[]; shjs=[]
def shatter(elem_html_fn, box_id, W, H, gx_n, gy_n, spread=2.6):
    """Tile an element into triangular shards inside a W×H box and emit fly-out tweens."""
    for gy in range(gy_n):
        for gx in range(gx_n):
            x0,y0=gx*W/gx_n,gy*H/gy_n; x1,y1=x0+W/gx_n,y0+H/gy_n
            for tri in ([(x0,y0),(x1,y0),(x0,y1)],[(x1,y0),(x1,y1),(x0,y1)]):
                k=len(shards)
                poly=",".join(f"{px:.0f}px {py:.0f}px" for px,py in tri)
                shards.append((box_id,elem_html_fn(k,poly)))
                cx=sum(p[0] for p in tri)/3-W/2; cy=sum(p[1] for p in tri)/3-H/2
                dx=cx*(spread+random.random()*1.6)+random.uniform(-40,40)
                dy=cy*1.4+random.uniform(120,420)
                rot=random.uniform(-160,160); dl=random.uniform(0,0.06)
                shjs.append(f'tl.to("#sh{k}",{{x:{dx:.0f},y:{dy:.0f},rotation:{rot:.0f},opacity:0,'
                            f'duration:{0.55+random.random()*0.25:.2f},ease:"power2.in"}},{tsh+dl:.2f});')
shatter(lambda k,poly:f'<img src="assets/logos/loom.svg" class="shard" id="sh{k}" style="clip-path:polygon({poly})"/>',
        "sb",400,400,3,3)
shatter(lambda k,poly:f'<span class="shardtx" id="sh{k}" style="clip-path:polygon({poly})">LOOM</span>',
        "sbt",560,170,4,2,spread=2.0)
logo_shards="".join(hh for b,hh in shards if b=="sb")
text_shards="".join(hh for b,hh in shards if b=="sbt")
h=( f'<div class="hookwrap" id="hw0">{r1}{r2}'
    f'<div class="lwrap" id="lw"><div class="shardbox" id="sb">{logo_shards}'
    f'<div class="crack" id="ck"></div></div>'
    f'<div class="shardboxt" id="sbt">{text_shards}</div></div></div>')
js=[
 f'tl.fromTo("#sb",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.24,ease:"power4.out"}},0.05);',
 ring_js(r1s,0.15),
 f'tl.fromTo("#sbt",{{opacity:0,y:36}},{{opacity:1,y:0,duration:0.26,ease:"back.out(1.8)"}},{T(6)-0.15:.2f});',
 # crack flash the instant before the shards fly
 f'tl.fromTo("#ck",{{opacity:0}},{{opacity:1,duration:0.05,yoyo:true,repeat:1,immediateRender:false}},{tsh-0.05:.2f});',
 "".join(shjs),
 ring_js(r2s,tsh+0.06),
 shake_js("#hw0",tsh+0.08)]
beat(s,e,"hook",h,js)

# ---- B1: LOOM -> YOOM letter morph (L flips out, Y flips in) ----
s,e=T(8),T(13)+0.4  # hold YOOM a beat longer
r3,r3s=ring()
tm=T(12)  # "Yoom."
h=( f'<div class="hookwrap" id="hw1">{r3}'
    f'<div class="morph" id="mw">'
    f'<span class="mslot"><span class="mlet lchar" id="mL">L</span><span class="mlet ychar" id="mY">Y</span></span>'
    f'<span class="mlet rest" id="mo1">O</span><span class="mlet rest" id="mo2">O</span><span class="mlet rest" id="mo3">M</span>'
    f'</div></div>')
js=[
 # LOOM settles in quietly (purple), per-letter rise
 "".join(f'tl.fromTo("#{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{s+0.10+k*0.05:.2f});' for k,i in enumerate(["mL","mo1","mo2","mo3"])),
 # the morph: L flips up and out, Y flips in from below — smooth, no slam
 f'tl.to("#mL",{{rotationX:88,y:-30,opacity:0,transformOrigin:"50% 100%",duration:0.28,ease:"power2.in"}},{tm-0.06:.2f});',
 f'tl.fromTo("#mY",{{rotationX:-88,y:30,opacity:0}},{{rotationX:0,y:0,opacity:1,transformOrigin:"50% 0%",duration:0.34,ease:"power3.out",immediateRender:false}},{tm+0.10:.2f});',
 # rest of the word glides from loom purple to white as the Y lands
 "".join(f'tl.to("#{i}",{{color:"#141414",textShadow:"0 0 60px rgba(240,129,63,0.25)",duration:0.4,ease:"power1.inOut"}},{tm+0.08:.2f});' for i in ["mo1","mo2","mo3"]),
 # gentle settle: whole word breathes once + soft ring, no shake (clean)
 f'tl.to("#mw",{{scale:1.05,yoyo:true,repeat:1,duration:0.14,ease:"sine.inOut"}},{tm+0.30:.2f});',
 ring_js(r3s,tm+0.22,2.2)]
beat(s,e,"hook",h,js)

# ---- B2: feature pills + stopwatch ----
s,e=T(13)+0.4,T(33)
h=( f'<div class="fwrap" id="fw">'
    f'<div class="fpill" id="fp0">🚫 NO SUBSCRIPTION</div>'
    f'<div class="fpill" id="fp1">💯 100% FREE</div>'
    f'<div class="fpill" id="fp2">🔓 100% OPEN SOURCE</div>'
    f'<div class="frow"><div class="fpill half" id="fp3">🏠 SELF-HOST</div>'
    f'<div class="swmini" id="sw"><svg viewBox="0 0 120 120" class="swsvg">'
    f'<circle cx="60" cy="60" r="50" fill="none" stroke="rgba(240,129,63,0.25)" stroke-width="10"/>'
    f'<circle id="swa" cx="60" cy="60" r="50" fill="none" stroke="{A}" stroke-width="10" '
    f'stroke-linecap="round" stroke-dasharray="314.2" stroke-dashoffset="314.2" transform="rotate(-90 60 60)"/>'
    f'<text x="60" y="72" text-anchor="middle" fill="#141414" font-size="34" font-weight="900" font-family="Montserrat">10:00</text>'
    f'</svg><div class="swlbl">MINUTES</div></div></div></div>')
js=[
 f'tl.fromTo("#fp0",{{opacity:0,x:-60,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.26,ease:"back.out(2)"}},{s+0.08:.2f});',
 f'tl.fromTo("#fp1",{{opacity:0,x:-60,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.26,ease:"back.out(2)"}},{T(18)-0.15:.2f});',
 f'tl.fromTo("#fp2",{{opacity:0,x:-60,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.26,ease:"back.out(2)"}},{T(22)-0.10:.2f});',
 f'tl.fromTo("#fp3",{{opacity:0,x:-60,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.26,ease:"back.out(2)"}},{T(27)-0.05:.2f});',
 f'tl.fromTo("#sw",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.26,ease:"back.out(2.2)"}},{T(31)-0.05:.2f});',
 f'tl.fromTo("#swa",{{attr:{{"stroke-dashoffset":314.2}}}},{{attr:{{"stroke-dashoffset":0}},duration:{max(0.5,e-0.2-T(31)):.2f},ease:"power1.inOut"}},{T(31):.2f});',
 f'tl.to("#sw",{{scale:1.08,yoyo:true,repeat:1,duration:0.09}},{T(32):.2f});']
beat(s,e,"feat",h,js)

# ---- B3: REC -> STOP -> UPLOAD -> LINK flow ----
s,e=T(33),T(58)
r4,r4s=ring()
h=( f'<div class="hookwrap" id="hw3">{r4}<div class="flowwrap">'
    f'<div class="steps">'
    f'<div class="step" id="st0"><div class="sic rec"><span class="recdot" id="rd"></span></div><div class="slb">REC</div></div>'
    f'<div class="sarr" id="sa0">→</div>'
    f'<div class="step" id="st1"><div class="sic"><span class="stopsq"></span></div><div class="slb">STOP</div></div>'
    f'<div class="sarr" id="sa1">→</div>'
    f'<div class="step" id="st2"><div class="sic up">↑</div><div class="upbar"><span id="ub"></span></div><div class="slb">UPLOAD</div></div>'
    f'<div class="sarr" id="sa2">→</div>'
    f'<div class="step" id="st3"><div class="sic lk">🔗</div><div class="slb">LINK</div></div>'
    f'</div><div class="linkpill" id="lp">✓ yoom.link/x7f2 — SHARE WITH ANYONE</div></div></div>')
js=[
 f'tl.fromTo("#st0",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.24,ease:"back.out(2.2)"}},{T(37):.2f});',
 f'tl.to("#rd",{{scale:1.35,yoyo:true,repeat:7,duration:0.3,ease:"sine.inOut"}},{T(37)+0.1:.2f});',
 f'tl.fromTo("#sa0",{{opacity:0}},{{opacity:1,duration:0.15}},{T(39)-0.1:.2f});',
 f'tl.fromTo("#st1",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.24,ease:"back.out(2.2)"}},{T(39):.2f});',
 f'tl.fromTo("#sa1",{{opacity:0}},{{opacity:1,duration:0.15}},{T(45)-0.1:.2f});',
 f'tl.fromTo("#st2",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.24,ease:"back.out(2.2)"}},{T(45):.2f});',
 f'tl.fromTo("#ub",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"power1.inOut"}},{T(45)+0.1:.2f});',
 f'tl.fromTo("#sa2",{{opacity:0}},{{opacity:1,duration:0.15}},{T(51)-0.1:.2f});',
 f'tl.fromTo("#st3",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.24,ease:"back.out(2.2)"}},{T(51):.2f});',
 f'tl.fromTo("#lp",{{opacity:0,y:24,scale:0.85}},{{opacity:1,y:0,scale:1,duration:0.26,ease:"back.out(2)"}},{T(55):.2f});',
 ring_js(r4s,T(57),2.2),
 shake_js("#hw3",T(57)+0.02,9)]
beat(s,e,"flow",h,js)

# ---- B4: GitHub repo ----
s,e=T(58),T(65)
r5,r5s=ring()
h=( f'<div class="hookwrap" id="hw4">{r5}<div class="ghwrap">'
    f'<img src="assets/logos/github-dark.svg" class="ghlogo" id="gl"/>'
    f'<div class="repopill" id="rp"><span class="repoico">📦</span> yoom-public</div></div></div>')
js=[
 f'tl.fromTo("#gl",{{opacity:0,scale:2.2,rotate:-14}},{{opacity:1,scale:1,rotate:0,duration:0.26,ease:"power4.out"}},{T(59):.2f});',
 ring_js(r5s,T(59)+0.12),
 shake_js("#hw4",T(59)+0.14,10),
 f'tl.fromTo("#rp",{{opacity:0,scale:0.6,y:20}},{{opacity:1,scale:1,y:0,duration:0.26,ease:"back.out(2.2)"}},{T(63):.2f});']
beat(s,e,"gh",h,js)

# ---- B5: SAVE bookmark ----
s,e=T(65),T(73)
r6,r6s=ring()
h=( f'<div class="hookwrap" id="hw5">{r6}<div class="svwrap">'
    f'<div class="svico" id="si"><svg viewBox="0 0 24 24" width="180" height="180">'
    f'<path d="M6 2h12a1 1 0 0 1 1 1v19l-7-4.5L5 22V3a1 1 0 0 1 1-1z" fill="{A}"/></svg></div>'
    f'<div class="svtxt" id="sv1">SAVE THIS <span class="accw">VIDEO</span></div></div></div>')
js=[
 f'tl.fromTo("#si",{{opacity:0,scale:2.4,rotate:12}},{{opacity:1,scale:1,rotate:0,duration:0.24,ease:"power4.out"}},{T(65)+0.02:.2f});',
 ring_js(r6s,T(65)+0.14,2.2),
 shake_js("#hw5",T(65)+0.16,10),
 f'tl.fromTo("#sv1",{{opacity:0,y:28}},{{opacity:1,y:0,duration:0.26,ease:"back.out(1.9)"}},{T(67):.2f});',
 f'tl.to("#si",{{scale:1.12,yoyo:true,repeat:1,duration:0.09}},{T(71):.2f});']
beat(s,e,"sv",h,js)

# ---- B6: tools burst + FREE stamp ----
s,e=T(73),T(86)
TOOLS=["🎥","📝","📊","🔗","🎨","⚙️","💬","📅","🔍","💸"]
tiles="".join(f'<span class="htile" id="tt{k}">{t}</span>' for k,t in enumerate(TOOLS))
r7,r7s=ring("red")
h=( f'<div class="hookwrap" id="hw6">{r7}<div class="twrap">'
    f'<div class="eyebrow" id="te"><span class="ebdot"></span>REBUILDING EVERY TOOL</div>'
    f'<div class="htiles tls" id="tg">{tiles}</div>'
    f'<div class="stampfree" id="fs">100% FREE</div></div></div>')
js=[
 f'tl.fromTo("#te",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.24,ease:"power3.out"}},{s+0.08:.2f});',
 "".join(f'tl.fromTo("#tt{k}",{{opacity:0,scale:0,y:26}},{{opacity:1,scale:1,y:0,duration:0.22,ease:"back.out(2.6)"}},{T(79)-0.35+k*0.045:.2f});' for k in range(10)),
 f'tl.fromTo("#fs",{{opacity:0,scale:2.3,rotate:-12}},{{opacity:1,scale:1,rotate:-6,duration:0.24,ease:"power4.out"}},{T(85):.2f});',
 ring_js(r7s,T(85)+0.12,2.4),
 shake_js("#hw6",T(85)+0.14),
 f'tl.to("#tg",{{opacity:0.35,duration:0.25}},{T(85):.2f});']
beat(s,e,"tools",h,js)

# ---- B7: calendar + tomorrow ----
s,e=T(86),TOTAL
days="".join(f'<span class="day" id="dy{k}">{n}</span>' for k,n in enumerate(["M","T","W","T","F","S","S"]))
r8,r8s=ring()
h=( f'<div class="hookwrap" id="hw7">{r8}<div class="calwrap">'
    f'<div class="eyebrow" id="ce"><span class="ebdot"></span>POSTING</div>'
    f'<div class="days" id="dw">{days}</div>'
    f'<div class="tmr" id="tm">SEE YOU <span class="accw">TOMORROW</span></div></div></div>')
js=[
 f'tl.fromTo("#ce",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.22,ease:"power3.out"}},{s+0.06:.2f});',
 "".join(f'tl.fromTo("#dy{k}",{{opacity:0,scale:0.4,y:20}},{{opacity:1,scale:1,y:0,duration:0.2,ease:"back.out(2.4)"}},{T(87)+k*0.09:.2f});' for k in range(7)),
 "".join(f'tl.to("#dy{k}",{{background:"{A}",color:"#1a0e06",duration:0.12}},{T(87)+0.15+k*0.09:.2f});' for k in range(7)),
 f'tl.fromTo("#tm",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.26,ease:"back.out(2)"}},{T(93):.2f});',
 ring_js(r8s,T(93)+0.10,2.2),
 shake_js("#hw7",T(93)+0.12,9)]
beat(s,e,"cal",h,js)

# ---- decorative bg ----
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
.eyebrow{{color:{A};font-size:32px;font-weight:800;letter-spacing:6px;text-transform:uppercase;display:flex;align-items:center;gap:13px}}
.ebdot{{width:14px;height:14px;border-radius:50%;background:{A};box-shadow:0 0 14px {A}}}
.hookwrap{{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.ring{{position:absolute;top:46%;left:50%;width:430px;height:430px;margin:-215px 0 0 -215px;border-radius:50%;border:6px solid {A};opacity:0;box-shadow:0 0 30px {GL}}}
.ring.red{{border-color:{RED};box-shadow:0 0 30px {REDD}}}
.accw{{color:{A};text-shadow:0 0 26px {A}}}
/* B0 loom */
.lwrap{{position:relative;display:flex;flex-direction:column;align-items:center;gap:26px}}
.shardbox{{position:relative;width:400px;height:400px;filter:drop-shadow(0 0 50px rgba(98,93,245,0.55))}}
.shard{{position:absolute;top:0;left:0;width:400px;height:400px;object-fit:contain}}
.shardboxt{{position:relative;width:560px;height:170px;margin-top:30px}}
.shardtx{{position:absolute;top:0;left:0;width:560px;height:170px;color:{LOOM};font-size:150px;font-weight:900;letter-spacing:2px;text-align:center;line-height:170px;text-shadow:0 0 40px rgba(98,93,245,0.45)}}
.crack{{position:absolute;inset:-20px;border-radius:50%;background:radial-gradient(circle,rgba(240,129,63,0.85),transparent 60%);opacity:0}}
.ltxt{{color:#fff;font-size:78px;font-weight:900;letter-spacing:-1px}}
.ltxt .loomw{{color:{LOOM}}}
.paypill{{color:#fff;font-size:56px;font-weight:900;border:4px solid {REDD};border-radius:18px;padding:10px 34px;background:rgba(30,14,18,0.8)}}
.strike{{position:absolute;top:47%;left:-30px;right:-30px;height:16px;background:{RED};border-radius:8px;transform:rotate(-14deg);transform-origin:left center;box-shadow:0 0 26px {REDD}}}
/* B1 loom->yoom morph */
.morph{{display:flex;align-items:baseline;perspective:900px}}
.mlet{{font-size:250px;font-weight:900;letter-spacing:-6px;line-height:0.9;color:{LOOM};text-shadow:0 0 60px rgba(98,93,245,0.35)}}
.mslot{{position:relative;display:inline-block}}
.mslot .mlet{{display:inline-block}}
.ychar{{position:absolute;top:0;left:0;color:{A};text-shadow:0 0 60px {GL};opacity:0}}
/* B2 features */
.fwrap{{display:flex;flex-direction:column;gap:26px;width:100%;padding:0 10px}}
.fpill{{color:#141414;font-size:56px;font-weight:900;border:3px solid {AD};border-radius:22px;padding:22px 36px;background:rgba(240,129,63,0.07);box-shadow:0 0 24px {GL};align-self:flex-start}}
.frow{{display:flex;align-items:center;gap:30px}}
.fpill.half{{align-self:auto}}
.swmini{{display:flex;align-items:center;gap:16px}}
.swsvg{{width:150px;height:150px;filter:drop-shadow(0 0 18px {GL})}}
.swlbl{{color:{A};font-size:34px;font-weight:900;letter-spacing:3px}}
/* B3 flow */
.flowwrap{{display:flex;flex-direction:column;align-items:center;gap:44px;width:100%}}
.steps{{display:flex;align-items:center;gap:18px}}
.step{{display:flex;flex-direction:column;align-items:center;gap:14px}}
.sic{{width:170px;height:170px;border-radius:30px;background:rgba(240,129,63,0.07);border:3px solid {AD};display:flex;align-items:center;justify-content:center;font-size:70px;color:{A};box-shadow:0 0 24px {GL}}}
.recdot{{width:64px;height:64px;border-radius:50%;background:{RED};box-shadow:0 0 24px {REDD}}}
.stopsq{{width:56px;height:56px;border-radius:12px;background:#141414}}
.sic.up{{font-weight:900}}
.upbar{{width:170px;height:12px;border-radius:6px;background:rgba(255,255,255,0.1);overflow:hidden}}
.upbar span{{display:block;height:100%;width:100%;transform-origin:left;transform:scaleX(0);background:{A};box-shadow:0 0 12px {A}}}
.slb{{color:#141414;font-size:30px;font-weight:900;letter-spacing:3px}}
.sarr{{color:{A};font-size:54px;font-weight:900}}
.linkpill{{color:#1a0e06;font-size:44px;font-weight:900;background:{A};border-radius:18px;padding:18px 34px;box-shadow:0 0 34px {A}}}
/* B4 github */
.ghwrap{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.ghlogo{{height:250px;width:250px;object-fit:contain;filter:drop-shadow(0 0 34px rgba(255,255,255,0.25))}}
.repopill{{color:#141414;font-size:64px;font-weight:900;font-family:ui-monospace,"SF Mono",Menlo,monospace;border:3px solid {AD};border-radius:20px;padding:18px 40px;background:rgba(240,129,63,0.07);box-shadow:0 0 28px {GL}}}
.repoico{{font-size:54px}}
.ghsub{{color:{A};font-size:38px;font-weight:800;letter-spacing:6px}}
/* B5 save */
.svwrap{{display:flex;flex-direction:column;align-items:center;gap:26px}}
.svico{{font-size:190px;line-height:1;filter:drop-shadow(0 0 30px {GL})}}
.svtxt{{color:#141414;font-size:92px;font-weight:900;letter-spacing:-2px}}
.svsub{{color:{GREY};font-size:40px;font-weight:800;letter-spacing:4px}}
/* B6 tools */
.twrap{{position:relative;display:flex;flex-direction:column;align-items:center;gap:34px}}
.htiles{{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;width:640px}}
.htile{{width:104px;height:104px;border-radius:22px;background:rgba(240,129,63,0.12);border:2px solid {AD};display:flex;align-items:center;justify-content:center;font-size:56px;box-shadow:0 0 18px {GL}}}
.stampfree{{position:absolute;top:56%;color:{RED};font-size:110px;font-weight:900;border:8px solid {RED};border-radius:24px;padding:8px 44px;box-shadow:0 0 38px {REDD};text-shadow:0 0 26px {REDD};background:rgba(255,255,255,0.7)}}
/* B7 calendar */
.calwrap{{display:flex;flex-direction:column;align-items:center;gap:40px}}
.days{{display:flex;gap:18px}}
.day{{width:118px;height:130px;border-radius:22px;background:rgba(240,129,63,0.07);border:3px solid {AD};color:#141414;font-size:56px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 0 18px {GL}}}
.tmr{{color:#141414;font-size:92px;font-weight:900;letter-spacing:-2px}}
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
print(f"short2: {bi} beats, total {TOTAL}s")
