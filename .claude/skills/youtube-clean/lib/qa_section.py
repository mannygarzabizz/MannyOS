#!/usr/bin/env python3
"""QA for one rendered section. Signal/pixel checks only - nothing here listens or reads like a human.

  python3 lib/qa_section.py sections/03-price [--video FILE] [--doc-step 0.5] [--quiet-db -45]

Checks (written to <section>/review/qa.json, exit code 1 if any hard check fails)
  1 ffprobe      1920x1080, 30 fps, h264/yuv420p, duration == voice duration +-1 frame
  2 audio        peak < -1 dBFS; quiet runs >= 0.3 s (10 ms RMS windows below --quiet-db) are listed
  3 boundaries   first/last 8 frames: stage area pure white + presenter card in the split position, OR 'cam' (presenter full
                 screen), OR 'screen' (capture card + slim presenter on the SCREEN grid) - clean joins either way
  4 contact      1 frame / 2 s -> review/sheet.jpg  (READ it)
  5 script doc   every --doc-step seconds: flags frames that look like a bright page of plain paragraph text
                 (Albert's Google Doc must never be shown). Flagged frames are saved to review/docflag-<t>.jpg; a flag is a
                 request to look, a pass is not proof - still read the sheet.
  doc detector self-test:  python3 lib/qa_section.py --selftest-doc img1.jpg [img2.jpg ...]
"""
import sys,json,subprocess,argparse,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
LIB=Path(__file__).resolve().parent;sys.path.insert(0,str(LIB))
import layout as L
W,H,FPS=L.W,L.H,L.FPS

def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def pcm(p,sr=48000):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(sr),'-f','f32le','pipe:1']),np.float32)
def peak_db(p):
 x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-f','f32le','pipe:1']),np.float32)
 return float(20*np.log10(max(1e-9,np.abs(x).max())))
def frame_at(p,t):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{max(0,t-.5/FPS):.4f}','-i',str(p),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
 return np.frombuffer(b,np.uint8).reshape(H,W,3)
def frames_range(p,start_frame,count):
 vf=f"select='between(n\\,{start_frame}\\,{start_frame+count-1})'"
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf',vf,'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
 return np.frombuffer(b,np.uint8).reshape(-1,H,W,3)

def quiet_runs(x,sr=48000,thr_db=-45,min_len=.3):
 n=sr//100;k=len(x)//n;rms=np.sqrt((x[:k*n].reshape(k,n).astype(float)**2).mean(1)+1e-12);q=20*np.log10(rms)<thr_db
 runs=[];i=0
 while i<k:
  if q[i]:
   j=i
   while j<k and q[j]:j+=1
   if (j-i)/100>=min_len:runs.append((round(i/100,2),round(j/100,2)))
   i=j
  else:i+=1
 return runs

# ---------------- script-doc detector ----------------
def _runs(mask_row):
 d=np.diff(np.concatenate(([0],mask_row.view(np.int8),[0])));return np.nonzero(d==1)[0],np.nonzero(d==-1)[0]
