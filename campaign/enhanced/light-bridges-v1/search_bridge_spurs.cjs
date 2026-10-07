// Search two-cell, one-way bridge-house spurs while preserving the old route order.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const archive=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../design/map-solutions-1000.json'),'utf8')).levels;
const key=p=>p.join(',');
const same=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const neighbors=p=>[[p[0]+1,p[1]],[p[0]-1,p[1]],[p[0],p[1]+1],[p[0],p[1]-1]];
const inGrid=(p,n)=>p[0]>=0&&p[1]>=0&&p[0]<n&&p[1]<n;
function replay(n,points){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<points.length;i++){
    const state=api.getState();
    if(level.lightBridge&&state.active&&!state.bridgeBuilt&&!api.useBridge())return null;
    if(!api.move(points[i]))return null;
  }
  const state=api.getState();return state.done&&!state.failed?{steps:state.turns,light:state.light}:null;
}
function noBridgeReachable(level,goal){
  const blocked=new Set(level.walls);blocked.add(key(level.lightBridge));
  if(level.repair?.effect==='open')blocked.delete(key(level.repair.tile));
  const seen=new Set([key(level.depot)]),queue=[level.depot];
  for(let i=0;i<queue.length;i++)for(const p of neighbors(queue[i])){
    const k=key(p);
    if(!inGrid(p,level.grid)||blocked.has(k)||seen.has(k)||same(p,level.oneWayTile)&&!same(queue[i],level.oneWayFrom))continue;
    seen.add(k);queue.push(p);
  }
  return seen.has(key(goal));
}
const results=[];
for(let n=701;n<=800;n++){
  const original=api.LEVELS[n-1],proof=archive[n-1].solutions[0].route;
  const points=proof.map(s=>s.p),bridge=original.lightBridge;
  const entry=points.findIndex(p=>same(p,bridge));
  const v=points[entry+1],dx=v[0]-bridge[0],dy=v[1]-bridge[1];
  if(entry<1||Math.abs(dx)+Math.abs(dy)!==1)throw Error(`Bad bridge route ${n}`);
  const firstLater=proof.findIndex((s,i)=>i>entry&&s.mask!==proof[entry].mask);
  const changed=firstLater>=0?proof[firstLater].mask^proof[firstLater-1].mask:0;
  const houseIndex=Math.log2(changed);
  if(!Number.isInteger(houseIndex))throw Error(`No later house at ${n}`);
  const routeCells=new Set(points.map(key));
  const protectedCells=new Set([original.depot,...original.homes.map(h=>h.p),...original.patrol,...(original.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(k=>original[k]?[original[k]]:[]),...(original.repair?[original.repair.tile]:[])].map(key));
  let best=null,geometricOptions=0,directedOptions=0,successfulOptions=0;
  for(const sign of [1,-1]){
    const ox=dy*sign,oy=-dx*sign,u=[bridge[0]+ox,bridge[1]+oy],w=[v[0]+ox,v[1]+oy];
    if(!inGrid(u,original.grid)||!inGrid(w,original.grid)||routeCells.has(key(u))||routeCells.has(key(w))||protectedCells.has(key(u))||protectedCells.has(key(w)))continue;
    const seals=neighbors(u).filter(p=>!same(p,bridge)&&!same(p,w));
    if(seals.some(p=>routeCells.has(key(p))||protectedCells.has(key(p))))continue;
    geometricOptions++;
    const level=structuredClone(original);
    level.homes[houseIndex].p=u;
    level.walls=[...new Set([...level.walls,...seals.map(key)])].filter(k=>k!==key(u)&&k!==key(w));
    level.oneWayTile=w;level.oneWayFrom=u;
    if(noBridgeReachable(level,u))continue;
    directedOptions++;
    const amended=[...points.slice(0,entry+1),u,w,...points.slice(entry+1)];
    for(let phase=0;phase<4;phase++)for(let phase2=0;phase2<4;phase2++){
      level.phase=phase;level.phase2=phase2;
      api.LEVELS[n-1]=level;
      const finish=replay(n,amended);
      if(finish)successfulOptions++;
      if(finish&&(!best||finish.light>best.finishLight))best={level:n,houseIndex,houseFrom:original.homes[houseIndex].p,
        houseTo:u,oneWayTile:w,oneWayFrom:u,addedWalls:seals.map(key),openedCells:[u,w].filter(p=>original.walls.includes(key(p))).map(key),
        phase,phase2,finishSteps:finish.steps,finishLight:finish.light,route:amended};
    }
  }
  api.LEVELS[n-1]=original;
  results.push({level:n,found:!!best,geometricOptions,directedOptions,successfulOptions,best});
  if(n%10===0)console.log(n,'found',results.filter(r=>r.found).length);
}
const output=path.join(__dirname,'bridge_spur_search.json');
fs.writeFileSync(output,JSON.stringify({scope:'Staged powered route and directed no-bridge reachability screen; no live map mutation.',rows:results},null,2));
console.log('Found staged bridge-house spurs',results.filter(r=>r.found).length,'/100');
