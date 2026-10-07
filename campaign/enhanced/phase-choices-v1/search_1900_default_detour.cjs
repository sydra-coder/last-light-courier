const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=path.resolve(__dirname,'..');
const base=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_signal_routes.json')))[1900].map(s=>s.slice(0,2));
const start=base[81],target=base[83],closed=base[82].join(',');
const paths=[];
function walk(p,tail,seen){
  if(tail.length>12)return;
  if(p[0]===target[0]&&p[1]===target[1]){paths.push(tail);return}
  for(const q of [[p[0]-1,p[1]],[p[0]+1,p[1]],[p[0],p[1]-1],[p[0],p[1]+1]]){
    const k=q.join(',');if(q[0]<15||q[0]>20||q[1]<6||q[1]>14||k===closed||seen.has(k))continue;
    walk(q,[...tail,q],new Set([...seen,k]));
  }
}
walk(start,[],new Set([start.join(',')]));paths.sort((a,b)=>a.length-b.length);
let found=null,tested=0;
for(const tail of paths){
  const route=[...base.slice(0,82),...tail,...base.slice(84)];
  api.choose(1900);api.begin();api.buyFreeRepair();
  let okay=true;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){okay=false;break}
  tested++;
  const end=api.getState();
  if(okay&&end.done&&!end.failed){found={level:1900,route,steps:end.turns,finishLight:end.light,localDetour:tail,tested};break}
}
fs.writeFileSync(path.join(__dirname,'default_1900_search.json'),JSON.stringify({tested,candidates:paths.length,found},null,2));
console.log(JSON.stringify({tested,candidates:paths.length,found:found&&{steps:found.steps,finishLight:found.finishLight,detour:found.localDetour}}));
if(!found)process.exitCode=1;
