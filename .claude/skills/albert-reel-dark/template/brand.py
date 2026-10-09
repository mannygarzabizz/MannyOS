"""Brand tiles (accepted on the Laya and AI-killed-software reels).

Added 22 Sep 2026: emoji() (Apple Color Emoji at native 160 px), tile_emoji, tile_fluent (Microsoft Fluent 3D PNGs in
assets/icons/fluent), tile_app (official App Store icons via the iTunes Search API, assets/icons/<App>.png), tile_icon,
tile_software (generic window glyph), tile_salesforce. Never draw person figures - use these.
 Pattern for ANY reel: rival = its own square logo filling the tile,
new tool = white tile + mark redrawn from its SVG, unrevealed tool = ink tile with a white "?".
Official icon sources, in order: the brand site's <link rel="apple-touch-icon"> / rel="icon" (curl the homepage and grep),
the repo's assets/ folder (logo .svg - redraw it so it is sharp at any size), then lobehub icons-static-png on jsDelivr.

Brand tiles for the Laya reel.

- Jev   = TypeSafe's own apple-touch-icon from typesafe.ai (assets/brand/typesafe-apple-touch.png):
          magenta #E551BA square with the black isometric mark. A brand's own square logo fills the tile.
- Laya  = the project's mark redrawn from assets/logo-mark.svg in github.com/NandhaKishorM/laya
          (open arc + eleven dots spiralling inward, #2A78D6), so it stays sharp at any size.
- "?"   = the unrevealed model: ink squircle, white question mark.
"""
from draw import *
import numpy as np
PINK='#E551BA';LAYA_BLUE='#2A78D6';SF_BLUE='#1FBDFE'
EMOJI_FONT='/System/Library/Fonts/Apple Color Emoji.ttc'

def _mask(im,size):
    im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(squircle_mask(size)))));return im

def _ring(im,size,color=(255,255,255,40)):
    """Hairline squircle ring (light, for the dark ground: dark tiles need it, white tiles keep it subtle)."""
    q=2;big=squircle_mask(size*q).resize((size,size),Image.Resampling.LANCZOS)
    inner=squircle_mask(size-4).resize((size-4,size-4));m=Image.new('L',(size,size));m.paste(inner,(2,2))
    edge=Image.fromarray(np.clip(np.array(big).astype(int)-np.array(m).astype(int),0,255).astype('uint8'))
    lay=Image.new('RGBA',(size,size),color);lay.putalpha(Image.fromarray((np.array(edge)*(color[3]/255)).astype('uint8')))
    im.alpha_composite(lay);return im

@lru_cache(None)
def tile_jev(size):
    im=Image.open(P/'assets/icons/TypeSafe.png').convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
    return _mask(im,size)

@lru_cache(None)
def laya_mark(size,color=LAYA_BLUE):
    """The Laya mark from its SVG (viewBox 64): arc r=21 centred (32,32) + dots with their own opacities."""
    q=4;S=size*q;k=S/64;im=blank(S,S);rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
    lay=blank(S,S);d=ImageDraw.Draw(lay)
    # arc from (22.141,13.458) sweeping counter-clockwise (large arc) to (42.5,50.187)
    a0=math.degrees(math.atan2(13.458-32,22.141-32));a1=math.degrees(math.atan2(50.187-32,42.5-32))
    w=5.0*k;r=21*k
    d.arc((32*k-r-w/2,32*k-r-w/2,32*k+r+w/2,32*k+r+w/2),start=a1,end=a0+360,fill=rgb+(242,),width=round(w))
    for ang in (a0,a1):   # round caps
        cx,cy=32*k+r*math.cos(math.radians(ang)),32*k+r*math.sin(math.radians(ang))
        d.ellipse((cx-w/2,cy-w/2,cx+w/2,cy+w/2),fill=rgb+(242,))
    im.alpha_composite(lay)
    dots=[(48.213,42.609,2.782,.929),(49.456,33.958,2.527,.894),(46.696,26.535,2.291,.852),(41.336,21.918,2.067,.803),
          (35.242,20.694,1.852,.749),(30.173,22.422,1.642,.691),(27.294,25.889,1.438,.628),(26.902,29.558,1.239,.562),
          (28.430,32.075,1.043,.493),(30.702,32.690,.850,.420),(32.0,32.0,2.35,1.0)]
    for cx,cy,rr_,op in dots:
        l2=blank(S,S);ImageDraw.Draw(l2).ellipse(((cx-rr_)*k,(cy-rr_)*k,(cx+rr_)*k,(cy+rr_)*k),fill=rgb+(round(255*op),));im.alpha_composite(l2)
    return im.resize((size,size),Image.Resampling.LANCZOS)

