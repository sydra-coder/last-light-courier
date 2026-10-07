const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const revisions=JSON.parse(fs.readFileSync(path.join(__dirname,'revisions.json')));
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'route_overrides.json')));
const rows=[];
for(const item of revisions){
  const n=item.level,route=routes[n];
  api.choose(n);api.begin();let blocked=null;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked={step:i,tile:route[i]};break}
  const end=api.getState();
  rows.push({level:n,blocked,done:end.done,failed:end.failed,steps:end.turns,light:end.light,quakeTriggered:end.quakeTriggered,aftershockRequired:!!api.getLevel().aftershock,aftershockStarted:end.aftershockStart!==null});
}
fs.writeFileSync(path.join(__dirname,'full-rule-replay.json'),JSON.stringify(rows,null,2));
const failures=rows.filter(x=>x.blocked||!x.done||x.failed||!x.quakeTriggered||(x.aftershockRequired&&!x.aftershockStarted)||x.light!==12);
console.log(JSON.stringify({tested:rows.length,passed:rows.length-failures.length,failures}));
if(failures.length)process.exitCode=1;
