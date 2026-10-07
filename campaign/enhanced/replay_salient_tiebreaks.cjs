const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const here=__dirname,dir=path.join(here,'salient-tiebreaks');
const rows=[],targets=(process.env.LLC_TIEBREAK_LEVELS||'1485,1698').split(',').map(Number);
for(const n of targets){
  const seen=new Set();
  for(const file of fs.readdirSync(dir).filter(x=>x.startsWith(`${n}-`)&&x.endsWith('.json'))){
    const data=JSON.parse(fs.readFileSync(path.join(dir,file))).rows[0];
    const route=data.staticCandidateRoute,key=JSON.stringify(route);
    if(seen.has(key))continue;seen.add(key);
    api.choose(n);api.begin();let blocked=null;
    for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked={step:i,tile:route[i]};break}
    const state=api.getState();
    rows.push({level:n,source:file,bound:data.eventAwareSteps,completed:!blocked&&state.done&&!state.failed,
      blocked,steps:state.turns,finishLight:state.light,route});
  }
}
fs.writeFileSync(path.join(here,process.env.LLC_TIEBREAK_OUTPUT||'salient-tiebreak-replay.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify({tested:rows.length,completed:rows.filter(x=>x.completed).map(({level,source,steps,finishLight})=>({level,source,steps,finishLight})),
  closestFailures:targets.map(n=>({level:n,latestBlock:Math.max(...rows.filter(x=>x.level===n).map(x=>x.blocked?.step||0))}))}));
