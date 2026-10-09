(() => {
  const packs = Object.freeze([
    {id:'llc_gems_050',amount:50,usd:'$0.99',name:'Spark'},
    {id:'llc_gems_150',amount:150,usd:'$2.99',name:'Pouch'},
    {id:'llc_gems_300',amount:300,usd:'$4.99',name:'Satchel'},
    {id:'llc_gems_650',amount:650,usd:'$9.99',name:'Chest'},
    {id:'llc_gems_1400',amount:1400,usd:'$19.99',name:'Vault'},
    {id:'llc_gems_3000',amount:3000,usd:'$39.99',name:'Treasury'}
  ]);
  const icon = '<svg class="gemIcon" viewBox="0 0 32 32" aria-hidden="true"><path d="M7 5h18l6 9-15 16L1 14z" fill="#50d9ed" stroke="#e4fbff" stroke-width="1.6"/><path d="M7 5l9 25L1 14z" fill="#448fd8"/><path d="M25 5l-9 25 15-16z" fill="#167fae"/><path d="M7 5l-6 9h30l-6-9z" fill="#a5f4fa"/><path d="M12 5h8l4 9H8z" fill="#e3ffff"/><path d="M8 14h16L16 30z" fill="#6fe5ef"/></svg>';
  const repairPrice = points => Number(points||0)<=0?0:Math.ceil(Number(points)/100);
  const toolPrices = Object.freeze({anchor_trap:6,decoy_light:7,reveal_pulse:8,lumen_flask:8,road_repair:9,light_bridge:10,map_stabilizer:11,freeze_seal:12,rewind:12});
  const toolPrice = id => toolPrices[id];
  window.LLCGemShop = Object.freeze({packs,icon,repairPrice,toolPrice,exchangePoints:2000,exchangeGems:20});
})();
