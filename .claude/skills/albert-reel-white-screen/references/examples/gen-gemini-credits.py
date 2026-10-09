#!/usr/bin/env python3
# short4 "$300 Gemini credits": WHITE style, staged cards per doctrine.
# B0 credit card tilts in -> red strike -> giant $0 slam + burst
# B1 $300 slam + FREE stamp + coin burst
# B2 credit card again -> shield-with-check pops over it ("won't charge")
# B3 globe -> red not-available strike -> VPN shield pill
# B4 payoff: confetti burst -> $300 slam -> GEMINI 3.1 PRO sparkle pill
# B5 youtube play button slam -> FULL GUIDE pill -> wink shake on "watch"
# B6 calendar days
import json, html, sys, random
A="#f0813f"; AD="rgba(240,129,63,0.45)"; GL="rgba(240,129,63,0.16)"
RED="#ff5470"; REDD="rgba(255,84,112,0.5)"; LOOM="#625DF5"
d=json.load(open(sys.argv[1]))
WS=[w for w in d["words"] if w.get("type")!="spacing" and w.get("start") is not None]
TOTAL=round(WS[-1]["end"],2)+0.23
EXPECT={58:"It'll",63:"credit",64:"card,",69:"won't",70:"charge",76:"credits.",
 77:"For",79:"countries,",81:"not",82:"available,",89:"VPN.",191:"And",194:"go.",
 198:"three",209:"best",210:"models",213:"world.",214:"I",218:"guide",220:"YouTube,",
 231:"watch",233:"Posting",234:"every",240:"tomorrow."}
for i,t in EXPECT.items():
    got=WS[i]["text"]
    assert got.lower().rstrip(",.!?")==t.lower().rstrip(",.!?"), f"anchor mismatch idx {i}: expected {t!r} got {got!r}"
def T(i): return round(WS[i]["start"],2)
random.seed(11)

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
def shake_js(t,amp=11,tgt=None):
    tgt=tgt or f"#in{bi}"
    return (f'tl.fromTo("{tgt}",{{x:0}},{{keyframes:[{{x:-{amp},duration:0.04}},'
            f'{{x:{amp-3},duration:0.04}},{{x:-{amp//2},duration:0.04}},{{x:0,duration:0.04}}]}},{t:.2f});')
def burst_html(pref,n=10):
    return "".join(f'<span class="bdot" id="{pref}{k}"></span>' for k in range(n))
def burst_js(pref,t,n=10,sx=260,sy=200):
    out=[]
    for k in range(n):
        out.append(f'tl.fromTo("#{pref}{k}",{{opacity:1,scale:0.4,x:0,y:0}},'
                   f'{{opacity:0,scale:1,x:{random.randint(-sx,sx)},y:{random.randint(-sy,sy)},'
                   f'duration:0.55,ease:"power2.out",immediateRender:false}},{t:.2f});')
    return "".join(out)
CARD=( '<div class="ccard" id="{id}"><div class="cchip"></div>'
       '<div class="cdots"><span></span><span></span><span></span><span></span></div></div>')

# ---- B2: card hovers -> shield slams -> red $ charge BOUNCES OFF ----
s,e=17.14,20.78
h=( f'<div class="hookwrap" id="hw2"><div class="cardwrap" id="cw2">{CARD.format(id="cc2")}'
    f'<div class="shield" id="sh2"><svg viewBox="0 0 100 110" width="190" height="209">'
    f'<path d="M50 4 L92 20 V56 C92 84 74 100 50 108 C26 100 8 84 8 56 V20 Z" fill="{A}"/>'
    f'<path d="M32 55 L45 68 L70 40" fill="none" stroke="#fff" stroke-width="9" '
    f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
    f'<div class="charge" id="ch2">$</div>{burst_html("b2",8)}</div></div>')
