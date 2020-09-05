#!/usr/local/bin/python3
import netCDF4 as nc
import os
import pair as pr
import random
import numpy as np


    





# dictionary = {"T"+str(i)+"R"+str(i):i for i in range (10) }
# print(dictionary)

# dist_BS_SC_MS = []
# Nsnapshots = 10
# N_Tx = 2
# N_Rx = 2
# tries = 50
# Nlinks = 0
# for ts in range(Nsnapshots):
#     for t in range (N_Tx):
#         for r in range (N_Rx):
#             for i in range (tries):
#                 xx = random.randint(0, 10)
#                 if (xx>5):
#                     dist_BS_SC_MS.append(pr.MyLink("snap"+str(ts),"Tx"+str(t),"Rx"+str(r),"Link"+str(Nlinks)))
#                     totDist = xx
#                     dist_BS_SC_MS[-1].makepair(totDist,None)
#                     Nlinks = Nlinks+1

    

H = [[1,2],[3,4]]
rank = np.linalg.matrix_rank(H)
print(rank)