const fs = require('fs');
const path = require('path');

const here = __dirname;
const generated = 'C:\\Users\\rahul\\.codex\\generated_images\\01a1112e-3975-75e3-9146-c1ec2019c43a';
const variants = JSON.parse(fs.readFileSync(path.join(here, 'manifest.json'), 'utf8'));
for (const v of variants) {
  v.file = `${v.id}-${v.name.toLowerCase().replaceAll(' ', '-')}.png`;
  fs.copyFileSync(path.join(generated, v.source), path.join(here, v.file));
}
const cards = variants.map(v => `<article class="card"><div class="art"><img src="${v.file}" alt="${v.name} sprite concept"></div><div class="meta"><b>${v.id} ${v.name}</b><span>isometric concept</span></div><div class="mini"><div class="tile"><img src="${v.file}" alt=""></div><span>phone tile preview</span></div></article>`).join('');
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><title>Last Light Courier | Courier Variants</title><style>
*{box-sizing:border-box}body{margin:0;background:#172537;color:#f8eedc;font:16px system-ui,sans-serif}.page{width:1500px;margin:auto;padding:32px 38px 42px}h1{font:700 38px Georgia,serif;margin:0 0 6px;color:#ffe2aa}.sub{margin:0 0 24px;color:#b7c9cd}.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}.card{border:1px solid #697d8a;border-radius:14px;background:#253849;overflow:hidden}.art{height:225px;background:radial-gradient(circle at 50% 72%,#68848b,#31485c 64%,#233549);background-size:20px 20px;position:relative;overflow:hidden}.art:before{content:"";position:absolute;inset:0;background-image:linear-gradient(45deg,#ffffff0a 25%,transparent 25%,transparent 75%,#ffffff0a 75%),linear-gradient(45deg,#ffffff0a 25%,transparent 25%,transparent 75%,#ffffff0a 75%);background-size:20px 20px;background-position:0 0,10px 10px}.art img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 7px 6px #101c29aa)}.meta{padding:9px 12px 4px}.meta b{display:block;font-size:15px}.meta span,.mini span{font-size:11px;color:#bdcbd0}.mini{padding:3px 12px 12px;display:flex;align-items:center;gap:10px}.tile{width:74px;height:64px;display:grid;place-items:center;background:linear-gradient(150deg,#8faeb0,#53707c);clip-path:polygon(50% 0,100% 35%,100% 72%,50% 100%,0 72%,0 35%)}.tile img{width:55px;height:55px;object-fit:contain}.foot{margin-top:17px;color:#b7c9cd;font-size:12px}
</style><div class="page"><h1>Last Light Courier · 18 courier concepts</h1><p class="sub">Original visual exploration · raised village art · lantern readability · six across for side-by-side comparison</p><main class="grid">${cards}</main><p class="foot">The small tile view is a scale test. Concepts need production cleanup, animation frames, and gameplay review before integration.</p></div></html>`;
fs.writeFileSync(path.join(here, 'contact-sheet.html'), html);
console.log(`Copied ${variants.length} sprites and wrote contact-sheet.html`);
