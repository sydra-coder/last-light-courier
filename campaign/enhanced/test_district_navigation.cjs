// Check that the 2,000-level picker renders 20 districts and only 10 chapters/levels at once.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
const line=pattern=>script?.match(pattern)?.[0];
const chapters=JSON.parse(line(/^const CHAPTERS=.*;$/m).split('=')[1].slice(0,-1));
const districts=JSON.parse(line(/^const DISTRICTS=.*;$/m).split('=')[1].slice(0,-1));
const renderLevels=line(/^function renderLevels\(\).*$/m);
const renderPicker=line(/^function renderPicker\(\).*$/m);
const renderRouteBook=line(/^function renderRouteBook\(.*$/m);
if(chapters.length!==200||districts.length!==20||!renderLevels||!renderPicker||!renderRouteBook)throw Error('Navigation data incomplete');
const nodes=new Map();
const $=id=>{
  if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',dataset:{},options:[],value:''});
  return nodes.get(id);
};
const ctx={CHAPTERS:chapters,DISTRICTS:districts,LEVELS:Array.from({length:2000},(_,i)=>({n:i+1,grid:8,homes:[[0,0]],cap:12})),save:{cleared:{}},level:{n:1},chapterShown:1,$,Object,String};
vm.runInNewContext(renderRouteBook+'\n'+renderPicker+'\n'+renderLevels+'\nthis.draw=()=>renderLevels();',ctx);
for(const [chapter,firstLevel] of [[1,1],[71,701],[181,1801],[200,1991]]){
  ctx.chapterShown=chapter;
  ctx.level={n:firstLevel};
  ctx.draw();
  const count=(id,token)=>($(id).innerHTML.match(new RegExp(token,'g'))||[]).length;
  if(count('districtSelect','<option')!==20||count('pickerDistrictSelect','<option')!==20)throw Error('District list wrong');
  if(count('chapters','data-chapter=')!==10||count('pickerChapters','data-picker-chapter=')!==10)throw Error(`Chapter list wrong at ${chapter}`);
  if(count('levelButtons','data-level=')!==10||count('pickerLevels','data-picker-level=')!==10)throw Error(`Level list wrong at ${chapter}`);
  if(!$('levelButtons').innerHTML.includes(`data-level="${firstLevel}"`))throw Error(`Level ${firstLevel} absent`);
}
console.log('PASS: 20 districts with 10 chapters and 10 levels shown per selection');
