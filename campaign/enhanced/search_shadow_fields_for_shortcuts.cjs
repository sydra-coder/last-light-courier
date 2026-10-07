// Test existing 2x2 post-delivery shadow fields against the five proven fast routes.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const auditPath=process.env.LLC_SHORTCUT_AUDIT_PATH||path.join(__dirname,'static-shortcut-audit-901-1000.json');
const direct=JSON.parse(fs.readFileSync(auditPath,'utf8')).rows;
const proofs=new Map(['quakes-v1/post_event_routes.json','road-events-v1/post_event_routes.json']
  .flatMap(file=>JSON.parse(fs.readFileSync(path.join(__dirname,file),'utf8'))).map(item=>[item.level,item]));
const secondMode=process.argv.includes('--second');
const targets=process.env.LLC_SHORTCUT_TARGETS?process.env.LLC_SHORTCUT_TARGETS.split(',').map(Number):secondMode?[974]:[943,953,960,974,982],results=[];
const key=p=>p.join(',');
function replay(n,points){api.choose(n);api.begin();const level=api.getLevel();if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,step:null,light:s.light};
}
for(const n of targets){
  const level=api.LEVELS[n-1],old=level.shadowInfluence2x2,reference=proofs.get(n).route.map(s=>s.p),shortcut=direct.find(row=>row.level===n)?.staticCandidateRoute;
  if(!shortcut)throw Error(`No static shortcut route for level ${n}`);
  const triggerCount=Number(process.env.LLC_FIELD_TRIGGER_COUNT||(secondMode?2:1)),houseKeys=new Set(level.homes.map(h=>key(h.p))),seenHomes=new Set();
  let triggerStep=-1;
  for(let i=1;i<shortcut.length;i++){
    if(houseKeys.has(key(shortcut[i])))seenHomes.add(key(shortcut[i]));
    if(seenHomes.size>=triggerCount){triggerStep=i;break}
  }
  const after=new Set(shortcut.slice(triggerStep+1).map(key));
  const firstReference=proofs.get(n).route.findIndex(s=>s.mask.toString(2).replace(/0/g,'').length>=triggerCount);
  const ref=new Set(reference.slice(firstReference+1).map(key)),walls=new Set(level.walls);
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),...(level.quakeEvent?[level.quakeEvent.close,...level.quakeEvent.open]:[]),
    ...(level.authoredEvent?[level.authoredEvent.tile]:[]),
    ...(level.chainEvent?[level.chainEvent.close,...level.chainEvent.open]:[]),
    ...(level.aftershock?[level.aftershock.tile]:[])].map(key));
  const candidates=[];
  for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
    const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]],keys=cells.map(key);
    if(keys.some(k=>ref.has(k)||walls.has(k)||protectedTiles.has(k)))continue;
    const hits=keys.filter(k=>after.has(k)).length;if(!hits)continue;
    level.shadowInfluence2x2={trigger:['','first_delivery','second_delivery','third_delivery','fourth_delivery'][triggerCount]||'delivery',triggerCount,origin:[x,y],cells};
    const safe=replay(n,reference),blocked=safe.done?replay(n,shortcut):{done:true};
    if(safe.done&&!blocked.done)candidates.push({origin:[x,y],cells,triggerCount,hits,directBlockedAt:blocked.step});
  }
  level.shadowInfluence2x2=old;
  candidates.sort((a,b)=>b.hits-a.hits||a.directBlockedAt-b.directBlockedAt);
  results.push({level:n,viable:candidates.length,best:candidates[0]||null,top:candidates.slice(0,8)});
}
fs.writeFileSync(process.env.LLC_SHORTCUT_CANDIDATE_OUTPUT||path.join(__dirname,secondMode?'shadow-field-second-candidates.json':'shadow-field-shortcut-candidates.json'),JSON.stringify(results,null,2));
console.log(results.map(x=>({level:x.level,viable:x.viable,best:x.best&&{origin:x.best.origin,hits:x.best.hits,blockedAt:x.best.directBlockedAt}})));
