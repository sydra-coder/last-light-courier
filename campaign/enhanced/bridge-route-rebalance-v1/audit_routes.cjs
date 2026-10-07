const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const changes=JSON.parse(fs.readFileSync(path.join(__dirname,'revisions.json')));
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'route_overrides.json')));
const rows=[];
for(const change of changes){
  const n=change.level,route=routes[n];
  api.choose(n);api.begin();let blocked=null,bridgeUsed=false;
  for(let i=1;i<route.length;i++){
    const state=api.getState();
    if(state.active&&!state.bridgeBuilt){if(!api.useBridge()){blocked={step:i,reason:'bridge unavailable'};break}bridgeUsed=true;}
    if(!api.move(route[i])){blocked={step:i,reason:api.getState().reason||'move rejected'};break;}
  }
  const state=api.getState();
  rows.push({level:n,bridgeUsed,blocked,done:state.done,failed:state.failed,steps:state.turns,light:state.light});
}
fs.writeFileSync(path.join(__dirname,'full-rule-replay.json'),JSON.stringify(rows,null,2));
const failures=rows.filter(x=>!x.bridgeUsed||x.blocked||!x.done||x.failed||x.light!==12);
console.log(JSON.stringify({tested:rows.length,passed:rows.length-failures.length,failures}));
if(failures.length)process.exitCode=1;
