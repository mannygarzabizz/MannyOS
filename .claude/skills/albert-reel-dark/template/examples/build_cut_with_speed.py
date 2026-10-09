"""Take selection for the Freebuff reel. One aligned master (camera video + screen-recording mic, mic timeline)."""
from pathlib import Path
import subprocess,json,math
P=Path(__file__).resolve().parent
SRC={'a':str(P/'edit/master.mov')}
# (source, start, end, beat)  seconds on the aligned master; trough-to-trough from a 10 ms RMS scan
select=[('a',23.79,26.20,'hook'),('a',28.19,29.57,'hook'),('a',31.09,32.82,'hook'),('a',40.88,42.21,'hook'),
 ('a',48.72,50.64,'how'),('a',63.92,67.48,'pay'),('a',75.52,76.84,'called'),('a',83.00,86.36,'agent'),
 ('a',88.20,91.52,'price'),('a',113.68,116.80,'free'),('a',118.58,121.38,'ads'),('a',129.70,134.14,'hours'),
 ('a',134.42,137.34,'glm'),('a',144.12,146.94,'smart'),('a',159.30,162.28,'crazy'),('a',168.68,171.08,'cta')]
SPEED={'hook':1.12}   # v4: the hook voice is sped up slightly (pitch-preserving atempo), picture retimed with it
ranges=[{'src':s,'start':a if n=='hook' else math.floor(a*30)/30,'end':b if n=='hook' else math.ceil(b*30)/30,'_':n,'speed':SPEED.get(n,1)} for s,a,b,n in select]
old=json.load(open(P/'edit/edl.json'))['ranges'] if (P/'edit/edl.json').exists() else []
json.dump({'sources':SRC,'ranges':ranges},open(P/'edit/edl.json','w'),indent=2)
(P/'edit/segments').mkdir(exist_ok=True)
time=0;beats=[]
for i,r in enumerate(ranges):
 src_dur=round(r['end']-r['start'],8);sp=r['speed'];dur=round(round(src_dur/sp*30)/30,8);(beats[-1].update(end=round(time+dur,8)) if beats and beats[-1]['name']==r['_'] else beats.append({'name':r['_'],'start':round(time,8),'end':round(time+dur,8)}));time+=dur
 if i>=len(old) or old[i]!=r or not (P/f'edit/segments/{i:02d}.mkv').exists():
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(r['start']),'-i',SRC[r['src']],'-t',str(src_dur),'-vf',f'setpts=(PTS-STARTPTS)/{sp},fps=30','-af',f'atempo={sp},atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={dur-.004}:d=0.004','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','pcm_s16le','-ar','48000','-t',str(dur),str(P/f'edit/segments/{i:02d}.mkv')],check=True)
 print(i,r['_'],round(time,3),flush=True)
json.dump(beats,open(P/'edit/beats.json','w'),indent=2)
(P/'edit/concat.txt').write_text('\n'.join(f"file 'segments/{i:02d}.mkv'" for i in range(len(ranges))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'edit/concat.txt'),'-c','copy',str(P/'edit/tight.mkv')],check=True)
print('DURATION',time)
