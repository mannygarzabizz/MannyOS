#!/usr/bin/env python3
"""FACE_CX / FACE_CY keyframes from macOS Vision face detection (lib/faces.swift) - use for the slim 'screen' presenter card and
any card where his head must be centred.   python3 lib/faces.py sections/<NN-name> [step_s=0.5]
Samples voice.mkv every step, detects the face box, smooths (median 3 + [.25,.5,.25]), prints FACE_CX=[(t,cx),...] and FACE_CY=
(median face-box centre y). Paste both into scenes.py. Frames with no face keep the neighbour value. Look at 3 rendered frames after."""
import sys,subprocess,json,os,tempfile,numpy as np
from pathlib import Path
D=Path(sys.argv[1]).resolve();step=float(sys.argv[2]) if len(sys.argv)>2 else .5;v=D/'voice.mkv';sw=Path(__file__).resolve().parent/'faces.swift'
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(v)]))
tmp=tempfile.mkdtemp();ts=list(np.arange(step/2,dur,step))
subprocess.run(['ffmpeg','-v','error','-i',str(v),'-vf',f'fps=1/{step},scale=960:-1','-q:v','3',f'{tmp}/f_%05d.jpg'],check=True)
files=sorted(os.listdir(tmp));out=subprocess.check_output(['swift',str(sw)]+[f'{tmp}/{f}' for f in files],text=True)
cx,cy={},{}
for line in out.splitlines():
    p=line.split(' ');name=p[0];boxes=[list(map(float,b.split(','))) for b in p[1:] if ',' in b]
    if not boxes:continue
    x,y,w,h=max(boxes,key=lambda b:b[2]*b[3]);i=int(name[2:7])-1;cx[i]=(x+w/2)*2;cy[i]=(y+h/2)*2
for f in files:os.remove(f'{tmp}/{f}')
os.rmdir(tmp)
n=len(files);xs=np.array([cx.get(i,np.nan) for i in range(n)]);good=~np.isnan(xs)
xs=np.interp(np.arange(n),np.nonzero(good)[0],xs[good]) if good.any() else np.full(n,1040.)
xs=np.array([np.median(xs[max(0,i-1):i+2]) for i in range(n)]);xs=np.convolve(np.pad(xs,1,mode='edge'),[.25,.5,.25],'valid')
print(f'# {int(good.sum())}/{n} frames with a face')
print('FACE_CX='+json.dumps([(round(float(t),2),int(round(x))) for t,x in zip(ts[:n],xs)]).replace('[[','[(').replace(']]',')]').replace('], [','), ('))
print(f'FACE_CY={int(np.median(list(cy.values()))) if cy else 470}')
