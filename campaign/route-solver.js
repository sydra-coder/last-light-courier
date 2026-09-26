// Pure movement solver shared by route archives and future state-aware hints.
const ROUTE_SOLVER=(()=>{
  const eq=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1],key=p=>p.join(','),count=m=>{let n=0;while(m){n+=m&1;m>>>=1}return n};
  function solve(level,current=null,options={}){
    const bought=!!options.repaired,repair=level.repair,capacity=level.cap+(bought&&repair?.effect==='beacon'?3:0),walls=new Set(level.walls);
    if(bought&&repair?.effect==='open')walls.delete(key(repair.tile));
    const start=current?{...current,pos:[...current.pos],trail:(current.trail||[]).slice(-2)}:{pos:level.depot,mask:0,light:capacity,phase:level.phase,phase2:level.phase2,active:false,fade:null,ice:null,gate:0,trail:[]};
    if(start.failed)return {status:'restart_needed',reason:start.reason||'Run ended',route:null};
    if(start.done)return {status:count(start.mask)>=level.required?'complete':'restart_needed',route:[]};
    const queue=[{...start,steps:0,parent:-1}],seen=new Map();let head=0;
    const signature=s=>[key(s.pos),s.mask,s.phase,s.phase2,s.fade,s.ice,s.gate,...s.trail.map(key)].join('|');
    seen.set(signature(start),start.light);
    function blocked(p,s){if(!s.active)return false;for(const [patrol,phase] of [[level.patrol,s.phase],[level.patrol2,s.phase2]])if(patrol&&(eq(p,patrol[phase])||eq(p,patrol[(phase+1)%patrol.length])))return true;return !!(level.echo&&s.trail.some(q=>eq(q,p)))}
    function hasExit(s){const [x,y]=s.pos,size=level.grid||8;return [[x+1,y],[x-1,y],[x,y+1],[x,y-1]].some(p=>p[0]>=0&&p[1]>=0&&p[0]<size&&p[1]<size&&!walls.has(key(p))&&!(eq(p,level.fade)&&s.fade===0)&&!(eq(p,level.ice)&&s.ice===0)&&!(eq(p,level.gate)&&s.gate<=0&&!(bought&&repair?.effect==='latch'))&&!blocked(p,s))}
    while(head<queue.length){
      const parent=head,s=queue[head++];
      if(s.steps&&(options.goal==='nextHouse'?s.mask!==start.mask&&hasExit(s):eq(s.pos,level.depot)&&count(s.mask)>=level.required)){
        const route=[];let index=parent;while(index>=0){const item=queue[index];route.push({p:item.pos,light:item.light,mask:item.mask,phase:item.phase,phase2:item.phase2,fade:item.fade,ice:item.ice,gate:item.gate,active:item.active,trail:item.trail});index=item.parent}
        route.reverse();return {status:'solved',steps:s.steps,route,explored:head};
      }
      const [x,y]=s.pos;
      for(const p of [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]){
        const size=level.grid||8;
        if(p[0]<0||p[1]<0||p[0]>=size||p[1]>=size||walls.has(key(p))||eq(p,level.fade)&&s.fade===0||eq(p,level.ice)&&s.ice===0||eq(p,level.gate)&&s.gate<=0&&!(bought&&repair?.effect==='latch')||blocked(p,s))continue;
        const hi=level.homes.findIndex(h=>eq(h.p,p)),bit=hi<0?0:1<<hi,fresh=!!bit&&!(s.mask&bit),mask=s.mask|bit,home=eq(p,level.depot)&&mask;
        // Returning to the depot ends the actual run, so partial banking cannot be traversed.
        if(home&&(options.goal==='nextHouse'||count(mask)<level.required))continue;
        const light=Math.min(capacity,s.light-(eq(p,level.dark)&&!(bought&&repair?.effect==='lamp')?2:1)+(fresh?2:0));
        if(light<=0&&!fresh&&!home)continue;
        const next={pos:p,mask,light,active:s.active||fresh,phase:s.active?(s.phase+1)%level.patrol.length:s.phase,phase2:s.active&&level.patrol2?(s.phase2+1)%level.patrol2.length:s.phase2,
          fade:eq(p,level.fade)&&s.fade===null?5:s.fade===null?null:Math.max(0,s.fade-1),ice:eq(p,level.ice)&&s.ice===null?4:s.ice===null?null:Math.max(0,s.ice-1),gate:eq(p,level.switch)?4:Math.max(0,s.gate-1),trail:level.echo?[...s.trail.slice(-1),s.pos]:[],steps:s.steps+1,parent};
        const id=signature(next);if((seen.get(id)??-Infinity)>=next.light)continue;seen.set(id,next.light);queue.push(next);
      }
    }
    return {status:'no_solution',reason:'No completion fits the remaining light, shadows and crossing timers.',route:null,explored:head};
  }
  return {solve};
})();
if(typeof module!=='undefined')module.exports=ROUTE_SOLVER;
