// Stage alternate quake-close tiles that block proven direct tours, preserving authored routes.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'static-shortcut-audit-901-1000.json'),'utf8'));
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
const targets=[943,953,960,974,982],results=[];
const key=p=>p.join(',');
function replay(n,points){api.choose(n);api.begin();const level=api.getLevel();if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return {done:false,failedAt:i};
  const s=api.getState();return {done:s.done&&!s.failed,finishLight:s.light,failedAt:null};
}
for(const n of targets){
  const level=api.LEVELS[n-1],original=level.quakeEvent.close,reference=proofs[n-801].route.map(s=>s.p),direct=source.rows[n-901].staticCandidateRoute;
  const first=direct.findIndex((p,i)=>i>0&&level.homes.some(h=>key(h.p)===key(p)));
  const refTiles=new Set(reference.map(key));
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),...level.quakeEvent.open,
    ...(level.aftershock?[level.aftershock.tile]:[])].map(key));
  const walls=new Set(level.walls),seen=new Set(),candidates=[];
  for(let i=first+1;i<direct.length-1;i++){
    const p=direct[i],k=key(p);if(seen.has(k)||refTiles.has(k)||protectedTiles.has(k)||walls.has(k))continue;seen.add(k);
    const degree=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dx,dy])=>{
      const x=p[0]+dx,y=p[1]+dy;return x>=0&&y>=0&&x<level.grid&&y<level.grid&&!walls.has(`${x},${y}`);
    }).length;
    level.quakeEvent.close=p;
    const a=replay(n,reference),b=a.done?replay(n,direct):{done:true};
    if(a.done&&!b.done)candidates.push({tile:p,directBlockedAt:b.failedAt,degree,referenceFinishLight:a.finishLight});
  }
  level.quakeEvent.close=original;
  candidates.sort((a,b)=>a.degree-b.degree||a.directBlockedAt-b.directBlockedAt);
  results.push({level:n,oldClose:original,firstDirectDelivery:first,viable:candidates.length,best:candidates[0]||null,top:candidates.slice(0,8)});
}
fs.writeFileSync(path.join(__dirname,'quake-shortcut-closure-candidates.json'),JSON.stringify(results,null,2));
console.log(results.map(r=>({level:r.level,viable:r.viable,best:r.best})));
