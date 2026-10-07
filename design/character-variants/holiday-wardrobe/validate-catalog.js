const fs=require('fs');
const path=require('path');
const vm=require('vm');
const assert=require('assert');
const dir=__dirname;
const catalog=require('./catalog.json');
assert.strictEqual(catalog.characters.length,18);
assert.strictEqual(catalog.themes.length,5);
for(const character of catalog.characters){
  assert.strictEqual(character.looks.length,5);
  for(const look of character.looks) assert(fs.existsSync(path.join(dir,look.asset)),`${character.name} ${look.theme}`);
}
const html=fs.readFileSync(path.join(dir,'shop-preview.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert(script,'shop script');
const elements={};
function el(id){return elements[id]??(elements[id]={value:'0',innerHTML:'',textContent:'',onclick:null,onchange:null});}
const saved={};
const context={document:{getElementById:el},localStorage:{getItem:k=>saved[k]??null,setItem:(k,v)=>{saved[k]=v}}};
vm.runInNewContext(script,context);
assert(el('wallet').textContent.includes('250'));
assert(el('detail').innerHTML.includes('Ember Scout'));
el('buy').onclick();
assert(el('wallet').textContent.includes('190'));
assert(el('detail').innerHTML.includes('Ember Scout'));
el('tabs').onclick({target:{closest:()=>({dataset:{i:'2'}})}});
assert(el('detail').innerHTML.includes('Diwali Lights'));
el('character').value='1';el('character').onchange();
assert(el('detail').innerHTML.includes('Moss Ranger'));
el('reset').onclick();
assert(el('wallet').textContent.includes('250'));
console.log('PASS: 18 characters, 90 looks, all assets present, buy/select/reset demo flow');
