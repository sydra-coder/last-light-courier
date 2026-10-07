const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const here=__dirname;
const revisions=JSON.parse(fs.readFileSync(path.join(here,'revisions.json'))).filter(x=>x.level<=300);
const routes=JSON.parse(fs.readFileSync(path.join(here,'route_overrides.json')));
const delayed={217:9,265:15,289:11};
const results=[];
for(const row of revisions){
  const n=row.level,route=routes[n],useAfter=delayed[n]||0;
  api.choose(n);api.begin();let problem=null,used=false;
  if(useAfter===0){used=api.usePower('reveal_pulse');if(!used)problem='pulse unavailable at start';}
  for(let i=1;i<route.length&&!problem;i++){
    if(i===useAfter){used=api.usePower('reveal_pulse');if(!used){problem=`pulse unavailable before step ${i}`;break;}}
    if(!api.move(route[i])){problem=`blocked step ${i}`;break;}
  }
  const end=api.getState();
  if(!problem&&(!used||!end.beaconRevealed||!end.done||end.failed||end.light<12))problem='powered completion mismatch';
  results.push({level:n,useAfterStep:useAfter,completed:!problem,steps:end.turns,finishLight:end.light,problem});
}
fs.writeFileSync(path.join(here,'power-sample-replay.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify({tested:results.length,passed:results.filter(x=>x.completed).length,failures:results.filter(x=>!x.completed)}));
if(results.some(x=>!x.completed))process.exitCode=1;