js=[
 f'tl.fromTo("#cc2",{{opacity:0,y:80,rotate:18,scale:0.7}},{{opacity:1,y:0,rotate:-6,scale:1,duration:0.34,ease:"back.out(1.6)"}},{T(63)-0.1:.2f});',
 f'tl.to("#cw2",{{y:-10,yoyo:true,repeat:5,duration:0.5,ease:"sine.inOut"}},{T(63)+0.3:.2f});',
 f'tl.fromTo("#sh2",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.22,ease:"power4.out"}},{T(69):.2f});',
 shake_js(T(69)+0.1,9),
 # the charge attempt: red $ flies in, hits the shield, deflects away with sparks
 f'tl.fromTo("#ch2",{{opacity:0,x:520,y:-160,rotation:0,scale:0.7}},{{opacity:1,x:130,y:-20,rotation:-30,scale:1,duration:0.3,ease:"power2.in",immediateRender:false}},{T(70):.2f});',
 burst_js("b2",T(70)+0.30,8,180,140),
 shake_js(T(70)+0.30,12),
 f'tl.to("#ch2",{{x:560,y:260,rotation:180,opacity:0,duration:0.45,ease:"power2.out"}},{T(70)+0.32:.2f});',
 f'tl.to("#sh2",{{scale:1.14,yoyo:true,repeat:1,duration:0.09}},{T(70)+0.30:.2f});',
 f'tl.to("#sh2",{{scale:1.08,yoyo:true,repeat:1,duration:0.11}},{T(76)-0.15:.2f});']
beat(s,e,"ctr",h,js)

# ---- B3: globe spins -> BANNED stamp -> VPN pill + tunnel arc ----
s,e=20.78,23.76
h=( f'<div class="hookwrap" id="hw3"><div class="gwrap" id="gw3">'
    f'<svg viewBox="0 0 100 100" width="250" height="250" class="gspin" id="globe3">'
    f'<circle cx="50" cy="50" r="44" fill="none" stroke="#141414" stroke-width="4.5"/>'
    f'<ellipse cx="50" cy="50" rx="20" ry="44" fill="none" stroke="#141414" stroke-width="3.5"/>'
    f'<ellipse cx="50" cy="50" rx="36" ry="44" fill="none" stroke="#141414" stroke-width="2"/>'
    f'<line x1="6" y1="50" x2="94" y2="50" stroke="#141414" stroke-width="3.5"/>'
    f'<line x1="12" y1="30" x2="88" y2="30" stroke="#141414" stroke-width="3"/>'
    f'<line x1="12" y1="70" x2="88" y2="70" stroke="#141414" stroke-width="3"/></svg>'
    f'<svg viewBox="0 0 100 100" width="270" height="270" class="ban" id="ban3">'
    f'<circle cx="50" cy="50" r="45" fill="none" stroke="{RED}" stroke-width="9"/>'
    f'<line x1="19" y1="81" x2="81" y2="19" stroke="{RED}" stroke-width="9" stroke-linecap="round"/></svg>'
   f'<div class="vokglow" id="vg3"></div>'
    f'<svg viewBox="0 0 120 120" width="200" height="200" class="vcheck"><path id="vck3" '
    f'd="M28 62 L52 86 L94 38" fill="none" stroke="#22c55e" stroke-width="13" '
    f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="130" stroke-dashoffset="130"/></svg>'
    f'{burst_html("b3",8)}</div>'
    f'<div class="vpnpill" id="vp3">VPN</div></div>')
