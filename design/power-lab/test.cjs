const lab=require('./engine.js');
const fs=require('node:fs');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const inline=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(Boolean);
if(inline.length!==1)throw Error('Expected one inline UI script');
new Function(inline[0]);
function signature(s){const h=s.history;return JSON.stringify([s.id,s.pos,s.light,s.turn,s.delivered,s.used,s.charge,s.shadow,s.trap,s.trapped,s.lure,s.freeze,s.revealed,s.bridge,s.repaired,s.stable,s.quake,s.done,s.failed,h&&[h.pos,h.light,h.turn,h.shadow,h.delivered]])}
function solve(start){
 const q=[[start,[]]],seen=new Set([signature(start)]);let found=null;
 for(let head=0;head<q.length;head++){
  const [s,route]=q[head];if(s.done){found=route;break}
  if(route.length>34||q.length>150000)continue;
  for(const a of lab.actions(s)){
   const t=lab.advance(s,a),k=signature(t);if(seen.has(k))continue;seen.add(k);
   q.push([t,[...route,a.type==='move'?a.dir:a.type]]);
  }
 }
 return {found,states:seen.size};
}
for(let id=1;id<=9;id++){
 const start=lab.create(id),{found,states}=solve(start);
 if(!found)throw Error(`Sample ${id} has no completed route; explored ${states}`);
 const noPower=lab.create(id);noPower.used=true;noPower.charge=0;
 const baseline=solve(noPower).found;
 console.log(`${id} ${lab.levels[id-1].power}: ${found.length} actions, ${states} states; no-power ${baseline?'SOLVABLE':'blocked'}; ${found.join(' ')}`);
}
