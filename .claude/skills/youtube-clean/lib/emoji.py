"""Real Apple emoji from /System/Library/Fonts/Apple Color Emoji.ttc (native 160 px colour strike, scaled with LANCZOS).

  emoji('🔥',96)            -> RGBA image 96 px tall-ish square, tight to the glyph, cached
  place_emoji(im,'🔥',x,y,96,anchor='lm')
  is_emoji('🔥') / split_emoji('Fast ⚡ thinking') -> [('text','Fast '),('emoji','⚡'),('text',' thinking')]
  verify('🔥')              -> dict(ok=..., reason=...): colour glyph, not tofu / not monochrome
  python3 emoji.py           -> writes emoji_test.png next to this file and asserts every glyph verifies

Limits: the bitmap strike is 160 px; above ~200 px redraw the emoji by hand (reel-clean/template/examples/eyes_hook.py).
This Pillow build has no raqm, so ZWJ sequences / flags / skin-tone modifiers are NOT shaped into one glyph:
stick to single-codepoint emoji (optionally followed by U+FE0F). emoji() raises on sequences it cannot render as one glyph.
"""
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
PATH='/System/Library/Fonts/Apple Color Emoji.ttc';STRIKE=160
@lru_cache(None)
def _font():return ImageFont.truetype(PATH,STRIKE)
def _ranges(o):
 return (0x1F000<=o<=0x1FAFF) or (0x2600<=o<=0x27BF) or (0x2B00<=o<=0x2BFF) or (0x2300<=o<=0x23FF) or o in (0x203C,0x2049,0x2122,0x2139,0x3030,0x303D,0x3297,0x3299,0x00A9,0x00AE) or (0x2190<=o<=0x21FF) or (0x25A0<=o<=0x25FF) or (0x2900<=o<=0x297F)
def is_emoji(s):
 s=s.replace('️','')
 return len(s)>0 and all(_ranges(ord(c)) for c in s)
def split_emoji(s):
 """Split a string into ('text',..)/('emoji',..) runs; one emoji codepoint (+VS16) per emoji run."""
 out=[];buf=''
 i=0
 while i<len(s):
  c=s[i]
  if _ranges(ord(c)) and c not in '©®™':
   if buf:out.append(('text',buf));buf=''
   e=c
   if i+1<len(s) and s[i+1]=='️':i+=1
   out.append(('emoji',e))
  elif c!='️':buf+=c
  i+=1
 if buf:out.append(('text',buf))
 return out
@lru_cache(maxsize=256)
def _native(ch):
 ch=ch.replace('️','')
 if len(ch)!=1:raise ValueError(f'emoji {ch!r}: only single-codepoint emoji can be rendered without raqm (no ZWJ/flags/skin tones)')
 f=_font();im=Image.new('RGBA',(STRIKE+80,STRIKE+80),(0,0,0,0))
 ImageDraw.Draw(im).text((40,40),ch,font=f,embedded_color=True)
 bb=im.getchannel('A').getbbox()
 if bb is None:raise ValueError(f'emoji {ch!r} rendered empty (not in Apple Color Emoji)')
 # square box around the glyph so every emoji scales alike
 cx,cy=(bb[0]+bb[2])/2,(bb[1]+bb[3])/2;s=max(bb[2]-bb[0],bb[3]-bb[1]);s=max(s,STRIKE*.9)
 return im.crop((round(cx-s/2),round(cy-s/2),round(cx+s/2),round(cy+s/2)))
@lru_cache(maxsize=1024)
def emoji(ch,size):
 """RGBA square of `size` px with the real Apple glyph."""
 size=max(2,int(round(size)));n=_native(ch)
 if size>200:print(f'[emoji] {ch} at {size}px is above the 160 px strike and will look soft; redraw it (see eyes_hook.py)')
 return n.resize((size,size),Image.Resampling.LANCZOS)
def place_emoji(im,ch,x,y,size,anchor='lt',opacity=1.):
 e=emoji(ch,size)
 ax={'l':0,'m':size/2,'r':size}[anchor[0]];ay={'t':0,'m':size/2,'b':size}[anchor[1]]
 if opacity<1:e=e.copy();e.putalpha(e.getchannel('A').point(lambda a:int(a*opacity)))
 im.alpha_composite(e,(int(round(x-ax)),int(round(y-ay))));return e
def verify_image(im):
 """True colour glyph? Tofu/missing glyphs are empty or a monochrome box; colour emoji have saturated, varied pixels."""
 a=np.asarray(im.convert('RGBA')).astype(int);al=a[...,3];op=al>200
 cover=op.mean()
 if cover<.12:return dict(ok=False,reason=f'almost empty (coverage {cover:.2f})',coverage=float(cover))
 rgb=a[...,:3][op];sat=(rgb.max(1)-rgb.min(1));colors=len(np.unique(rgb//8,axis=0))
 res=dict(coverage=float(cover),mean_saturation=float(sat.mean()),saturated_fraction=float((sat>60).mean()),distinct_colours=int(colors))
 res['ok']=bool(colors>=24 and (res['saturated_fraction']>.15 or colors>=120));res['reason']='colour glyph' if res['ok'] else 'monochrome / tofu-like'
 return res
def verify(ch):
 try:return verify_image(_native(ch))
 except ValueError as e:return dict(ok=False,reason=str(e))
if __name__=='__main__':
 test='🔥⚡👀🚀💸✅🧠📈🤯❤️';parts=[e for k,e in split_emoji(test) if k=='emoji']
 sheet=Image.new('RGBA',(len(parts)*180+20,420),'white');ok=True
 for i,ch in enumerate(parts):
  r=verify(ch);ok&=r['ok'];print(ch,r)
  place_emoji(sheet,ch,20+i*180,20,160);place_emoji(sheet,ch,20+i*180,220,72);place_emoji(sheet,ch,120+i*180,230,40)
 # negative control: a glyph that is not an emoji must NOT verify
 neg=Image.new('RGBA',(200,200),(0,0,0,0));d=ImageDraw.Draw(neg);d.rectangle((40,30,160,170),outline='black',width=8);print('tofu control',verify_image(neg));assert not verify_image(neg)['ok']
 out=Path(__file__).with_name('emoji_test.png');sheet.convert('RGB').save(out);print('wrote',out);assert ok,'an emoji did not render as a colour glyph'
