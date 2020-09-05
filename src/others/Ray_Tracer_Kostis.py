# 2D Ray Tracing Single Bounce

import numpy as np
from numpy import sin ,cos ,sqrt,arccos,arctan
import Simulation_Par as sp
import Transceivers as tr
import Antenna_Pattern as ap
import Ray_Producer as rp
import Circular_Scatterers as sc
import config
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
from netCDF4 import Dataset





def History(timestep , distances,thetaInterval,SCx,SCy):

    nc=Dataset("RT_"+str(timestep)+".nc","w",format="NETCDF4")
    nc.createDimension("NumberOfHits",len(distances))
    nc.createDimension("AngleStep",len(thetaInterval))
    
    nc.createDimension("ScPositionX",len(SCx))
    nc.createDimension("ScPositionY",len(SCy))
    
    data = nc.createVariable("Distances","f4","NumberOfHits")
    data[:]=distances
    
    data= nc.createVariable("ThetaInterval","f4","AngleStep")
    data[:]= thetaInterval

    data= nc.createVariable("SCx","f4","ScPositionX")
    data[:]= SCx[:]
    
    data= nc.createVariable("SCy","f4","ScPositionY")
    data[:]= SCy[:]

    nc.close()
    
    return True




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
MSx = rx.elementPositions[:,0]       
MSy = rx.elementPositions[:,1] 
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

# The total number of Transmitted Rays:
Nrays = len(thetaInterval)
# Total distance Tx-Scatterer-Rx:
dist = []
# Rays origin is:
A = [BSx[0],BSy[0]]
for i in tqdm(range(Nrays)):
    # Direction vector for any line 
    B = [cos(thetaInterval[i]),sin(thetaInterval[i])]
    for jj in range (NSC):
        # coordinates for the Center of each Circular Scatterer
        C = [CSCx[jj],CSCy[jj]]
        # x,y for the Intersection Point Transmitted Ray-Scatterer
        x,y = rays.intersection(A,B,C,scat.radius)
        # Check for intersection point between Reflected Ray - Receiver
        if (x!=False):
            # The new origin of the Reflected Ray:
            Ar = [x,y]
            # The angle of reflection (90°-atheta):
            a = 0.5*np.pi-thetaInterval[i]
            Br = [cos(a),sin(a)]
            xx,yy = rays.intersection(Ar,Br,[rx.C[0],rx.C[1]],rx.r)
            if (xx!=False):
                distBS_SC = sqrt(((BSx[0]-x)**2) + ((BSy[0]-y)**2)) 
                distSC_MT = sqrt(((x-xx)**2) + ((y-yy)**2))
                dist.append(distBS_SC + distSC_MT)

    History("1",dist,thetaInterval,CSCx,CSCy)



       

