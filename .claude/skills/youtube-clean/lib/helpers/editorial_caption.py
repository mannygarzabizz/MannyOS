"""Approved full-graphics cinematic caption typography (Arial Bold + Times Bold Italic), adapted from the 9:16 reel helper
to the 1920x1080 YouTube intro: bigger type (120-170 px, default 140), max line width 1560 px, no reel-specific scene hacks.
render_words(group, frame) returns an RGBA row; each word pops in (0.96->1 scale over 3 frames) on its own entry_frame and
never moves afterwards. group = {'text': 'WORDS UPPER', 'words':[{'text','entry_frame'}], optional 'big','color','cap','maxw'}."""
import math
from PIL import Image,ImageDraw,ImageFont
cache={}
SIZE=140;MAXW=1560;MIN=120;MAX=170
def font(size,serif=False):
 key=(size,serif)
 if key not in cache:
  name='Times New Roman Bold Italic.ttf' if serif else 'Arial Bold.ttf'
  cache[key]=ImageFont.truetype('/System/Library/Fonts/Supplemental/'+name,size)
 return cache[key]
# Independent word mode: group includes words with entry_frame and text.
special={'CLAUDE':'Claude','CHATGPT':'ChatGPT','GOOGLE':'Google','GEMINI':'Gemini','CLI':'CLI','AI':'AI','I':'I',"I'M":"I'm","I'LL":"I'll","I'VE":"I've"}
serif=set()
def parts_of(g):
 parts=[special.get(w,w.lower()) for w in g['text'].split()]
 if parts and (parts[0] in ['stop','because','just','then'] or g.get('cap')):parts[0]=parts[0][0].upper()+parts[0][1:]
 return parts
def layout(g):
 parts=parts_of(g);size=int(g.get('big') or SIZE);maxw=g.get('maxw',MAXW)
 while True:
  fonts=[font(size+6 if w in serif else size,w in serif) for w in parts]
  gap=font(size).getlength(' ');width=sum(f.getlength(w) for w,f in zip(parts,fonts))+gap*(len(parts)-1)
  if width<=maxw or size<=60:break
  size-=2
 return parts,fonts,gap,width,size
def render_words(g,n):
 parts,fonts,gap,width,size=layout(g)
 boxes=[f.getbbox(w,anchor='ls') for w,f in zip(parts,fonts)]
 top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
 row=Image.new('RGBA',(math.ceil(width)+64,bottom-top+64));x=32;baseline=32-top
 for w,f,b,timing in zip(parts,fonts,boxes,g['words']):
  age=n-timing['entry_frame']
  if age>=0:
   tile=Image.new('RGBA',(b[2]-b[0]+32,b[3]-b[1]+32))
   ImageDraw.Draw(tile).text((16-b[0],16-b[1]),w,font=f,anchor='ls',fill=g.get('color','#1D1D1F'))
   scale=.96+.04*(1-(1-min(1,age/3))**3)
   obj=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
   # Each word scales around its own center; the existing word never moves/replays.
   px=x+b[0]-16+(tile.width-obj.width)/2;py=baseline+b[1]-16+(tile.height-obj.height)/2
   row.alpha_composite(obj,(round(px),round(py)))
  x+=f.getlength(w)+gap
 return row
