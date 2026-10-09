"""Instagram-style comment animation. Returns a transparent 900x430 Pillow image.
UI illustration only; no account action. Configure keyword, timings and viewer label.
"""
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def font(size):return ImageFont.truetype(str(ROOT/'assets/fonts/Inter.ttf'),size)
def text(im,s,x,y,size=30,color='#262626',center=False):
 d=ImageDraw.Draw(im);f=font(size);b=d.textbbox((0,0),s,font=f)
 d.text((x-(b[2]-b[0])/2 if center else x,y-b[1]),s,font=f,fill=color)
def avatar(im,x,y,r=25):
 d=ImageDraw.Draw(im);d.ellipse((x-r,y-r,x+r,y+r),fill='#DBDBDB');d.ellipse((x-r*.30,y-r*.58,x+r*.30,y+.02*r),fill='white');d.ellipse((x-r*.6,y+r*.1,x+r*.6,y+r*.86),fill='white')
def heart(im,x,y,size=25):
 # Cubic-style sampled outline, no font/emoji dependency.
 import math
 pts=[]
 for i in range(65):
  a=i/64*2*math.pi;xx=16*math.sin(a)**3;yy=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)
  pts.append((x+xx*size/32,y-yy*size/32))
 ImageDraw.Draw(im).line(pts,fill='#262626',width=2,joint='curve')
def render(t,keyword='GEMINI',viewer='you',type_start=.25,type_duration=.6,post_at=1.95):
 im=Image.new('RGBA',(900,430));d=ImageDraw.Draw(im)
 d.rounded_rectangle((0,0,899,429),radius=19,fill='white')
 text(im,'Comments',450,34,34,center=True)
 d.line([(43,36),(29,51),(43,66)],fill='#262626',width=3,joint='curve')
 d.line([(1,97),(898,97)],fill='#EFEFEF',width=2)
 posted=t>=post_at
 if posted:
  avatar(im,51,159,25);text(im,viewer,98,128,29);text(im,keyword,98,168,52)
  text(im,'1s',98,236,23,'#8E8E8E');text(im,'Reply',143,236,23,'#8E8E8E');heart(im,843,167,28)
 else:
  text(im,'No comments yet.',450,165,35,center=True)
  text(im,'Start the conversation.',450,221,27,'#8E8E8E',True)
 d.line([(1,297),(898,297)],fill='#EFEFEF',width=2)
 avatar(im,48,361,25)
 d.rounded_rectangle((91,319,869,402),radius=41,outline='#DBDBDB',width=2)
 fraction=max(0,min(1,(t-type_start)/type_duration));typed=keyword[:int(len(keyword)*fraction)] if not posted else ''
 if typed:text(im,typed,121,338,44)
 else:text(im,'Add a comment…',121,347,29,'#8E8E8E')
 text(im,'Post',813,347,29,'#0095F6' if typed else '#B3DBF7',True)
 return im
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('out',type=Path);ap.add_argument('--time',type=float,default=1);ap.add_argument('--keyword',default='GEMINI');a=ap.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True);render(a.time,a.keyword).save(a.out)
