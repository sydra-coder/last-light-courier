(() => {
  const options={all:'All hazards',roads:'Roads & crossings',weather:'Weather & light',shadows:'Shadow pressure',circuit:'Circuit & travel'};
  const requested=new URLSearchParams(location.search).get('scenario');
  const scenario=Object.hasOwn(options,requested)?requested:'all';
  const has=name=>scenario==='all'||scenario===name;
  const spine=[[1,10]];
  for(let y=9;y>=2;y--)spine.push([1,y]);
  for(let x=2;x<=9;x++)spine.push([x,2]);
  for(let y=3;y<=10;y++)spine.push([9,y]);
  for(let x=8;x>=1;x--)spine.push([x,10]);
  const level={
    n:1,chapter:1,grid:12,brief:'Regression arena: test a power, inspect a hazard, then replay. Three deliveries and a depot return complete the route.',
    depot:[1,10],homes:[
      {p:[2,2],name:'Beacon Cottage',points:100},
      {p:[9,2],name:'Clocktower Home',points:120},
      {p:[9,9],name:'Canal House',points:140},
      {p:[10,4],name:'Hidden Lantern',points:160}
    ],required:3,bonus:100,cap:66,noShadow:false,spine,
    walls:['4,4','7,4','4,7','7,7','5,9'],
    patrol:[[5,5],[6,5],[6,6],[5,6]],phase:0,
    patrol2:[[7,5],[8,5],[8,6],[7,6]],phase2:1,
    repair:{tile:[4,4],name:'Clear split boulder',band:'S',cost:50,effect:'open',stepsSaved:2},
    reviewPower:'lumen_flask'
  };
  if(has('roads'))Object.assign(level,{
    fade:[5,3],ice:[6,3],dark:[4,3],switch:[8,4],gate:[8,5],
    collapseTile:[4,5],lightBridge:[6,8],bridgeCost:1,lightBridgeRequiresPower:true,
    hiddenRoad:[10,3],hiddenHouseIndex:3,beaconHouseIndex:99,
    oneWayTile:[3,5],oneWayFrom:[3,6],
    authoredEvent:{kind:'road_close',trigger:'first_delivery',tile:[4,6],cue:'The marked side road closes after the first delivery.'},
    phaseChoice:{decision:'depot_signal_before_first_delivery',signalLightCost:0,defaultClose:[4,6],alternateClose:[6,4]}
  });
  if(has('weather'))Object.assign(level,{
    aftershock:{tile:[3,6],trigger:'first_delivery',closeAfter:8},
    floodRoad:{tile:[7,9],trigger:'first_delivery',closeAfter:4},
    stormWind:{trigger:'first_delivery',from:[8,8],to:[8,9]},
    quakeEvent:{trigger:'first_delivery',close:[6,7],open:[[7,7]]},
    nightfall:{trigger:'first_delivery',tile:[6,9],extraLight:1,fogRadius:3},
    dayNightCycle:{nightMoves:6,dayMoves:4,starts:'first_delivery',moonRoad:[7,8],entryChecks:'phase_before_move'}
  });
  if(has('shadows'))Object.assign(level,{
    patrol3:[[3,7],[3,8],[4,8],[4,7]],phase3:0,patrol3Wake:1,
    shadowSpawner:{trigger:'first_delivery',origin:[6,5],stages:[[6,5],[6,6],[5,5],[5,6]],growthTurns:[0,3,6],influence:'2x2'},
    mergeSplit:{mergedCells:[[5,5],[6,5],[7,5],[5,6],[6,6],[7,6],[5,7],[6,7],[7,7]],splitCells:[[5,5],[7,7]],mergeAfter:9,splitAfter:13},
    shadowInfluence2x2:{trigger:'first_delivery',origin:[7,7],cells:[[7,7],[8,7],[7,8],[8,8]],triggerCount:1},
    sentinelCenter:[5,8],hunterDen:[0,0],shadowDoor:[8,6],shadowLock:[5,5],lockPatrol:1
  });
  if(has('circuit'))Object.assign(level,{
    rechargeHouse:[3,8],rechargeAmount:4,leechPatrol:1,
    lumenNetwork:{sourceHouseIndex:0,relayTile:[3,3],charge:2,sealedUntilSource:true},
    lightTransfer:{source:[2,2],receiver:[4,8],storedLight:1,mode:'automatic_split_and_pickup'},
    lightOverloadGate:{tile:[8,3],minLight:0,maxLight:66,check:'light_after_entry',opens:'always_if_in_range'},
    transitLink:{stops:[[3,7],[8,7]],rideLight:2,unlocks:'first_delivery'},
    chainEvent:{trigger:'second_delivery',close:[7,3],open:[[7,7]]}
  });
  window.LLCRegression={level,scenario,options};
})();
