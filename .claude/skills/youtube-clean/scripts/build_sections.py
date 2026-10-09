#!/usr/bin/env python3
"""YouTube Clean — build every section's voice.mkv in ONE pass, picture and sound guaranteed 1:1.

  python3 build_sections.py <project_dir> [section ...]

Reads <project>/edit/edl.json:
  {"sources":{"cam":"/abs/camera.mp4","screen":"/abs/screen-recording.mov"},
   "ranges":[{"sec":"00-intro","start":78.21,"end":84.20}, ...]}      # times are CAMERA seconds, in playback order

For each section writes sections/<sec>/voice.mkv = camera PICTURE + screen-recording AUDIO, plus timeline.json, _cam.wav, _voice.wav.

Why this exists (lesson of 2026-09-18): cutting each range to its own file and concatenating them pads every cut's video to a
whole frame and leaves timestamp gaps at the joins -> the presenter drifts up to 0.5 s out of lip-sync by the end of a section.
So here there are NO per-range files:
  * audio = one gapless buffer; range k occupies samples [P_k, P_k+N_k); 4 ms fades at range edges
  * video = ONE encoder per section on a constant 30 fps clock; output frame i (t=i/30) shows the camera frame at
            range.start + (t - P_k/SR)  -> rounding never accumulates
  * screen-mic offset: measured per range by cross-correlation against the camera audio, then ONE median offset per section
            (short ranges can lock +-10 ms off on their own)
Then run verify_sync.py. Do not hand sections to agents until it reports <= 40 ms everywhere.
"""
import json,sys,os,math,subprocess,wave,numpy as np
SR=48000;FPS=30
def wav48(src,out):
    if not os.path.exists(out): subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vn','-ar',str(SR),'-ac','2','-c:a','pcm_s16le',out],check=True)
    w=wave.open(out); return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,2).astype(np.float32)/32768
