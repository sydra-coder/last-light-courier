// Check generated zoom follow math without requiring a local browser surface.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(path.resolve(process.env.LLC_PREVIEW_PATH||path.resolve(__dirname,'../../design/campaign-2000-preview/index.html')),'utf8');
if(!html.includes('.boardZoom .button,.gameViewSection .viewChoices button{min-height:44px}')||
   !html.includes('.boardZoom .mini{display:block;font-size:10px;line-height:1.3}')||
   !html.includes("Math.max(1.5,(level.grid||8)/6)*100+'%'"))
  throw Error('Phone zoom size or guidance missing');
if(!html.includes("setAttribute?.('aria-label',zoomed?'Fit map':'Zoom map')")||
   !html.includes("setAttribute?.('aria-pressed',String(zoomed))"))
  throw Error('Zoom toggle accessibility state missing');
const start=html.indexOf('function focusZoomMap(){');
const end=html.indexOf('function render(){',start);
if(start<0||end<0)throw Error('Generated zoom follow function missing');
const source=html.slice(start,end);
let zoomed=false,last=null;
const viewport={clientWidth:300,clientHeight:220,scrollTo:p=>last=p};
const frame={parentElement:viewport,classList:{contains:()=>zoomed}};
const courier={offsetLeft:500,offsetTop:260,offsetWidth:48,offsetHeight:48};
const board={querySelector:s=>s.includes('data-x="12"')&&s.includes('data-y="7"')?courier:null};
const ctx={$:id=>id==='scene'?{parentElement:frame}:id==='board'?board:null,state:{pos:[12,7]}};
vm.runInNewContext(source+'\nthis.focus=focusZoomMap;',ctx);
ctx.focus();if(last!==null)throw Error('Fit mode unexpectedly scrolled');
zoomed=true;ctx.focus();
if(last.left!==374||last.top!==174)throw Error(`Wrong zoom follow target: ${JSON.stringify(last)}`);
console.log('PASS: zoom follows courier, fit does not scroll, and phone controls meet source-level size/label checks');
