"""Synth SFX for the Opus 5.5 reel: bazooka launch, rocket flight, full-screen explosion, tile drop thud.
All 48 kHz stereo, peak-normalised; mix.py sets the level per cue."""
import numpy as np,wave
from pathlib import Path
sr=48000;A=Path(__file__).resolve().parent/'audio/sources'
def save(name,x):
    x=x/(abs(x).max()+1e-9)*.98;st=np.stack([x,x],1)
    with wave.open(str(A/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
    print(name,f'{len(x)/sr:.2f}s')
def lp(x,fc):
    a=np.exp(-2*np.pi*fc/sr);y=np.zeros_like(x);z=0
    for i in range(len(x)):z=a*z+(1-a)*x[i];y[i]=z
    return y
def hp(x,fc):return x-lp(x,fc)
rnd=np.random.default_rng(7)
def t_(d):return np.arange(int(sr*d))/sr
# --- bazooka launch: thump + whoosh with a sweeping band-pass -----------------------------
t=t_(.55);n=rnd.standard_normal(len(t))
thump=np.sin(2*np.pi*(70*np.exp(-t*6)+35)*t)*np.exp(-t*14)*1.2
wh=lp(hp(n,300),3200)*np.exp(-t*7)*(1-np.exp(-t*90))
crack=hp(n,1500)*np.exp(-t*80)*.9
save('bazooka-launch.wav',thump+wh*.9+crack)
# --- rocket flight: rising hiss 0.35 s -------------------------------------------------------
t=t_(.35);n=rnd.standard_normal(len(t))
f=1200+3000*(t/.35)**1.5;hiss=lp(hp(n,900),2500)*np.sin(2*np.pi*np.cumsum(f)/sr)*.6+lp(hp(n,1500),6000)*.5
save('rocket-flight.wav',hiss*(.4+.6*t/.35))
# --- explosion: crack + long low rumble + noise tail, 1.6 s ---------------------------------
t=t_(1.6);n=rnd.standard_normal(len(t))
crack=hp(n,800)*np.exp(-t*45)*1.4
body=lp(n,900)*np.exp(-t*3.2)*1.1
rumble=lp(n,140)*np.exp(-t*1.6)*2.4+np.sin(2*np.pi*(55*np.exp(-t*2)+28)*t)*np.exp(-t*2.2)*1.6
tail=lp(n,2500)*np.exp(-t*2.6)*.35
save('explosion.wav',crack+body+rumble+tail)
# --- tile drop thud + tiny bounce ----------------------------------------------------------
t=t_(.32)
th=np.sin(2*np.pi*(95*np.exp(-t*20)+42)*t)*np.exp(-t*22)+hp(rnd.standard_normal(len(t)),2000)*np.exp(-t*120)*.5
save('thud.wav',th)
