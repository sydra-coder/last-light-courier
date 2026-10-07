// Exploratory local-wall search for five proven straight shortcut maps.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const staticAudit=JSON.parse(fs.readFileSync(path.join(__dirname,'static-shortcut-audit-901-1000.json'),'utf8'));
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
const targets=[943,953,960,974,982],results=[];
const key=p=>p.join(','),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
function pathBetween(level,walls,start,goal,neighbors){
  const q=[start],seen=new Set([key(start)]),parents=new Map();
  for(let head=0;head<q.length;head++){
    const p=q[head];if(eq(p,goal)){
      const route=[p];while(!eq(route.at(-1),start))route.push(parents.get(key(route.at(-1))));
      return route.reverse();
    }
    for(const [dx,dy] of neighbors){
      const next=[p[0]+dx,p[1]+dy],k=key(next);
      if(next[0]<0||next[1]<0||next[0]>=level.grid||next[1]>=level.grid||walls.has(k)||seen.has(k)||eq(next,level.depot)&&!eq(next,goal))continue;
      seen.add(k);parents.set(k,p);q.push(next);
    }
  }
  return null;
}
function longest(points){let best=0,run=0,previous='';for(let i=1;i<points.length;i++){
  const d=`${points[i][0]-points[i-1][0]},${points[i][1]-points[i-1][1]}`;
  run=d===previous?run+1:1;best=Math.max(best,run);previous=d;
}return best}
const orders=[[[1,0],[-1,0],[0,1],[0,-1]],[[-1,0],[1,0],[0,-1],[0,1]],[[0,1],[0,-1],[1,0],[-1,0]],[[0,-1],[0,1],[-1,0],[1,0]]];
for(const n of targets){
  const level=api.LEVELS[n-1],originalWalls=level.walls,proof=proofs[n-801],reference=proof.route.map(s=>s.p);
  const staticRoute=staticAudit.rows[n-901].staticCandidateRoute;
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),level.quakeEvent.close,...level.quakeEvent.open,
    ...(level.aftershock?[level.aftershock.tile]:[])].map(key));
  let found=null,attempts=0;
  const seen=new Set();
  const directions=staticRoute.slice(1).map((p,i)=>[p[0]-staticRoute[i][0],p[1]-staticRoute[i][1]].join(','));
  const priority=[];let runStart=0;
  for(let i=1;i<=directions.length;i++){
    if(i<directions.length&&directions[i]===directions[runStart])continue;
    if(i-runStart>12)for(let j=runStart+1;j<i;j++)priority.push({index:j,distance:Math.abs(j-(runStart+i)/2)});
    runStart=i;
  }
  const indices=[...priority.sort((a,b)=>a.distance-b.distance).map(x=>x.index),...Array.from({length:staticRoute.length-2},(_,i)=>i+1)];
  for(const i of indices){
    if(found)break;
    const tile=staticRoute[i],tileKey=key(tile);
    if(seen.has(tileKey)||protectedTiles.has(tileKey)||originalWalls.includes(tileKey))continue;
    seen.add(tileKey);
    const walls=new Set([...originalWalls,tileKey]);
    for(const order of orders){
      const points=[reference[0]];let possible=true;
      for(let j=1;j<reference.length-1;j++){
        if(!eq(reference[j],tile)){points.push(reference[j]);continue}
        const detour=pathBetween(level,walls,reference[j-1],reference[j+1],order);
        if(!detour||detour.length>8){possible=false;break}
        points.push(...detour.slice(1,-1));
      }
      if(!possible)continue;
      points.push(reference.at(-1));
      if(longest(points)>12)continue;
      attempts++;
      level.walls=[...originalWalls,tileKey];api.choose(n);api.begin();
      if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
      let blocked=null;
      for(let j=1;j<points.length;j++)if(!api.move(points[j])){blocked=j;break}
      const end=api.getState();
      if(blocked===null&&end.done&&!end.failed){found={level:n,wall:tileKey,steps:end.turns,finishLight:end.light,longestStraight:longest(points),points};break}
    }
  }
  level.walls=originalWalls;
  results.push(found||{level:n,found:false,attempts});
}
fs.writeFileSync(path.join(__dirname,'anti-shortcut-detour-candidates.json'),JSON.stringify(results,null,2));
console.log(results.map(x=>({level:x.level,wall:x.wall||null,steps:x.steps||null,attempts:x.attempts||null})));
