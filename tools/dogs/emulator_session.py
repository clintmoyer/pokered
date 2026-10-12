#!/usr/bin/env python3
"""Headless emulator driver for developer playthroughs; JSON lines on stdin."""
from pathlib import Path
import json, re, shutil, sys
from pyboy import PyBoy
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
QA=ROOT/'build/qa'; QA.mkdir(parents=True,exist_ok=True)
shutil.copyfile(ROOT/'pokered.gbc',QA/'session.gb')
symbols={}
for line in (ROOT/'pokered.sym').read_text().splitlines():
    m=re.match(r'([0-9a-fA-F]+):([0-9a-fA-F]+) (\S+)',line)
    if m: symbols[m[3]]=(int(m[1],16),int(m[2],16))
chars={}
for c,v in re.findall(r'^\s*charmap "([^"\n]+)",\s*\$([0-9a-fA-F]+)',(ROOT/'constants/charmap.asm').read_text(),re.M):
    chars.setdefault(int(v,16),c)
gb=PyBoy(str(QA/'session.gb'),window='null',sound_emulated=False)
gb.set_emulation_speed(0)
def read(name): return gb.memory[symbols[name][1]]
def snapshot(name='screen'):
    gb.tick(1)
    gb.screen.image.resize((640,576),Image.Resampling.NEAREST).save(QA/(name+'.png'))
    start=symbols['wTileMap'][1]
    rows=[''.join(chars.get(gb.memory[start+y*20+x],' ') for x in range(20)) for y in range(18)]
    return dict(map=read('wCurMap'),x=read('wXCoord'),y=read('wYCoord'),battle=read('wIsInBattle'),party=read('wPartyCount'),text=rows)
print(json.dumps({'ready':True}),flush=True)
try:
    for line in sys.stdin:
        command=json.loads(line)
        if 'buttons' in command:
            for button in command['buttons'].split(): gb.button_press(button)
            gb.tick(command.get('hold',8))
            for button in command['buttons'].split(): gb.button_release(button)
        gb.tick(command.get('frames',60))
        if 'set' in command:
            for name,value in command['set'].items():
                address=symbols[name][1]
                if isinstance(value,list): gb.memory[address:address+len(value)] = value
                else: gb.memory[address] = value
        if 'save_state' in command:
            with (QA/command['save_state']).open('wb') as f: gb.save_state(f)
        if 'load_state' in command:
            with (QA/command['load_state']).open('rb') as f: gb.load_state(f)
        if 'read' in command:
            print(json.dumps({name:read(name) for name in command['read']}),flush=True)
        print(json.dumps(snapshot(command.get('name','screen'))),flush=True)
        if command.get('quit'): break
finally:
    gb.stop()
