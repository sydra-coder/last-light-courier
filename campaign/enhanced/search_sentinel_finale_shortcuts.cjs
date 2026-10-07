// Screen staged 3x3 Sentinel placements against proven finale shortcuts.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const direct=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'static-shortcut-audit-1901-2000.json'),'utf8')).rows.map(r=>[r.level,r]));
const proofs=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8')).map(r=>[r.level,r]));
const targets=[1905,1910,1916,1926],key=p=>p.join(','),results=[];
function replay(n,points){api.choose(n);api.begin();const l=api.getLevel();if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,light:s.light};
}
for(const n of targets){
  const level=api.LEVELS[n-1],old=level.sentinelCenter;
  const record=proofs.get(n),reference=record.route.map(s=>s.p),shortcut=direct.get(n).staticCandidateRoute;
  const refAfter=new Set(record.route.filter(s=>s.mask>0).map(s=>key(s.p)));
  const shortcutAfter=new Set(shortcut.slice(shortcut.findIndex(p=>level.homes.some(h=>key(h.p)===key(p)))+1).map(key));
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),level.authoredEvent.tile,level.chainEvent.close,...level.chainEvent.open].map(key));
  const walls=new Set(level.walls),candidates=[];
  for(let y=1;y<level.grid-1;y++)for(let x=1;x<level.grid-1;x++){
    const cells=[];for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++)cells.push([x+dx,y+dy]);
    const keys=cells.map(key);
    if(walls.has(key([x,y]))||keys.some(k=>refAfter.has(k)||protectedTiles.has(k)))continue;
    const hits=keys.filter(k=>shortcutAfter.has(k)).length;if(!hits)continue;
    level.sentinelCenter=[x,y];
    const safe=replay(n,reference),blocked=safe.done?replay(n,shortcut):{done:true};
    if(safe.done&&!blocked.done)candidates.push({origin:[x,y],cells,hits,directBlockedAt:blocked.step});
  }
  level.sentinelCenter=old;
  candidates.sort((a,b)=>b.hits-a.hits||a.directBlockedAt-b.directBlockedAt);
  results.push({level:n,viable:candidates.length,best:candidates[0]||null,top:candidates.slice(0,12)});
}
const output=path.join(__dirname,'shadow-fields-late-v1/finale-sentinel-candidates.json');
fs.writeFileSync(output,JSON.stringify(results,null,2));
console.log(results.map(r=>({level:r.level,viable:r.viable,best:r.best&&r.best.origin})));
