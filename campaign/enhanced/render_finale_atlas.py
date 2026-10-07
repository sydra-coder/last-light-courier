"""Render compact source-map contact sheets for visual review of levels 1901-2000."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--preview',type=Path,default=root/'design/campaign-2000-preview/index.html')
parser.add_argument('--output-dir',type=Path,default=root/'campaign/enhanced/finale-visual-audit')
args=parser.parse_args()
html=args.preview
line=next(line for line in html.open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])[1900:]
proofs=json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[900:]
assert len(levels)==len(proofs)==100
out=args.output_dir
out.mkdir(parents=True,exist_ok=True)
font=ImageFont.load_default()
tile=8
panel=210
for page in range(4):
    image=Image.new('RGB',(panel*5,panel*5),'#171e2d')
    draw=ImageDraw.Draw(image)
    for index in range(25):
        level=levels[page*25+index]
        proof=proofs[page*25+index]
        assert level['n']==proof['level']
        x0=(index%5)*panel+18
        y0=(index//5)*panel+33
        grid=level['grid']
        walls=set(level['walls'])
        for y in range(grid):
            for x in range(grid):
                fill='#121a28' if f'{x},{y}' in walls else '#40506a'
                draw.rectangle((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),fill=fill)
        route=[step['p'] for step in proof['route']]
        for a,b in zip(route,route[1:]):
            draw.line((x0+a[0]*tile+tile//2,y0+a[1]*tile+tile//2,x0+b[0]*tile+tile//2,y0+b[1]*tile+tile//2),fill='#77d6d0',width=2)
        for home in level['homes']:
            x,y=home['p']
            draw.ellipse((x0+x*tile+1,y0+y*tile+1,x0+x*tile+tile-2,y0+y*tile+tile-2),fill='#ffc276')
        for loop in (level.get('patrol'),level.get('patrol2')):
            if loop:
                for x,y in loop:
                    draw.rectangle((x0+x*tile+2,y0+y*tile+2,x0+x*tile+tile-3,y0+y*tile+tile-3),fill='#ef6f80')
        x,y=level['depot']
        draw.ellipse((x0+x*tile,y0+y*tile,x0+x*tile+tile-1,y0+y*tile+tile-1),fill='#fff5d2',outline='#ba833e')
        px=(index%5)*panel+11
        py=(index//5)*panel+10
        draw.text((px,py),f"{level['n']}  {level.get('masteryArchetype','')}  {len(route)-1} steps",font=font,fill='#f6e5c7')
    target=out/f'levels_{1901+page*25}_{1925+page*25}.png'
    image.save(target)
    print(target)
