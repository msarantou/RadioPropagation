# 2D Ray Tracing Single Bounce
#!/usr/local/bin/python3
import numpy as np
from numpy import sin ,cos ,sqrt,arccos,arctan
import Simulation_Par as sp
import Transceivers as tr
import Antenna_Pattern as ap
import Ray_Producer as rp
import Circular_Scatterers as sc
import config
import pair as pr
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
from Output import Save, OpenFile
import netCDF4 as nc

# The file in which all outputs are stored
file="../Output/Output.nc"

## Basic parameters for the simulation: Call for Simulation_Par Class 
parameters = sp.SimulationParameters(config.fc,config.F,config.V,config.dist)                        
lamda = parameters.lamda

## Transmitter Topology: Call for Transceivers class
tx = tr.Transceiver(config.Tmode,config.TnAntennas,config.Tspacing,config.Tposition,parameters)                                   
tx.elementPositionsCalc()                                                       
BSx = tx.elementPositions[:,0]       
BSy = tx.elementPositions[:,1] 
N_Tx = tx.nAntennas 
OpenFile(file)
success = Save(file,"BS","BSposx","BSposy",BSx,BSy)
if (not success):
    sys.exit("Error writing file")

## Transmitter's Radiated Power in Far Field: Call for Antenna_Pattern Class
antenna = ap.Antenna(config.type,config.length,config.I0,config.mode,config.r,config.atheta,config.phi,lamda)
antenna.radiationPattern()
# Radiation Intensity and Power:
U = antenna.U
P = antenna.P
Save(file,"Dipole","theta","P",config.atheta,P)

## Receiver Topology: Call for Transceivers class
rx = tr.Transceiver(config.Rmode,config.RnAntennas,config.Rspacing,config.Rposition,parameters)                                   
rx.elementPositionsCalc()    
MSx = rx.elementPositions[:,0]       
MSy = rx.elementPositions[:,1] 
N_Rx = rx.nAntennas  
Save(file,"MS","MSposx","MSposy",MSx,MSy)
rx.Track() 
for i in range (N_Rx):
    Save(file,"MStrack"+str(i),"MStrackx"+str(i),"MStracky"+str(i),rx.C[i,:,0],rx.C[i,:,1])

## Generate Circular Scatterers: Call for Circular_Scatterers Class
scat = sc.CircularScatterers(config.NSC,config.radius,config.n)
NSC = scat.NSC
CSCx = scat.CSCx
CSCy = scat.CSCy
Save(file,"SC","SCposx","SCposy",CSCx,CSCy)

## Define the Transmitted Rays Interval, find Intersection Points: Call for Ray_Producer Class
rays = rp.Ray(config.r,config.atheta,config.phi,U)
rays.evaluateRays()
print("The HPBW of the antenna is:",rays.HPBW*180/np.pi,"°")
Save(file,"Total_Rays","atheta","U",config.atheta,U)
# All theta values from which rays are regarder to be generated:
thetaInterval = rays.thetaHPBW
Save(file,"Transmitted_Rays","thetaInterval","None",thetaInterval,None)

total = 0
# Check for Intersection Point between Tx - Scatterer
# The total number of Transmitted Rays:
Nrays = len(thetaInterval)
# Distance Tx-Scatterer:
distBS_SC = []
# P:x,y components for the Intersection Point 
P = []
# Br for the Direction vector of the Reflected Ray
Br = []
bounce = True
for t in tqdm(range (N_Tx)):
    P.append(pr.MyPair("Tx"+str(t),rx = None))
    Br.append(pr.MyPair("Tx"+str(t),rx = None))
    distBS_SC.append(pr.MyPair("Tx"+str(t),rx = None))
    # Rays origin is:
    A = [BSx[t],BSy[t]]
    for i in range(Nrays):
        # Direction vector for any line 
        B = [cos(thetaInterval[i]),sin(thetaInterval[i])]
        for jj in range (NSC):
            # coordinates for the Center of each Circular Scatterer
            C = [CSCx[jj],CSCy[jj]]
            x,y,Rr = rays.intersection(A,B,C,scat.radius,bounce)
            if (x!=False):
                P[t].makepair(x,y)
                Br[t].makepair(Rr[0],Rr[1])
                distBS_SC[t].makepair(sqrt(((BSx[t]-x)**2) + ((BSy[t]-y)**2)),None)

# Check for Intersection Point between Scatterer - Receiver
# Overall Distance Tx-Scatterer-Rx:
dist_BS_SC_MS = []
lx=[]
ly=[]
bounce = False 
# plot1 = plt.figure(1)
for t in range (N_Tx):
    for r in range (N_Rx):
        for i in range (len(P[t].data)):
            xx,yy = rays.intersection(P[t].data[i].get(),Br[t].data[i].get(),[MSx[r],MSy[r]],rx.r,bounce)
            if (xx!=False):
                hitX,hitY = P[t].data[i].get()
                distSC_MT = (sqrt(((hitX-MSx)**2) + ((hitY-MSy)**2)))
                dist_BS_SC_MS.append(pr.MyPair("Tx"+str(t),"Rx"+str(r)))
                totDist = distBS_SC[t].data[i].get()[0]+distSC_MT 
                dist_BS_SC_MS[-1].makepair(totDist,None)
                lx.append(BSx[t])
                ly.append(BSy[t])                
                lx.append(hitX)
                ly.append(hitY)
                lx.append(MSx[r])
                ly.append(MSy[r])
Save(file,"Links","lx","ly",lx,ly)
                
                    
