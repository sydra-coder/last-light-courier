(function(root){
 const levels=root.SHADOW_LEVELS||(typeof require!=='undefined'?require('./levels.js'):[]);
 const eq=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
 const tile=(l,p)=>l.map[p[1]]?.[p[0]]||'#';
 const find=(l,c)=>{for(let y=0;y<l.map.length;y++){let x=l.map[y].indexOf(c);if(x>=0)return[x,y]}return null};
 const clone=s=>JSON.parse(JSON.stringify(s));
 function create(id){const l=levels[id-1];if(!l)throw Error('Unknown shadow level');return{id,pos:find(l,'D'),light:l.light,turn:0,delivered:false,lampVisited:false,lampLit:false,drained:false,shadow:[...l.start],sealed:false,spawned:false,used:false,done:false,failed:false,message:l.brief}}
 function threat(s){const l=levels[s.id-1];if(s.id===1)return [s.shadow];if(s.id===2)return [s.shadow];if(s.id===3)return [[4,3]];if(s.id===4)return s.spawned?[[4,3]]:[];if(s.id===5)return s.turn>=4&&s.turn<=6?[[4,3]]:[[4,1],[4,5]];return []}
 function danger(s,p){if(s.id===3||s.id===5&&s.turn>=4&&s.turn<=6)return Math.abs(p[0]-4)<=1&&Math.abs(p[1]-3)<=1;return threat(s).some(t=>eq(t,p))}
 function nextHunter(s){const [x,y]=s.shadow,[px,py]=s.pos,candidates=[];if(py!==y)candidates.push([x,y+Math.sign(py-y)]);if(px!==x)candidates.push([x+Math.sign(px-x),y]);return candidates.find(p=>tile(levels[0],p)!=='#')||s.shadow}
 function nextLeech(turn){const route=[[4,1],[4,2],[4,1],[4,2],[4,1],[4,2],[4,3],[4,2],[4,1],[4,2]];return route[Math.min(turn,route.length-1)]}
 function actions(s){if(s.done||s.failed)return[];const l=levels[s.id-1],a=[];for(const[dx,dy,dir]of[[0,-1,'up'],[-1,0,'left'],[1,0,'right'],[0,1,'down']]){const p=[s.pos[0]+dx,s.pos[1]+dy];if(tile(l,p)!=='#')a.push({type:'move',p,dir})}a.push({type:'wait'});if(s.id===4&&!s.sealed&&Math.abs(s.pos[0]-4)+Math.abs(s.pos[1]-1)<=1)a.push({type:'seal'});return a}
 function advance(s,a){const legal=actions(s).some(x=>x.type===a.type&&(a.type!=='move'||eq(x.p,a.p)));if(!legal)return s;let z=clone(s),l=levels[s.id-1];z.turn++;z.light--;
  if(a.type==='move')z.pos=[...a.p];
  if(a.type==='seal'){z.sealed=true;z.spawned=false;z.used=true;z.message='Nest sealed. The minion disappears and no new shadow will spawn.'}
  if(s.id===1){if(z.turn%2===0)z.shadow=nextHunter(z);if(danger(z,z.pos)){z.failed=true;z.message='The Hunter caught the courier.'}}
  if(s.id===2){z.shadow=nextLeech(z.turn);if(z.turn===6&&z.lampLit){z.lampLit=false;z.drained=true;z.message='The Leech extinguished the recharge house. Delivery credit remains.'}if(danger(z,z.pos)){z.failed=true;z.message='The Leech caught the courier.'}}
  if(s.id===3&&danger(z,z.pos)){z.failed=true;z.message='The Sentinel influence caught the courier.'}
  if(s.id===4){if(z.turn>=5&&!z.sealed)z.spawned=true;if(danger(z,z.pos)){z.failed=true;z.message='The spawned shadow blocked the courier.'}else if(z.turn===5&&!z.sealed)z.message='A small shadow spawned on the center road.'}
  if(s.id===5){if(danger(z,z.pos)){z.failed=true;z.message='The merged shadow caught the courier.'}else if(z.turn===4)z.message='Two shadows merged; the center is dangerous until turn seven.';else if(z.turn===7)z.message='The shadow split back into two smaller forms.'}
  if(tile(l,z.pos)==='L'&&!z.failed){if(!z.lampVisited){z.lampVisited=true;z.lampLit=true;z.light=Math.min(l.light,z.light+4);z.message='Recharge house lit; four light restored.'}else if(!z.lampLit){z.lampLit=true;z.used=true;z.message='Recharge house relit; delivery credit was never lost.'}}
  if(tile(l,z.pos)==='H'&&!z.delivered&&!z.failed){z.delivered=true;z.light=Math.min(l.light,z.light+2);z.message=s.id===2&&z.drained?'House delivered, but the Leech extinguished the recharge house. Relight it on return.':'House delivered. Return to the depot.'}
  if(z.light<0){z.failed=true;z.message='The lantern ran out.'}
  const complete=z.delivered&&(s.id!==2||z.lampLit&&z.drained)&&(s.id!==4||z.sealed);
  if(tile(l,z.pos)==='D'&&complete&&!z.failed){z.done=true;z.message=`${l.name} sample complete.`}
  return z
 }
 function status(s){const l=levels[s.id-1],next=clone(s);next.turn++;if(s.id===1&&next.turn%2===0)next.shadow=nextHunter(next);if(s.id===2)next.shadow=nextLeech(next.turn);if(s.id===4&&next.turn>=5&&!next.sealed)next.spawned=true;return{level:l,threats:threat(s),nextThreats:threat(next),phase:s.id===5?(s.turn<4?`Merge in ${4-s.turn} moves`:s.turn<=6?`Merged until turn 7`:'Split apart'):null}}
 root.SHADOW_LAB={levels,create,actions,advance,status,tile,eq,danger};if(typeof module!=='undefined')module.exports=root.SHADOW_LAB;
})(typeof window!=='undefined'?window:globalThis);
