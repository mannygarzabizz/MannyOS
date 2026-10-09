#!/usr/bin/env python3
"""Section renderer for YouTube Clean (1920x1080, 30 fps, white ground, presenter card right).

  python3 lib/render_section.py sections/03-price               # full render -> sections/03-price/03-price.mp4
  python3 lib/render_section.py sections/03-price --preview     # contact sheet, 1 frame / 2 s -> review/preview.jpg
  python3 lib/render_section.py sections/03-price --strip 4.1,4.3,4.6   # motion strip (section-local seconds)
  options: --out FILE  --crf 16  --preset medium  --face-cx 1040

Section folder must hold
  voice.mkv        final voice cut (camera video + audio). Never retimed: video is resampled to 30 fps, audio is muxed as is.
  transcript.json  {"words":[{"text","start","end"}]}   section-local seconds
  beats.json       [{"name","start","end"}, ...]
  scenes.py        graphics(beat,t,S,at) -> RGBA 1920x1080 layer (transparent ground; draw.canvas()) or None
                   MODES=[(0,'split'),(4.2,'full'),(8.0,'split')]      section-local START time of each 0.35 s card move
                   optional: FACE_CX=1040 or [(t,cx),...]   FACE_CY=470   CAPTIONS=[{...}] (see captions.py)
                             CINE_BEATS={'hook'} CINE_Y=560 edit_groups(G) (intro cinematic captions)
                             overlay(beat,t,S,at,st) -> RGBA layer drawn above the presenter card (captions over the 'cam' full-screen mode)
                             cam_zoom(t) -> (zoom>=1, cx, cy) or None: push-in on the camera picture, centred on source pixel (cx,cy)
                                            (cy is the face/subject centre; crop_box adds 6 % headroom). Ease it; <= 1.8x (25 fps source).
  scenes.py does `from draw import *` / `import layout, captions, emoji` (lib/ is on sys.path). The runner sets scenes.RT =
  {'track': ModeTrack, 'duration': D, 'frames': N} so a scene can ask RT['track'].stage_progress(t).

Draw order: white ground -> graphics -> captions -> presenter card (always on top, so nothing can cover Albert).
Section boundaries are enforced: first/last 8 frames are white + card in split, graphics/captions fade in/out around them -
EXCEPT when the section starts/ends in 'screen' or 'cam' mode: then the screen card / full-screen presenter stays on (clean join).
"""
import sys,json,subprocess,argparse,importlib.util,re,time,threading,queue,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
LIB=Path(__file__).resolve().parent
sys.path.insert(0,str(LIB/'helpers'));sys.path.insert(0,str(LIB))
import layout as L
import captions as C
from draw import sf

W,H,FPS=L.W,L.H,L.FPS
def bare(s):return re.sub(r'[^a-z0-9.$%]','',s.lower())
def probe(path):
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
 v=next(s for s in j['streams'] if s['codec_type']=='video');a=next((s for s in j['streams'] if s['codec_type']=='audio'),None)
 return j,v,a
def audio_duration(path):
 """Exact voice length in seconds from decoded samples (mkv streams carry no reliable duration field)."""
 n=0;p=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','s16le','pipe:1'],stdout=subprocess.PIPE)
 while True:
  b=p.stdout.read(1<<20)
  if not b:break
  n+=len(b)
 p.wait();return n/2/48000

