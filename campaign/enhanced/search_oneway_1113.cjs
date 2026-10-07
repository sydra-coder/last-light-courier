// Stage a one-way entry that preserves Level 1113's route and rejects direct tours.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=__dirname,n=1113;
const proof=JSON.parse(fs.readFileSync(path.join(root,'road-events-v1/post_event_routes.json'),'utf8'))[n-1001];
const reference=proof.route.map(x=>x.p);
const variants=['ENWS','WSEN','NESW','SWNE'].map(order=>{
  const rows=JSON.parse(fs.readFileSync(path.join(root,`multi-band-variants-v1/reroute-v3-1101-${order}.json`),'utf8')).rows;
  return {order,route:rows[n-1101].staticCandidateRoute};
});
const level=api.LEVELS[n-1],oldTile=level.oneWayTile,oldFrom=level.oneWayFrom;
const key=p=>p.join(',');
const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
  level.authoredEvent?.tile,level.repair?.tile].filter(Boolean).map(key));
function replay(route){api.choose(n);api.begin();const l=api.getLevel();if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,step:route.length-1,light:s.light};
}
const options=[];
for(let i=1;i<reference.length;i++){
  const p=reference[i],from=reference[i-1];
  if(protectedTiles.has(key(p))||reference.findIndex(tile=>key(tile)===key(p))!==i)continue;
  level.oneWayTile=p;level.oneWayFrom=from;
  const safe=replay(reference);
  if(!safe.done)continue;
  const attempts=variants.map(v=>({order:v.order,...replay(v.route)}));
  const blocked=attempts.filter(x=>!x.done).length;
  if(blocked)options.push({tile:p,from,blocked,attempts});
}
level.oneWayTile=oldTile;level.oneWayFrom=oldFrom;
options.sort((a,b)=>b.blocked-a.blocked||a.attempts.reduce((v,x)=>v+x.step,0)-b.attempts.reduce((v,x)=>v+x.step,0));
fs.writeFileSync(path.join(root,'multi-band-variants-v1/oneway-1113-candidates.json'),JSON.stringify(options,null,2));
console.log('one-way options',options.length,'best',options[0]&&{tile:options[0].tile,from:options[0].from,blocked:options[0].blocked});