@lru_cache(None)
def tile_laya(size):
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill='white')
    k=round(size*.74);im.alpha_composite(laya_mark(k),((size-k)//2,(size-k)//2))
    return _ring(_mask(im,size),size)

@lru_cache(None)
def tile_q(size):
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill='#2C2C2E')   # dark mode: raised grey, not ink
    f=sf(size*.66,'Heavy');ImageDraw.Draw(im).text((size/2,size/2),'?',font=f,fill='white',anchor='mm')
    return _ring(_mask(im,size),size,(255,255,255,56))

@lru_cache(None)
def tile_claude(size):return apptile('Claude',size)

@lru_cache(None)
def emoji(ch,size=160):
    """Apple Color Emoji bitmap. The font only ships 160 px glyphs; render there and downscale, never upscale."""
    f=ImageFont.truetype(EMOJI_FONT,160);im=blank(200,200);ImageDraw.Draw(im).text((100,100),ch,font=f,embedded_color=True,anchor='mm')
    bb=im.getbbox();im=im.crop(bb) if bb else im
    if size!=max(im.size):
        k=size/max(im.size);im=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.Resampling.LANCZOS)
    return im


@lru_cache(None)
def tile_emoji(ch,size,frac=.62,bg='white'):
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill=bg)
    e=emoji(ch,round(size*frac));im.alpha_composite(e,((size-e.width)//2,(size-e.height)//2))
    return _ring(_mask(im,size),size) if bg=='white' else _mask(im,size)


@lru_cache(None)
def tile_software(size,bg='white'):
    """Generic software: a little macOS window with traffic lights and three content lines."""
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill=bg);q=4;S=size*q;w=blank(S,S);d=ImageDraw.Draw(w)
    x0,y0,x1,y1=S*.16,S*.22,S*.84,S*.78;r=S*.06
    d.rounded_rectangle((x0,y0,x1,y1),radius=r,fill='#F4F4F6',outline='#C9C9CE',width=q*2)
    d.rounded_rectangle((x0,y0,x1,y0+S*.13),radius=r,fill='#E4E4E8');d.rectangle((x0,y0+S*.07,x1,y0+S*.13),fill='#E4E4E8')
    for i,c in enumerate(['#FF5F57','#FEBC2E','#28C840']):d.ellipse((x0+S*.04+i*S*.06,y0+S*.045,x0+S*.04+i*S*.06+S*.04,y0+S*.085),fill=c)
    for i in range(3):
        ln=(.44,.30,.38)[i];d.rounded_rectangle((x0+S*.07,y0+S*.21+i*S*.11,x0+S*.07+S*ln,y0+S*.21+i*S*.11+S*.05),radius=S*.025,fill='#B9B9C0' if i else '#8E8E93')
    im.alpha_composite(w.resize((size,size),Image.Resampling.LANCZOS))
    return _ring(_mask(im,size),size) if bg=='white' else _mask(im,size)


@lru_cache(None)
def tile_fluent(name,size,frac=.70):
    """White tile + a Microsoft Fluent 3D emoji figure (assets/icons/fluent/<name>.png, 256 px, MIT)."""
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill='white');k=round(size*frac)
    fig=Image.open(P/'assets/icons/fluent'/f'{name}.png').convert('RGBA').resize((k,k),Image.Resampling.LANCZOS)
    im.alpha_composite(fig,((size-k)//2,(size-k)//2+round(size*.03)));return _ring(_mask(im,size),size)


@lru_cache(None)
def tile_app(name,size):
    """An official App Store icon (assets/icons/<name>.png, 512 px) filling the squircle - Salesforce, Notion, Slack, HubSpot, Zoom, Dropbox..."""
    if name=='Notion':return tile_icon('Notion',size,.70)
    im=Image.open(P/'assets/icons'/f'{name}.png').convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
    return _ring(_mask(im,size),size)


@lru_cache(None)
def tile_icon(name,size,frac=.66,bg='white'):
    """White tile + a mark from assets/icons (lobehub / official PNGs)."""
    im=blank(size,size);ImageDraw.Draw(im).rectangle((0,0,size,size),fill=bg);k=round(size*frac);im.alpha_composite(icon(name,k),((size-k)//2,(size-k)//2))
    return _ring(_mask(im,size),size)


@lru_cache(None)
def tile_salesforce(size):
    """Official Salesforce app icon (white ground, blue cloud) filling the squircle."""
    im=Image.open(P/'assets/icons/Salesforce.png').convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
    return _ring(_mask(im,size),size)


def tracked(im,s,cx,y,n,color,gap,weight='Medium'):
    """Letter-spaced small caps on ONE baseline (anchor 'ls'); centred on cx, y is the baseline."""
    f=sf(n,weight);wd=sum(f.getlength(c) for c in s)+gap*(len(s)-1);x=cx-wd/2;d=ImageDraw.Draw(im)
    for c in s:
        d.text((x,y),c,font=f,fill=color,anchor='ls');x+=f.getlength(c)+gap

if __name__=='__main__':
    sheet=Image.new('RGBA',(4*300+100,380),BG)
    for i,t in enumerate([tile_jev(260),tile_q(260),tile_laya(260),tile_claude(260)]):place(sheet,t,40+i*300,60,sh=True)
    sheet.convert('RGB').save(P/'examples/brand_tiles.jpg');print('examples/brand_tiles.jpg')
