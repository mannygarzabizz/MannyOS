"""Synthesise the machine-gun round used by mg_hook.py / shootout.py -> audio/sources/mg-round.wav.
Tighter than the pistol (make_gunshot.py): 10 ms crack + 40 ms body + 55 ms pitch-dropping thump, so 13 rounds/s stay separate.
Mixed at -19 dB in a burst, -16 dB on the first round; the pistol crack (gunshot.wav, -15/-17 dB) marks a tile breaking."""
import numpy as np, wave
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sr=48000;n=int(sr*.20);t=np.arange(n)/sr;rng=np.random.default_rng(11);noise=rng.standard_normal(n)
crack=noise*np.exp(-t/.010)
k=np.exp(-np.arange(300)/45.);k/=k.sum();body=np.convolve(noise,k,'same')*np.exp(-t/.040)*2.0
f=170*np.exp(-t/.035)+55;thump=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t/.055)*1.2
x=crack*.95+body+thump;x*=np.minimum(1,t/.0012);x=np.tanh(x*1.7)
tail=np.zeros(n);d=int(.024*sr);tail[d:]=x[:-d]*.18;x=x+tail
x/=abs(x).max();x*=.9;st=np.stack([x,x],1)
with wave.open(str(P/'audio/sources/mg-round.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
print('audio/sources/mg-round.wav')
