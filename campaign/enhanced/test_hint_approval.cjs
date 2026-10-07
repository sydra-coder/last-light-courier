// Verify the generated approval handler spends exactly one hint; rejection is separate.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html'),'utf8');
const source=html.match(/\$\('hintApprove'\)\.addEventListener\('click',\(\)=>\{[^}]*\}\);/)?.[0];
if(!source)throw Error('Generated hint approval handler missing');
const approve={handler:null,addEventListener(_type,handler){this.handler=handler}};
let persists=0,closes=0,renders=0;
const pendingHint={route:[{p:[1,1]},{p:[1,2]}],steps:1};
const ctx={pendingHint,hintPath:null,save:{hints:3},$:id=>id==='hintApprove'?approve:null,
  persist:()=>persists++,closeHint:()=>closes++,render:()=>renders++};
vm.runInNewContext(source,ctx);
approve.handler();
if(ctx.save.hints!==2||ctx.hintPath!==pendingHint||persists!==1||closes!==1||renders!==1)
  throw Error('Approval did not use exactly one hint and reveal its route');
console.log('PASS: generated approval action spends one hint and displays the selected route');
