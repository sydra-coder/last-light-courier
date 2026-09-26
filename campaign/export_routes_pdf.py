from pathlib import Path
import json,math,argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader
parser=argparse.ArgumentParser();parser.add_argument('--catalog',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();data=json.loads(args.catalog.read_text(encoding='utf-8'));total=len(data['levels']);variants=sum(len(l['solutions']) for l in data['levels'])
pdfmetrics.registerFont(TTFont('Route',r'C:\Windows\Fonts\arial.ttf'));pdfmetrics.registerFont(TTFont('RouteBold',r'C:\Windows\Fonts\arialbd.ttf'));pdfmetrics.registerFontFamily('Route',normal='Route',bold='RouteBold',italic='Route',boldItalic='RouteBold')
W,H=landscape(A4);file=args.output;c=canvas.Canvas(str(file),pagesize=(W,H));c.setTitle(f'Last Light Courier - {total} maps - {variants} verified solution routes');page=0
style=ParagraphStyle('body',fontName='Route',fontSize=12,leading=19,textColor=HexColor('#26354c'))
def text(text,x,y,width):
 p=Paragraph(text,style);_,h=p.wrap(width,900);p.drawOn(c,x,y-h);return y-h-16
def header(title,subtitle):
 global page
 page+=1;c.setFillColor(HexColor('#f4f7fb'));c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(HexColor('#20324a'));c.setFont('RouteBold',21);c.drawString(32,H-44,title);c.setFont('Route',9);c.setFillColor(HexColor('#526278'));c.drawString(32,H-65,subtitle);c.setStrokeColor(HexColor('#cad5e2'));c.line(32,H-76,W-32,H-76);c.setFont('Route',8);c.drawString(32,19,'Verified movement rules | 26 September 2026 | Map and rules fingerprints stored in JSON');c.drawRightString(W-32,19,str(page))
header('Solution routes for every map',f'{total} maps | {variants} verified routes | {total} without repairs and {variants-total} with a purchased repair')
y=H-106
for t in [
'<b>What is stored:</b> one shortest legal completion route for each map, and one shortest route after its existing repair is purchased. Completion means lighting the required number of houses and returning to the depot; it does not necessarily require every house. These are valid reference solutions, not all possible ways of winning.',
'<b>How to read a route page:</b> numbered tiles and arrows show movement order. S marks the starting depot. A plus sign means the tile is visited more than once; use the move table for every visit. In the table, each entry is <b>move number / column,row / light remaining</b>. Coordinates start at 1. Move 0 is the starting state.',
'<b>Colors:</b> gray = rubble; blue = depot; gold = house; violet outline = patrol loop; green = switch; purple = gate; brown = fading crossing; cyan = ice; dark blue = dark street. Yellow move entries mark a newly lit house. Green entries mark the finish. For an open-road repair the upgraded tile has a green outline.',
'<b>State-aware hints:</b> a stored starting route is not sufficient after the player has moved differently. The solver calculates a new route from their actual position, remaining light, lit houses, patrol phases, Echo trail, crossing timers and purchased terrain. If there is no solution from that state, the hint must report it instead of pretending the starting route still works.',
'<b>Versioning:</b> the companion JSON stores map fingerprints, a rules fingerprint, each ordered tile and its light/shadow/timer state. Regenerate and validate this archive when a map or rule changes. Planned gems, tunnel tokens and repair-required maps are not yet in these layouts; those changes will require new archives and action-aware routes.'
]:y=text(t,32,y,W-64)
c.showPage()
for entry in data['levels']:
 l=entry['map'];size=l.get('grid',8)
 for v in entry['solutions']:
  repaired=v['repairPurchased'];route=v['route'];mode='Repair purchased' if repaired else 'No repair'
  header(f'Level {l["n"]} - {mode}',f'{size} x {size} | Required houses: {l["required"]} of {len(l["homes"])} | {v["steps"]} moves | Start light {route[0]["light"]} | Finish light {route[-1]["light"]}')
  side=330;tile=side/size;x0=46;y0=147
  walls=set(l['walls']);r=l['repair'];gap=tuple(r['tile']) if repaired and r and r['effect']=='open' else None
  if gap:walls.discard(','.join(map(str,gap)))
  homes={tuple(h['p']) for h in l['homes']};pat=set(map(tuple,l['patrol']+(l['patrol2'] or [])));features={tuple(l[f]):f for f in ['switch','gate','fade','ice','dark'] if l[f]};visits={}
  for i,s in enumerate(route):visits.setdefault(tuple(s['p']),[]).append(i)
  def center(p):return (x0+(p[0]+.5)*tile,y0+(size-p[1]-.5)*tile)
  for yy in range(size):
   for xx in range(size):
    p=(xx,yy);color='#d7dee7' if f'{xx},{yy}' in walls else '#ffffff';kind=features.get(p)
    if p in homes:color='#ffe1a3'
    if p==tuple(l['depot']):color='#a9d7e8'
    if kind:color={'switch':'#b6ddbf','gate':'#d4c2e5','fade':'#dfbc9b','ice':'#c0e8f0','dark':'#75879d'}[kind]
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor('#bfccd8'));c.setLineWidth(.4);c.rect(x0+xx*tile,y0+(size-1-yy)*tile,tile,tile,fill=1,stroke=1)
    if p in pat:c.setStrokeColor(HexColor('#a086bd'));c.setLineWidth(1);c.rect(x0+xx*tile+2,y0+(size-1-yy)*tile+2,tile-4,tile-4,fill=0,stroke=1)
    if gap==p:c.setStrokeColor(HexColor('#1c9b61'));c.setLineWidth(2);c.rect(x0+xx*tile+1,y0+(size-1-yy)*tile+1,tile-2,tile-2,fill=0,stroke=1)
  c.setStrokeColor(HexColor('#358d85'));c.setFillColor(HexColor('#358d85'));c.setLineWidth(1)
  for a,b in zip(route,route[1:]):
   ax,ay=center(a['p']);bx,by=center(b['p']);c.line(ax,ay,bx,by);mx=ax+(bx-ax)*.77;my=ay+(by-ay)*.77;angle=math.atan2(by-ay,bx-ax);d=min(3.5,tile*.16);p=c.beginPath();p.moveTo(mx,my);p.lineTo(mx-d*math.cos(angle-.6),my-d*math.sin(angle-.6));p.lineTo(mx-d*math.cos(angle+.6),my-d*math.sin(angle+.6));p.close();c.drawPath(p,fill=1,stroke=0)
  for p,ids in visits.items():
   cx,cy=center(p);label='S' if ids[0]==0 else str(ids[0])+('+' if len(ids)>1 else '');c.setFont('RouteBold',max(5.5,min(10,tile*.3)));width=pdfmetrics.stringWidth(label,'RouteBold',max(5.5,min(10,tile*.3)));c.setFillColor(white);c.rect(cx-width/2-1,cy-4,width+2,9,fill=1,stroke=0);c.setFillColor(HexColor('#16384c'));c.drawCentredString(cx,cy-2,label)
  c.setFont('Route',7);c.setFillColor(HexColor('#526278'))
  for i in range(size):c.drawCentredString(x0+(i+.5)*tile,y0+side+6,str(i+1));c.drawRightString(x0-5,y0+(size-i-.5)*tile-2,str(i+1))
  c.setFont('Route',9);c.drawString(x0,126,'Arrows = move order. Number+ = repeated visit.')
  c.drawString(x0,111,'Read the table for every move and remaining light.')
  if repaired:text('Upgrade: '+r['name']+' ('+r['effect']+').',x0,92,330)
  else:text('No purchase is needed for this reference solution.',x0,92,330)
  tx=409;top=489;col=96;cols=4;rowh=11.8
  c.setFont('RouteBold',10);c.setFillColor(HexColor('#20324a'));c.drawString(tx,503,'Move / column,row / light remaining')
  totalrows=math.ceil(len(route)/cols)
  assert top-totalrows*rowh>50,(l['n'],v['steps'])
  for i,s in enumerate(route):
   column=i//totalrows;row=i%totalrows;cx=tx+column*col;cy=top-row*rowh
   fresh=i>0 and s['mask']!=route[i-1]['mask'];finish=i==len(route)-1
   if fresh or finish:c.setFillColor(HexColor('#d5eadc' if finish else '#ffe9be'));c.rect(cx,cy-9,col-3,rowh-1,fill=1,stroke=0)
   c.setFillColor(HexColor('#20324a'));c.setFont('Route',8.2);c.drawString(cx+3,cy-7,f'{i:03d} / {s["p"][0]+1:02d},{s["p"][1]+1:02d} / {s["light"]}')
  c.showPage()
c.save();reader=PdfReader(str(file));assert len(reader.pages)==variants+1;print('Created route PDF:',len(reader.pages),'pages')
