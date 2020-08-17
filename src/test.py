

import numpy as np 
import random
# import pair as pr
import pair as pr
 


NT=3
NR=1
NSC=3


p=[]

for i in range(NT):
    a=pr.Hits("TR"+str(i)) 
    p.append(a)
    
    for j in range(NR):
    
        for k in range(NSC):

            
            hits=random.randint(10,20) 
            x=random.randint(1,100)
            y=random.randint(1,100)


            p[i].makepair(x,y)
































