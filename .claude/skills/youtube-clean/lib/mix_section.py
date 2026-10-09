#!/usr/bin/env python3
"""Standard per-section audio mix — agents use THIS, they do not write their own.   python3 lib/mix_section.py sections/<NN-name>

Reads  sections/<s>/sfx.json   {"sfx":[{"file":"whoosh-snap.mp3","t":14.55,"peak_db":-31}, …]}   (files from lib/audio/sources)
       sections/<s>/voice.mkv  (untouched voice; samples are only summed, never processed)
       sections/<s>/<s>-nosfx.mp4  = the runner's render. Every run: if <s>.mp4 is NOT tagged comment=ytclean-mixed it is a fresh
                                     render and replaces <s>-nosfx.mp4 (2026-09-19 bug: a re-render used to be muxed onto the OLD picture)
Writes sections/<s>/stem_nomusic.wav  (voice + SFX, NO music — the stitch lays music in ONE pass across sections)
       sections/<s>/<s>.mp4           (video stream-copied, no -shortest). If <project>/stitch.json has a music block covering
                                       this section, the PREVIEW mp4 also carries the music at the exact track offset it will
                                       have in the master (fixed chain: gain → sidechain 0.03/2/15/250), so Albert hears it.
Rules baked in: NO pop/bubbly samples (rejected 2026-09-18) — a cue using pop.mp3 aborts; whooshes ≈ −31 dBFS peak, one per
mode change, none in the first/last second; UI click only where a cursor presses; peak must stay < −1 dBFS."""
import sys,json,os,subprocess,numpy as np,wave
from pathlib import Path
SR=48000;FPS=30
def load(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar',str(SR),'-f','f32le','pipe:1']),np.float32).reshape(-1,2).copy()
def main():
    H=Path(sys.argv[1]).resolve();s=H.name;P=H.parents[1];A=P/'lib/audio/sources';voice=load(H/'voice.mkv');mix=np.zeros_like(voice);D=len(voice)/SR
    cues=json.load(open(H/'sfx.json')).get('sfx',[]) if (H/'sfx.json').exists() else []
    for c in cues:
        if 'pop' in c['file'].lower():sys.exit(f"pop sample in cue list ({c}) — Albert rejected pop/bubbly sounds")
        if c['t']<1.0 or c['t']>D-1.0:print(f"[warn] cue at {c['t']} s is inside the first/last second of the section")
        x=load(A/c['file']);x=x/max(1e-9,np.abs(x).max())*10**(c['peak_db']/20);i=int(c['t']*SR);k=min(len(x),len(mix)-i)
        if k>0:mix[i:i+k]+=x[:k]
    stem=voice+mix;w=wave.open(str(H/'stem_nomusic.wav'),'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(stem,-1,1)*32767).astype(np.int16).tobytes());w.close()
    out=stem.copy();note='no music'
    sj=P/'stitch.json'
    if sj.exists():
        C=json.load(open(sj));M=C.get('music');secs=C['sections']
        if M and s in secs and secs.index(M['from'])<=secs.index(s)<=secs.index(M['to']):
            def dur(x):
                v=P/'sections'/x/'voice.mkv';n=len(load(v));return round(n/SR*FPS)/FPS
            # "start_at": seconds into the 'from' section where the music begins (e.g. after a silent cold open)
            t0=M.get('track_start',0)+sum(dur(x) for x in secs[secs.index(M['from']):secs.index(s)])-M.get('start_at',0)
            off=max(0.,-t0);t0=max(0.,t0);io=int(round(off*SR))
            fg=(f"[0:a]aresample={SR},atrim=start={t0:.6f}:end={t0+D-off+2:.6f},asetpts=PTS-STARTPTS,volume={M.get('gain_db',-20)}dB[m];[1:a]aresample={SR},atrim=start={off:.6f},asetpts=PTS-STARTPTS,apad=pad_dur=2[k];"
                f"[m][k]sidechaincompress=threshold=0.03:ratio=2:attack=15:release=250[o]")
            bed=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/M['file']),'-i',str(H/'voice.mkv'),'-filter_complex',fg,'-map','[o]','-ac','2','-ar',str(SR),'-f','f32le','pipe:1']),np.float32).reshape(-1,2).copy()[:len(out)-io]
            assert len(bed)>=len(out)-io-SR//100,('music bed came back short',len(bed),len(out)-io)
            if s==M['from']:a=int(M.get('fade_in',.5)*SR);bed[:a]*=np.linspace(0,1,a,dtype=np.float32)[:,None]
            if s==M['to']:b=int(M.get('fade_out',3)*SR);bed[-b:]*=np.linspace(1,0,b,dtype=np.float32)[:,None]
            out[io:io+len(bed)]+=bed;note=f'music preview from track {t0:.3f} s at section {off:.2f} s'
    pk=20*np.log10(np.abs(out).max()+1e-9)
    if pk>=-1.0:sys.exit(f'peak {pk:.2f} dBFS — too hot')
    src=H/f'{s}-nosfx.mp4';cur=H/f'{s}.mp4'
    tag=subprocess.run(['ffprobe','-v','error','-show_entries','format_tags=comment','-of','csv=p=0',str(cur)],capture_output=True,text=True).stdout.strip() if cur.exists() else ''
    if cur.exists() and tag!='ytclean-mixed':os.replace(cur,src)   # <s>.mp4 is a fresh render (never mixed) -> it IS the picture now
    elif not src.exists():sys.exit(f'no picture: neither a fresh {cur.name} nor {src.name}')
    raw=H/'_mix.f32';out.astype(np.float32).tofile(raw)
    subprocess.check_call(['ffmpeg','-v','error','-y','-i',str(src),'-f','f32le','-ar',str(SR),'-ac','2','-i',str(raw),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-metadata','comment=ytclean-mixed','-movflags','+faststart',str(H/f'{s}.mp4')]);os.remove(raw)
    print(f'{s}: {len(cues)} cues, peak {pk:.2f} dBFS, {note}; wrote stem_nomusic.wav and {s}.mp4')
if __name__=='__main__':main()
