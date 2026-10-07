(function(root){
 const base=['#########','#.......#','#.......#','#D.....H#','#.......#','#.......#','#########'];
 const crossing=['#########','#.......#','#.#####.#','#D..X..H#','#.#####.#','#.......#','#########'];
 const levels=[
  {id:1,n:111,power:'Anchor Trap',light:10,map:['#########','#.......#','#...T...#','#D.....H#','#.......#','#.......#','#########'],shadow:[[4,3],[4,2],[4,2],[4,3]],target:'T',brief:'Place a trap on the marked tile. The patrol enters it on turn one and stays there, clearing an exact-light route.',tip:'Lay the trap before your first move. It catches the shadow off the main road.'},
  {id:2,n:131,power:'Decoy Light',light:10,map:['#########','#...C...#','#.......#','#D.....H#','#.......#','#.......#','#########'],shadow:[[4,3],[4,2],[4,2],[4,3]],target:'C',brief:'Set a false light above the road. The shadow moves toward it for four turns, clearing an exact-light crossing.',tip:'Deploy the decoy before crossing the middle of the road.'},
  {id:3,n:211,power:'Reveal Pulse',light:13,map:crossing.map(r=>r.replace('X','R')),target:'R',brief:'A hidden crossing lies under the mist. Reveal Pulse exposes it and opens the short route.',tip:'Use Reveal Pulse, cross R, light the house and return.'},
  {id:4,n:311,power:'Lumen Flask',light:8,map:base,brief:'The direct delivery and return take twelve moves. The flask restores six light, up to the lantern cap.',tip:'Walk toward the house, then drink the flask when you have room for all six light.'},
  {id:5,n:411,power:'Road Repair',light:14,map:crossing.map(r=>r.replace('X','P')),target:'P',brief:'Repair the broken center road permanently for this run. It opens a safe direct return.',tip:'Repair P, then use the new road to deliver and return.'},
  {id:6,n:511,power:'Freeze Seal',light:10,map:base,shadow:[[4,3],[4,2],[4,2],[4,3]],brief:'Freeze the moving shadow for four turns. Timing the seal off the road preserves an exact-light route.',tip:'Move right once, then freeze the shadow while it is above the road.'},
  {id:7,n:711,power:'Light Bridge',light:14,map:crossing.map(r=>r.replace('X','B')),target:'B',brief:'Create a bridge over the gap. It lasts fourteen moves, enough for a careful round trip.',tip:'Activate the bridge before entering B. Cross back before its timer ends.'},
  {id:8,n:811,power:'Map Stabilizer',light:10,map:crossing.map(r=>r.replace('X','Q')),target:'Q',brief:'A quake closes the center road after turn four. Stabilize the map to keep the exact-light return open.',tip:'Use Stabilizer before turn four, then deliver and return via Q.'},
  {id:9,n:1411,power:'Rewind',light:10,map:['#########','#.......#','#.......#','#D..M..H#','#.......#','#.......#','#########'],target:'M',brief:'Rewind undoes your last move and restores its light and map state. A wrong turn would exhaust this exact-light run.',tip:'Step up once, rewind the mistake, and then take the direct road.'}
 ];
 root.POWER_LEVELS=levels;
 if(typeof module!=='undefined')module.exports=levels;
})(typeof window!=='undefined'?window:globalThis);