class Section:
 def __init__(self,folder,face_cx=None):
  self.dir=Path(folder).resolve();self.voice=self.dir/'voice.mkv'
  for f in ['voice.mkv','transcript.json','beats.json','scenes.py']:
   if not (self.dir/f).exists():raise SystemExit(f'missing {self.dir/f}')
  B=json.load(open(self.dir/'beats.json'));self.beats=B['beats'] if isinstance(B,dict) else B
  T=json.load(open(self.dir/'transcript.json'));self.words=T['words'] if isinstance(T,dict) else T
  self.S={b['name']:b for b in self.beats}
  _,v,_=probe(self.voice);self.sw,self.sh=int(v['width']),int(v['height'])
  self.D=audio_duration(self.voice);self.N=round(self.D*FPS)
  # SYNC GUARD: the voice file's picture and sound must be the same length (<= 1.5 frames apart). A longer video stream means
  # the cuts were joined with padded segments and the presenter will drift out of lip-sync. Rebuild voice.mkv
  # (edit/rebuild_video.py: one encoder, constant 30 fps clock) instead of rendering.
  vf=int(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',str(self.voice)]).decode().strip().strip(','))
  if abs(vf/FPS-self.D)>1.5/FPS:raise SystemExit(f'SYNC GUARD: {self.voice} has {vf} video frames = {vf/FPS:.3f}s but {self.D:.3f}s of audio. Picture and sound are not 1:1 - rebuild the voice file, do not render.')
  sys.path.insert(0,str(self.dir))
  spec=importlib.util.spec_from_file_location('scenes',self.dir/'scenes.py');self.scenes=importlib.util.module_from_spec(spec);sys.modules['scenes']=self.scenes;spec.loader.exec_module(self.scenes)
  sc=self.scenes
  self.track=L.ModeTrack(getattr(sc,'MODES',[(0,'split')]),self.D)
  for w in self.track.warnings:print('[modes]',w)
  self.face_cx=face_cx if face_cx is not None else getattr(sc,'FACE_CX',1040);self.face_cy=getattr(sc,'FACE_CY',470)
  sc.RT={'track':self.track,'duration':self.D,'frames':self.N}
  self.caps=[C.resolve(s,self.at,self.S) for s in getattr(sc,'CAPTIONS',[])]
  self.groups=C.cinematic_groups(self.beats,self.words,set(getattr(sc,'CINE_BEATS',())))
  if hasattr(sc,'edit_groups'):self.groups=sc.edit_groups(self.groups) or self.groups
  self.cine_y=getattr(sc,'CINE_Y',560)
  if self.groups:json.dump(self.groups,open(self.dir/'caption-groups.json','w'),indent=1)
  self.t_in=L.CLEAN_FRAMES/FPS;self.t_out=(self.N-L.CLEAN_FRAMES)/FPS
  self.overlaps=[]
 def at(self,name,word,default=0,nth=0):
  """Beat-local onset (s) of a spoken word inside beat `name`; `default` if it is not in the transcript."""
  b=self.S[name];ww=[w for w in self.words if b['start']-.01<=w['start']<b['end']-.01 and bare(w['text'])==bare(word)]
  return ww[nth]['start']-b['start'] if len(ww)>nth else default
 def beat(self,t):return next((b for b in self.beats if b['start']<=t<b['end']),self.beats[-1])
 def layers(self,n):
  """(graphics, captions) RGBA layers for output frame n, or (None,None) on the clean boundary frames."""
  t=n/FPS
  edge=n<L.CLEAN_FRAMES or n>=self.N-L.CLEAN_FRAMES
  keep=self.track.mode(t) in ('screen','cam') and not self.track.moving(t)   # a section may start/end ON the screen share or on him full screen: no white blink at the join
  if edge and not keep:return None,None
  b=self.beat(t);g=self.scenes.graphics(b,t-b['start'],self.S,self.at)
  if g is not None and (g.size!=(W,H) or g.mode!='RGBA'):
   c=Image.new('RGBA',(W,H),(255,255,255,0));c.alpha_composite(g.convert('RGBA'));g=c
  cap=None
  live=[s for s in self.caps if s['_start']<=t<s['_end']];gg=[x for x in self.groups if x['start']<=t<x['end']]
  if live or gg:
   cap=Image.new('RGBA',(W,H),(255,255,255,0))
   for s in live:C.draw_spec(cap,s,t)
   for x in gg[:1]:C.cinematic(cap,x,n,y=x.get('y',self.cine_y))
  env=1. if keep else L.smooth((t-self.t_in)/.2)*L.smooth((self.t_out-t)/.2)
  if env<1:
   for lay in (g,cap):
    if lay is not None:lay.putalpha(lay.getchannel('A').point(lambda a:int(a*env)))
  return g,cap
 def frame(self,n,cam,check=False):
  t=n/FPS;im=Image.new('RGBA',(W,H),L.GROUND+(255,));g,cap=self.layers(n);st=self.track.state(t)
  if check and not self.track.moving(t) and self.track.mode(t) in ('split','face'):
   px=sum(L.overlap_with_card(l,st) for l in (g,cap) if l is not None)
   if px>40:self.overlaps.append((round(t,3),px))
  if g is not None:im.alpha_composite(g)
  if cap is not None:im.alpha_composite(cap)
  fcx,fcy=L.face_at(self.face_cx,t),self.face_cy
  cz=getattr(self.scenes,'cam_zoom',None)              # optional scenes.cam_zoom(t)->(zoom,cx,cy)|None: push-in on the camera picture (e.g. a cold-open sip)
  if cz is not None:
   r=cz(t)
   if r:st=st._replace(zoom=st.zoom*max(1.,r[0]));fcx,fcy=r[1],r[2]
  L.composite_card(im,cam,st,fcx,fcy)
  ov=getattr(self.scenes,'overlay',None)            # ADDITIVE (intro rev 4): optional scenes.overlay(beat,t,S,at,st) drawn ABOVE the presenter ('cam' mode captions)
  if ov is not None and L.CLEAN_FRAMES<=n<self.N-L.CLEAN_FRAMES:
   b=self.beat(t);o=ov(b,t-b['start'],self.S,self.at,st)
   if o is not None:im.alpha_composite(o)
  return im.convert('RGB')
 def cam_at(self,t):
  t=min(max(0,t),self.D-.05)
  buf=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{max(0,t-.5/FPS):.4f}','-i',str(self.voice),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
  return np.frombuffer(buf,np.uint8).reshape(self.sh,self.sw,3)

def label(im,s):
 d=ImageDraw.Draw(im);f=sf(20,'Semibold');w=f.getlength(s);d.rounded_rectangle((8,8,24+w,40),8,fill=(0,0,0));d.text((16,12),s,font=f,fill='white')
def report_overlaps(sec):
 if sec.overlaps:
  print(f'[WARN] graphics/captions under the presenter card on {len(sec.overlaps)} checked frames; first at t={sec.overlaps[0][0]}s ({sec.overlaps[0][1]} px). Keep split-mode graphics inside x<={L.STAGE[2]}.')
 else:print('[ok] no graphics or captions under the presenter card (split/face frames)')
def preview(sec):
 out=sec.dir/'review';out.mkdir(exist_ok=True)
 ns=[0]+[round(t*FPS) for t in np.arange(1,sec.D,2)]+[sec.N-1];cols=4;tw_,th=480,270
 sheet=Image.new('RGB',(cols*tw_,math.ceil(len(ns)/cols)*th),'#CCCCCC')
 for i,n in enumerate(ns):
  im=sec.frame(n,sec.cam_at(n/FPS),check=True).resize((tw_,th),Image.Resampling.LANCZOS);label(im,f'{n/FPS:.2f}s {sec.track.mode(n/FPS)}');sheet.paste(im,((i%cols)*tw_,(i//cols)*th))
 sheet.save(out/'preview.jpg',quality=90);print(out/'preview.jpg');report_overlaps(sec)
def strip(sec,times):
 out=sec.dir/'review';(out/'frames').mkdir(parents=True,exist_ok=True);tw_,th=640,360
 sheet=Image.new('RGB',(len(times)*tw_,th),'#CCCCCC')
 for i,t in enumerate(times):
  n=round(t*FPS);im=sec.frame(n,sec.cam_at(n/FPS),check=True);im.save(out/'frames'/f'f_{t:07.3f}.jpg',quality=93)
  sm=im.resize((tw_,th),Image.Resampling.LANCZOS);label(sm,f'{t:.2f}s');sheet.paste(sm,(i*tw_,0))
 name=out/('strip-'+'_'.join(f'{t:g}' for t in times)[:60]+'.jpg');sheet.save(name,quality=90);print(name);print(out/'frames');report_overlaps(sec)

def render(sec,out,crf=16,preset='medium'):
 size=sec.sw*sec.sh*3
 dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(sec.voice),'-an','-vf',f'fps={FPS}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE,bufsize=size)
 enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0',
  '-i',str(sec.voice),'-map','0:v','-map','1:a:0','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset',preset,'-crf',str(crf),'-pix_fmt','yuv420p',
  '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-r',str(FPS),
  '-c:a','aac','-b:a','256k','-ar','48000','-t',f'{sec.N/FPS:.6f}','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 q=queue.Queue(maxsize=6)
 def reader():
  last=None
  for n in range(sec.N):
   b=dec.stdout.read(size)
   if len(b)==size:last=np.frombuffer(b,np.uint8).reshape(sec.sh,sec.sw,3)
   elif last is None:q.put(None);return
   q.put(last)                       # camera ran out a frame early -> hold the last frame
  q.put(None)
 threading.Thread(target=reader,daemon=True).start()
 t0=time.time()
 for n in range(sec.N):
  cam=q.get()
  if cam is None:raise RuntimeError(f'no camera frame for output frame {n}')
  enc.stdin.write(sec.frame(n,cam,check=True).tobytes())
  if n%150==0 and n:print(f'{n}/{sec.N}  {n/(time.time()-t0):.1f} fps',flush=True)
 enc.stdin.close();rc=enc.wait();dec.kill()
 if rc:raise RuntimeError('encoder failed')
 dt=time.time()-t0;print(f'{out}\n{sec.N} frames in {dt:.1f}s = {sec.N/dt:.1f} fps (voice {sec.D:.3f}s)');report_overlaps(sec)
 json.dump({'frames':sec.N,'seconds':round(dt,2),'fps':round(sec.N/dt,2),'voice_duration':sec.D,'modes':sec.track.modes,'overlap_frames':len(sec.overlaps)},open(sec.dir/'render.json','w'),indent=1)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('folder');ap.add_argument('--preview',action='store_true');ap.add_argument('--strip');ap.add_argument('--out')
 ap.add_argument('--crf',type=int,default=16);ap.add_argument('--preset',default='medium');ap.add_argument('--face-cx',type=float)
 a=ap.parse_args();sec=Section(a.folder,a.face_cx)
 if a.preview:preview(sec)
 elif a.strip:strip(sec,[float(x) for x in a.strip.split(',')])
 else:render(sec,Path(a.out) if a.out else sec.dir/f'{sec.dir.name}.mp4',a.crf,a.preset)
