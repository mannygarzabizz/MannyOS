"""Approved full-graphics caption typography. caption(group, frame_age, hook) returns RGBA."""
import math
from PIL import Image,ImageDraw,ImageFont
cache={}
def font(size,serif=False):
 key=(size,serif)
 if key not in cache:
  name='Times New Roman Bold Italic.ttf' if serif else 'Arial Bold.ttf'
  cache[key]=ImageFont.truetype('/System/Library/Fonts/Supplemental/'+name,size)
 return cache[key]
def caption(g,age,hook):
 # Sentence-case typographic contrast follows the user's reference.
 special={'CLAUDE':'Claude','CHATGPT':'ChatGPT','GOOGLE':'Google','CLOUD':'Cloud','GEMINI':'Gemini','CLI':'CLI','AI':'AI','/MODEL':'/model'}
 parts=[special.get(w,w.lower()) for w in g['text'].split()]
 if parts[0] in ['stop','because','just','then']:parts[0]=parts[0].capitalize()
 serif_words={'Claude','ChatGPT','$20','$300','/model'}
 size=112
 while True:
  fonts=[font(size+5 if w in serif_words else size,w in serif_words) for w in parts]
  width=sum(f.getlength(w) for w,f in zip(parts,fonts))+font(size).getlength(' ')*(len(parts)-1)
  if width<=912:break
  size-=2
 boxes=[f.getbbox(w,anchor='ls') for w,f in zip(parts,fonts)]
 top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
 layer=Image.new('RGBA',(math.ceil(width)+32,bottom-top+16));d=ImageDraw.Draw(layer);x=16
 for w,f in zip(parts,fonts):
  d.text((x,8-top),w,font=f,anchor='ls',fill=g.get('color','#F5F5F7'))
  x+=f.getlength(w)+font(size).getlength(' ')
 v=min(1,age/3);scale=.96+.04*(1-(1-v)**3)
 return layer.resize((round(layer.width*scale),round(layer.height*scale)),Image.Resampling.LANCZOS)

# Independent word mode: group includes words with entry_frame, scene, and text.
special={'CLAUDE':'Claude','CHATGPT':'ChatGPT','GOOGLE':'Google','CLOUD':'Cloud','GEMINI':'Gemini','CLI':'CLI','AI':'AI','/MODEL':'/model'}
serif={'Claude','ChatGPT','$20','$300','/model'}
def render_words(g,n):
 parts=[special.get(w,w.lower()) for w in g['text'].split()]
 if parts[0] in ['stop','because','just','then'] or g.get('cap'):parts[0]=parts[0][0].upper()+parts[0][1:]
 size=185 if g['scene']=='credit' and g['text']=='$300' else (100 if g['scene']=='hook' else 112);maxw=600 if g['scene']=='hook' else 912
 if g.get('big'):size,maxw=g['big'],912
 while True:
  fonts=[font(size+5 if w in serif else size,w in serif) for w in parts]
  gap=font(size).getlength(' ');width=sum(f.getlength(w) for w,f in zip(parts,fonts))+gap*(len(parts)-1)
  if width<=maxw:break
  size-=2
 boxes=[f.getbbox(w,anchor='ls') for w,f in zip(parts,fonts)]
 top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
 row=Image.new('RGBA',(math.ceil(width)+48,bottom-top+48));x=24;baseline=24-top
 for w,f,b,timing in zip(parts,fonts,boxes,g['words']):
  age=n-timing['entry_frame']
  if age>=0:
   tile=Image.new('RGBA',(b[2]-b[0]+32,b[3]-b[1]+32))
   ImageDraw.Draw(tile).text((16-b[0],16-b[1]),w,font=f,anchor='ls',fill=g.get('color','#F5F5F7'))
   scale=.96+.04*(1-(1-min(1,age/3))**3)
   obj=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
   # Each word scales around its own center; the existing word never moves/replays.
   px=x+b[0]-16+(tile.width-obj.width)/2;py=baseline+b[1]-16+(tile.height-obj.height)/2
   row.alpha_composite(obj,(round(px),round(py)))
  x+=f.getlength(w)+gap
 return row
