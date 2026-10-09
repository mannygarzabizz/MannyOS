from draw import *
import json,subprocess,re,math,sys
sys.path.insert(0,str(P/'helpers'));import editorial_caption as editorial
import scenes
# Instagram trims/overlays the top of a reel, so ALL graphics are drawn in the usual 1080x1920 scene canvas and then moved
# down by TOP_SHIFT. The split line (and presenter chip) moves with it: 768 -> SPLIT_Y. Scenes keep their old coordinates.
# ---- EDIT PER REEL: CROP_Y, FULL, CAPY, special/serif words and OVERRIDE (values below are the accepted Laya reel) ----
TOP_SHIFT=90;SPLIT_Y=768+TOP_SHIFT;PH=1920-SPLIT_Y;CROP_Y=372   # CROP_Y: top of the presenter crop in the source frame
B=json.load(open(P/'edit/beats.json'));D=B[-1]['end'];N=round(D*30);S={b['name']:b for b in B}
FULL={'hook','local','speed','problem','claude'}
CAPY={'hook':1090,'local':1000,'speed':1070,'problem':1070,'claude':1010}
TOK=json.load(open(P/'edit/transcript.json'))['words']
editorial.special.update({'JEV':'Jev','LAYA':'Laya','CLAUDE':'Claude','SYSTEM':'System','ONE':'One','FAST':'FAST','250':'250','30':'30'})
editorial.serif.update({'Laya','free','250','30','Claude'})
# Manual caption grouping for every full-screen beat (cap = sentence-start capital, big/color = payoff).
OVERRIDE={
 'hook':    [(2,{'cap':1}),(2,{}),(1,{'big':170,'color':'#1E8E3E'}),(3,{}),(2,{}),(1,{'big':170})],
 'local':   [(3,{'cap':1}),(1,{'big':150}),(2,{}),(1,{}),(3,{}),(2,{}),(2,{}),(1,{})],
 'speed':   [(2,{'cap':1}),(2,{}),(1,{}),(1,{'big':190}),(1,{}),(2,{}),(2,{}),(2,{}),(1,{'big':190,'color':'#1E8E3E'}),(1,{})],
 'problem': [(2,{'cap':1}),(2,{}),(2,{}),(2,{}),(2,{}),(2,{})],
 'claude':  [(3,{'cap':1}),(1,{}),(2,{}),(2,{})],
}
def bare(s):return re.sub(r'[^a-z0-9.]','',s.lower())
def at(name,word,default=0,nth=0):
 b=S[name];ww=[w for w in TOK if b['start']-.01<=w['start']<b['end']-.01 and bare(w['text'])==bare(word)]
 return ww[nth]['start']-b['start'] if len(ww)>nth else default
GROUPS=[]
for b in B:
 b['mode']='full' if b['name'] in FULL else 'split'
 ww=[w for w in TOK if b['start']<=w['start']<b['end']]
 groups=[];cur=[]
 if b['name'] in OVERRIDE:
  i=0;groups=[]
  for n,opt in OVERRIDE[b['name']]:
   if i<len(ww):groups.append((ww[i:i+n],opt));i+=n
  if i<len(ww):groups.append((ww[i:],{}))
  for k,(ws,opt) in enumerate(groups):
   GROUPS.append({'scene':b['name'],'mode':b['mode'],'text':' '.join(w['text'].strip('.,!?"') for w in ws).upper(),
    'start':math.floor(ws[0]['start']*30)/30,
    'end':math.floor(groups[k+1][0][0]['start']*30)/30 if k+1<len(groups) else b['end'],
    'words':[{'text':w['text'],'entry_frame':math.floor(w['start']*30)} for w in ws],**opt})
  continue
 for w in ww:
  cap=2 if b['mode']=='full' else 4
  if cur and (len(cur)>=cap or len(' '.join(x['text'] for x in cur+[w]))>(18 if b['mode']=='full' else 23)):groups.append(cur);cur=[]
  cur.append(w)
  if re.search(r'[.,!?]$',w['text']) and len(cur)>=2:groups.append(cur);cur=[]
 if cur:groups.append(cur)
 for k,ws in enumerate(groups):
  GROUPS.append({'scene':b['name'],'mode':b['mode'],'text':' '.join(w['text'].strip('.,!?"') for w in ws).upper(),'start':math.floor(ws[0]['start']*30)/30,'end':math.floor(groups[k+1][0]['start']*30)/30 if k+1<len(groups) else b['end'],'words':[{'text':w['text'],'entry_frame':math.floor(w['start']*30)} for w in ws]})