js=[
 f'tl.fromTo("#gw3",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.26,ease:"back.out(2)"}},{s+0.10:.2f});',
 f'tl.fromTo("#globe3",{{rotation:-8}},{{rotation:8,duration:2.6,ease:"sine.inOut"}},{s+0.10:.2f});',
 f'tl.fromTo("#ban3",{{opacity:0,scale:2.6,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:0.2,ease:"power4.out",immediateRender:false}},{T(82)-0.05:.2f});',
 f'tl.to("#globe3",{{filter:"grayscale(1) opacity(0.45)",duration:0.2}},{T(82):.2f});',
 shake_js(T(82)+0.05,12),
 # VPN saves it: ban shatters off, globe revives, tunnel arc dashes across, pill slams
 f'tl.to("#ban3",{{opacity:0,scale:1.7,duration:0.22,ease:"power2.in"}},{T(89)-0.12:.2f});',
 burst_js("b3",T(89)-0.05,8,220,160),
 f'tl.to("#globe3",{{filter:"grayscale(0) opacity(1)",duration:0.25}},{T(89)-0.05:.2f});',
 f'tl.fromTo("#vg3",{{opacity:0,scale:0.5}},{{opacity:1,scale:1.2,duration:0.4,ease:"power2.out",immediateRender:false}},{T(89)-0.02:.2f});',
 f'tl.fromTo("#vck3",{{attr:{{"stroke-dashoffset":130}}}},{{attr:{{"stroke-dashoffset":0}},duration:0.35,ease:"power2.out"}},{T(89):.2f});',
 f'tl.to(".vcheck",{{scale:1.12,yoyo:true,repeat:1,duration:0.1,ease:"power2.out"}},{T(89)+0.38:.2f});',
 f'tl.fromTo("#vp3",{{opacity:0,scale:0,y:24}},{{opacity:1,scale:1,y:0,duration:0.26,ease:"back.out(2.2)"}},{T(89):.2f});',
 shake_js(T(89)+0.1,10)]
beat(s,e,"ctr",h,js)

# ---- B4: payoff — confetti -> $300 -> GEMINI sparkle pill ----
s,e=50.30,55.48
CONF="".join(f'<span class="conf {"round" if k%3==2 else ""}" id="cf{k}" style="background:{c}"></span>'
             for k,c in enumerate(([A,"#ffd166",LOOM,RED,"#22c55e"]*6)[:26]))
h=( f'<div class="hookwrap" id="hw4">{CONF}<div class="big300" id="t300b">$300</div>'
    f'<div class="gempill" id="gp4"><svg viewBox="0 0 100 100" width="52" height="52">'
    f'<path d="M50 2 L60 40 L98 50 L60 60 L50 98 L40 60 L2 50 L40 40 Z" fill="{LOOM}"/></svg>'
    f' GEMINI 3.1 PRO</div></div>')
cjs="".join(
    f'tl.fromTo("#cf{k}",{{opacity:1,scale:{0.6+random.random()*0.6:.2f},x:0,y:0,rotation:0}},'
    f'{{keyframes:[{{x:{random.randint(-420,420)},y:{-random.randint(140,420)},rotation:{random.randint(-220,220)},duration:{0.38+random.random()*0.22:.2f},ease:"power2.out"}},'
    f'{{y:{random.randint(240,520)},x:"+={random.randint(-90,90)}",rotation:"+={random.randint(-160,160)}",duration:{0.7+random.random()*0.4:.2f},ease:"power1.in"}}],'
    f'opacity:0,duration:{1.3+random.random()*0.4:.2f},ease:"none",immediateRender:false}},WONE+{(random.random()*0.12):.2f});'
    for k in range(26))
cjs=cjs.replace("WONE",f"{T(192):.2f}")
js=[cjs,
 f'tl.fromTo("#t300b",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:0.24,ease:"power4.out"}},{T(198):.2f});',
 shake_js(T(198)+0.12,13),
 f'tl.fromTo("#gp4",{{opacity:0,y:30,scale:0.7}},{{opacity:1,y:0,scale:1,duration:0.28,ease:"back.out(2)"}},{T(209):.2f});',
 f'tl.to("#gp4",{{scale:1.06,yoyo:true,repeat:1,duration:0.12}},{T(213):.2f});']
beat(s,e,"ctr",h,js)

