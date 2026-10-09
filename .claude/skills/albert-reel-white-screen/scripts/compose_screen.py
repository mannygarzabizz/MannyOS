#!/usr/bin/env python3
"""Split-screen tutorial composite (white popout style + screen-share windows).
Layers: white cards base -> per-window screen shadow + rounded zoomed screen
(enable=between) -> speaker frame shadow -> rounded speaker frame -> head popout
RGBA sequence -> captions. Then loudnorm + music.
Usage: compose_screen.py <cfg.json> <out.mp4>
cfg: { cut, cards, capt_dir, seg_dir, windows_json, music, offset_speaker (src crop y for
frame = 1080 - offset; popout strip overlay at 870), music_vol }"""
import json, sys, subprocess, os
cfg=json.load(open(sys.argv[1])); OUT=sys.argv[2]
CUT=cfg["cut"]; CARDS=cfg["cards"]; CAPT=cfg["capt_dir"]; SEG=cfg["seg_dir"]
WIN=json.load(open(cfg["windows_json"]))["windows"]
MUSIC=cfg["music"]; MVOL=cfg.get("music_vol",0.06)
OFF=cfg["offset_speaker"]           # screen_y = src_y + OFF
FT=cfg.get("frame_top",1020)         # top edge of the floating video frame
PT=cfg.get("popout_top",FT-300)     # top of the head-popout strip (must match segmentation Y0=PT-OFF)
CY=cfg.get("capt_y",40)             # caption overlay y
FH=1890-FT                          # frame interior height (bottom margin 30)
fy0=FT-OFF                          # source crop y for the frame interior
DUR=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","csv=p=0",CUT],capture_output=True,text=True).stdout.strip())
FOUT=max(0,DUR-2)

inputs=["-i",CUT,"-i",CARDS,"-loop","1","-i",f"{SEG}/frame_mask.png",
        "-framerate","25","-i",f"{SEG}/popout/%05d.png",
        "-framerate","12","-i",f"{CAPT}/%05d.png",
        "-loop","1","-i",f"{SEG}/frame_shadow.png",
        "-loop","1","-i",f"{SEG}/screen_mask.png",
        "-loop","1","-i",f"{SEG}/screen_shadow.png"]
ni=8
NW=len(WIN)
fc=[f"[0:v]scale=1080:-2,crop=1020:{FH}:30:{fy0}[vf]",
    "[2:v]format=gray[mk]","[vf][mk]alphamerge[vfa]",
    "[6:v]format=gray,split="+str(NW)+"".join(f"[smk{n}]" for n in range(NW)),
    "[7:v]split="+str(NW)+"".join(f"[shd{n}]" for n in range(NW))]
cur="[1:v]"
# screen windows: shadow + rounded screen, each enabled in its own time window
for n,w in enumerate(WIN):
    inputs+=["-i",f"{SEG}/screens/w{n}.mp4"]
    A,B=w["start"],w["end"]
    fc.append(f"[{ni}:v]scale=1020:574,setsar=1[sc{n}]")
    fc.append(f"[sc{n}][smk{n}]alphamerge,setpts=PTS+{A}/TB[sca{n}]")
    fc.append(f"{cur}[shd{n}]overlay=0:0:enable='between(t,{A},{B})'[ss{n}]")
    fc.append(f"[ss{n}][sca{n}]overlay=30:120:enable='between(t,{A},{B})'[sw{n}]")
    cur=f"[sw{n}]"; ni+=1
fc.append(f"{cur}[5:v]overlay=0:0:shortest=1[fs]")
fc.append(f"[fs][vfa]overlay=30:{FT}[sp]")
fc.append(f"[sp][3:v]overlay=0:{PT}[pp]")
TITLE=cfg.get("title_png")
if TITLE:
    inputs+=["-loop","1","-i",TITLE]
    fc.append(f"[pp][4:v]overlay=0:{CY}[cap]")
    TW=cfg.get("title_window")
    en=f":enable='between(t,{TW[0]},{TW[1]})'" if TW else ""
    fc.append(f"[cap][{ni}:v]overlay=0:0:shortest=1{en}[final]"); ni+=1
else:
    fc.append(f"[pp][4:v]overlay=0:{CY}[final]")
subprocess.run(["ffmpeg","-y","-v","error"]+inputs+["-filter_complex",";".join(fc),
    "-map","[final]","-map","0:a","-c:v","libx264","-preset","medium","-crf","21",
    "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",OUT+".noaudio.mp4"],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT+".noaudio.mp4","-i",MUSIC,"-filter_complex",
    f"[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[vo];[1:a]atrim=start=4,asetpts=PTS-STARTPTS,"
    f"volume={MVOL},afade=in:st=0:d=0.5,afade=out:st={FOUT}:d=2[m];"
    f"[vo][m]amix=inputs=2:duration=first:normalize=0[a]",
    "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",
    "-movflags","+faststart",OUT],check=True)
os.remove(OUT+".noaudio.mp4")
print("DONE ->",OUT)
