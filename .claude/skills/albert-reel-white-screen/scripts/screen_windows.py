#!/usr/bin/env python3
"""Screen-share window extractor for split-screen tutorial reels (PUNCH-IN zooms).
Maps each FINAL-timeline window back through the edit EDLs to the raw screen recording,
crops away pillarbox bars (mac 16:10-ish screens inside a 16:9 recording), and applies a
PUNCH-IN zoom: brief full view -> fast ease onto the relevant UI (input field, dictation
popup, button) -> steady hold with a subtle drift. NOT a slow ken-burns.

windows.json:
{
  "screen_src": "...", "offset": 1.585,
  "src_crop": "1664:936:128:40",      # from cropdetect + trimming menubar/dock to 16:9;
                                       # omit for an exactly-16:9 source
  "edl": "edit/edl.json", "edl_sil": "edit/edl_sil.json", "extra_edls": [...],
  "windows": [ {"start":5.7,"end":9.5,"zoom":1.6,"fx":0.45,"fy":0.30,"hold":0.5,"punch":0.35}, ... ]
    # zoom = punch target scale; fx/fy = focus point (fractions of CROPPED content);
    # hold = seconds of full view before the punch; punch = punch duration seconds
}
Focus picking (do this by LOOKING at a frame of each window): typing -> the input field;
dictation tool popup on screen -> the popup; a button/URL being clicked -> that region;
reading output -> the text block. Zoom 1.6-1.9 for small UI, 1.3-1.5 for text blocks.
Usage: screen_windows.py <windows.json> <outdir>"""
import json, sys, subprocess, os

cfg=json.load(open(sys.argv[1])); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)

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

for n,w in enumerate(cfg["windows"]):
    A,B=w["start"],w["end"]; D=B-A
    # per-window source override (multi-recording reels: hook pair vs body pair)
    src=w.get("screen_src",cfg["screen_src"]); off=w.get("offset",cfg["offset"])
    src_t=w["src_t"] if "src_t" in w else to_master(A)+off   # src_t: absolute source time (footage from another moment)
    crop=w.get("src_crop",cfg.get("src_crop"))
    pre=(f"crop={crop}," if crop else "")+"scale=1920:1080,fps=25"
    P=max(1,int(w.get("punch",0.35)*25))
    stages=w.get("stages") or [{"at":w.get("hold",0.5),"zoom":w.get("zoom",1.5),
                                "fx":w.get("fx",0.5),"fy":w.get("fy",0.4)}]
    # keyframed punch chain: full view -> stage0 focus -> stage1 focus -> ... (cosine eases)
    def kf_chain(vals, frames):
        # piecewise expr over 'on': eases from prev val to vals[k] starting at frames[k]
        expr=f"{vals[-1]}"
        for k in range(len(vals)-1,0,-1):
            F=frames[k]; a=vals[k-1]; b=vals[k]
            ease=f"({a}+({b}-{a})*(0.5-0.5*cos(PI*(on-{F})/{P})))"
            expr=f"if(lt(on,{F}),{vals[k-1] if k>0 else vals[0]},if(lt(on,{F+P}),{ease},{expr}))"
        return expr
    zs=[1.001]+[s["zoom"] for s in stages]
    fxs=[stages[0]["fx"]]+[s["fx"] for s in stages]
    fys=[stages[0]["fy"]]+[s["fy"] for s in stages]
    frames=[0]+[max(1,int(s["at"]*25)) for s in stages]
    zexpr=kf_chain(zs,frames); fxe=kf_chain(fxs,frames); fye=kf_chain(fys,frames)
    vf=(f"{pre},zoompan=z='{zexpr}':d=1"
        f":x='(iw-iw/zoom)*({fxe})':y='(ih-ih/zoom)*({fye})':s=1920x1080:fps=25")
    out=os.path.join(OUT,f"w{n}.mp4")
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{src_t:.3f}","-i",src,
        "-t",f"{D:.3f}","-an","-vf",vf,"-c:v","libx264","-preset","medium","-crf","19",
        "-pix_fmt","yuv420p",out],check=True)
    print(f"w{n}: final {A:.2f}-{B:.2f} <- src {src_t:.2f} stages={stages}")
print(f"OK {len(cfg['windows'])} windows -> {OUT}")
