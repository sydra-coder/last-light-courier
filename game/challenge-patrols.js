(() => {
  const same=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
  const key=p=>p.join(',');
  const dist=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
  function routes(level){const size=level.grid||8,walls=new Set(level.walls||[]),fixed=new Set(level.n===1800?[key(level.depot)]:[key(level.depot),...level.homes.map(h=>key(h.p))]),open=p=>p[0]>=0&&p[1]>=0&&p[0]<size&&p[1]<size&&!walls.has(key(p))&&!fixed.has(key(p));const result=[];
    for(let w=2;w<=5;w++)for(let h=2;h<=5;h++){const length=2*(w+h)-4;if(length<6||length>14)continue;for(let y=0;y<=size-h;y++)for(let x=0;x<=size-w;x++){const cycle=[];for(let dx=0;dx<w;dx++)cycle.push([x+dx,y]);for(let dy=1;dy<h;dy++)cycle.push([x+w-1,y+dy]);for(let dx=w-2;dx>=0;dx--)cycle.push([x+dx,y+h-1]);for(let dy=h-2;dy>=1;dy--)cycle.push([x,y+dy]);if(cycle.every(open))result.push(cycle)}}
    if(result.length)return result;
    const dirs=[[1,0],[-1,0],[0,1],[0,-1]];
    for(let y=0;y<size;y++)for(let x=0;x<size;x++){const start=[x,y];if(!open(start))continue;const stack=[[start]];while(stack.length){const path=stack.pop();if(path.length>=5){result.push([...path,...path.slice(1,-1).reverse()]);continue}const tail=path.at(-1);for(const d of dirs){const p=[tail[0]+d[0],tail[1]+d[1]];if(open(p)&&!path.some(q=>same(p,q)))stack.push([...path,p])}}}
    return result;
  }
  function score(level,route,phase){const spine=level.spine||[],wake=level.n===1800?3:1;let seen=new Set(),first=-1;for(let i=1;i<spine.length;i++){const home=level.homes.findIndex(h=>same(h.p,spine[i]));if(home>=0)seen.add(home);if(seen.size>=wake){first=i;break}}if(first<0)return null;let clock=(phase+first-spine.findIndex((p,i)=>i>0&&level.homes.some(h=>same(h.p,p))))%route.length,impact=0,near=0;const existing=[...(level.patrol||[]),...(level.patrol2||[])];for(let i=first+1;i<spine.length;i++){const pos=spine[i-1],target=spine[i],a=route[clock],b=route[(clock+1)%route.length];if(same(target,a)||same(target,b))return null;for(const p of [[pos[0]+1,pos[1]],[pos[0]-1,pos[1]],[pos[0],pos[1]+1],[pos[0],pos[1]-1]])if(!same(p,target)&&(same(p,a)||same(p,b)))impact++;if(dist(pos,a)<=2||dist(pos,b)<=2)near++;clock=(clock+1)%route.length}const overlap=route.filter(p=>existing.some(q=>same(p,q))).length;return impact*5+near*.6+route.length*.3-overlap*2}
  function plan(level){const candidates=routes(level);let best=null;for(const route of candidates)for(let phase=0;phase<route.length;phase++){const value=score(level,route,phase);if(value===null)continue;if(!best||value>best.score)best={route,phase,score:value}}return best}
  function apply(levels){const report=[];for(const level of levels){if(level.n%20!==0&&level.n!==70)continue;const chosen=plan(level);if(chosen){level.patrol3=chosen.route;level.phase3=chosen.phase;level.patrol3Wake=level.n===1800?3:1;level.patrolChallenge=true;report.push({level:level.n,length:chosen.route.length,impact:Math.round(chosen.score)})}else report.push({level:level.n,length:0,impact:0})}return report}
  const api={apply,plan,score};if(typeof module!=='undefined')module.exports=api;else window.LLCChallenges=api;
})();
