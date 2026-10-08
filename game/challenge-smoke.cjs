const path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+path.resolve(__dirname,'index.html').replaceAll('\\','/'));
 await page.waitForFunction(()=>!!window.__campaign&&!!window.LLC_CHALLENGE_REPORT);
 const audit=await page.evaluate(()=>({count:LLC_CHALLENGE_REPORT.length,failed:LLC_CHALLENGE_REPORT.filter(x=>!x.length),minimum:Math.min(...LLC_CHALLENGE_REPORT.map(x=>x.length)),echoDisabled:LLC_DISABLE_ECHO}));
 if(audit.count!==101||audit.failed.length||audit.minimum<6||!audit.echoDisabled)throw Error(JSON.stringify(audit));
 const runs=[];
 for(const n of [20,40,60,70,80,100]){
   const result=await page.evaluate(n=>{__campaign.choose(n);const l=__campaign.levels[n-1];let accepted=0,blockedAt=null;for(let i=1;i<l.spine.length;i++){if(__campaign.move(l.spine[i]))accepted++;else{blockedAt=i;break}const s=__campaign.getState();if(s.done||s.failed)break}const s=__campaign.getState();return {level:n,accepted,blockedAt,done:s.done,failed:s.failed,patrol3:l.patrol3?.length,turns:s.turns}},n);
   runs.push(result);
   if(n===70){await page.evaluate(()=>__campaign.choose(70));await page.screenshot({path:path.join(__dirname,'challenge-level70-sample.png')})}
 }
 const hint=await page.evaluate(()=>{__campaign.choose(70);const l=__campaign.levels[69];for(let i=1;i<l.spine.length;i++){__campaign.move(l.spine[i]);if(__campaign.getState().mask)break}const result=__campaign.hintRoute();return {status:result.status,steps:result.steps,routeLength:result.route?.length}});
 if(hint.status!=='solved'||hint.routeLength<2)throw Error('Challenge hint failed: '+JSON.stringify(hint));
 await page.evaluate(()=>{__campaign.choose(1401);const l=__campaign.levels[1400];for(let i=1;i<l.spine.length;i++){if(!__campaign.move(l.spine[i]))break;if(__campaign.getState().mask.toString(2).replaceAll('0','').length>=3)break}});
 if(!(await page.locator('.boardframe').evaluate(el=>el.classList.contains('zoomed'))))await page.locator('#zoomMap').click();
 const zoom=await page.evaluate(()=>{const v=document.querySelector('.mapViewport'),cells=[...document.querySelectorAll('#board .cell')],min=Math.min(...cells.map(c=>c.getBoundingClientRect().left)),max=Math.max(...cells.map(c=>c.getBoundingClientRect().right)),r=v.getBoundingClientRect();return {left:min,viewportLeft:r.left,right:max,viewportRight:r.right,scrollLeft:v.scrollLeft}});
 if(zoom.left>zoom.viewportLeft+12||zoom.right<zoom.viewportRight-12)throw Error('Zoom exposed empty map border: '+JSON.stringify(zoom));
 await page.screenshot({path:path.join(__dirname,'large-map-zoom-after.png')});
 if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({audit,runs,hint,zoom}));
 await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
