"""ACCEPTED (Laya reel, 21 Sep 2026). Albert: "When we talk about local show a MacBook computer."
A MacBook Pro drawn from scratch (front view): black bezel with the camera notch, space-grey lid edge,
aluminium base with the thumb scoop, soft contact shadow. The lid opens by scaling about the hinge.

macbook(w, screen, open) -> RGBA, width = w*1.13 (the base is wider than the lid)
desktop(w, h)            -> a Sonoma-like wallpaper (cached)
wifi(im, x, y, on, k)    -> menu-bar Wi-Fi glyph; when off it greys out and a slash draws in with k 0..1
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from draw import *
import numpy as np

@lru_cache(maxsize=8)
def desktop(w,h):
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32);u=xx/w;v=yy/h
    a=np.array([38,70,190],np.float32);b=np.array([150,84,220],np.float32);c=np.array([245,150,120],np.float32)
    k1=np.clip(1.2*u*.6+v*.7-.15,0,1)[...,None];k2=np.clip((u-.35)**2*2.2+(v-1.05)**2*1.6,0,1)[...,None]
    img=a*(1-k1)+b*k1;img=img*(k2)+c*(1-k2)*.9+img*(1-k2)*.1
    wave=(np.sin(u*5.5+v*3.0)*.5+.5)[...,None]*18;img=np.clip(img+wave,0,255)
    return Image.fromarray(np.dstack([img.astype(np.uint8),np.full((h,w),255,np.uint8)]),'RGBA').filter(ImageFilter.GaussianBlur(3))

def wifi(im,x,y,on=True,k=0):
    d=ImageDraw.Draw(im);col='#1D1D1F' if on else '#8A8A8E'
    for r in (19,13,7):d.arc((x-r,y+7-r,x+r,y+7+r),225,315,fill=col,width=3)
    d.ellipse((x-2.5,y+5,x+2.5,y+10),fill=col)
    if not on and k>0:
        x0,y0,x1,y1=x-13,y-9,x+13,y+11
        d.line([(x0,y0),(x0+(x1-x0)*k,y0+(y1-y0)*k)],fill=(255,255,255,255),width=6)
        d.line([(x0,y0),(x0+(x1-x0)*k,y0+(y1-y0)*k)],fill='#1D1D1F',width=3)

@lru_cache(maxsize=4)
def _base(w):
    """Aluminium base + contact shadow, width bw."""
    bw=round(w*1.13);bh=round(w*.036);pad=60;im=blank(bw+2*pad,bh+pad+40)
    sh=blank(im.width,im.height);ImageDraw.Draw(sh).ellipse((pad+bw*.04,bh+8,pad+bw*.96,bh+40),fill=(0,0,0,70));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    q=3;b=blank(bw*q,bh*q);d=ImageDraw.Draw(b)
    for yy in range(bh*q):                                          # vertical metal gradient
        u=yy/(bh*q);g=round(lerp(222,150,u**1.4));d.line([(0,yy),(bw*q,yy)],fill=(g,g+1,g+5,255))
    m=Image.new('L',(bw*q,bh*q));ImageDraw.Draw(m).rounded_rectangle((0,-bh*q,bw*q-1,bh*q-1),radius=round(bh*q*.85),fill=255)
    b.putalpha(m)
    sw=round(bw*.15*q);ImageDraw.Draw(b).rounded_rectangle(((bw*q-sw)/2,-10*q,(bw*q+sw)/2,bh*q*.36),radius=round(bh*q*.3),fill=(120,121,126,255))   # thumb scoop
    ImageDraw.Draw(b).line([(0,1),(bw*q,1)],fill=(245,245,248,255),width=q)
    im.alpha_composite(b.resize((bw,bh),Image.Resampling.LANCZOS),(pad,0));return im,bw,bh,pad

def macbook(w,screen,open_=1.0):
    bez=round(w*.019);top=round(w*.024);sw,sh=w-2*bez,screen.height*(w-2*bez)//screen.width
    lh=sh+top+bez;lid=blank(w,lh)
    rr(lid,(0,0,w-1,lh-1),'#8E9096',round(w*.030));rr(lid,(2,2,w-3,lh-1),'#0A0A0B',round(w*.028))
    scr=screen if screen.size==(sw,sh) else screen.resize((sw,sh),Image.Resampling.LANCZOS)
    m=Image.new('L',(sw,sh));ImageDraw.Draw(m).rounded_rectangle((0,0,sw-1,sh-1),radius=round(w*.014),fill=255)
    s2=scr.copy();s2.putalpha(m);lid.alpha_composite(s2,(bez,top))
    nw,nh=round(w*.118),round(w*.021);rr(lid,((w-nw)/2,top-2,(w+nw)/2,top+nh),'#0A0A0B',round(nh*.45))      # notch
    ImageDraw.Draw(lid).ellipse((w/2-3,top+nh/2-5,w/2+3,top+nh/2+1),fill='#1C2430')
    base,bw,bh,pad=_base(w);out=blank(bw,lh+bh+44)
    open_=max(.04,min(1,open_))
    if open_<1:lid=lid.resize((w,max(2,round(lh*open_))),Image.Resampling.LANCZOS)
    out.alpha_composite(base,(-pad,lh))
    out.alpha_composite(lid,((bw-w)//2,lh-lid.height))
    return out

if __name__=='__main__':
    s=desktop(904,568);ops=[.12,.35,.65,1.0];sheet=Image.new('RGBA',(len(ops)*560,420),BG)
    for i,o in enumerate(ops):
        scr=s if o>=1 else Image.blend(Image.new('RGBA',s.size,'#050506'),s,max(0,(o-.35)/.65))
        mb=macbook(470,scr,o);sheet.alpha_composite(mb,(i*560+(560-mb.width)//2,40))
    sheet.convert('RGB').save(Path(__file__).with_name('macbook_strip.jpg'));print('macbook_strip.jpg')
