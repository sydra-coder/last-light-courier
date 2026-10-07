(function(root){
  const levels=typeof module!=='undefined'?require('./levels.js'):root.LAB_LEVELS;
  const key=(x,y)=>`${x},${y}`;
  const same=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
  const distance=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
  function setup(id){
    const level=levels[id-1];if(!level)throw Error('Unknown lab level '+id);
    const found={houses:[],features:{}};let depot=null,east=null;
    level.map.forEach((row,y)=>{if(row.length!==9)throw Error(`Level ${id} row ${y} width ${row.length}`);[...row].forEach((c,x)=>{if(c==='D')depot=[x,y];if(c==='E')east=[x,y];if(c==='H'||c==='h')found.houses.push({p:[x,y],hidden:c==='h'});if(!'.#DHEh'.includes(c))found.features[key(x,y)]=c})});
    if(!depot||!found.houses.length)throw Error('Missing depot or house '+id);
    return {level,depot,east,...found};
  }
  function create(id){const map=setup(id);return {id,pos:[...map.depot],turn:0,light:map.level.light,delivered:[],revealed:false,opened:null,bored:false,bridgeSpent:false,used:false,choice:null,switched:false,lureUntil:0,wardUntil:0,flareUntil:0,anchorUntil:0,anchorPhase:0,senseUntil:0,power:null,trapInventory:id===2?1:0,trapPlaced:null,shadowTrapped:false,trappedAt:null,done:false,failed:false,message:map.level.help}}
  function tile(map,p){return map.level.map[p[1]]?.[p[0]]||'#'}
  function phase(s,nextTurn){return s.anchorUntil>=nextTurn?s.anchorPhase:nextTurn}
  function shadowPos(map,s,turn=s.turn){if(s.shadowTrapped)return s.trappedAt;if(!map.level.shadows.length||s.flareUntil>0&&s.flareUntil>=turn)return null;if(s.lureUntil>0&&s.lureUntil>=turn)return [5,3];const path=s.switched&&map.level.altShadows?map.level.altShadows:map.level.shadows;return path[turn%path.length]}
  function passable(map,s,p,nextTurn,from){const c=tile(map,p),k=key(...p);if(c==='#')return false;if(c==='h'&&!s.revealed)return false;if(c==='U'&&!s.revealed)return false;if((c==='R'||c==='T')&&s.opened!==k)return false;if(c==='X'&&!s.bored)return false;if(c==='F'&&(phase(s,nextTurn)-1)%4>=2)return false;if(c==='Q'&&nextTurn<6)return false;if(c==='O'){const horizontal=p[1]===from[1];if(horizontal&&nextTurn%2!==0||!horizontal&&nextTurn%2===0)return false}if(c==='B'&&s.bridgeSpent)return false;return true}
  function possible(s){if(s.done||s.failed)return [];const map=setup(s.id),out=[];for(const [dx,dy,name] of [[1,0,'right'],[-1,0,'left'],[0,1,'down'],[0,-1,'up']]){const p=[s.pos[0]+dx,s.pos[1]+dy];if(passable(map,s,p,s.turn+1,s.pos))out.push({type:'move',dir:name,p})}out.push({type:'wait',label:'Wait 1 turn'});for(const [k,c] of Object.entries(map.features)){const p=k.split(',').map(Number);if(distance(s.pos,p)>1)continue;if(c==='Y'&&s.trapInventory>0)out.push({type:'use',target:k,label:'Lay shadow trap (1)'});if(c==='L'&&s.lureUntil<=s.turn)out.push({type:'use',target:k,label:'Ring bell'});if(c==='W'&&s.wardUntil<=s.turn)out.push({type:'use',target:k,label:'Light 3×3 ward'});if((c==='R'||c==='T')&&!s.opened)out.push({type:'use',target:k,label:c==='R'?'Repair upper bridge':'Repair lower bridge'});if(c==='X'&&!s.bored)out.push({type:'use',target:k,label:'Bore tunnel'});if(c==='V'&&!s.switched)out.push({type:'use',target:k,label:'Switch patrol route'})}if(s.id===16&&!s.power){for(const power of ['Flare','Anchor','Sense'])out.push({type:'power',power,label:`Use ${power}`})}return out}
  function advance(original,action){const map=setup(original.id),s={...original,pos:[...original.pos],delivered:[...original.delivered]};if(s.done||s.failed)return s;
    const allowed=possible(original);const valid=allowed.some(a=>a.type===action.type&&(a.type==='move'?same(a.p,action.p):a.type==='use'?a.target===action.target:a.type==='power'?a.power===action.power:true));if(!valid){s.message='That move or action is not available now.';return s}
    const oldPos=[...s.pos];const nextTurn=s.turn+1;let cost=1,msg='';
    if(action.type==='move'){
      s.pos=[...action.p];const c=tile(map,s.pos),k=key(...s.pos);
      if(tile(map,oldPos)==='B'&&!same(oldPos,s.pos))s.bridgeSpent=true;
      if(c==='Y'&&s.trapPlaced===k&&!s.shadowTrapped)msg='You stepped onto your laid trap. Move away before the shadow arrives.';
      if(c==='F'){if(s.id!==16)s.used=true;msg='You crossed the ford while the water was low.'}
      if(c==='G'){cost=action.p[0]<oldPos[0]?3:1;if(cost===3){s.used=true;msg='You pushed west against the gust: 3 light spent.'}else msg='The wind carried you along for 1 light.'}
      if(c==='Q'){s.used=true;msg='The quake opened a new route.'}
      if(c==='O'){s.used=true;msg='You entered the junction on the open axis.'}
      if(c==='N'&&nextTurn>=5){cost=2;s.used=true;msg='Nightfall doubled the cost of this dark street.'}
      if(c==='B'){s.used=true;msg='Crossed the fragile bridge. It will close when you leave.'}
      if(c==='E'){s.used=true;msg='East depot reached.'}
    }else if(action.type==='wait'){msg='You waited one turn and spent one light.'}
    else if(action.type==='use'){
      const p=action.target.split(',').map(Number),c=tile(map,p);
      if(c==='Y'){s.trapPlaced=action.target;s.trapInventory=0;msg='Trap laid from inventory. Watch the patrol approach the marked tile.'}
      if(c==='L'){s.lureUntil=nextTurn+6;s.used=true;msg='The bell lured the patrol away for six turns.'}
      if(c==='W'){s.wardUntil=nextTurn+6;s.used=true;msg='A 3×3 ward glows for six turns.'}
      if(c==='R'||c==='T'){s.opened=action.target;s.choice=c;s.used=true;msg=`${c==='R'?'Upper':'Lower'} bridge repaired. The other crossing stays closed.`}
      if(c==='X'){s.bored=true;s.used=true;msg='Rubble cleared. A tunnel now connects the streets.'}
      if(c==='V'){s.switched=true;s.used=true;msg='The patrol changed to the lower circuit.'}
    }else if(action.type==='power'){
      s.power=action.power;s.used=true;
      if(action.power==='Flare'){s.flareUntil=nextTurn+4;msg='Flare banished the shadow for four turns.'}
      if(action.power==='Anchor'){s.anchorUntil=nextTurn+4;s.anchorPhase=nextTurn;msg='Anchor holds the flood clock for four turns.'}
      if(action.power==='Sense'){s.senseUntil=nextTurn+4;msg='Sense shows the next four patrol positions.'}
    }
    s.turn=nextTurn;s.light-=cost;
    if(s.id===2&&s.trapPlaced&&!s.shadowTrapped&&same(shadowPos(map,s),s.trapPlaced.split(',').map(Number))){s.shadowTrapped=true;s.trappedAt=s.trapPlaced.split(',').map(Number);s.used=true;msg='Shadow caught! It is frozen on the trap tile and cannot move again this run.'}
    if(!s.failed&&action.type==='move'){
      const hi=map.houses.findIndex(h=>same(h.p,s.pos));if(hi>=0&&!s.delivered.includes(hi)){const prerequisite=s.id===2?s.shadowTrapped:s.id===3?s.lureUntil>=s.turn:s.id===4?s.wardUntil>=s.turn:s.id===13?s.bridgeSpent||s.used:s.id===14?s.switched:s.id===16?!!s.power:true;if(!prerequisite){msg='This house needs the trial mechanic first. Check the guide and try again.'}else{s.delivered.push(hi);s.light=Math.min(map.level.light,s.light+2);msg=`House ${hi+1} lit. Two light restored. ${msg}`;if(s.id===1&&hi===0){s.revealed=true;s.used=true;msg='House 1 lit → east gate OPEN. This is a shortcut to House 2; the south road was always open.'}if(s.id===5&&hi===0){s.revealed=true;s.used=true;msg+=' A second house appeared.'}}}
    }
    const wardCenter=Object.entries(map.features).find(([,c])=>c==='W')?.[0].split(',').map(Number);const inWard=s.wardUntil>0&&s.wardUntil>=s.turn&&wardCenter&&Math.max(Math.abs(s.pos[0]-wardCenter[0]),Math.abs(s.pos[1]-wardCenter[1]))<=1;
    if(!s.failed&&same(s.pos,shadowPos(map,s))&&!inWard){s.failed=true;msg='The shadow caught the courier. Retry or change its timing.'}
    if(!s.failed&&s.light<0){s.failed=true;msg='The lantern ran out of light.'}
    const atBank=same(s.pos,map.depot)||map.east&&same(s.pos,map.east);const allDelivered=s.delivered.length===map.houses.length;
    if(!s.failed&&atBank&&allDelivered){if(s.id===15&&!same(s.pos,map.east))msg='Deliveries banked at the old depot. This trial asks you to test the east depot.';else if(!map.level.requiredUse||s.used){s.done=true;msg=`Trial complete! ${s.id===15?'You chose the alternate depot.':'The mechanic changed the route.'}`}else msg='Deliveries complete. Try the highlighted mechanic before banking.'}
    s.message=msg||'Move, wait, or use the highlighted action.';return s
  }
  function status(s){const map=setup(s.id),t=s.turn;return {name:map.level.name,rule:map.level.rule,houses:`${s.delivered.length}/${map.houses.length}`,shadow:shadowPos(map,s),nextShadow:shadowPos(map,s,t+1),floodOpen:(phase(s,t+1)-1)%4<2,trapInventory:s.trapInventory,trapPlaced:s.trapPlaced,shadowTrapped:s.shadowTrapped,quakeOpen:t+1>=6,rotationHorizontal:(t+1)%2===0,nightfall:t>=5,ward:s.wardUntil>0&&s.wardUntil>=t,used:s.used,bank:map.east}}
  const api={levels,setup,create,possible,advance,status,tile,shadowPos,key};root.LAB=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
