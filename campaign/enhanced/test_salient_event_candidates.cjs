const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=__dirname;
const routes=JSON.parse(fs.readFileSync(path.join(dir,'reference-hints-v1/normalized_routes.json')));
const output=[];
for(const n of [1009,1035,1037]){
  const candidates=JSON.parse(fs.readFileSync(path.join(dir,`salient-event-${n}-candidates.json`))).candidates;
  const level=api.LEVELS[n-1],original=level.authoredEvent.tile;
  let selected=null;
  for(const candidate of candidates){
    level.authoredEvent.tile=candidate.tile;
    api.choose(n);api.begin();
    const route=routes[n-201];let first=false,okay=true;
    for(let i=1;i<route.length;i++){
      if(!api.move(route[i].slice(0,2))){okay=false;break}
      if(!first&&api.getState().mask){first=true;if(api.isOpen(candidate.tile))throw Error(`${n}: new road did not close`)}
    }
    const end=api.getState();
    if(okay&&end.done&&!end.failed){selected={level:n,oldTile:original,newTile:candidate.tile,
      affectedTargets:candidate.affectedTargets,maxIncrease:candidate.maxIncrease,steps:end.turns,finishLight:end.light};break}
  }
  level.authoredEvent.tile=original;
  output.push(selected||{level:n,failed:true});
}
fs.writeFileSync(path.join(dir,'salient-event-runtime-candidates.json'),JSON.stringify(output,null,2));
console.log(JSON.stringify(output));
