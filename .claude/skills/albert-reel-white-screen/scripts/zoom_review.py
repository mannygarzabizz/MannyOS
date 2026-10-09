#!/usr/bin/env python3
"""Zoom REVIEW step for split-screen tutorial reels (MANDATORY after screen_windows.py).
Verifies every rendered screen window actually shows CONTENT at its punch target —
catches "zoomed in on nothing" (blank terminal space, empty panels).

For each window and each stage: samples frames from the rendered w<N>.mp4 during the
stage's settled period and computes a detail score (mean gradient magnitude of the
central 80% region, 0-255 scale). Blank dark/white areas score <1.5; readable UI/text
scores >3. Stages below threshold are FLAGGED, and the source frame is scanned with a
sliding viewport (the window's zoom size, 12x12 grid) for the highest-detail focus,
printed as a suggested fx/fy.

Suggestions are STARTING POINTS — eyeball the suggested region (it prints the crop) and
prefer semantically right targets (input line WITH text, banner, popup) over raw max
detail. Usage: zoom_review.py <windows.json> <screens_dir> [threshold=1.5]
Exit code 1 if any stage flagged."""
import json, sys, subprocess, os, tempfile
from PIL import Image

cfg=json.load(open(sys.argv[1])); SDIR=sys.argv[2]
TH=float(sys.argv[3]) if len(sys.argv)>3 else 1.5

def load_ranges(p):
    return [(float(r["start"]),float(r["end"])) for r in json.load(open(p))["ranges"]]
def make_mapper(ranges):
    def f(t):
        acc=0.0
        for a,b in ranges:
            d=b-a
            if t<=acc+d: return a+(t-acc)
            acc+=d
        return ranges[-1][1]
    return f
chain=[]
for p in cfg.get("extra_edls",[])[::-1]: chain.append(make_mapper(load_ranges(p)))
if cfg.get("edl_sil"): chain.append(make_mapper(load_ranges(cfg["edl_sil"])))
chain.append(make_mapper(load_ranges(cfg["edl"])))
def to_master(t):
    for m in chain: t=m(t)
    return t

def grab(path,t,vf=None):
    fd,tmp=tempfile.mkstemp(suffix=".png"); os.close(fd)
    cmd=["ffmpeg","-y","-v","error","-ss",f"{t:.3f}","-i",path]
    if vf: cmd+=["-vf",vf]
    cmd+=["-frames:v","1",tmp]
    subprocess.run(cmd,check=True)
    im=Image.open(tmp).convert("L"); os.unlink(tmp)
    return im

def detail(im, box=None):
    """mean abs gradient over region (0-255 scale)"""
    if box: im=im.crop(box)
    im=im.resize((240,135))
    px=list(im.get_flattened_data()) if hasattr(im,"get_flattened_data") else list(im.getdata())
    w,h=240,135; tot=0; n=0
    for y in range(0,h-1,2):
        row=y*w
        for x in range(0,w-1,2):
            p=px[row+x]
            tot+=abs(p-px[row+x+1])+abs(p-px[row+w+x]); n+=2
    return tot/n

flagged=[]
for n,w in enumerate(cfg["windows"]):
    A,B=w["start"],w["end"]; D=B-A
    stages=w.get("stages") or [{"at":w.get("hold",0.5),"zoom":w.get("zoom",1.5),
                                "fx":w.get("fx",0.5),"fy":w.get("fy",0.4)}]
    wp=os.path.join(SDIR,f"w{n}.mp4")
    for si,st in enumerate(stages):
        t0=st["at"]+w.get("punch",0.35)+0.15
        t1=stages[si+1]["at"]-0.1 if si+1<len(stages) else D-0.1
        if t1<=t0: t1=t0+0.05
        scores=[]
        for frac in (0.15,0.5,0.85):
            t=t0+(t1-t0)*frac
            im=grab(wp,min(t,D-0.05))
            W,H=im.size
            scores.append(detail(im,(int(W*0.1),int(H*0.1),int(W*0.9),int(H*0.9))))
        sc=sum(scores)/len(scores)
        ok=sc>=TH
        print(f"w{n} stage{si} z{st['zoom']} @({st['fx']},{st['fy']}) score={sc:.2f} {'PASS' if ok else 'FLAG <-- zooming on nothing?'}")
        if not ok:
            # scan source frame for the most detailed viewport at this zoom
            src_t=w["src_t"]+(t0+t1)/2 if "src_t" in w else to_master(A+ (t0+t1)/2 )+w.get("offset",cfg["offset"])
            crop=w.get("src_crop",cfg.get("src_crop"))
            im=grab(w.get("screen_src",cfg["screen_src"]),src_t,vf=(f"crop={crop}," if crop else "")+"scale=960:540")
            z=st["zoom"]; vw,vh=int(960/z),int(540/z)
            best=None
            for gy in range(12):
                for gx in range(12):
                    fx,fy=gx/11,gy/11
                    x=int((960-vw)*fx); y=int((540-vh)*fy)
                    s=detail(im,(x,y,x+vw,y+vh))
                    if best is None or s>best[0]: best=(s,fx,fy)
            flagged.append((n,si,best))
            print(f"   suggest: fx={best[1]:.2f} fy={best[2]:.2f} (detail {best[0]:.2f}) — verify it's the RIGHT content, not just the busiest")
if flagged:
    print(f"\n{len(flagged)} stage(s) flagged"); sys.exit(1)
print("\nall stages PASS")
