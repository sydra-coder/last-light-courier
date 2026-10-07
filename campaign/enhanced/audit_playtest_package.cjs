// Ensure the Windows launcher, standalone preview, guide and workbook coexist.
const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'../..');
const preview=path.join(root,'design/campaign-2000-preview/index.html');
const launcher=path.join(root,'Start-2000-Level-Playtest.bat');
const guide=path.join(root,'PLAYTEST_START_HERE.md');
const workbook=path.join(root,'outputs/01a1112f-b897-7c03-a6b3-f25018e9f557/Last_Light_Courier_2000_Level_Playtest_Status.xlsx');
for(const file of [preview,launcher,guide,workbook])if(!fs.existsSync(file))throw Error(`Missing review artifact: ${file}`);
const html=fs.readFileSync(preview,'utf8');
const bat=fs.readFileSync(launcher,'utf8');
const instructions=fs.readFileSync(guide,'utf8');
if(!bat.includes('%~dp0design\\campaign-2000-preview\\index.html')||!instructions.includes('Start-2000-Level-Playtest.bat'))
  throw Error('Launcher and guide disagree on preview location');
if(/<script[^>]+src=|<link[^>]+href=|<img[^>]+src=|\bfetch\(/i.test(html))
  throw Error('Preview depends on an external asset or fetch request');
const levels=require('./test_integrated_preview.cjs').LEVELS;
if(levels.length!==2000||levels[0].n!==1||levels[1999].n!==2000)
  throw Error('Standalone preview does not contain all 2000 levels');
console.log(`PASS: launcher, self-contained ${Math.round(fs.statSync(preview).size/1024/1024)} MiB preview, 2000 levels, guide and workbook`);
