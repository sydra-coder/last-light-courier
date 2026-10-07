const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../design/map-solutions-1000.json'),'utf8')).levels[700].solutions[0].route;
const points=proof.map(s=>s.p),bridge=[16,11];
const entry=points.findIndex(p=>p[0]===bridge[0]&&p[1]===bridge[1]);
if(entry<1)throw Error('Bridge absent from archived route');
points.splice(entry+1,0,[16,12],[17,12]);
function run(buildBridge,phase=api.LEVELS[700].phase,phase2=api.LEVELS[700].phase2){
  api.LEVELS[700].phase=phase;api.LEVELS[700].phase2=phase2;
  api.choose(701);api.begin();api.buyFreeRepair();
  let failure=null;
  for(let i=1;i<points.length;i++){
    if(buildBridge&&api.getState().active&&!api.getState().bridgeBuilt)api.useBridge();
    if(!api.move(points[i])){const s=api.getState();failure={step:i,pos:points[i],reason:s.reason,light:s.light};break;}
  }
  const s=api.getState();return {completed:s.done&&!s.failed,steps:s.turns,light:s.light,mask:s.mask,bridgeBuilt:s.bridgeBuilt,failure};
}
const attempts=[];
for(let phase=0;phase<4;phase++)for(let phase2=0;phase2<4;phase2++)attempts.push({phase,phase2,...run(true,phase,phase2)});
console.log(JSON.stringify({withBridge:attempts.filter(a=>a.completed),bestFailures:attempts.sort((a,b)=>b.steps-a.steps).slice(0,4),withoutBridge:run(false)},null,2));
