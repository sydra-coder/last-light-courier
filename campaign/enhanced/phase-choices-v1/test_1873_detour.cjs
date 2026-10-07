const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=path.resolve(__dirname,'..');
const route=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_routes.json')))[1873-201].map(x=>x.slice(0,2));
const start=[20,18],target=[20,21],blocked='20,19';
const paths=[];
function enumerate(p,steps,seen){
  if(steps.length>12)return;
  if(p[0]===target[0]&&p[1]===target[1]){paths.push(steps);return}
  for(const q of [[p[0]-1,p[1]],[p[0]+1,p[1]],[p[0],p[1]-1],[p[0],p[1]+1]]){
    const k=q.join(',');if(q[0]<17||q[0]>21||q[1]<17||q[1]>21||k===blocked||seen.has(k))continue;
    enumerate(q,[...steps,q],new Set([...seen,k]));
  }
}
enumerate(start,[],new Set([start.join(',')]));
paths.sort((a,b)=>a.length-b.length);
let record=null;
for(const tail of paths){
  const amended=[...route.slice(0,80),...tail];
  api.choose(1873);api.begin();if(!api.signal())throw Error('Signal unavailable');
  let success=true;
  for(let i=1;i<amended.length;i++)if(!api.move(amended[i])){success=false;break}
  const end=api.getState();
  if(success&&end.done&&!end.failed){record={level:1873,signal:true,steps:end.turns,finishLight:end.light,route:amended};break}
}
if(!record)throw Error(`${paths.length} local detours tested without a completion`);
fs.writeFileSync(path.join(__dirname,'signal_1873_detour.json'),JSON.stringify(record,null,2));
console.log(JSON.stringify({steps:record.steps,finishLight:record.finishLight}));