# ---- B5: the actual YouTube video card ----
s,e=55.48,59.32
h=( f'<div class="hookwrap" id="hw5"><div class="ytcard" id="yc5">'
    f'<div class="ytthumbwrap"><img src="assets/yt_thumb.jpg" class="ytthumb"/>'
    f'<div class="ytplay" id="ypl5"><span class="yttri sm"></span></div></div>'
    f'<div class="yttitle">Never Pay for AI Ever Again</div>'
    f'<div class="ytmeta">54K views &middot; 1 month ago</div></div></div>')
js=[
 f'tl.fromTo("#yc5",{{opacity:0,scale:0.6,y:60}},{{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{T(218):.2f});',
 shake_js(T(220),10),
 f'tl.to("#ypl5",{{scale:1.18,yoyo:true,repeat:3,duration:0.28,ease:"sine.inOut"}},{T(220)+0.3:.2f});',
 f'tl.to("#yc5",{{scale:1.04,yoyo:true,repeat:1,duration:0.12}},{T(231):.2f});']
beat(s,e,"ctr",h,js)

# ---- B6: calendar ----
s,e=59.32,TOTAL
days="".join(f'<span class="day" id="dy{k}">{n}</span>' for k,n in enumerate(["M","T","W","T","F","S","S"]))
h=f'<div class="hookwrap" id="hw6"><div class="days">{days}</div></div>'
js=[
 "".join(f'tl.fromTo("#dy{k}",{{opacity:0,scale:0.4,y:20}},{{opacity:1,scale:1,y:0,duration:0.2,ease:"back.out(2.4)"}},{T(234)+k*0.08:.2f});' for k in range(7)),
 "".join(f'tl.to("#dy{k}",{{background:"{A}",color:"#1a0e06",duration:0.12}},{T(234)+0.14+k*0.08:.2f});' for k in range(7))]
beat(s,e,"ctr",h,js)

# ---- decorative bg (white) ----
NP=22
parts_html="".join(f'<span class="pt" id="pt{k}" style="left:{(k*131+40)%1040}px;top:{(k*97+30)%760}px;width:{5+(k%3)*3}px;height:{5+(k%3)*3}px;opacity:{0.12+0.2*((k*7)%5)/5:.2f}"></span>' for k in range(NP))
streaks_html="".join(f'<span class="stk" id="stk{k}" style="top:{120+k*230}px"></span>' for k in range(3))
bg=['tl.to("#glow",{x:120,y:30,scale:1.15,duration:6,yoyo:true,repeat:12,ease:"sine.inOut"},0);',
    'tl.to("#grid",{backgroundPosition:"0px 110px",duration:6,ease:"none",repeat:12},0);']
for k in range(NP):
    dur=4+(k%5)
    bg.append(f'tl.to("#pt{k}",{{y:-{120+(k%4)*60},duration:{dur},ease:"none",repeat:{int(70/dur)+1}}},0);')
    bg.append(f'tl.to("#pt{k}",{{opacity:0,duration:{dur},yoyo:true,repeat:{int(70/dur)+1},ease:"sine.inOut"}},0);')
