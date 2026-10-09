// Injected inside the campaign closure by build.cjs.
const powerCart=Object.create(null);
const powerCartTotal=()=>POWER_CATALOG.reduce((total,item)=>total+(powerCart[item.id]||0)*window.LLCGemShop.toolPrice(item.id),0);
function renderPowerShop(){
  const box=$('powerShop');if(!box)return;
  const wasOpen=!!box.querySelector('details')?.open;
  syncPowerUnlocks();
  const rows=POWER_CATALOG.map(item=>{
    const earned=!!save.powerUnlocked[item.id],stock=save.powerStock[item.id]||0,qty=powerCart[item.id]||0;
    const price=window.LLCGemShop.toolPrice(item.id),icon=POWER_UI[item.id]?.icon||'✦';
    return '<div class="shopRow powerCartRow" data-cart-row="'+item.id+'"><span class="cartPowerIcon" aria-hidden="true">'+icon+'</span><span class="cartPowerName"><b>'+item.name+'</b><small>'+(earned?'×'+stock:'Level '+item.milestone)+'</small></span><span class="cartUnitPrice">'+window.LLCGemShop.icon+' '+price+'</span><div class="cartStepper"><button type="button" data-cart-minus="'+item.id+'" aria-label="Remove one '+item.name+'" '+(!qty?'disabled':'')+'>−</button><output aria-label="'+item.name+' selected">'+qty+'</output><button type="button" data-cart-plus="'+item.id+'" aria-label="Add one '+item.name+'" '+(!earned||powerCartTotal()+price>save.gems?'disabled':'')+'>+</button></div></div>';
  }).join('');
  const total=powerCartTotal();
  box.innerHTML='<div class="powerGemBalance">'+window.LLCGemShop.icon+' '+save.gems.toLocaleString()+'</div><details><summary>Powers</summary>'+rows+'</details><div class="powerCartFooter"><span class="cartTotal" aria-label="Cart total '+total+' gems">'+window.LLCGemShop.icon+' '+total+'</span><button type="button" data-cart-purchase '+(!total||total>save.gems?'disabled':'')+'>Purchase</button></div>';
  if(wasOpen)box.querySelector('details').open=true;
}
$('powerShop').addEventListener('click',event=>{
  const plus=event.target.closest('[data-cart-plus]'),minus=event.target.closest('[data-cart-minus]');
  if(plus||minus){
    const id=(plus||minus).dataset[plus?'cartPlus':'cartMinus'];
    const item=POWER_CATALOG.find(entry=>entry.id===id);if(!item)return;
    const qty=powerCart[id]||0,price=window.LLCGemShop.toolPrice(id);
    if(plus){if(!save.powerUnlocked?.[id]||qty>=99||powerCartTotal()+price>save.gems)return;powerCart[id]=qty+1}
    else{if(!qty)return;powerCart[id]=qty-1}
    renderPowerShop();return;
  }
  if(!event.target.closest('[data-cart-purchase]'))return;
  const selected=POWER_CATALOG.filter(item=>powerCart[item.id]>0);
  const total=powerCartTotal();
  if(!selected.length||total<=0||total>save.gems||selected.some(item=>!save.powerUnlocked?.[item.id]))return;
  save.gems-=total;
  for(const item of selected){save.powerStock[item.id]=(save.powerStock[item.id]||0)+powerCart[item.id];powerCart[item.id]=0}
  persist();render();setStatus('Powers restocked',selected.length+' types',total+' gems spent.');window.dispatchEvent(new Event('llc:gem-balance-change'));
});
syncPowerUnlocks();
