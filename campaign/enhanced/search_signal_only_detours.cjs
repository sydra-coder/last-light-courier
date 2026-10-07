// Find short signaled detours through the road closed by the default choice.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=path.join(__dirname,'signal-route-rebalance-v1');
const routes=JSON.parse(fs.readFileSync(path.join(dir,'route_overrides.json')));
const hints=JSON.parse(fs.readFileSync(path.join(dir,'hints/normalized_routes.json')));
const key=p=>p.join(',');
function shortest(level,start,goal,forbidden,order){
  const walls=new Set(level.walls),closed=key(level.phaseChoice.alternateClose);
  const queue=[start],prev=new Map([[key(start),null]]),point=new Map([[key(start),start]]);
  const deltas={E:[1,0],W:[-1,0],S:[0,1],N:[0,-1]};
  for(let at=0;at<queue.length;at++){
    const here=queue[at],k=key(here);
    if(k===key(goal)){
      const route=[];let p=k;
      while(p!==null){route.push(point.get(p));p=prev.get(p)}
      return route.reverse();
    }
    for(const ch of order){
      const [dx,dy]=deltas[ch],next=[here[0]+dx,here[1]+dy],nk=key(next);
      if(next.some(v=>v<0||v>=level.grid)||walls.has(nk)||nk===closed||forbidden.has(nk)||prev.has(nk))continue;
      prev.set(nk,k);point.set(nk,next);queue.push(next);
    }
  }
  return null;
}
const results=[];
for(const n of [1805,1817]){
  const level=api.LEVELS[n-1],route=routes[n],marks=hints[n-201],via=level.authoredEvent.tile;
  const candidates=[];
  for(let i=1;i<route.length-3;i++)for(let j=i+1;j<Math.min(route.length-1,i+17);j++){
    const mask=marks[i][2];
    if(!mask||marks[j][2]!==mask)continue;
    if(Math.abs(route[i][0]-via[0])+Math.abs(route[i][1]-via[1])>8)continue;
    if(Math.abs(route[j][0]-via[0])+Math.abs(route[j][1]-via[1])>8)continue;
    const forbidden=new Set([key(level.depot)]);
    level.homes.forEach((h,index)=>{if(!(mask&(1<<index)))forbidden.add(key(h.p))});
    for(const order of ['EWSN','WENS','NESW','SWNE']){
      const a=shortest(level,route[i],via,forbidden,order);
      const b=shortest(level,via,route[j],forbidden,order);
      if(!a||!b)continue;
      const candidate=[...route.slice(0,i+1),...a.slice(1),...b.slice(1),...route.slice(j+1)];
      if(candidate.length-1>route.length+11||candidate.length-1<route.length)continue;
      api.choose(n);api.begin();if(!api.signal())throw Error(`Signal unavailable ${n}`);
      let blockedAt=null;
      for(let step=1;step<candidate.length;step++)if(!api.move(candidate[step])){blockedAt=step;break}
      const end=api.getState();
      if(blockedAt===null&&end.done&&!end.failed&&end.light>=1)
        candidates.push({level:n,route:candidate,steps:end.turns,finishLight:end.light,
          replaced:[i,j],via,order});
    }
  }
  const unique=[...new Map(candidates.map(c=>[c.route.map(key).join(';'),c])).values()];
  unique.sort((a,b)=>a.steps-b.steps||b.finishLight-a.finishLight);
  results.push({level:n,successful:unique.length,best:unique.slice(0,5)});
}
fs.writeFileSync(path.join(dir,'signal-only-detours.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results.map(x=>({level:x.level,successful:x.successful,best:x.best[0]&&{steps:x.best[0].steps,finishLight:x.best[0].finishLight,replaced:x.best[0].replaced,via:x.best[0].via}}))));
