#!/usr/bin/env python3
"""Exact lip-sync proof on the DELIVERED section mp4s.   python3 verify_final_sync.py <project_dir> [section ...]

For 6 frames spread over each section (incl. ~1 s before the end, where drift is largest) the section's own renderer
re-creates that exact output frame with the camera picture shifted by k = -6..+6 frames and we find the k that best matches
the delivered frame. Graphics/captions are identical for every k, so only the presenter decides. k must be 0 (±1 frame).
Frames where the presenter barely moves (flat error curve) are skipped. Exit 1 if any |k| > 1."""
import sys,glob,subprocess,os,numpy as np
P=os.path.abspath(sys.argv[1]);only=set(sys.argv[2:]);sys.path.insert(0,P+'/lib');sys.path.insert(0,P+'/lib/helpers')
import render_section as RS
bad=0
for d in sorted(glob.glob(P+'/sections/*/')):
    name=d.rstrip('/').split('/')[-1]
    if only and name not in only: continue
    if not os.path.exists(d+name+'.mp4') or not os.path.exists(d+'scenes.py'): continue
    for m in [m for m in list(sys.modules) if m=='scenes']: del sys.modules[m]
    sec=RS.Section(d);res=[]
    for t in list(np.linspace(1.5,sec.D-1.0,6)):
        n=round(t*RS.FPS);b=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{max(0,(n-.5)/RS.FPS):.4f}','-i',d+name+'.mp4','-frames:v','1','-vf','scale=480:270','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
        g=np.frombuffer(b,np.uint8).astype(np.float32)
        if len(g)!=480*270*3: continue
        curve=[]
        for k in range(-6,7):
            im=sec.frame(n,sec.cam_at((n+k)/RS.FPS)).resize((480,270));curve.append(float(((np.asarray(im,np.float32).ravel()-g)**2).mean()))
        if min(curve)<0.75*np.median(curve): res.append(int(np.argmin(curve))-6)
    ok=bool(res) and all(abs(k)<=1 for k in res);bad+=not ok
    print(('ok  ' if ok else ('??  ' if not res else 'BAD '))+name,'presenter offset in frames at sampled moments:',res)
sys.exit(1 if bad else 0)
