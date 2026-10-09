#!/usr/bin/env python3
"""YouTube Clean — stitch the ACCEPTED sections into the master.   python3 stitch.py <project_dir>

Reads <project>/stitch.json:
  {"sections":["00-intro","01-…",…],                      # playback order; each has sections/<s>/<s>.mp4
   "music":{"file":"audio/track.mp3","from":"00-intro","to":"02-…","track_start":0.0,"start_at":0.0 (s into 'from', e.g. after a silent cold open),
            "gain_db":-20,"fade_in":0.5,"fade_out":3.0},   # optional; ONE continuous pass across from…to
   "target_lufs":-14,"out":"renders/master.mp4"}
Dry stem per section (voice + SFX, NO music): sections/<s>/stem_nomusic.wav if present, else the audio of <s>.mp4
(so a section whose own mix contains music MUST provide stem_nomusic.wav).

Same rules as build_sections.py — this is where lip-sync is lost if done naively:
  * picture: every section is decoded and fed to ONE encoder on a constant 30 fps clock (no concat demuxer, no -shortest)
  * sound  : one buffer on the same frame grid; section k starts at sample round(F_k/30*48000) where F_k = frames before it
  * music  : one sidechain pass keyed by the whole dry mix → no level step at section joins; fade-out ends exactly at the
             end of the "to" section
  * loudness: static gain to target LUFS, then a limiter at −1.5 dBFS (its 5 ms latency is trimmed off again); measured and printed
Then verifies: frame count, per-section audio offset (cross-correlation vs the stems, must be 0 ms), picture identity at the
middle of each section, and writes chapters.txt + stitch_report.json next to the master."""
import json,sys,os,subprocess,numpy as np,wave,math
SR=48000;FPS=30
def sh(*a):return subprocess.check_output(a)
def nframes(p):return int(sh('ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',p).decode().strip().strip(','))
def pcm(p,extra=()):return np.frombuffer(sh('ffmpeg','-v','error',*extra,'-i',p,'-vn','-ac','2','-ar',str(SR),'-f','f32le','pipe:1'),np.float32).reshape(-1,2).copy()
def lufs(path):
    o=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',path,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=[l for l in o.splitlines() if l.strip().startswith('I:')][-1].split()[1];P=[l for l in o.splitlines() if l.strip().startswith('Peak:')][-1].split()[1];return float(I),float(P)
