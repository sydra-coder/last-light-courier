(() => {
  const fixture=window.LLCRegression;
  if(!fixture)return;
  const level=fixture.level;
  fixture.title='Level 500 · Test Remix';
  fixture.saveKey='last-light-courier-level-500-test-v1';
  level.n=500;
  level.chapter=50;
  level.brief='Isolated 12×12 Level 500 test remix. Four deliveries, then return to the depot. All nine current powers are stocked; switch hazard setups and replay as often as needed.';
  level.homes=[
    {p:[1,5],name:'Westwatch House',points:180},
    {p:[2,2],name:'Beacon Cottage',points:200},
    {p:[9,2],name:'Clocktower Home',points:220},
    {p:[9,9],name:'Canal House',points:240},
    {p:[10,4],name:'Hidden Lantern',points:260}
  ];
  level.required=4;
  level.cap=70;
  level.bonus=500;
  if(level.hiddenRoad)level.hiddenHouseIndex=4;
  if(level.lumenNetwork)level.lumenNetwork.sourceHouseIndex=1;
})();
