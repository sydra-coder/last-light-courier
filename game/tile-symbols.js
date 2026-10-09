/* Compact, repeatable board symbols. Every blocked road, delivery and event keeps
   the same silhouette and color in all three map views. */
(() => {
  const C={ink:'#14212b',cream:'#fff2d1',stone:'#d5e2e2',blocked:'#ad454a',gold:'#ffd16f',green:'#70efad',blue:'#82d9f6',violet:'#d4a7ff'};
  const path=(c,points,fill,stroke=C.ink,width=3)=>{c.beginPath();points.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.closePath();c.fillStyle=fill;c.fill();if(stroke){c.lineWidth=width;c.strokeStyle=stroke;c.stroke()}};
  const line=(c,points,color=C.cream,width=5)=>{c.beginPath();points.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.lineCap='round';c.lineJoin='round';c.lineWidth=width;c.strokeStyle=color;c.stroke()};
  const circle=(c,x,y,r,fill,stroke=C.ink,width=3)=>{c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fillStyle=fill;c.fill();if(stroke){c.lineWidth=width;c.strokeStyle=stroke;c.stroke()}};
  const box=(c,x,y,w,h,r,fill,stroke=C.ink,width=3)=>{c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill();if(stroke){c.lineWidth=width;c.strokeStyle=stroke;c.stroke()}};
  const at=(c,x,y,draw)=>{c.save();c.translate(x,y);draw();c.restore();return true};
  const bars=(c,color)=>{for(const x of [-15,-5,5,15])line(c,[[x,-17],[x,17]],color,4);line(c,[[-22,-20],[22,-20]],color,4);line(c,[[-22,20],[22,20]],color,4)};
  const bolt=c=>path(c,[[-3,-23],[12,-23],[3,-5],[14,-5],[-9,24],[-3,4],[-15,4]],C.gold,C.ink,2);
  const hourglass=c=>{line(c,[[-17,-20],[17,-20],[-8,18],[8,18],[-17,-20]],C.cream,4);line(c,[[-17,21],[17,21]],C.gold,5);circle(c,0,0,3,C.gold,null)};
  const depotMark=(c,x,y)=>at(c,x,y,()=>{
    // The roof and side posts stay visible even while the courier stands on the depot.
    circle(c,0,0,33,'#12374b',C.blue,3);
    box(c,-27,-12,54,37,5,'#b7d8d2',C.ink,3);
    box(c,-23,-7,9,30,2,'#f4e6b9',C.ink,2);
    box(c,14,-7,9,30,2,'#f4e6b9',C.ink,2);
    box(c,-23,-2,7,10,2,'#ffe39a',C.ink,1);
    box(c,16,-2,7,10,2,'#ffe39a',C.ink,1);
    box(c,-11,-6,22,31,8,'#174c61','#f4d38a',3);
    path(c,[[-33,-12],[0,-31],[33,-12]],'#efb75f',C.ink,4);
    line(c,[[-32,-13],[0,-31],[32,-13]],'#fff1c3',4);
    box(c,-10,-37,20,10,3,'#efbd69',C.ink,2);
    circle(c,0,-32,3,'#fff4c2',null);
    line(c,[[-25,22],[25,22]],C.gold,4);
  });
  const house=(c,x,y,lit,depot=false)=>depot?depotMark(c,x,y):at(c,x,y,()=>{
    circle(c,0,0,31,lit?'#176b4d':'#4a4559',lit?C.green:'#d9b7a7',3);
    box(c,-19,-3,38,25,3,lit?'#e1ab60':'#956e66',C.ink,3);
    path(c,[[-25,-3],[0,-25],[25,-3]],lit?'#ffd06d':'#d79278',C.ink,4);
    box(c,-6,7,12,15,2,lit?'#fff6c0':'#353b4b',C.ink,2);
    if(lit){circle(c,19,-20,11,C.green,C.ink,2);line(c,[[13,-20],[18,-15],[26,-25]],C.ink,3.5)}
  });
  const rubble=(c,x,y)=>at(c,x,y,()=>{
    box(c,-30,-28,60,56,8,'#243441',C.blocked,4);
    path(c,[[-26,17],[-16,-11],[-5,4],[7,-19],[27,17]],C.stone,C.ink,4);
    line(c,[[-26,22],[26,22]],C.blocked,5);
    line(c,[[-22,-22],[-12,-22]],C.cream,3);
  });
  const crates=(c,x,y)=>at(c,x,y,()=>{box(c,-28,-25,56,51,7,'#483727',C.blocked,4);for(const dx of [-16,6]){box(c,dx-8,-13,22,23,2,'#c18a4d',C.ink,2);line(c,[[dx-6,-11],[dx+12,8]],C.cream,2)}line(c,[[-22,19],[22,19]],C.blocked,5)});
  const bridge=(c,x,y,broken)=>at(c,x,y,()=>{box(c,-29,-22,58,44,7,broken?'#493c37':'#335b5f',broken?C.blocked:C.blue,4);for(const dx of [-15,0,15])line(c,[[dx,-15],[dx,15]],C.cream,3);if(broken)line(c,[[-24,19],[24,-19]],C.blocked,7)});
  const feature=(c,x,y,kind,closed)=>at(c,x,y,()=>{
    const danger=closed||['collapse','aftershockroad','floodroad','dark','hunterden'].includes(kind);
    const purple=['shadowdoor','shadowlock','hunterden','dark'].includes(kind);
    const cyan=['ice','lightbridge','transitstop','lightreceiver','lumenrelay','moonroad'].includes(kind);
    const accent=danger?C.blocked:purple?C.violet:cyan?C.blue:C.gold;
    box(c,-27,-27,54,54,9,purple?'#302c46':danger?'#3d3039':'#263f47',accent,4);
    switch(kind){
      case 'fade':case 'aftershockroad':hourglass(c);if(kind==='aftershockroad')line(c,[[-21,18],[-9,8],[0,16],[10,5],[21,16]],C.blocked,3);break;
      case 'switch':circle(c,0,8,13,C.gold,C.ink,3);line(c,[[0,5],[15,-17]],C.cream,6);circle(c,15,-17,6,C.green,C.ink,2);break;
      case 'gate':case 'overloadgate':bars(c,accent);if(kind==='overloadgate')bolt(c);break;
      case 'ice':for(let a=0;a<3;a++){c.save();c.rotate(a*Math.PI/3);line(c,[[0,-20],[0,20]],C.cream,4);c.restore()}break;
      case 'dark':circle(c,0,0,15,C.violet,null);circle(c,7,-7,15,'#302c46',null);break;
      case 'collapse':line(c,[[-18,-16],[17,16]],C.gold,8);line(c,[[-18,16],[-5,3],[4,12],[18,-16]],C.cream,4);break;
      case 'floodroad':for(const y of [-9,4,17])line(c,[[-20,y],[-8,y-5],[5,y],[19,y-5]],C.blue,4);break;
      case 'duskroad':case 'nightfall':case 'moonroad':circle(c,0,0,16,C.gold,null);circle(c,8,-7,16,'#263f47',null);break;
      case 'lightbridge':bridge(c,0,0,closed);break;
      case 'shadowdoor':circle(c,0,0,18,C.violet,C.ink,3);circle(c,0,0,10,'#20172d',null);break;
      case 'shadowlock':box(c,-15,-2,30,23,4,C.violet,C.ink,3);c.beginPath();c.arc(0,-2,10,Math.PI,0);c.strokeStyle=C.cream;c.lineWidth=5;c.stroke();break;
      case 'oneway':line(c,[[-19,0],[17,0]],C.cream,7);path(c,[[5,-13],[22,0],[5,13]],C.gold,C.ink,2);break;
      case 'hunterden':for(const dx of [-12,0,12])line(c,[[dx-4,-14],[dx+4,14]],C.violet,5);break;
      case 'recharge':case 'lumenrelay':bolt(c);break;
      case 'lightreceiver':path(c,[[0,-22],[20,0],[0,22],[-20,0]],C.blue,C.ink,3);circle(c,0,0,6,C.cream,null);break;
      case 'transitstop':line(c,[[-18,-8],[15,-8]],C.cream,4);line(c,[[18,8],[-15,8]],C.blue,4);path(c,[[9,-16],[23,-8],[9,0]],C.gold,C.ink,2);path(c,[[-9,0],[-23,8],[-9,16]],C.blue,C.ink,2);break;
      default:circle(c,0,0,11,accent,C.ink,3);break;
    }
    if(closed&&kind!=='lightbridge'){line(c,[[-21,21],[21,-21]],C.blocked,5)}
  });
  const sprites={};
  for(const name of ['rock-slab','rock-spires','rock-rubble','tree-pine','tree-oak','tree-dead','bush-thorn','repair-rock','repair-tree','repair-bush','house-unlit','house-lit','switch-idle','switch-active','switch-expiring']){
    const img=new Image();img.onload=()=>window.__campaign?.redraw?.();img.src='../design/board-objects/'+name+'.png';sprites[name]=img;
  }
  const sprite=(c,name,x,y,w=65,h=65)=>{const img=sprites[name];if(!img?.complete||!img.naturalWidth)return false;c.drawImage(img,x-w/2,y-h/2,w,h);return true};
  const blocker=(c,x,y,p,repair,name='')=>{
    let asset;
    if(repair)asset=/tree|trunk|branch|wood|log/i.test(name)?'repair-tree':/bush|thorn|hedge/i.test(name)?'repair-bush':'repair-rock';
    else asset=['rock-slab','rock-spires','rock-rubble','tree-pine','tree-oak','tree-dead','bush-thorn'][(p[0]*17+p[1]*31)%7];
    return sprite(c,asset,x,y-5,68,68)||rubble(c,x,y);
  };
  const storyHouse=(c,x,y,lit,depot=false)=>{
    if(depot)return depotMark(c,x,y);
    const ok=sprite(c,lit?'house-lit':'house-unlit',x,y-8,69,69);
    if(ok&&lit)at(c,x+22,y-24,()=>{circle(c,0,0,10,C.green,C.ink,2);line(c,[[-5,0],[-1,4],[5,-5]],C.ink,3)});
    return ok||house(c,x,y,lit,false);
  };
  const storyFeature=(c,x,y,kind,closed,gateTurns=0)=>{
    if(kind!=='switch')return feature(c,x,y,kind,closed);
    return sprite(c,gateTurns===1?'switch-expiring':gateTurns>1?'switch-active':'switch-idle',x,y-3,58,58)||feature(c,x,y,kind,closed);
  };
  window.LLCTileArt={house:storyHouse,rubble,crates,bridge,feature:storyFeature,blocker};
})();
