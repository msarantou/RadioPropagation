# 2D Ray Tracing

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


## Basic parameters for the simulation: Call for Simulation_Par Class 

parameters = sp.SimulationParameters(config.fc)                        
lamda = parameters.lamda


## Transmitter Topology: Call for Transceivers class

tx = tr.Transceceiver(config.mode,config.nAntennas,config.spacing,config.position,parameters)                                   
tx.elementPositionsCalc()                                                       
BSx = tx.elementPositions[:,0]       
BSy = tx.elementPositions[:,1] 
BSz = tx.elementPositions[:,2]  
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


## Define the Transmitted Rays Interval, find Intersection Points with Scatterrers: Call for Ray_Producer Class

rays = rp.Ray(config.r,config.atheta,config.phi,U)
rays.evaluateRays()
print("The HPBW of the antenna is:",rays.HPBW*180/np.pi,"°")
plot3 = plt.figure(3)
ax1 = plt.subplot(111, polar=True)
plt.plot(config.atheta, U,'b',label='U < Umax/2')
# All theta values from which rays are regarder to be generated:
thetaInterval = rays.thetaHPBW
plt.plot(thetaInterval, U[np.nonzero(U>(np.amax(U))/2)],'r',label='U > Umax/2 - Radiation Interval')
plt.legend(loc="center left")
plt.title('Dipole λ/2 - Radiation Intensity')

# The total number of Transmitted Rays:
Nrays = len(thetaInterval)
# All Rays origin is:
A = [BSx[0],BSy[0]]
# An array that stores the intersection points (the new origin of the reflected ray)
Ar = []
# An array for the new angle of reflection (90°-atheta)
a = []
for i in tqdm(range(Nrays)):
    # Direction vector for any line with origin (0,0)
    B = [1,np.tan(thetaInterval[i])]
    for jj in range (NSC):
        # x-y coordinates for the Center of each Circular Scatterer
        Cx = CSCx[jj]
        Cy = CSCy[jj]
        C = [Cx,Cy]
        t = rays.intersection(A,B,C,scat.radius)
        if (t!=False):
            Ar.append(t)
            a.append(0.5*np.pi-config.atheta[i])

# Total number of reflected rays
Nr = len(Ar)
for k in range (Nr):
    Br = [1,np.tan(a[k])]

# plt.show()

       

