import random
import numpy as np
green = [0,200,0]
black = [0,0,0]
ship_map=[green]*10+[black]*54

    
random.shuffle(ship_map)
rmap=random.sample(ship_map, len(ship_map))
#print(rmap)
#maparr=np.array([np.array(ship_mapi) for ship_mapi in ship_map])

maparr=np.array(rmap)
nmaparr=np.resize(maparr,(8,8,3))
#b=np.reshape(maparr(-1,8))
#print(nmaparr[0,0])

for x in nmaparr:
    for y in nmaparr:
        print(x,y)
        