#!/usr/bin/env python3
"""Clean B-ROLL clip from ANY moment of the screen recording (not synced to the voice) — same cleaning as build_screen.py.

  python3 build_screen_clip.py <project> <section> <name> <screen_t0> <dur>
  -> sections/<section>/<name>.mp4 (1920x930, 30 fps, no audio) + <name>_meta.json + review/<name>_sheet.jpg (1 frame / 0.5 s)
  In scenes.py: CLIP=SS.Screen(__file__,'<name>');  SS.card(CLIP, T_clip, ...)  where T_clip = clip-local seconds.

Use when Albert says "show my screen there" but the synced screen at that moment is his script / something else (e.g. the
"You're in!" e-mail he recorded earlier). screen_t0 is SCREEN-recording time. READ the sheet: no script doc, no inbox list, no
private labels in the part you show (focus/crop past them)."""
import json,sys,os,math,subprocess,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build_screen as B
P,sec,name,t0,dur=os.path.abspath(sys.argv[1]),sys.argv[2],sys.argv[3],float(sys.argv[4]),float(sys.argv[5])
scr=json.load(open(f'{P}/edit/edl.json'))['sources']['screen'];d=f'{P}/sections/{sec}/';NF=int(round(dur*B.FPS))
def frames(scale):
    w,h=scale;p=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{t0:.4f}','-i',scr,'-map','0:v:0','-vf',f'fps={B.FPS},scale={w}:{h}','-frames:v',str(NF),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
    last=None
    for i in range(NF):
        b=p.stdout.read(w*h*3)
        if len(b)==w*h*3: last=np.frombuffer(b,np.uint8).reshape(h,w,3)
        yield last
    p.stdout.close();p.wait()
y0=np.array([B.chrome_bottom(None,a.astype(int)) for a in frames((960,540))],float)
ys=np.array([y0[max(0,i-4):i+5].max() for i in range(NF)]);ys=np.where(ys>0,np.minimum(ys+8,470),0)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{B.OW}x{B.OH}','-r',str(B.FPS),'-i','pipe:0','-c:v','libx264','-preset','fast','-crf','15','-pix_fmt','yuv420p','-r',str(B.FPS),'-video_track_timescale','30000',d+name+'.mp4'],stdin=subprocess.PIPE)
for i,a in enumerate(frames((1920,1080))): enc.stdin.write(np.ascontiguousarray(B.crop(a,ys[i])).tobytes())
enc.stdin.close();enc.wait()
leaks=B.leak_scan(d+name+'.mp4')
json.dump({'fps':B.FPS,'frames':NF,'size':[B.OW,B.OH],'screen_t0':t0,'y0':[int(v) for v in ys],'zoomed':[bool(v==0) for v in ys],'cuts':[],'leak_frames':leaks,'held_blank_frames':[]},open(d+name+'_meta.json','w'))
os.makedirs(d+'review',exist_ok=True);rows=math.ceil(dur*2/8)
subprocess.run(['ffmpeg','-v','error','-y','-i',d+name+'.mp4','-vf',f'fps=2,scale=320:-1,tile=8x{rows}','-frames:v','1','-q:v','4',d+f'review/{name}_sheet.jpg'])
print(f'{sec}/{name}.mp4: {NF} frames from screen {t0:.2f}s, chrome cropped in {int((ys>0).mean()*100)} %, leak scan {len(leaks)} {leaks[:10]}')
