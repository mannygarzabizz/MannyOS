#!/usr/bin/env python3
"""Soft click under every FULL-SCREEN caption (Albert, 2026-09-20 — he likes the cinematic-caption clicks and wants them on the
'cam' captions too).   python3 scripts/camcap_clicks.py <project> <section> [--also-last] [--dry]

Imports the section's scenes.py (so CAM_CAPS' word times are already resolved by camcaps.make_overlay), builds one
caption-mouse-down cue as each caption's first word lands (+ its last word with --also-last) and MERGES them into
sections/<sec>/sfx.json, keeping every other cue and dropping duplicates within 40 ms. Run it after editing CAM_CAPS, then
mix_section.py. Safe to re-run: it replaces the camcap cues it wrote before (rows whose 'why' starts with 'camcap ')."""
import sys,os,json,importlib.util
from pathlib import Path
LIB=Path(__file__).resolve().parent.parent/'lib'
sys.path.insert(0,str(LIB/'helpers'));sys.path.insert(0,str(LIB))
P,sec=Path(sys.argv[1]).resolve(),sys.argv[2];D=P/'sections'/sec
also_last='--also-last' in sys.argv;dry='--dry' in sys.argv
sys.path.insert(0,str(D));os.chdir(D)
import camcaps
spec=importlib.util.spec_from_file_location('scenes',D/'scenes.py');m=importlib.util.module_from_spec(spec);sys.modules['scenes']=m;spec.loader.exec_module(m)
caps=getattr(m,'CAM_CAPS',None)
if not caps:sys.exit(f'{sec}: scenes.py has no CAM_CAPS — nothing to click')
new=camcaps.click_cues(caps,also_last=also_last)
J=D/'sfx.json';cur=json.load(open(J)).get('sfx',[]) if J.exists() else []
keep=[c for c in cur if not str(c.get('why','')).startswith('camcap ')]
out=keep+[n for n in new if not any(k['file']==n['file'] and abs(k['t']-n['t'])<.04 for k in keep)]
out.sort(key=lambda r:r['t'])
print(f'{sec}: {len(new)} camcap clicks ({len(out)-len(keep)} added, {len(cur)-len(keep)} old camcap cues replaced), {len(out)} cues total')
for r in out:print(f"  {r['t']:8.3f}  {r['file']:24s} {r.get('peak_db','')}  {r.get('why','')}")
if dry:sys.exit(0)
json.dump({'sfx':out},open(J,'w'),indent=1);print(f'wrote {J} — now run: python3 lib/mix_section.py sections/{sec}')