def main():
    P=os.path.abspath(sys.argv[1]);C=json.load(open(P+'/stitch.json'));secs=C['sections'];out=os.path.join(P,C.get('out','renders/master.mp4'));os.makedirs(os.path.dirname(out),exist_ok=True)
    vids=[f'{P}/sections/{s}/{s}.mp4' for s in secs];F=[nframes(v) for v in vids];F0=np.concatenate([[0],np.cumsum(F)]).astype(int);N=int(F0[-1]);total=int(round(N/FPS*SR))
    dry=np.zeros((total,2),np.float32);f=int(.004*SR);ramp=np.linspace(0,1,f,dtype=np.float32)[:,None];stems=[]
    for s,v,f0,nf in zip(secs,vids,F0,F):
        st=f'{P}/sections/{s}/stem_nomusic.wav';a=pcm(st if os.path.exists(st) else v);n=int(round(nf/FPS*SR));a=a[:n]
        if len(a)<n:a=np.vstack([a,np.zeros((n-len(a),2),np.float32)])
        a[:f]*=ramp;a[-f:]*=ramp[::-1];i=int(round(f0/FPS*SR));dry[i:i+n]=a[:total-i];stems.append((i,a))
    mix=dry.copy();M=C.get('music')
    if M:
        i0=int(round((F0[secs.index(M['from'])]/FPS+M.get('start_at',0))*SR));i1=int(round(F0[secs.index(M['to'])+1]/FPS*SR));L=(i1-i0)/SR
        np.ascontiguousarray(np.vstack([dry[i0:i1],np.zeros((2*SR,2),np.float32)])).tofile(out+'.key.f32')   # +2 s: sidechaincompress returns a bed shorter than its inputs
        fg=(f"[0:a]aresample={SR},atrim=start={M.get('track_start',0):.6f}:end={M.get('track_start',0)+L+2:.6f},asetpts=PTS-STARTPTS,volume={M.get('gain_db',-20)}dB[m];"
            f"[m][1:a]sidechaincompress=threshold=0.03:ratio=2:attack=15:release=250[o]")
        bed=np.frombuffer(sh('ffmpeg','-v','error','-i',os.path.join(P,M['file']),'-f','f32le','-ar',str(SR),'-ac','2','-i',out+'.key.f32','-filter_complex',fg,'-map','[o]','-ac','2','-ar',str(SR),'-f','f32le','pipe:1'),np.float32).reshape(-1,2).copy();os.remove(out+'.key.f32')
        assert len(bed)>=i1-i0-SR//100,('music bed came back short',len(bed),i1-i0)
        bed=bed[:i1-i0];bed=np.vstack([bed,np.zeros((i1-i0-len(bed),2),np.float32)]) if len(bed)<i1-i0 else bed
        a=int(M.get('fade_in',.5)*SR);b=int(M.get('fade_out',3)*SR);bed[:a]*=np.linspace(0,1,a,dtype=np.float32)[:,None];bed[-b:]*=np.linspace(1,0,b,dtype=np.float32)[:,None];mix[i0:i1]+=bed
    tmpw=out+'.premaster.wav';w=wave.open(tmpw,'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes());w.close()
    I,_=lufs(tmpw);g=C.get('target_lufs',-14)-I;fin=out+'.audio.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',tmpw,'-af',f'volume={g:.2f}dB,alimiter=limit=0.84:attack=5:release=60:level=disabled,atrim=start=0.005,apad=pad_dur=0.005','-ar',str(SR),'-c:a','pcm_s16le',fin],check=True)
    I2,P2=lufs(fin);print(f'loudness: {I:.1f} LUFS → gain {g:+.1f} dB → {I2:.1f} LUFS, true peak {P2:.1f} dBFS')
    # picture: ONE encoder  (--reuse-video: keep an existing master's picture if its frame count is right, redo audio only)
    if '--reuse-video' in sys.argv and os.path.exists(out) and nframes(out)==N:
        os.replace(out,out+'.v.mp4');subprocess.run(['ffmpeg','-v','error','-y','-i',out+'.v.mp4','-i',fin,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-movflags','+faststart',out],check=True);os.remove(out+'.v.mp4');vids_enc=False
    else:vids_enc=True
    enc=None if not vids_enc else subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','yuv420p','-s','1920x1080','-r',str(FPS),'-i','pipe:0','-i',fin,'-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','320k','-movflags','+faststart',out],stdin=subprocess.PIPE)
    FB=1920*1080*3//2;wr=0
    for v,nf in (zip(vids,F) if vids_enc else []):
        dec=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-an','-vf','format=yuv420p','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE);got=0;last=None
        while got<nf:
            b=dec.stdout.read(FB)
            if len(b)<FB:break
            enc.stdin.write(b);last=b;got+=1
        while got<nf and last is not None:enc.stdin.write(last);got+=1
        dec.stdout.close();dec.wait();wr+=got
    if vids_enc:enc.stdin.close();enc.wait();assert wr==N,(wr,N)
    # verify
    rep={'frames_expected':N,'frames':nframes(out),'lufs':I2,'true_peak':P2,'sections':[]};ma=pcm(out).mean(1);ok=rep['frames']==N
    for s,v,f0,nf,(i,a) in zip(secs,vids,F0,F,stems):
        n=min(len(a),SR*20);x=a[:n].mean(1);y=ma[max(0,i-2400):i+n+2400];L=len(x)+len(y);X=np.fft.irfft(np.fft.rfft(y,L)*np.conj(np.fft.rfft(x,L)),L);k=int(np.argmax(X[:4801]));off=(k-min(2400,i))/SR*1000
        # picture identity at 5 moments; a moment only counts when the error curve is NOT flat (still frames / holds match any
        # neighbour -> the single-midpoint check of 2026-09-19 reported a false '+3 frames' on a held shot). Exact frame seeks.
        def g(p,n):return np.frombuffer(sh('ffmpeg','-v','error','-ss',f'{max(0,(n-.5)/FPS):.4f}','-i',p,'-frames:v','1','-vf','scale=160:90,format=gray','-f','rawvideo','pipe:1'),np.uint8).astype(np.float32)
        votes=[]
        for q in (.15,.35,.5,.65,.85):
            m=int(nf*q);g1=g(v,m);err={d:float(((g(out,f0+m+d)-g1)**2).mean()) for d in range(-3,4)}
            b=min(err,key=err.get);srt=sorted(err.values())
            if srt[1]>1.5*srt[0]+2:votes.append(b)          # clear minimum only
        best=max(votes,key=abs) if votes else 0
        rep['sections'].append({'section':s,'start':f'{int(f0/FPS//60)}:{int(f0/FPS%60):02d}','frames':int(nf),'audio_offset_ms':round(off,1),'picture_offset_frames':best});ok&=abs(off)<2 and abs(best)<=1
        print(f"{s:28s} starts {rep['sections'][-1]['start']}  audio offset {off:+.1f} ms  picture offset {best:+d} frames")
    open(os.path.dirname(out)+'/chapters.txt','w').write('\n'.join(f"{r['start'] if r['start']!='0:0' else '0:00'} {r['section'].split('-',1)[1].replace('-',' ').capitalize()}" for r in rep['sections'])+'\n')
    json.dump(rep,open(os.path.dirname(out)+'/stitch_report.json','w'),indent=1);os.remove(tmpw);os.remove(fin);print('MASTER',out,'OK' if ok else 'CHECK FAILED');sys.exit(0 if ok else 1)
if __name__=='__main__':main()