for k in range(3):
    bg.append(f'tl.fromTo("#stk{k}",{{x:-1200}},{{x:1200,duration:{5+k*2},ease:"none",repeat:12}},{k*1.5});')

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
.inner.ctr{{align-items:center}}
.hookwrap{{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px}}
.ccard{{position:relative;width:460px;height:290px;border-radius:26px;background:linear-gradient(135deg,#2b2b36,#15151d);box-shadow:0 18px 40px rgba(20,20,20,0.25)}}
.cchip{{position:absolute;top:56px;left:44px;width:74px;height:54px;border-radius:10px;background:{A}}}
.cdots{{position:absolute;bottom:48px;left:44px;display:flex;gap:22px}}
.cdots span{{width:64px;height:12px;border-radius:6px;background:rgba(255,255,255,0.35)}}
.strike{{position:absolute;width:640px;height:16px;background:{RED};border-radius:8px;transform:rotate(-16deg);box-shadow:0 0 26px {REDD}}}
.strike.sm{{width:340px;height:13px}}
.zero{{position:absolute;color:#141414;font-size:300px;font-weight:900;letter-spacing:-8px;text-shadow:0 0 60px {GL}}}
.big300{{color:#141414;font-size:270px;font-weight:900;letter-spacing:-8px;text-shadow:0 0 60px {GL}}}
.stampfree{{position:absolute;bottom:110px;color:{RED};font-size:120px;font-weight:900;border:8px solid {RED};border-radius:24px;padding:6px 46px;box-shadow:0 0 38px {REDD};text-shadow:0 0 26px {REDD};background:rgba(255,255,255,0.75)}}
.bdot{{position:absolute;left:50%;top:50%;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:{A};box-shadow:0 0 14px {A};opacity:0}}
.conf{{position:absolute;left:50%;top:46%;width:16px;height:26px;margin:-8px 0 0 -8px;border-radius:4px;opacity:0}}
.conf.round{{width:16px;height:16px;border-radius:50%}}
.shield{{position:absolute;filter:drop-shadow(0 10px 24px {GL})}}
.gwrap{{position:relative;display:flex;align-items:center;justify-content:center}}
.gwrap .strike{{position:absolute}}
.vpnpill{{color:#fff;font-size:64px;font-weight:900;letter-spacing:4px;background:#22c55e;border-radius:22px;padding:20px 54px;box-shadow:0 14px 34px {GL}}}
.gempill{{display:flex;align-items:center;gap:18px;color:#141414;font-size:56px;font-weight:900;border:3px solid {AD};border-radius:22px;padding:18px 40px;background:rgba(240,129,63,0.07)}}
.ytbtn{{width:330px;height:232px;border-radius:52px;background:#ff0033;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 44px rgba(255,0,51,0.35)}}
.yttri{{width:0;height:0;border-left:86px solid #fff;border-top:52px solid transparent;border-bottom:52px solid transparent;margin-left:14px}}
.ytpill{{color:#141414;font-size:52px;font-weight:900;letter-spacing:3px;border:3px solid {AD};border-radius:20px;padding:16px 38px;background:rgba(240,129,63,0.07)}}
.cardwrap{{position:relative;display:flex;align-items:center;justify-content:center}}
.charge{{position:absolute;width:120px;height:120px;border-radius:50%;background:{RED};color:#fff;font-size:74px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px {REDD};opacity:0}}
.gspin{{filter:none}}
.ban{{position:absolute;opacity:0;filter:drop-shadow(0 0 22px {REDD})}}
.vcheck{{position:absolute;filter:drop-shadow(0 4px 16px rgba(34,197,94,0.5))}}
.vokglow{{position:absolute;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(34,197,94,0.28),transparent 62%);opacity:0}}
.ytcard{{display:flex;flex-direction:column;gap:18px;width:860px}}
.ytthumbwrap{{position:relative;width:860px;height:484px;border-radius:28px;overflow:hidden;box-shadow:0 18px 44px rgba(20,20,20,0.3)}}
.ytthumb{{width:100%;height:100%;object-fit:cover}}
.ytplay{{position:absolute;top:50%;left:50%;width:150px;height:106px;margin:-53px 0 0 -75px;border-radius:26px;background:#ff0033;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(255,0,51,0.5)}}
.yttri.sm{{border-left:40px solid #fff;border-top:24px solid transparent;border-bottom:24px solid transparent;margin-left:8px}}
.yttitle{{color:#141414;font-size:52px;font-weight:900}}
.ytmeta{{color:#8b938e;font-size:38px;font-weight:700}}
.days{{display:flex;gap:18px}}
.day{{width:118px;height:130px;border-radius:22px;background:rgba(240,129,63,0.07);border:3px solid {AD};color:#141414;font-size:56px;font-weight:900;display:flex;align-items:center;justify-content:center}}
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
print(f"short4: {bi} beats, total {TOTAL}s")
