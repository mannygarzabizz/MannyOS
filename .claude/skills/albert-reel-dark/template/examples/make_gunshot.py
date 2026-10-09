"""Synthesise the stylised gunshot used by gun_hook.py -> audio/sources/gunshot.wav (the SFX kit has no shot).
Noise crack (18 ms decay) + low-passed body (75 ms) + pitch-dropping sine thump (150 -> 48 Hz) + two short room taps,
soft-clipped with tanh. Mixed at -15 dB (first / last round), -17 dB (singles), -19 dB (burst)."""
import numpy as np, wave
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sr=48000;n=int(sr*.42);t=np.arange(n)/sr;rng=np.random.default_rng(7);noise=rng.standard_normal(n)
crack=noise*np.exp(-t/.018)
k=np.exp(-np.arange(400)/60.);k/=k.sum();body=np.convolve(noise,k,'same')*np.exp(-t/.075)*2.2
f=150*np.exp(-t/.05)+48;thump=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t/.09)*1.3
x=crack*.9+body+thump;x*=np.minimum(1,t/.0015);x=np.tanh(x*1.6)
tail=np.zeros(n);d=int(.031*sr);tail[d:]=x[:-d]*.22;d2=int(.057*sr);tail[d2:]+=x[:-d2]*.12;x=x+tail
x/=abs(x).max();x*=.9;st=np.stack([x,x],1)
with wave.open(str(P/'audio/sources/gunshot.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
print('audio/sources/gunshot.wav')
