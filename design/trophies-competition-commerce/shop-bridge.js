// Web-facing shop adapter. The Android host must verify before sending any grant.
// The browser has no payment simulator and never mints gems from a click.
(function (root) {
  const listeners = new Set();
  const knownProducts = Object.freeze(['gems_small', 'gems_medium', 'outfit_marigold']);
  const state = { available: !!root.CourierAndroid?.shopRequest, products: [], gems: 0, outfits: [], pending: [] };
  const notify = () => listeners.forEach(fn => fn({...state, products:[...state.products], outfits:[...state.outfits], pending:[...state.pending]}));
  const api = {
    getState: () => ({...state, products:[...state.products], outfits:[...state.outfits], pending:[...state.pending]}),
    subscribe(fn) { listeners.add(fn); fn(api.getState()); return () => listeners.delete(fn); },
    refresh() { if(state.available) root.CourierAndroid.shopRequest(JSON.stringify({action:'refresh'})); },
    buy(productId) {
      if(!knownProducts.includes(productId)) throw new Error('Unknown shop product');
      if(!state.available) throw new Error('Google Play shop is unavailable in this browser');
      root.CourierAndroid.shopRequest(JSON.stringify({action:'buy', productId}));
    },
    restore() { if(state.available) root.CourierAndroid.shopRequest(JSON.stringify({action:'restore'})); },
    // Called only by the native host after its verification service approves entitlements.
    receiveNativeState(json) {
      const next=JSON.parse(json);
      state.available=next.available === true;
      state.products=Array.isArray(next.products)?next.products.filter(p=>knownProducts.includes(p.id)):[];
      state.gems=Number.isSafeInteger(next.gems)&&next.gems>=0?next.gems:state.gems;
      state.outfits=Array.isArray(next.outfits)?next.outfits.filter(x=>knownProducts.includes(x)):state.outfits;
      state.pending=Array.isArray(next.pending)?next.pending.filter(x=>knownProducts.includes(x)):[];
      notify();
    }
  };
  root.CourierShop=api;
})(window);