def speech_rms(x):
    m=x.mean(1);fr=m[:len(m)//480*480].reshape(-1,480);e=np.sqrt((fr**2).mean(1));return float(np.sqrt((e[e>np.percentile(e,40)]**2).mean()))
def main():
    P=os.path.abspath(sys.argv[1]);only=set(sys.argv[2:]);E=json.load(open(f'{P}/edit/edl.json'));cam,scr=E['sources']['cam'],E['sources']['screen']
    for s in ('cam','screen'):
        st=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=start_time','-of','csv=p=0',E['sources'][s]]).decode().split()
        if any(abs(float(x))>1e-3 for x in st if x not in ('N/A','')): sys.exit(f'{s}: a stream does not start at 0 ({st}) - remux it first, offsets would be wrong')
    C=wav48(cam,f'{P}/edit/cam48.wav');S=wav48(scr,f'{P}/edit/screen48.wav');Cm,Sm=C.mean(1),S.mean(1)
    # VO INSERTS: any other key in edl.sources is a voice-over take (a recording of him talking with no usable
    # camera picture — e.g. a screen recording made later). A range carrying {"src": "<key>"} takes its AUDIO from
    # that file; its PICTURE is one held camera frame from "hold" (default: the previous range's end), because the
    # scene MUST cover a VO range with `full:hidden` — we never show a face that is not saying these words.
    INS={k:wav48(v,f'{P}/edit/_ins_{k}.wav') for k,v in E['sources'].items() if k not in ('cam','screen')}
    if INS: print('VO insert sources:',{k:round(len(v)/SR,2) for k,v in INS.items()})
    # coarse global offset (screen_time - cam_time). 2026-09-20 fix: the old version correlated raw samples in a
    # b-window of only [t-10,t+40], so any offset beyond ~+20 s lost overlap and locked ~3 s wrong (silently, until
    # verify_sync caught it). Now: 100 Hz log-amplitude envelopes, NORMALISED correlation, full-overlap lags only,
    # a wide search (-60 .. +100 s), several probe times, and confidence-weighted line fit. Silent windows are dropped.
    HOP=SR//100
    def _env(x):
        n=len(x)//HOP;return np.log1p(np.abs(x[:n*HOP].reshape(n,HOP)).mean(1)*50)
    EC,ES=_env(Cm),_env(Sm)
    def off_at(t,win=40.0):
        a=EC[int(t*100):int((t+win)*100)]
        lo=max(0.0,t-60.0);b=ES[int(lo*100):int((t+win+100)*100)]
        if len(b)<=len(a)+1:b=ES[int(lo*100):]
        if len(a)<200 or len(b)<=len(a)+1:return None
        a=a-a.mean();bm=b-b.mean();L=len(a)+len(b)
        X=np.fft.irfft(np.fft.rfft(bm,L)*np.conj(np.fft.rfft(a,L)),L)[:len(b)-len(a)+1]
        nrm=np.sqrt(np.convolve(bm**2,np.ones(len(a)),'valid'))[:len(X)]
        X=X/(np.linalg.norm(a)*nrm+1e-9);k=int(np.argmax(X))
        return k/100.0-(t-lo),float(X[k])
    dur=len(Cm)/SR
    probes=[t for t in np.linspace(30,max(31,dur-70),9)]
    pts=[]
    for t in probes:
        r=off_at(t)
        if r and r[1]>=0.35:pts.append((float(t),r[0],r[1]))
    print('screen-cam offset (s):',[(round(t),round(o,4),round(c,2)) for t,o,c in pts])
    if not pts:sys.exit('could not measure the screen-cam offset on any window - check that both files are the same take')
    med=float(np.median([o for _,o,_ in pts]))
    pts=[q for q in pts if abs(q[1]-med)<1.0]
    if len(pts)>=3:
        _pf=np.polyfit(np.array([q[0] for q in pts],float),np.array([q[1] for q in pts],float),1)
        _a1,_a0=float(_pf[0]),float(_pf[1])          # NB: do not name this A - the section loop reuses A for the audio buffer
        coarse=lambda t:_a0+_a1*float(t)
        print(f'  drift {_a1*60*1000:+.2f} ms/min, offset at t=0 {_a0:.4f} s, {len(pts)} good windows')
    else:
        coarse=lambda t:med
        print(f'  constant offset {med:.4f} s ({len(pts)} good windows)')
    secs=[];[secs.append(r['sec']) for r in E['ranges'] if r['sec'] not in secs]
    pad=int(.25*SR);f=int(.004*SR);ramp=np.linspace(0,1,f)[:,None]
    for sec in secs:
        if only and sec not in only: continue
        d=f'{P}/sections/{sec}/';os.makedirs(d,exist_ok=True);R=[r for r in E['ranges'] if r['sec']==sec]
        N=[int(round((r['end']-r['start'])*SR)) for r in R];Pk=np.concatenate([[0],np.cumsum(N)]).astype(int);total=int(Pk[-1])
        lags=[]
        for r,n in zip(R,N):
            if n<SR*1.5 or r.get('src') in INS: continue
            a=Cm[int(r['start']*SR):int(r['start']*SR)+n];c0=int((r['start']+coarse(r['start']))*SR);b=Sm[c0-pad:c0+n+pad];L=len(a)+len(b)
            X=np.fft.irfft(np.fft.rfft(b,L)*np.conj(np.fft.rfft(a,L)),L);lags.append((c0-pad+int(np.argmax(X[:2*pad+1])))/SR-r['start'])
        med=float(np.median(lags)) if lags else coarse(R[0]['start'])
        A=np.zeros((total,2),np.float32);B=np.zeros((total,2),np.float32)
        for r,n,p in zip(R,N,Pk):
            if r.get('src') in INS:                      # VO: same audio in both buffers - there is no pair to align
                src=INS[r['src']];s0=int(round(r['start']*SR));seg=src[s0:s0+n].copy()
                if len(seg)<n: seg=np.vstack([seg,np.zeros((n-len(seg),2),np.float32)])
                seg[:f]*=ramp;seg[-f:]*=ramp[::-1];A[p:p+n]=seg;B[p:p+n]=seg
                continue
            for buf,src,o in ((A,C,0.0),(B,S,med)):
                s0=int(round((r['start']+o)*SR));seg=src[s0:s0+n].copy();seg[:f]*=ramp;seg[-f:]*=ramp[::-1];buf[p:p+len(seg)]=seg
        # VO inserts are recorded on a different mic at a different level, and the section-wide normalisation below
        # cannot fix that - it is ONE gain over a buffer the main voice dominates, so the insert stays ~4 dB low and
        # audibly drops (Albert, 2026-09-20). Level-match each VO range to the section's own speech first.
        vo_i=[k for k,r in enumerate(R) if r.get('src') in INS]
        if vo_i and len(vo_i)<len(R):
            def _srms(x):
                m=x.mean(1);fr=m[:len(m)//480*480].reshape(-1,480);e=np.sqrt((fr**2).mean(1))
                e=e[e>np.percentile(e,40)];return float(np.sqrt((e**2).mean())) if len(e) else 0.
            keep=np.ones(total,bool)
            for k in vo_i: keep[Pk[k]:Pk[k]+N[k]]=False
            main=_srms(B[keep]);vo=_srms(np.vstack([B[Pk[k]:Pk[k]+N[k]] for k in vo_i]))
            if main>1e-6 and vo>1e-6:
                g=min(6.0,main/vo)                       # cap the lift so a noisy take cannot be shouted up
                for k in vo_i: A[Pk[k]:Pk[k]+N[k]]*=g;B[Pk[k]:Pk[k]+N[k]]*=g
                print(f'  VO level-matched {20*math.log10(g):+.1f} dB to the section speech level')
        # every section is brought to the SAME speech level (speech-frame RMS −26 dBFS, peak-capped at −3 dBFS) so sections match
        # each other and a later rebuild of one section lands at the same level; final loudness is set once, at the stitch
        B*=10**(-26/20)/max(speech_rms(B),1e-6);pk=float(np.abs(B).max());B*=min(1.0,0.70/max(pk,1e-6))
        for name,buf in (('_cam.wav',A),('_voice.wav',B)):
            w=wave.open(d+name,'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(buf,-1,1)*32767).astype(np.int16).tobytes());w.close()
        NF=math.ceil(total/SR*FPS);tl=[]
        enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','yuv420p','-s','1920x1080','-r',str(FPS),'-i','pipe:0','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','30000',d+'_video_exact.mkv'],stdin=subprocess.PIPE)
        FB=1920*1080*3//2;written=0
        for k,(r,n,p) in enumerate(zip(R,N,Pk)):
            f0=math.ceil(p/SR*FPS-1e-9);f1=NF if k==len(R)-1 else math.ceil((p+n)/SR*FPS-1e-9);nf=f1-f0
            if nf<=0: continue
            vo=r.get('src') in INS
            hold=r.get('hold', R[k-1]['end']-0.05 if k else 0.0) if vo else None
            src_t=hold if vo else r['start']+(f0/FPS-p/SR)
            tl.append({'f0':f0,'f1':f1,'src_t':round(src_t,4),'p_s':round(p/SR,4),'cam_start':r['start'],'cam_end':r['end'],
                       **({'vo':r['src'],'held_frame':True} if vo else {})})
            dec=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{src_t:.4f}','-i',cam,'-map','0:v:0','-vf',f'fps={FPS},scale=1920:1080,format=yuv420p','-frames:v',str(1 if vo else nf),'-f','rawvideo','pipe:1'],stdout=subprocess.PIPE)
            got=0;last=None
            while got<nf:
                buf=dec.stdout.read(FB)
                if len(buf)<FB: break
                enc.stdin.write(buf);last=buf;got+=1
            while got<nf and last is not None: enc.stdin.write(last);got+=1
            dec.stdout.close();dec.wait();written+=got
        enc.stdin.close();enc.wait();assert written==NF,(sec,written,NF)
        subprocess.run(['ffmpeg','-v','error','-y','-i',d+'_video_exact.mkv','-i',d+'_voice.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','pcm_s16le',d+'voice.mkv'],check=True)
        json.dump({'fps':FPS,'frames':NF,'audio_s':total/SR,'screen_minus_cam_s':round(med,4),'cam':cam,'timeline':tl},open(d+'timeline.json','w'),indent=1)
        print(f'{sec}: {NF} frames = {NF/FPS:.3f}s picture, {total/SR:.3f}s sound, screen-mic offset {med:.4f}s, {len(R)} ranges')
if __name__=='__main__': main()
