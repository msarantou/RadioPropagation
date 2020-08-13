# 2D Ray Tracing Single Bounce

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

## Basic parameters for the simulation: Call for Simulation_Par Class 

parameters = sp.SimulationParameters(config.fc)                        
lamda = parameters.lamda


## Transmitter Topology: Call for Transceivers class

tx = tr.Transceiver(config.Tmode,config.TnAntennas,config.Tspacing,config.Tposition,parameters)                                   
tx.elementPositionsCalc()                                                       
BSx = tx.elementPositions[:,0]       
BSy = tx.elementPositions[:,1] 
N_Tx = tx.nAntennas                                                             
plot1 = plt.figure(1)
plt.plot(BSx,BSy,'k^')
plt.title('BS Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


## Transmitter's Radiated Power in Far Field: Call for Antenna_Pattern Class

antenna = ap.Antenna(config.type,config.length,config.I0,config.mode,config.r,config.atheta,config.phi,lamda)
antenna.radiationPattern()
# Radiation Intensity and Power:
U = antenna.U
P = antenna.P
plot2 = plt.figure(2)
plt.plot(config.atheta*180/np.pi,P)
plt.title('Radiated Power with Elevation Angle')
plt.xlabel('Theta [deg°]')
plt.ylabel('P [W]')
plt.grid()


## Receiver Topology: Call for Transceivers class

rx = tr.Transceiver(config.Rmode,config.RnAntennas,config.Rspacing,config.Rposition,parameters)                                   
rx.elementPositionsCalc()                                                       
MSx = rx.C[:,0]       
MSy = rx.C[:,1] 
N_Rx = rx.nAntennas                                                             
plot3 = plt.figure(3)
plt.plot(MSx,MSy,'k^')
plt.title('MS Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


## Generate Circular Scatterers: Call for Circular_Scatterers Class

scat = sc.CircularScatterers(config.NSC,config.radius,config.n)
NSC = scat.NSC
CSCx = scat.CSCx
CSCy = scat.CSCy
fig, ax = plt.subplots(1, 1)
ax.scatter(CSCx, CSCy, s=scat.radius)
plt.title('Circular Scatterers')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


## Define the Transmitted Rays Interval, find Intersection Points: Call for Ray_Producer Class

rays = rp.Ray(config.r,config.atheta,config.phi,U)
rays.evaluateRays()
print("The HPBW of the antenna is:",rays.HPBW*180/np.pi,"°")
plot5 = plt.figure(5)
ax1 = plt.subplot(111, polar=True)
plt.plot(config.atheta, U,'b',label='U < Umax/2')
# All theta values from which rays are regarder to be generated:
thetaInterval = rays.thetaHPBW
plt.plot(thetaInterval, U[np.nonzero(U>(np.amax(U))/2)],'r',label='U > Umax/2 - Radiation Interval')
plt.legend(loc="center left")
plt.title('Dipole λ/2 - Radiation Intensity')




# Check for Intersection Intersection Point between Tx - Scatterer
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
    P.append(pr.MyPair("Tx"+str(t)))
    Br.append(pr.MyPair("Tx"+str(t)))
    distBS_SC.append(pr.MyPair("Tx"+str(t)))
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

finaldist = []
bounce = False 


# plot1 = plt.figure(1)

for t in range (N_Tx):
    for r in range (N_Rx):
        for i in range (len(P[t].data)):
            xx,yy = rays.intersection(P[t].data[i].get(),Br[t].data[i].get(),[MSx[r],MSy[r]],rx.r,bounce)
            if (xx!=False):

                hitX,hitY=P[t].data[i].get()
                distSC_MT=(sqrt(((hitX-xx)**2) + ((hitY-yy)**2)))
                finaldist.append(pr.MyPair("Tx"+str(t)+"Rx"+str(r)))
                finaldist[-1].tx=t
                finaldist[-1].rx=r
                totDist=distBS_SC[t].data[i].get()[0]+distSC_MT 
                finaldist[-1].makepair(totDist,None)
                # ----------
                # lx=[]
                # ly=[]
                # lx.append(BSx[t])
                # ly.append(BSy[t])                
                # lx.append(hitX)
                # ly.append(hitY)
                # lx.append(MSx[r])
                # ly.append(MSy[r])
                # plt.plot(lx,ly,linewidth= 0.2)
    
                
                # ----------       
                        


# plt.plot(BSx,BSy,'k^')
# plt.plot(MSx,MSy,'r^')
# plt.scatter(CSCx, CSCy, s=0.05)
# plt.title('BS Antennas Position')
# plt.xlabel('x [m]')
# plt.ylabel('y [m]')
plt.show()

