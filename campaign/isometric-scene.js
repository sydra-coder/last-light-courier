// Raised village renderer. Game rules and hit targets stay in campaign.template.html.
const ISO=(()=>{
  const canvas=document.getElementById('scene'),ctx=canvas.getContext('2d');
  const W=800,H=600,tw=46,th=29,depth=9;
  const project=p=>[400+(p[0]-p[1])*47,70+(p[0]+p[1])*32];
  let travel=null,repairFlash=null,pending=false;
  function size(){const ratio=Math.min(devicePixelRatio||1,2);const w=Math.round(W*ratio),h=Math.round(H*ratio);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h}ctx.setTransform(ratio,0,0,ratio,0,0)}
  function line(x1,y1,x2,y2,color,width=2){ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()}
  function ellipse(x,y,rx,ry,color){ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fillStyle=color;ctx.fill()}
  function rect(x,y,w,h,r,fill,stroke,width=1){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke()}}
  function polygon(points,fill,stroke,width=1){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke()}}
  function tile(x,y,p,wall,feature,lit,safe,danger){
    const floor=wall?'#495b68':lit?'#876b55':feature==='ice'?'#537e91':feature==='fade'?'#8e755d':feature==='dark'?'#414b64':feature==='switch'?'#537764':feature==='gate'?'#685b70':(p[0]+p[1])%2?'#4d6973':'#5a7479';
    const edge=safe?'#b2f9d5':danger?'#ff9b9e':lit?'#f9d99c':wall?'#8a9ca4':'#879ba1';
    ellipse(x,y+33,39,13,'#08162488');
    polygon([[x-tw,y],[x,y+th],[x,y+th+depth],[x-tw,y+depth]],'#273b48','#20303d',1);
    polygon([[x,y+th],[x+tw,y],[x+tw,y+depth],[x,y+th+depth]],'#1c3341','#142a36',1);
    if(safe||danger){ctx.save();ctx.shadowColor=safe?'#96efc7':'#ff8e9e';ctx.shadowBlur=18;polygon([[x,y-th],[x+tw,y],[x,y+th],[x-tw,y]],floor,edge,5);ctx.restore()}
    else polygon([[x,y-th],[x+tw,y],[x,y+th],[x-tw,y]],floor,edge,2);
    if(!wall&&!feature&&!lit){line(x-8,y+4,x+1,y+10,'#bdd0c344',1.3);line(x+8,y-8,x+15,y-4,'#c3d0c544',1.2)}
    if(danger){ellipse(x,y,5,3,'#ff9b9e')}else if(safe){ellipse(x,y,5,3,'#c1ffe0')}
  }
  function house(x,y,lit,depot=false){
    ctx.save();ctx.translate(x,y-7);ctx.scale(.93,.93);
    if(lit){const g=ctx.createRadialGradient(0,-8,3,0,-8,45);g.addColorStop(0,'#ffd98488');g.addColorStop(1,'#ffd98400');ellipse(0,-7,45,45,g)}
    ellipse(0,24,31,7,'#081521aa');
    rect(-25,-13,50,37,3,depot?'#597f95':lit?'#b97b60':'#866c77',depot?'#c2e5e9':'#e7c6a6',2.5);
    polygon([[-31,-13],[0,-42],[31,-13]],depot?'#3a637d':lit?'#765063':'#4b556d',depot?'#c3e9ea':lit?'#ffe2ac':'#d5bcae',3);
    rect(-9,1,18,23,2,depot?'#2c506b':lit?'#ffda81':'#413b50','#f4d1aa',2);
    rect(-20,-5,10,11,1,lit?'#ffe7a2':'#414353','#efcead',1.6);
    rect(10,-5,10,11,1,lit?'#ffe7a2':'#414353','#efcead',1.6);
    if(depot){ellipse(0,-19,5,5,'#ffe3a1');rect(-28,12,8,14,2,'#d3a86b','#ffe4ab',1)}
    if(lit){ellipse(-29,13,6,4,'#ffd78b88');ellipse(29,13,6,4,'#ffd78b88');rect(19,-34,11,11,3,'#f3d17b','#fff0b8',1);ctx.fillStyle='#3e3b40';ctx.font='bold 10px Segoe UI';ctx.fillText('✓',21,-25)}
    ctx.restore();
  }
  function rubble(x,y){ctx.save();ctx.translate(x,y-3);ctx.scale(1.12,1.12);ellipse(0,23,28,6,'#08152199');polygon([[-29,16],[-17,-11],[-4,2],[8,-19],[29,14],[25,22],[-25,22]],'#647582','#b8c4c8',2);line(-17,0,-4,9,'#384c5a',3);line(8,-13,0,3,'#3a4e5b',3);line(0,3,12,11,'#3a4e5b',3);ctx.restore()}
  function crates(x,y){ctx.save();ctx.translate(x,y-4);ellipse(0,23,30,6,'#08152199');for(const [bx,by] of [[-22,0],[2,2],[-9,-17]]){rect(bx,by,23,22,2,'#8a644d','#d8aa77',2);line(bx+2,by+3,bx+21,by+19,'#523d38',2);line(bx+20,by+3,bx+3,by+19,'#523d38',2)}ctx.restore()}
  function bridge(x,y,broken){ctx.save();ctx.translate(x,y);if(broken){rect(-30,-6,22,20,2,'#8c694e','#d2a87b',2);rect(8,-6,22,20,2,'#8c694e','#d2a87b',2);line(-7,-2,7,7,'#ffe3a377',2)}else{rect(-30,-7,60,22,2,'#9b7857','#e5bb88',2);for(let a=-18;a<24;a+=12)line(a,-6,a,14,'#5b473f',2)}ctx.restore()}
  function gate(x,y,opened){ctx.save();ctx.translate(x,y-6);line(-24,18,-24,-25,'#d7c4d2',5);line(24,18,24,-25,'#d7c4d2',5);line(-25,-25,25,-25,'#ead7dd',5);if(!opened)for(let a=-14;a<21;a+=11)line(a,-23,a,18,'#9a85a0',5);else{line(23,-22,30,16,'#b8a7bc',4);ellipse(0,9,13,4,'#a4e1b177')}ctx.restore()}
  function featureArt(x,y,feature,closed){
    if(feature==='fade'){bridge(x,y,closed);return}
    if(feature==='gate'){gate(x,y,!closed);return}
    if(feature==='ice'){polygon([[x-26,y+3],[x-8,y-18],[x+21,y-14],[x+30,y+5],[x+10,y+17]],closed?'#65747f':'#97d9e5','#e4f9fc',2);line(x-8,y-18,x+3,y+9,'#e7f8ff',2);line(x+3,y+9,x-12,y+18,'#e7f8ff',2);return}
    if(feature==='dark'){ellipse(x,y-5,24,20,'#293649');ellipse(x-5,y-11,12,12,'#d2c1d9');ellipse(x+1,y-14,12,12,'#293649');return}
    if(feature==='switch'){polygon([[x,y-22],[x+21,y],[x,y+18],[x-21,y]],'#679b7a','#c6f4c9',3);ellipse(x,y-2,6,6,'#fff0a9');return}
  }
  function courier(x,y,moving,t){ctx.save();ctx.translate(x,y-13);ctx.scale(.8,.8);ellipse(0,23,19,5,'#081521aa');const step=moving?Math.sin(t*.028)*4:0;line(-6,9,-9+step,23,'#273e54',6);line(6,9,8-step,23,'#273e54',6);ctx.beginPath();ctx.moveTo(-16,-4);ctx.lineTo(-18,17);ctx.quadraticCurveTo(0,27,18,17);ctx.lineTo(14,-5);ctx.closePath();ctx.fillStyle='#bd6859';ctx.fill();ctx.strokeStyle='#f7c894';ctx.lineWidth=2;ctx.stroke();ellipse(0,-13,13,15,'#476984');ellipse(1,-8,9,10,'#eabb91');polygon([[-15,-18],[-5,-31],[6,-31],[17,-14],[8,-21],[-5,-18]],'#36536c');ellipse(4,-9,1.5,1.6,'#27354a');line(10,3,21,5,'#edbf94',5);const g=ctx.createRadialGradient(21,7,2,21,7,31);g.addColorStop(0,'#ffe5a8aa');g.addColorStop(1,'#ffce6d00');ellipse(21,7,31,31,g);rect(15,0,13,17,2,'#dfa65d','#fff1b7',2);rect(18,3,7,9,1,'#fff0b0');ctx.restore()}
  function shadow(x,y,echo=false,moving=false,t=0){ctx.save();ctx.translate(x,y-12);ctx.scale(.84,.84);ctx.globalAlpha=echo?.55:1;const g=ctx.createRadialGradient(0,0,3,0,0,33);g.addColorStop(0,'#b28ceaa0');g.addColorStop(1,'#b28cea00');ellipse(0,0,33,33,g);ellipse(0,22,18,5,'#241739aa');const sway=moving?Math.sin(t*.02)*3:0;ctx.beginPath();ctx.moveTo(-18,13);ctx.quadraticCurveTo(-22,-13,0,-24);ctx.quadraticCurveTo(23,-14,18,13);ctx.lineTo(10+sway,8);ctx.lineTo(5,20);ctx.lineTo(-3,11);ctx.lineTo(-11,20);ctx.closePath();ctx.fillStyle=echo?'#927db7':'#614783';ctx.fill();ctx.strokeStyle='#d6b5f2';ctx.lineWidth=2;ctx.stroke();ellipse(-7,-5,3.5,2.2,'#f4dcff');ellipse(7,-5,3.5,2.2,'#f4dcff');ctx.restore()}
  const ease=f=>f*f*(3-2*f),interp=(a,b,f)=>[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f];
  function position(from,to,progress){return from&&to?interp(from,to,progress):to||from}
  function frame(now){pending=false;draw(now)}
  function schedule(){if(!pending){pending=true;requestAnimationFrame(frame)}}
  function draw(now=performance.now()){
    size();ctx.clearRect(0,0,W,H);const bg=ctx.createLinearGradient(0,0,W,H);bg.addColorStop(0,'#2c4150');bg.addColorStop(1,'#172b3a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
    for(let i=0;i<45;i++)ellipse((i*173+59)%W,(i*97+31)%H,1.2,1.2,'#fff0d31d');
    const walls=activeWalls(),objects=[];
    for(let sum=0;sum<=14;sum++)for(let y=0;y<8;y++){const x=sum-y;if(x<0||x>7)continue;const p=[x,y],[cx,cy]=project(p),id=k(p),wall=walls.has(id),feature=featureAt(p),hi=homeIndex(p),lit=hi>=0&&!!(state.mask&(1<<hi)),adj=Math.abs(x-state.pos[0])+Math.abs(y-state.pos[1])===1,safe=adj&&legal(p),danger=adj&&open(p)&&!safe&&!state.done&&!state.failed;tile(cx,cy,p,wall,feature,lit,safe,danger);
      const repairTile=level.repair&&eq(p,level.repair.tile),name=level.repair?.name.toLowerCase()||'';
      if(wall)objects.push({y:cy,draw:()=>repairTile&&(name.includes('crate')||name.includes('debris'))?crates(cx,cy):repairTile&&(name.includes('bridge')||name.includes('crossing'))?bridge(cx,cy,true):rubble(cx,cy)});
      else if(hi>=0)objects.push({y:cy,draw:()=>house(cx,cy,lit)});
      else if(eq(p,level.depot))objects.push({y:cy,draw:()=>house(cx,cy,false,true)});
      else if(feature){const closed=(feature==='fade'&&state.fade===0)||(feature==='ice'&&state.ice===0)||(feature==='gate'&&state.gate<=0&&!(repaired()&&level.repair?.effect==='latch'));objects.push({y:cy,draw:()=>featureArt(cx,cy,feature,closed)})}
      if(repairTile&&repaired()&&level.repair.effect==='open')objects.push({y:cy+1,draw:()=>bridge(cx,cy,false)});
    }
    let progress=1,moving=false;if(travel){progress=Math.min(1,(now-travel.start)/430);moving=progress<1;if(!moving)travel=null}else progress=1;const eased=ease(progress);
    const actor=travel?position(travel.from,travel.to,eased):state.pos;
    const addShadow=(patrol,phase,from,to)=>{if(!state.active||!patrol)return;const pos=travel?position(from,to,eased):patrol[phase];if(!pos)return;const [x,y]=project(pos);if(travel&&from&&to&&moving){const [ox,oy]=project(from);line(ox,oy,x,y,'#b48ae077',8)}objects.push({y:y+2,draw:()=>shadow(x,y,false,moving,now)})};
    addShadow(level.patrol,state.phase,travel?.shadowFrom,travel?.shadowTo);
    addShadow(level.patrol2,state.phase2,travel?.shadow2From,travel?.shadow2To);
    if(level.echo&&state.active&&state.trail.length>=2){const [ex,ey]=project(state.trail[state.trail.length-2]);objects.push({y:ey+1,draw:()=>shadow(ex,ey,true,false,now)})}
    const [px,py]=project(actor);objects.push({y:py+3,draw:()=>courier(px,py,moving,now)});objects.sort((a,b)=>a.y-b.y);for(const o of objects)o.draw();
    if(repairFlash){const age=now-repairFlash.start;if(age<750){const [rx,ry]=project(repairFlash.tile);ctx.save();ctx.globalAlpha=1-age/750;ctx.strokeStyle='#ffe2a1';ctx.lineWidth=4;ctx.beginPath();ctx.ellipse(rx,ry,15+age/9,8+age/15,0,0,Math.PI*2);ctx.stroke();for(let i=0;i<7;i++){const a=i*Math.PI*2/7,dist=6+age/14;rect(rx+Math.cos(a)*dist,ry+Math.sin(a)*dist*.55-age/28,5,4,1,i%2?'#e8bb7f':'#a6a5a0')}ctx.restore()}else repairFlash=null}
    if(moving||repairFlash)schedule();
  }
  return {project,render:()=>draw(),cancel:()=>{travel=null;repairFlash=null},move:(from,to,shadowFrom,shadowTo,shadow2From,shadow2To)=>{travel={from,to,shadowFrom,shadowTo,shadow2From,shadow2To,start:performance.now()};draw()},repair:tile=>{repairFlash={tile,start:performance.now()};draw()}};
})();
