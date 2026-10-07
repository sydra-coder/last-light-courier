(function(root){
 const levels=root.POWER_LEVELS||(typeof require!=='undefined'?require('./levels.js'):[]);
 const key=p=>p.join(',');
 const equal=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
 const find=(l,c)=>{for(let y=0;y<l.map.length;y++){const x=l.map[y].indexOf(c);if(x>=0)return [x,y]}return null};
 const tile=(l,p)=>l.map[p[1]]?.[p[0]]||'#';
 const copy=s=>JSON.parse(JSON.stringify(s));
 function create(id){const l=levels[id-1];if(!l)throw Error('Unknown sample');return {id,pos:find(l,'D'),light:l.light,cap:l.light+6,turn:0,delivered:false,used:false,charge:1,shadow:l.shadow?l.shadow[0]:null,trap:false,trapped:false,lure:0,freeze:0,revealed:false,bridge:0,repaired:false,stable:false,quake:false,history:null,done:false,failed:false,message:l.brief}}
 function level(s){return levels[s.id-1]}
 function canEnter(s,p,nextTurn){const c=tile(level(s),p);if(c==='#')return false;if(c==='R'&&!s.revealed||c==='B'&&s.bridge<nextTurn||c==='P'&&!s.repaired||c==='Q'&&nextTurn>=4&&!s.stable)return false;return true}
 function actions(s){if(s.done)return [];const l=level(s),a=[];if(s.charge&&(!s.failed||l.power==='Rewind'))a.push({type:'power',label:l.power});if(s.failed)return a;
  for(const [dx,dy,dir] of [[0,-1,'up'],[-1,0,'left'],[1,0,'right'],[0,1,'down']]){const p=[s.pos[0]+dx,s.pos[1]+dy];if(canEnter(s,p,s.turn+1))a.push({type:'move',p,dir})}
  a.push({type:'wait',label:'Wait'});return a}
 function advance(s,a){const l=level(s);if(!actions(s).some(x=>x.type===a.type&&(a.type!=='move'||equal(x.p,a.p))))return s;let z=copy(s);z.history=null;
  if(a.type==='power'){
    if(l.power==='Rewind'){
      if(!s.history){z.message='Make one move first, then rewind it.';return z}
      z={...copy(s.history),charge:0,used:true,history:null,message:'Last move undone; light and shadow state restored.'};return z
    }
    z.charge=0;z.used=true;
    if(l.power==='Anchor Trap'){z.trap=true;z.message='Trap laid on the marked tile. Let the shadow enter it.'}
    if(l.power==='Decoy Light'){z.lure=4;z.message='Decoy lit for four turns. The shadow will move toward it.'}
    if(l.power==='Reveal Pulse'){z.revealed=true;z.message='Hidden crossing revealed and opened.'}
    if(l.power==='Lumen Flask'){z.light=Math.min(z.cap,z.light+6);z.message='Lantern restored by up to six light.'}
    if(l.power==='Freeze Seal'){z.freeze=4;z.message='Shadow frozen for four turns.'}
    if(l.power==='Light Bridge'){z.bridge=z.turn+14;z.message='Bridge formed for fourteen moves.'}
    if(l.power==='Road Repair'){z.repaired=true;z.message='Broken road repaired for this run.'}
    if(l.power==='Map Stabilizer'){z.stable=true;z.message='Quake cancelled; center road stays open.'}
    return z;
  }
  z.history=copy({...s,history:null});z.turn++;
  if(a.type==='move')z.pos=[...a.p];
  z.light--;
  if(l.shadow){
    if(z.trapped){/* remains fixed */}
    else if(z.freeze>0){z.freeze--}
    else if(z.lure>0){const dest=find(l,'C'),p=[...z.shadow];if(p[0]!==dest[0])p[0]+=Math.sign(dest[0]-p[0]);else if(p[1]!==dest[1])p[1]+=Math.sign(dest[1]-p[1]);z.shadow=p;z.lure--}
    else z.shadow=[...l.shadow[z.turn%l.shadow.length]];
    if(z.trap&&equal(z.shadow,find(l,'T'))){z.trapped=true;z.message='Shadow caught. It cannot move for the rest of this run.'}
    if(equal(z.pos,z.shadow)){z.failed=true;z.message='The shadow caught you. Rewind if available, or retry.'}
  }
  if(l.power==='Map Stabilizer'&&z.turn>=4&&!z.stable){z.quake=true;z.message='Quake! The center road has closed.'}
  if(tile(l,z.pos)==='H'&&!z.delivered){z.delivered=true;z.light=Math.min(z.cap,z.light+2);z.message='House lit. Return to the depot.'}
  if(z.light<0){z.failed=true;z.message='The lantern ran out.'}
  if(z.delivered&&tile(l,z.pos)==='D'&&z.used&&!z.failed){z.done=true;z.message=`Sample complete: ${l.power} changed the route.`}
  else if(z.delivered&&tile(l,z.pos)==='D'&&!z.used&&!z.failed)z.message='Delivery complete. Use the sample power before finishing this test.';
  return z;
 }
 function status(s){const l=level(s);return {level:l,shadow:s.shadow,trapTarget:find(l,'T'),nextShadow:l.shadow&&!s.trapped&&!s.freeze&&!s.lure?l.shadow[(s.turn+1)%l.shadow.length]:null,bridgeLeft:Math.max(0,s.bridge-s.turn),quakeIn:s.stable?null:Math.max(0,4-s.turn)}}
 root.POWER_LAB={levels,create,actions,advance,status,tile,find,equal};
 if(typeof module!=='undefined')module.exports=root.POWER_LAB;
})(typeof window!=='undefined'?window:globalThis);
