const fs=require('fs');
const path=require('path');
const dir=__dirname;
const generated='C:\\Users\\rahul\\.codex\\generated_images\\01a1112e-3975-75e3-9146-c1ec2019c43a';
const variants=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
const notes={
  'night-wisp':'All-season patrol shape',
  'dussehra-ember':'Saffron ember flecks',
  'halloween-hush':'Pumpkin-orange smoke curls',
  'diwali-afterglow':'Gold sparks inside violet haze',
  'winter-frost':'Cool frost at the rim',
  'new-year-stardrift':'Silver-blue star motes',
  'canal-mist':'Cool canal fog in the wisps',
  'old-city-cinder':'Ash and muted copper motes',
  'bell-hollow':'Broad bell-like silhouette',
  'ribbon-wraith':'Tall twin-ribbon silhouette',
  'moth-veil':'Wide folded-wing silhouette',
  'crescent-lurker':'Open crescent silhouette',
  'shard-mask':'Angular broken-mask silhouette',
  'ink-puddle':'Low horizontal silhouette',
  'thorn-crown':'Jagged crown silhouette',
  'eclipse-orb':'Compact circular silhouette',
  'veil-hand':'Five-fingered hand silhouette',
  'serpent-coil':'Coiled spiral silhouette',
  'hourglass-shade':'Pinched hourglass silhouette'
};
for(const v of variants){v.file=`${v.id}-${v.slug}.png`;fs.copyFileSync(path.join(generated,v.source),path.join(dir,v.file));}
const cards=variants.map(v=>`<article class="card"><div class="art"><img src="${v.file}" alt="${v.name} shadow concept"></div><div class="meta"><b>${v.id} ${v.name}</b><span>${notes[v.slug]}</span></div><div class="samples"><div><div class="tile"><img src="${v.file}" alt=""></div><small>Patrol</small></div><div><div class="tile echo"><img src="${v.file}" alt=""></div><small>Echo</small></div></div></article>`).join('');
const html=`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Last Light Courier · Shadow designs</title><style>
*{box-sizing:border-box}body{margin:0;background:#142638;color:#f8eedd;font:15px system-ui,sans-serif}.page{width:1450px;margin:auto;padding:28px 36px 36px}h1{font:700 36px Georgia,serif;color:#ffe0a0;margin:0 0 4px}.sub{color:#bdcbd0;margin:0 0 13px}.modes{display:flex;gap:8px;margin:12px 0 20px}.modes button{padding:8px 15px;border:1px solid #8095a3;border-radius:8px;background:#2b4356;color:#f9eedd;font-weight:800;cursor:pointer}.modes button.active{border-color:#ffe0a0;background:#695b5d}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{border:1px solid #718697;border-radius:13px;background:#24394b;overflow:hidden}.art{height:220px;position:relative;overflow:hidden;background-color:#3a5667;background-image:linear-gradient(45deg,#ffffff0a 25%,transparent 25%,transparent 75%,#ffffff0a 75%),linear-gradient(45deg,#ffffff0a 25%,transparent 25%,transparent 75%,#ffffff0a 75%);background-size:20px 20px;background-position:0 0,10px 10px}.art img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.meta{padding:9px 12px 5px}.meta b{display:block;color:#ffe1ac;font-size:16px}.meta span{font-size:11px;color:#bdcbd0}.samples{display:flex;gap:22px;padding:4px 12px 12px}.samples>div{text-align:center}.samples small{display:block;margin-top:3px;color:#b9c8ce;font-size:11px}.tile{width:80px;height:68px;display:grid;place-items:center;background:linear-gradient(155deg,#829fa6,#4c6a78);clip-path:polygon(50% 0,100% 35%,100% 72%,50% 100%,0 72%,0 35%)}.tile img{width:48px;height:52px;object-fit:contain;filter:drop-shadow(0 0 2px #b289e0)}.tile.echo{background:linear-gradient(155deg,#829fa6,#4c6a78)}.tile.echo img{opacity:.55;filter:brightness(1.3) drop-shadow(0 0 2px #c3a8ed)}body[data-mode="overhead"] .tile{clip-path:inset(3px round 5px);background:linear-gradient(130deg,#7c98a2,#546e7a)}body[data-mode="night"] .tile{background:linear-gradient(155deg,#363751,#24283f)}body[data-mode="night"] .art{background-color:#26364f}.foot{margin-top:17px;color:#b8c9ce;font-size:12px}
</style><div class="page"><h1>Last Light Courier · shadow concepts</h1><p class="sub">Eleven earlier designs plus eight new silhouettes · same patrol and Echo rules</p><div class="modes"><button data-mode="isometric" class="active">Isometric</button><button data-mode="overhead">Storybook</button><button data-mode="night">Night</button></div><main class="grid">${cards}</main><p class="foot">Phone tile previews show each design as a solid patrol and a paler Echo. These are visual studies; actual visibility in normal play still needs testing.</p></div><script>for(const b of document.querySelectorAll('[data-mode]'))b.onclick=()=>{document.body.dataset.mode=b.dataset.mode;for(const x of document.querySelectorAll('[data-mode]'))x.classList.toggle('active',x===b)};</script></html>`;
fs.writeFileSync(path.join(dir,'shadow-review.html'),html);
const newCards=variants.filter(v=>v.type==='new-shape').map(v=>`<article class="card"><div class="art"><img src="${v.file}" alt="${v.name} shadow concept"></div><div class="meta"><b>${v.id} ${v.name}</b><span>${notes[v.slug]}</span></div><div class="samples"><div><div class="tile"><img src="${v.file}" alt=""></div><small>Patrol</small></div><div><div class="tile echo"><img src="${v.file}" alt=""></div><small>Echo</small></div></div></article>`).join('');
const newHtml=html.replace('Eleven earlier designs plus eight new silhouettes','Eight new silhouettes with distinct outlines').replace(cards,newCards);
fs.writeFileSync(path.join(dir,'new-shapes-review.html'),newHtml);
console.log(`Copied ${variants.length} transparent shadows and built shadow-review.html`);
