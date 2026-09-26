"""Larger route puzzles for the second hundred, with verified no-repair routes."""
import random

def build_extended(price):
    levels=[]
    for n in range(101,201):
        rng=random.Random(n*9187)
        tier=(n-101)//20
        size=10+2*tier
        # Winding delivery lanes, separated by walls, with a return road.
        rows=list(range(1,size-1,2))
        if len(rows)%2: rows=rows[:-1]
        route=[[0,rows[0]],[1,rows[0]]]
        cursor=2
        for i,y in enumerate(rows):
            endpoint=rng.randrange(size-4,size-1) if i%2==0 else rng.randrange(2,5)
            xs=range(cursor,endpoint+1) if i%2==0 else range(cursor,endpoint-1,-1)
            route.extend([[x,y] for x in xs])
            if i<len(rows)-1:
                x=route[-1][0]
                route.append([x,y+1])
                cursor=x
        y=rows[-1]
        route.extend([[x,y] for x in range(route[-1][0]-1,-1,-1)])
        route.extend([[0,t] for t in range(y-1,rows[0],-1)])
        # Rotate and reflect entire boards to vary navigation.
        def transform(p):
            x,y=p
            if n%2:x=size-1-x
            if n%3:y=size-1-y
            if n%4<2:x,y=y,x
            return [x,y]
        route=list(map(transform,route))
        depot=route[0];length=len(route)
        house_count=4+tier
        picks=[round(length*(i+1)/(house_count+1))+rng.choice([-1,0,1]) for i in range(house_count)]
        homes=[route[i] for i in picks]
        used={tuple(p) for p in [depot,*homes]}
        def feature(index):
            for j in range(index,length-1):
                if tuple(route[j]) not in used:
                    used.add(tuple(route[j]));return route[j]
        switch=feature(picks[0]+2)
        si=route.index(switch)
        gate=feature(si+2)
        fade=feature(round(length*.45))
        ice=feature(round(length*.7))
        dark=feature(round(length*.8))
        spine=route+[depot]
        activation=picks[0]
        patrols=[]
        squares=[]
        for y in range(size-1):
            for x in range(size-1):
                sq=[[x,y],[x+1,y],[x+1,y+1],[x,y+1]]
                if any(p in homes or p==depot for p in sq):continue
                overlap=sum(p in route for p in sq)
                if overlap:
                    for phase in range(4):
                        if all(spine[t]!=sq[(phase+t-activation)%4] and spine[t]!=sq[(phase+t-activation-1)%4] for t in range(activation+1,len(spine))):
                            squares.append((overlap,sq,phase));break
        rng.shuffle(squares);squares.sort(key=lambda v:-v[0])
        for _,sq,phase in squares:
            if any(set(map(tuple,sq)) & set(map(tuple,other[0])) for other in patrols):continue
            patrols.append((sq,phase))
            if len(patrols)==2:break
        assert len(patrols)==2
        open_tiles=set(map(tuple,route))|set(map(tuple,patrols[0][0]+patrols[1][0]))
        walls={f'{x},{y}' for y in range(size) for x in range(size) if (x,y) not in open_tiles}
        # Extra loops between separated lanes offer shorter but timed alternatives.
        shortcuts=[]
        for y in range(1,size-1):
            for x in range(1,size-1):
                if f'{x},{y}' in walls:
                    opposite=(((x-1,y) in open_tiles and (x+1,y) in open_tiles) or ((x,y-1) in open_tiles and (x,y+1) in open_tiles))
                    if opposite:shortcuts.append([x,y])
        rng.shuffle(shortcuts)
        repair_tile=shortcuts[0] if shortcuts else None
        for p in shortcuts[1:2+min(3,tier)]:walls.discard(f'{p[0]},{p[1]}')
        repair={'tile':repair_tile,'name':'Reopen delivery passage','band':'R','cost':price(n,'R'),'effect':'open','stepsSaved':None} if repair_tile else None
        # Light margin shrinks within each chapter; houses replenish two lights.
        cap=length+1-2*house_count+max(1,4-(n-101)%20//5)
        level={'n':n,'chapter':(n-1)//10+1,'grid':size,'brief':f'Light all {house_count} houses. Plan the winding streets, gate timing and return route.',
               'depot':depot,'homes':[{'p':p,'name':f'Outpost {i+1}','points':420+60*i+20*tier} for i,p in enumerate(homes)],
               'walls':sorted(walls),'repair':repair,'fade':fade,'ice':ice,'dark':dark,'switch':switch,'gate':gate,
               'echo':True,'patrol':patrols[0][0],'phase':patrols[0][1],'patrol2':patrols[1][0],'phase2':patrols[1][1],
               'cap':cap,'spine':spine,'required':house_count,'bonus':500+100*tier}
        assert len(set(map(tuple,route)))==len(route)
        assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(spine,spine[1:]))
        levels.append(level)
    return levels
