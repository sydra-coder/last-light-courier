"""Render source-map atlas for the 1001–1900 shortcut street candidates."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'campaign/enhanced'
parser=argparse.ArgumentParser()
parser.add_argument('--preview',type=Path,default=BASE/'late-shortcut-streets-v1/candidate_index_v3.html')
parser.add_argument('--targets',type=Path,default=BASE/'late-shortcut-streets-v1/candidate_walls.json')
parser.add_argument('--output-dir',type=Path,default=BASE/'late-shortcut-streets-v1/atlas')
args=parser.parse_args()
preview=args.preview
line=next(x for x in preview.open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs={p['level']:p for p in json.loads((BASE/'road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))}
targets=sorted(map(int,json.loads(args.targets.read_text(encoding='utf-8'))))
out=args.output_dir
out.mkdir(parents=True,exist_ok=True)
font=ImageFont.load_default();tile=8;panel=210
for page in range((len(targets)+24)//25):
    group=targets[page*25:(page+1)*25]
    image=Image.new('RGB',(panel*5,panel*5),'#171e2d');draw=ImageDraw.Draw(image)
    for index,n in enumerate(group):
        level=levels[n-1];route=[step['p'] for step in proofs[n]['route']]
        x0=(index%5)*panel+18;y0=(index//5)*panel+33
        walls=set(level['walls'])
        for y in range(level['grid']):
            for x in range(level['grid']):
                draw.rectangle((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),
                               fill='#121a28' if f'{x},{y}' in walls else '#40506a')
        for a,b in zip(route,route[1:]):
            draw.line((x0+a[0]*tile+tile//2,y0+a[1]*tile+tile//2,
                       x0+b[0]*tile+tile//2,y0+b[1]*tile+tile//2),fill='#77d6d0',width=2)
        for house in level['homes']:
            x,y=house['p'];draw.ellipse((x0+x*tile+1,y0+y*tile+1,x0+x*tile+tile-2,y0+y*tile+tile-2),fill='#ffc276')
        x,y=level['depot'];draw.ellipse((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),fill='#fff5d2')
        draw.text(((index%5)*panel+11,(index//5)*panel+10),f'{n}  {len(route)-1} steps',font=font,fill='#f6e5c7')
    target=out/f'candidate_shortcuts_{page+1}.png';image.save(target);print(target)
