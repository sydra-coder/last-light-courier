const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const secondMode=process.argv.includes('--second');
const candidates=JSON.parse(fs.readFileSync(process.env.LLC_FIELD_REROUTE_INPUT||path.join(__dirname,secondMode?'shadow-field-second-reroute-candidates.json':'shadow-field-reroute-candidates.json'),'utf8'));
const proofs=new Map(['quakes-v1/post_event_routes.json','road-events-v1/post_event_routes.json']
  .flatMap(file=>JSON.parse(fs.readFileSync(path.join(__dirname,file),'utf8'))).map(item=>[item.level,item]));
const results=[];
function replay(n,route){api.choose(n);api.begin();const l=api.getLevel();if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return {done:false,failedAt:i};
  const s=api.getState();return {done:s.done&&!s.failed,finishLight:s.light};
}
for(const entry of candidates){
  const l=api.LEVELS[entry.level-1],sentinelMode=process.env.LLC_FIELD_REROUTE_MODE==='sentinel';
  const old=sentinelMode?l.sentinelCenter:l.shadowInfluence2x2;
  if(sentinelMode)l.sentinelCenter=entry.field.origin;
  else l.shadowInfluence2x2={trigger:entry.field.triggerCount===2?'second_delivery':'first_delivery',triggerCount:entry.field.triggerCount||1,origin:entry.field.origin,cells:entry.field.cells};
  const ref=proofs.get(entry.level).route.map(s=>s.p);
  const reference=replay(entry.level,ref);
  const direct=entry.route?replay(entry.level,entry.route):{done:false,failedAt:0};
  results.push({level:entry.level,origin:entry.field.origin,staticSteps:entry.staticSteps,
    referenceDone:reference.done,staticTourDone:direct.done,blockedAt:direct.failedAt||null});
  if(sentinelMode)l.sentinelCenter=old;else l.shadowInfluence2x2=old;
}
fs.writeFileSync(process.env.LLC_FIELD_REROUTE_OUTPUT||path.join(__dirname,secondMode?'shadow-field-second-reroute-audit.json':'shadow-field-reroute-audit.json'),JSON.stringify(results,null,2));
for(const n of process.env.LLC_FIELD_REROUTE_TARGETS?process.env.LLC_FIELD_REROUTE_TARGETS.split(',').map(Number):secondMode?[974]:[943,953,960,974,982]){
  const rows=results.filter(r=>r.level===n);
  console.log(n,'reference',rows.every(r=>r.referenceDone),'static reroute rejected',rows.filter(r=>!r.staticTourDone).length+'/'+rows.length,
    'first',rows.find(r=>!r.staticTourDone)||null);
}
