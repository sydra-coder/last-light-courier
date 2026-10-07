const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=__dirname;
const plan=JSON.parse(fs.readFileSync(path.join(dir,'salient-event-batch-plan.json'))).rows;
const defaults=JSON.parse(fs.readFileSync(path.join(dir,'reference-hints-v1/normalized_routes.json')));
const signals=JSON.parse(fs.readFileSync(path.join(dir,'reference-hints-v1/normalized_signal_routes.json')));
function replay(n,route,signal,tile){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired)api.buyFreeRepair();
  if(signal&&!api.signal())return {done:false,reason:'signal unavailable'};
  let eventChecked=false;
  for(let i=1;i<route.length;i++){
    if(!api.move(route[i].slice(0,2)))return {done:false,reason:`move ${i} rejected`};
    if(!eventChecked&&api.getState().eventTriggered){
      eventChecked=true;
      if(!signal&&api.isOpen(tile))return {done:false,reason:'new road did not close'};
    }
  }
  const end=api.getState();return {done:eventChecked&&end.done&&!end.failed,steps:end.turns,finishLight:end.light};
}
const rows=[];
for(const item of plan){
  if(!item.candidates.length){rows.push({level:item.level,selected:null,reason:'no static candidate'});continue}
  const n=item.level,level=api.LEVELS[n-1],event=level.authoredEvent;
  const old=event.tile,oldDefault=level.phaseChoice?.defaultClose;
  let selected=null,attempted=0;
  for(const candidate of item.candidates){
    event.tile=candidate.tile;
    if(level.phaseChoice)level.phaseChoice.defaultClose=candidate.tile;
    const normal=replay(n,defaults[n-201],false,candidate.tile);attempted++;
    if(!normal.done)continue;
    const signal=level.phaseChoice?replay(n,signals[n],true,candidate.tile):null;
    if(signal&&!signal.done)continue;
    selected={tile:candidate.tile,affectedTargets:candidate.affectedTargets,
      maxIncrease:candidate.maxIncrease,defaultSteps:normal.steps,defaultFinishLight:normal.finishLight,
      signalSteps:signal?.steps,signalFinishLight:signal?.finishLight};
    break;
  }
  event.tile=old;if(level.phaseChoice)level.phaseChoice.defaultClose=oldDefault;
  rows.push({level:n,oldTile:old,attempted,selected});
}
fs.writeFileSync(path.join(dir,'salient-event-batch-runtime.json'),JSON.stringify({rows},null,2));
console.log(JSON.stringify({weak:rows.length,selected:rows.filter(r=>r.selected).length,
  none:rows.filter(r=>!r.selected).length,selectedLevels:rows.filter(r=>r.selected).map(r=>r.level)}));
