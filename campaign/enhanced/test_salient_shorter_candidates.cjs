const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=__dirname,rows=[];
for(const n of [1483,1485,1610,1698]){
  const source=JSON.parse(fs.readFileSync(path.join(dir,`salient-cert-default-${n}.json`))).rows[0];
  const route=source.staticCandidateRoute;
  api.choose(n);api.begin();let blocked=null;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked={step:i,tile:route[i],reason:api.getState().reason};break}
  const end=api.getState();
  rows.push({level:n,lowerBound:source.eventAwareSteps,completed:!blocked&&end.done&&!end.failed,
    blocked,steps:end.turns,finishLight:end.light,route});
}
fs.writeFileSync(path.join(dir,'salient-shorter-candidate-replay.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows.map(({level,lowerBound,completed,blocked,steps,finishLight})=>({level,lowerBound,completed,blocked,steps,finishLight}))));
