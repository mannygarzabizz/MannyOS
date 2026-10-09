#!/usr/bin/env python3
"""YouTube Clean — build every section's CLEAN screen-share layer on the section's exact timeline.

  python3 build_screen.py <project_dir> [section ...]          (run AFTER build_sections.py + verify_sync.py)

Reads edit/edl.json (sources.screen) + sections/<sec>/timeline.json (frame ranges, camera seconds, screen-cam offset).
Writes sections/<sec>/screen.mp4  — 1920x930, 30 fps, exactly timeline.frames frames, NO audio, frame i == voice.mkv frame i
       sections/<sec>/screen_meta.json — per frame: chrome bottom y0 found in the source, zoomed flag, cut frames
       sections/<sec>/review/screen_sheet.jpg — 1 frame / 2 s contact sheet, 10 per row (tile n = second 2n). The mediator READS it and marks script spans.

What "clean" means (Albert, 2026-09-19 — Screen Studio recordings with auto zoom):
  * The browser/OS chrome (menu bar, tabs, URL bar, bookmarks) is never shown. Un-zoomed frames carry it in the top ~150 px of
    1080; Screen Studio's zoom slides it out. Per frame we find the chrome's bottom edge (rows of teal menu bar / neutral dark
    grey that end in a bright page row), smooth it over time, and crop below it. Output aspect is fixed (1920x930) so the card
    never changes shape: un-zoomed -> rows 150..1080; fully zoomed -> centre rows 75..1005; continuous in between.
  * Jump cuts from the voice cut would make a zooming capture jerk. Every cut gets a 5-frame cross-dissolve on the screen layer
    only (the camera keeps its hard cut, the audio is untouched) — reads as a soft "time passes" blink.
  * Blank / reload flashes (a near-uniform frame: tab switch, page reload, loading spinner) (runs of <= 10 frames with content on both sides) are replaced
    by the last good frame.
  * Independent leak scan over the OUTPUT (teal or 59-grey rows in the top 48 px) - read every flagged frame; flags on dark
    app pages are usually false positives.
  * No retiming: screen time = camera time + the section's measured offset, frame for frame with the voice.
"""
import json,sys,os,math,subprocess,numpy as np
from PIL import Image
FPS=30;OW,OH=1920,930;CH=150;XF=5   # CH = chrome height in an un-zoomed 1080p frame (measure once per recording; see --chrome)
def chrome_bottom(g,rgb):
    """rgb: HxWx3 int array (any height; 540 in pass 1). Returns the chrome's bottom edge in 1080p rows (0 = no chrome visible).
    Chrome = macOS menu bar (teal on this Mac) + Chrome tabs + URL bar + BOOKMARKS BAR. The bookmarks bar is always the lowest
    chrome element and has a flat #3B3B3B (59 grey) background at every zoom level, on light AND dark pages -> find the lowest
    THICK 59-grey band whose rows above are all chrome-like (teal, or dark neutral <= 70). A 1-2 px 59 line also separates tabs
    from the URL bar - thickness rejects it. No band + teal menu bar = another app window (e.g. Claude desktop) -> CH."""
    H=rgb.shape[0];k=1080/H;a=rgb[:,40:-40];lim=min(H,int(420/k))
    near=(np.abs(a[:lim]-59).max(2)<=6).mean(1)
    top=rgb[:max(2,int(6/k)),100:-100].reshape(-1,3).mean(0);teal=(top[1]-top[0])>40
    runs=[];y=0
    while y<lim:
        if near[y]>=.6:
            y0=y;gap=0
            while y<lim and (near[y]>=.6 or (near[y]>.05 and gap<int(16/k))):
                gap=0 if near[y]>=.6 else gap+1;y+=1
            y1=y-gap
            if (y1-y0)*k>=14: runs.append((y0,y1))
        y+=1
    for y0,y1 in reversed(runs):
        ab=a[:y0].astype(int)
        if len(ab):
            tl=(ab[...,1].mean(1)-ab[...,0].mean(1))>40
            dk=np.array([np.bincount((r.mean(1)//4).astype(int),minlength=64).argmax()*4<=72 for r in ab])
            if not (tl|dk).mean()>.9: continue
        # include the bar's dark bottom border / shadow (thicker when zoomed): extend while rows are dark and unlike the page
        md=lambda r:np.bincount((r.mean(1)//4).astype(int),minlength=64).argmax()*4
        page=md(a[min(H-1,y1+int(40/k))]);e=y1
        while e<min(H,y1+int(24/k)) and md(a[e])<=90 and abs(md(a[e])-page)>6: e+=1
        return int(round(e*k))
    if teal: return CH
    # sliver at the very top (zoom transitions: a few px of bookmarks bar / its dark border / motion-blurred chrome) on a light page
    mode=lambda r:np.bincount((r.mean(1)//4).astype(int),minlength=64).argmax()*4
    y=0
    while y<H and mode(a[y])<=90: y+=1
    if 0<y*k<=48 and y+int(8/k)<H and mode(a[y+int(8/k)])>150: return int(round(y*k))+2
    return 0
def crop(a,y):
    """1920x1080 frame + chrome bottom y (1080 rows, 0 = none) -> 1920x930 chrome-free frame, fixed aspect, continuous in y."""
    y=float(y)
    if y<=CH: top=y+(1-y/CH)*(CH/2);h=1080-CH
    else: top=y;h=1080-y
    w=h*OW/OH;x=(1920-w)/2
    if abs(h-OH)<1 and abs(top-round(top))<1e-6: return a[int(round(top)):int(round(top))+OH]
    return np.asarray(Image.fromarray(a).resize((OW,OH),Image.BICUBIC,box=(x,top,x+w,top+h)))
def main():
    P=os.path.abspath(sys.argv[1]);only=set(a for a in sys.argv[2:] if not a.startswith('--'))
    E=json.load(open(f'{P}/edit/edl.json'));scr=E['sources']['screen']
    secs=[];[secs.append(r['sec']) for r in E['ranges'] if r['sec'] not in secs]
    for sec in secs:
        if only and sec not in only: continue
        d=f'{P}/sections/{sec}/';T=json.load(open(d+'timeline.json'));off=T['screen_minus_cam_s'];NF=T['frames'];tl=T['timeline']
        # pass 1: analysis at 960x540 -> y0 per frame
        y0=np.zeros(NF);flat=np.zeros(NF,bool);FB=960*540*3
        for k,r in enumerate(tl):
            nf=r['f1']-r['f0']
            dec=subprocess.Popen(['ffmpeg','-v','error','-ss',f"{r['src_t']+off:.4f}",'-i',scr,'-map','0:v:0','-vf',f'fps={FPS},scale=960:540','-frames:v',str(nf),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
            for i in range(nf):
                b=dec.stdout.read(FB)
                if len(b)<FB: y0[r['f0']+i]=y0[r['f0']+i-1] if i else 0;continue
                a=np.frombuffer(b,np.uint8).reshape(540,960,3);yy=chrome_bottom(None,a.astype(int));y0[r['f0']+i]=yy
                sm=a[int(yy/2)+4::4,::4].reshape(-1,3).astype(int);flat[r['f0']+i]=(np.abs(sm-np.median(sm,0)).max(1)<=8).mean()>.996
            dec.stdout.close();dec.wait()
        # smooth inside each range (max over +-4 frames of the raw detections: never a median, it deletes one-frame detections in fast zooms) + 8 px safety
        ys=y0.copy()
        for r in tl:
            s=y0[r['f0']:r['f1']];n=len(s)
            if n<2: continue
            m=np.array([s[max(0,i-4):i+5].max() for i in range(n)])
            ys[r['f0']:r['f1']]=m
        ys=np.where(ys>0,np.minimum(ys+8,470),0)
        # blank / reload flashes: SHORT runs (<= 10 frames) of near-uniform frames with real content on both sides -> hold previous
        hold=np.zeros(NF,bool);i=0
        while i<NF:
            if flat[i]:
                j=i
                while j<NF and flat[j]: j+=1
                if j-i<=10 and i>0 and j<NF: hold[i:j]=True
                i=j
            else: i+=1
        # pass 2: full-res crop + cross-dissolve at cuts
        enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{OW}x{OH}','-r',str(FPS),'-i','pipe:0','-c:v','libx264','-preset','fast','-crf','15','-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','30000',d+'screen.mp4'],stdin=subprocess.PIPE)
        FB=1920*1080*3;tail=[];written=0;cuts=[];prev=None;holds=0
        for k,r in enumerate(tl):
            nf=r['f1']-r['f0'];last=None
            dec=subprocess.Popen(['ffmpeg','-v','error','-ss',f"{r['src_t']+off:.4f}",'-i',scr,'-map','0:v:0','-vf',f'fps={FPS},scale=1920:1080','-frames:v',str(nf+XF),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
            newtail=[]
            for i in range(nf+XF):
                b=dec.stdout.read(FB)
                if len(b)<FB:
                    if i<nf and last is not None: b=last
                    else: break
                last=b;a=np.frombuffer(b,np.uint8).reshape(1080,1920,3)
                if i>=nf:
                    yt=chrome_bottom(None,a[::2,::2].astype(int));newtail.append(crop(a,max(ys[r['f1']-1],yt+8 if yt else 0)));continue
                out=crop(a,ys[r['f0']+i])
                if hold[r['f0']+i] and prev is not None: out=prev;holds+=1
                else: prev=out
                if i<len(tail):
                    w=(i+1)/(XF+1);out=(out.astype(np.float32)*w+tail[i].astype(np.float32)*(1-w)).astype(np.uint8)
                enc.stdin.write(np.ascontiguousarray(out).tobytes());written+=1
            dec.stdout.close();dec.wait();tail=newtail
            if k: cuts.append(r['f0'])
        enc.stdin.close();enc.wait();assert written==NF,(sec,written,NF)
        leaks=leak_scan(d+'screen.mp4')
        json.dump({'fps':FPS,'frames':NF,'leak_frames':leaks,'held_blank_frames':[int(x) for x in np.nonzero(hold)[0]],'size':[OW,OH],'chrome_px':CH,'cuts':cuts,'y0':[int(v) for v in ys],'zoomed':[bool(v==0) for v in ys]},open(d+'screen_meta.json','w'))
        os.makedirs(d+'review',exist_ok=True);cols=10;n=max(1,math.ceil(NF/FPS/2));rows=math.ceil(n/cols)
        subprocess.run(['ffmpeg','-v','error','-y','-i',d+'screen.mp4','-vf',f"fps=1/2,scale=384:-1,tile={cols}x{rows}",'-frames:v','1','-q:v','4',d+'review/screen_sheet.jpg'])
        print(f'{sec}: screen.mp4 {NF} frames, {len(cuts)} dissolved cuts, chrome cropped in {int((ys>0).mean()*100)} % of frames, held {holds} blank/reload frames, LEAK SCAN: {len(leaks)} suspect frames {leaks[:12]}')
def leak_scan(path):
    """Independent check on the OUTPUT: any frame whose top 48 px still hold a teal menu-bar row or a 59-grey bookmarks row."""
    bad=[];FB=960*465*3
    p=subprocess.Popen(['ffmpeg','-v','error','-i',path,'-vf','scale=960:465','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
    n=0
    while True:
        b=p.stdout.read(FB)
        if len(b)<FB: break
        t=np.frombuffer(b,np.uint8).reshape(465,960,3)[:24,40:-40].astype(int)
        teal=((t[...,1]-t[...,0])>60).mean(1).max()>.6;g59=(np.abs(t-59).max(2)<=6).mean(1).max()>.6
        if teal or g59: bad.append(n)
        n+=1
    p.wait();return bad
if __name__=='__main__': main()
