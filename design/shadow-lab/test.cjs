const lab=require('./engine.js');
const fs=require('node:fs');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const inline=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).filter(Boolean);
if(inline.length!==1)throw Error('Expected one inline UI script');new Function(inline[0]);
const sig=s=>JSON.stringify([s.id,s.pos,s.light,s.turn,s.delivered,s.lampVisited,s.lampLit,s.drained,s.shadow,s.sealed,s.spawned,s.used,s.failed]);
for(let id=1;id<=5;id++){
 const start=lab.create(id),q=[[start,[]]],seen=new Set([sig(start)]);let win=null;
 for(let h=0;h<q.length;h++){const[s,path]=q[h];if(s.done){win=path;break}if(s.failed||s.turn>35||q.length>180000)continue;
  for(const a of lab.actions(s)){const z=lab.advance(s,a),k=sig(z);if(seen.has(k))continue;seen.add(k);q.push([z,[...path,a.dir||a.type]])}}
 if(!win)throw Error(`${lab.levels[id-1].name} unsolved after ${seen.size} states`);
 console.log(`${id} ${lab.levels[id-1].name}: ${win.length} actions, ${seen.size} states; ${win.join(' ')}`);
}