def text_lines(rgb):
 """Find text-line boxes: dark, low-saturation ink on a bright ground. -> list of (x0,y0,x1,y1)."""
 a=rgb.astype(np.int16);g=a.mean(2);sat=a.max(2)-a.min(2)
 ink=(g<125)&(sat<60)
 # smear ink horizontally (word gaps ~ up to 22 px) with a box filter
 k=23;c=np.cumsum(np.pad(ink,((0,0),(k//2+1,k//2)),mode='constant').astype(np.int32),1);sm=(c[:,k:]-c[:,:-k])>0
 boxes=[];open_=[]   # open_: [x0,x1,y0,ylast]
 for y in range(sm.shape[0]):
  s,e=_runs(sm[y]);cur=[(int(p),int(q)) for p,q in zip(s,e) if q-p>=110]
  nxt=[]
  for o in open_:
   hit=next((r for r in cur if min(r[1],o[1])-max(r[0],o[0])>.5*min(r[1]-r[0],o[1]-o[0])),None)
   if hit is not None:cur.remove(hit);nxt.append([min(o[0],hit[0]),max(o[1],hit[1]),o[2],y])
   elif y-o[3]<=1:nxt.append(o)
   else:boxes.append((o[0],o[2],o[1],o[3]+1))
  nxt+= [[r[0],r[1],y,y] for r in cur];open_=nxt
 boxes+=[(o[0],o[2],o[1],o[3]+1) for o in open_]
 out=[]
 for x0,y0,x1,y1 in boxes:
  h=y1-y0;w=x1-x0
  if not (4<=h<=46 and w>=160 and w/h>=6):continue
  x0+=k//2;x1-=k//2                                  # undo the smear
  pad=6;reg=g[max(0,y0-pad):y1+pad,max(0,x0-pad):x1+pad]
  if np.median(reg)<222:continue                      # ground behind the line must be a bright page
  out.append((x0,y0,x1,y1))
 return out
def doc_score(rgb,region=None):
 """Looks like a page of plain paragraph text? -> dict(flag, lines, full_lines, left, reason)
 Rule: >=5 text lines sharing one left edge (+-6 px), similar height, regular pitch, of which >=3 are 'full' wrapped lines
 (within 12 % of the longest) and the longest is >= 22x the line height (running prose, not labels or a feature list)."""
 if region:rgb=rgb[region[1]:region[3],region[0]:region[2]]
 ls=text_lines(rgb);best=dict(flag=False,lines=0,full_lines=0,left=None,total_lines=len(ls))
 if len(ls)<5:return best
 lefts=np.array([b[0] for b in ls])
 for x in sorted(set(lefts.tolist())):
  grp=[b for b in ls if abs(b[0]-x)<=6]
  if len(grp)<5:continue
  hs=np.array([b[3]-b[1] for b in grp]);hm=np.median(hs);grp=[b for b in grp if .6*hm<=b[3]-b[1]<=1.6*hm]
  if len(grp)<5:continue
  ws=np.array([b[2]-b[0] for b in grp]);wmax=ws.max();full=int((ws>=.88*wmax).sum())
  ys=np.sort(np.array([(b[1]+b[3])/2 for b in grp]));dy=np.diff(ys);ok_=dy[dy>=1.2*hm];pitch=float(np.percentile(ok_,20)) if len(ok_) else 0   # base line pitch; paragraph gaps are multiples of it
  regular=float((np.abs(dy/pitch-np.round(dy/pitch))<.22).mean()) if pitch>0 else 0
  flag=bool(full>=3 and wmax>=22*hm and regular>=.7 and pitch<=4*hm)
  cand=dict(flag=flag,lines=len(grp),full_lines=full,left=int(x),line_h=float(hm),max_w=int(wmax),pitch=float(pitch),regular=regular,total_lines=len(ls))
  if (cand['flag'],cand['lines'])>(best['flag'],best['lines']):best=cand
 return best
def scan_docs(video,dur,step,outdir):
 flags=[];t=step/2
 p=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-vf',f'fps=1/{step}:start_time=0:round=down','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE);i=0
 while True:
  b=p.stdout.read(W*H*3)
  if len(b)<W*H*3:break
  fr=np.frombuffer(b,np.uint8).reshape(H,W,3);r=doc_score(fr)
  if r['flag']:
   tt=round(i*step,2);r['t']=tt;flags.append(r);Image.fromarray(fr).save(outdir/f'docflag-{tt:07.2f}.jpg',quality=88)
  i+=1
 p.wait();return flags,i

def contact_sheet(video,dur,out,step=2.,cols=5,tw=384,th=216):
 ts=list(np.arange(step/2,dur,step));sheet=Image.new('RGB',(cols*tw,math.ceil(len(ts)/cols)*th),'#CCCCCC')
 from draw import sf
 for i,t in enumerate(ts):
  im=Image.fromarray(frame_at(video,t)).resize((tw,th),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im);s=f'{t:.1f}s';d.rounded_rectangle((6,6,22+sf(16).getlength(s),30),6,fill='black');d.text((14,9),s,font=sf(16),fill='white')
  sheet.paste(im,((i%cols)*tw,(i//cols)*th))
 sheet.save(out,quality=90);return len(ts)

def boundaries(video,nframes):
 res={'ok':True,'bad':[]};x0=L.CARD[0]-40
 for name,start in (('first',0),('last',max(0,nframes-L.CLEAN_FRAMES))):
  fr=frames_range(video,start,L.CLEAN_FRAMES)
  if len(fr)<L.CLEAN_FRAMES:res['ok']=False;res['bad'].append(f'{name}: decoded {len(fr)} frames');continue
  for k,f in enumerate(fr):
   stage=f[:, :x0];card=f[L.CARD[1]+60:L.CARD[1]+L.CARD[3]-60,L.CARD[0]+40:L.CARD[0]+L.CARD[2]-40]
   if float(f[:, :x0].std())>25 and float(f[40:200,40:400].std())>4.5:continue   # boundary in 'cam' (full-screen presenter): allowed
   sx,sy,sw,sh=L.SCREEN[:4];cx,cy,cw,ch=L.SCREEN_CARD[:4]
   if f[:90,:].min()>=200 and f[sy+60:sy+sh-60,sx+60:sx+sw-60].std()>4 and f[cy+60:cy+ch-60,cx+30:cx+cw-30].std()>12:continue   # boundary in 'screen' (capture card + slim presenter): allowed
   white=int(stage.min());corner=f[L.CARD[1]+2:L.CARD[1]+8,L.CARD[0]+2:L.CARD[0]+8].mean()
   if white<246:res['ok']=False;res['bad'].append(f'{name}[{k}] stage not white (min {white})')
   if card.std()<12:res['ok']=False;res['bad'].append(f'{name}[{k}] presenter card missing')
 return res

def main():
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('folder',nargs='?');ap.add_argument('--video');ap.add_argument('--doc-step',type=float,default=.5);ap.add_argument('--quiet-db',type=float,default=-45.)
 ap.add_argument('--selftest-doc',nargs='+')
 a=ap.parse_args()
 if a.selftest_doc:
  for f in a.selftest_doc:
   im=np.asarray(Image.open(f).convert('RGB'));print(Path(f).name,doc_score(im))
  return 0
 sec=Path(a.folder).resolve();video=Path(a.video) if a.video else sec/f'{sec.name}.mp4';voice=sec/'voice.mkv';rev=sec/'review';rev.mkdir(exist_ok=True)
 for old in rev.glob('docflag-*.jpg'):old.unlink()
 R={'video':str(video),'checks':{}};fails=[]
 j=probe(video);v=next(s for s in j['streams'] if s['codec_type']=='video');au=next((s for s in j['streams'] if s['codec_type']=='audio'),None)
 vdur=float(v.get('duration') or j['format']['duration']);nfr=int(v.get('nb_frames') or round(vdur*FPS));voice_d=len(pcm(voice))/48000
 c=dict(width=v['width'],height=v['height'],fps=v['r_frame_rate'],codec=v['codec_name'],pix_fmt=v['pix_fmt'],frames=nfr,video_duration=vdur,format_duration=float(j['format']['duration']),
        audio=(au or {}).get('codec_name'),audio_duration=float((au or {}).get('duration',0) or 0),voice_duration=voice_d)
 c['ok']=bool(v['width']==W and v['height']==H and v['r_frame_rate'] in ('30/1','30000/1000') and v['pix_fmt']=='yuv420p' and abs(vdur-voice_d)<=1/FPS+1e-3 and au is not None and abs(c['audio_duration']-voice_d)<=1/FPS+.03)
 R['checks']['ffprobe']=c
 if not c['ok']:fails.append('ffprobe')
 x=pcm(video);pk=peak_db(video);runs=quiet_runs(x,thr_db=a.quiet_db)
 R['checks']['audio']=dict(peak_dbfs=round(pk,2),peak_ok=bool(pk<-1),quiet_threshold_db=a.quiet_db,quiet_runs_ge_0_3s=runs,quiet_ok=not runs,voice_peak_dbfs=round(peak_db(voice),2))
 if pk>=-1:fails.append('peak')
 if runs:fails.append('quiet-runs')
 b=boundaries(video,nfr);R['checks']['boundaries']=b
 if not b['ok']:fails.append('boundaries')
 n=contact_sheet(video,vdur,rev/'sheet.jpg');R['checks']['contact_sheet']=dict(path=str(rev/'sheet.jpg'),frames=n)
 flags,scanned=scan_docs(video,vdur,a.doc_step,rev);R['checks']['script_doc']=dict(frames_scanned=scanned,step=a.doc_step,flagged=flags,ok=not flags)
 if flags:fails.append('script-doc')
 R['failed']=fails;R['scope']='ffprobe, PCM peak/RMS, pixel checks on decoded frames. No perceptual listening, no OCR. Read review/sheet.jpg.'
 json.dump(R,open(rev/'qa.json','w'),indent=1);print(json.dumps(R,indent=1));print('QA',('FAILED: '+', '.join(fails)) if fails else 'passed')
 return 1 if fails else 0
if __name__=='__main__':sys.exit(main())