json.dump(GROUPS,open(P/'caption-groups.json','w'),indent=2);json.dump({'duration':D,'scenes':B},open(P/'scenes.json','w'),indent=2)
def graphics(b,t):return scenes.graphics(b,t,S,at)
def caption(im,b,n):
 t=n/30;gg=[g for g in GROUPS if g['scene']==b['name'] and g['start']<=t<g['end']]
 if not gg:return
 g=gg[0]
 if g['mode']=='full':
  obj=editorial.render_words(g,n);place(im,obj,(1080-obj.width)/2,CAPY.get(b['name'],982)+TOP_SHIFT-obj.height/2)
 else:
  f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',45);sz=45
  while ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',sz).getlength(g['text'])>965:sz-=1
  f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',sz);width=round(f.getlength(g['text']))+42
  rr(im,((1080-width)/2,SPLIT_Y-39,(1080+width)/2,SPLIT_Y+39),'#1C1C1E',10,'#3A3A3C',2);d=ImageDraw.Draw(im);bb=d.textbbox((0,0),g['text'],font=f);d.text((540-(bb[2]-bb[0])/2,SPLIT_Y-(bb[3]-bb[1])/2-bb[1]),g['text'],font=f,fill='white')
def frame(n,person=None):
 # whole-frame lookup: beat starts carry float residue (7.30000001 > 7.3) and drew the previous beat for one frame at every cut (found 22 Sep 2026)
 t=n/30;b=next((b for b in B if round(b['start']*30)<=n<round(b['end']*30)),B[-1]);g_=graphics(b,t-b['start']);im=Image.new('RGBA',g_.size,BG);im.alpha_composite(g_.crop((0,0,g_.width,g_.height-TOP_SHIFT)),(0,TOP_SHIFT))
 if b['mode']=='split' and person is not None:place(im,person,0,SPLIT_Y)
 caption(im,b,n);return im.convert('RGB')
def person_at(t):
 buf=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(P/'edit/tight.mkv'),'-frames:v','1','-vf',f'crop=1080:{PH}:0:{CROP_Y}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
 return Image.frombytes('RGB',(1080,PH),buf).convert('RGBA')
def preview(frac=.65,tag='preview'):
 sheet=Image.new('RGB',(5*270,3*480),'#222')
 for i,b in enumerate(B):
  t=b['start']+min((b['end']-b['start'])*frac,2.3);n=round(t*30);im=frame(n,person_at(t));im.save(P/f'renders/{tag}-{b["name"]}.jpg');sheet.paste(im.resize((270,480)),((i%5)*270,(i//5)*480))
 sheet.save(P/f'renders/contact-{tag}.jpg')
def strip(name,times,out):
 b=S[name];sheet=Image.new('RGB',(len(times)*270,480),'#222')
 for i,lt in enumerate(times):
  t=b['start']+lt;im=frame(round(t*30),person_at(t) if b['mode']=='split' else None);sheet.paste(im.resize((270,480)),(i*270,0))
 sheet.save(out)
def render():
 dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(P/'edit/tight.mkv'),'-vf',f'fps=30,crop=1080:{PH}:0:{CROP_Y}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
 out=P/'renders/clean-voice.mp4'
 enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1080x1920','-framerate','30','-i','pipe:0','-i',str(P/'edit/tight.mkv'),'-map','0:v','-map','1:a','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(N/30),'-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for n in range(N):
  data=dec.stdout.read(1080*PH*3)
  if len(data)!=1080*PH*3:raise RuntimeError(f'Short video frame {n}')
  enc.stdin.write(frame(n,Image.frombytes('RGB',(1080,PH),data).convert('RGBA')).tobytes())
  if n%150==0:print(f'{n}/{N}',flush=True)
 enc.stdin.close();assert enc.wait()==0;dec.stdout.close();dec.wait();print(out)
if __name__=='__main__':
 if '--preview' in sys.argv:preview()
 elif '--strip' in sys.argv:
  i=sys.argv.index('--strip');strip(sys.argv[i+1],[float(x) for x in sys.argv[i+2].split(',')],P/f'renders/strip-{sys.argv[i+1]}.jpg')
 else:render()
