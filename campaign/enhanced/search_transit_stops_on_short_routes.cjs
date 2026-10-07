// Search same-delivery-phase stop pairs on the staged short walking routes.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=path.join(__dirname,'transit-walk-rebalance-v1');
const routes=JSON.parse(fs.readFileSync(path.join(dir,'route_overrides.json')));
const hints=JSON.parse(fs.readFileSync(path.join(dir,'hints/normalized_routes.json')));
const output=[];
for(const n of [1763,1799]){
  const level=api.LEVELS[n-1],oldStops=level.transitLink.stops,route=routes[n],marks=hints[n-201];
  const candidates=[];
  for(let i=1;i<route.length-5;i++)for(let j=i+5;j<route.length-1;j++){
    if(!marks[i][2]||marks[i][2]!==marks[j][2]||route[i].join()===route[j].join())continue;
    level.transitLink.stops=[route[i],route[j]];
    api.choose(n);api.begin();
    let blockedAt=null;
    for(let k=1;k<=i;k++)if(!api.move(route[k])){blockedAt=k;break}
    if(blockedAt===null&&!api.move(route[j]))blockedAt=j;
    if(blockedAt===null)for(let k=j+1;k<route.length;k++)if(!api.move(route[k])){blockedAt=k;break}
    const end=api.getState();
    if(blockedAt===null&&end.done&&!end.failed)
      candidates.push({level:n,boardAtStep:i,exitAtOldStep:j,stops:[route[i],route[j]],
        steps:end.turns,finishLight:end.light,walkingSteps:route.length-1});
  }
  level.transitLink.stops=oldStops;
  candidates.sort((a,b)=>a.steps-b.steps||b.finishLight-a.finishLight);
  output.push({level:n,tested:candidates.length,best:candidates.slice(0,10)});
}
fs.writeFileSync(path.join(dir,'new-stop-search.json'),JSON.stringify(output,null,2));
console.log(JSON.stringify(output.map(x=>({level:x.level,successfulPairs:x.tested,best:x.best[0]||null}))));
