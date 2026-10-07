// Verify fresh-test control clears only the candidate preview save after approval.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html'),'utf8');
const key=html.match(/const saveKey='([^']+)'/)?.[1];
const handler=html.split(/\r?\n/).find(line=>line.startsWith("$('menuFresh').addEventListener('click'"));
if(key!=='last-light-courier-2000-candidate-v1'||!handler||!html.includes('id="menuFresh"'))
  throw Error('Fresh test control or isolated save key missing');
let consent=false,removed=[],reloaded=0;
const button={handler:null,addEventListener(_type,fn){this.handler=fn}};
const ctx={saveKey:key,$:id=>id==='menuFresh'?button:null,
  window:{confirm:()=>consent},localStorage:{removeItem:k=>removed.push(k)},
  location:{reload:()=>reloaded++}};
vm.runInNewContext(handler,ctx);
button.handler();
if(removed.length||reloaded)throw Error('Rejected fresh-test action changed save');
consent=true;button.handler();
if(removed.length!==1||removed[0]!==key||reloaded!==1)
  throw Error('Fresh-test action did not clear exactly the candidate save');
console.log('PASS: fresh-test control preserves rejected saves and clears only the candidate save on approval');
