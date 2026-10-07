// Try short movement delays around blocked steps of a different house-order tour.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'early-order-301-310-static.json'))).rows.find(x=>x.level===301);
const initial=source.staticCandidateRoute;
const queue=[{route:initial,extra:0}],seen=new Set([JSON.stringify(initial)]),results=[];
let found=null,tested=0;
while(queue.length&&tested<3000){
  const item=queue.shift();tested++;
  api.choose(301);api.begin();let blocked=null;
  for(let i=1;i<item.route.length;i++)if(!api.move(item.route[i])){blocked=i;break}
  const state=api.getState();
  if(blocked===null&&state.done&&!state.failed){found={route:item.route,steps:state.turns,finishLight:state.light,extra:item.extra};break}
  if(blocked===null||item.extra>=16)continue;
  const current=state.pos,desired=item.route[blocked];
  results.push({extra:item.extra,blocked,position:current,desired});
  for(const side of [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]){
    if(side[0]===desired[0]&&side[1]===desired[1]||!api.isOpen(side))continue;
    const route=[...item.route.slice(0,blocked),side,[...current],...item.route.slice(blocked)];
    const key=JSON.stringify(route);if(seen.has(key))continue;seen.add(key);
    queue.push({route,extra:item.extra+2});
  }
}
const output={level:301,staticSteps:initial.length-1,tested,queued:queue.length,found,
  failureSamples:results.slice(0,20)};
fs.writeFileSync(path.join(__dirname,'early-order-301-dynamic-search.json'),JSON.stringify(output,null,2));
console.log(JSON.stringify({tested,queued:queue.length,found:found&&{steps:found.steps,finishLight:found.finishLight,extra:found.extra},
  sample:results.slice(0,3)}));
