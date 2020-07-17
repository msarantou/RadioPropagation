# 2D Ray Tracing

import numpy as np
from numpy import sin ,cos ,sqrt,arccos,arctan
import Simulation_Parameters as sp
import Transceiver as tr
import Antenna_Pattern as ap
import Ray_Producer as rp
import Circular_Scatterers as sc
import matplotlib.pyplot as plt
import numpy.linalg as la
import math
from pylab import *

# Basic parameters for the simulation 

parameters = sp.SimulationParameters(2e9,0,8,[10,0,0],5)    
lamda = parameters.lamda

# Transmitter Topology

tx = tr.Transceceiver(0,1,parameters.lamda,[0,0,0],parameters)                  # Call for Transceiver.py class                  
tx.elementPositionsCalc()                                                       # Allocate BS antennas in space 
BSx = tx.elementPositions[:,0]       
BSy = tx.elementPositions[:,1] 
BSz = tx.elementPositions[:,2]  
N_Tx = tx.nAntennas                                                             # Number of Tx antennas
plot1 = plt.figure(1)
plt.plot(BSx,BSy,'k^')
plt.title('BS Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

# Transmitter's Radiated Power in Far Field
# Half- Wavelength Dipole: Scanning interval for theta (atheta), phi=0 and r=(2*D^2)/λ as the minimum limit for 
# the Far Field.

atheta = np.arange((-np.pi/2)+1e-10,np.pi/2,0.01)
phi = 0
r = (2*(lamda/2)**2)/lamda
antenna = ap.Antenna(0,1/2,1,0,r,atheta,phi,lamda)
antenna.radiationPattern()
plot2 = plt.figure(2)
plt.plot(atheta*180/np.pi,antenna.P)
plt.title('Radiated Power with Elevation Angle')
plt.xlabel('Theta [deg°]')
plt.ylabel('P [W]')
plt.grid()

# Define the Transmitted rays

rays = rp.Ray(r,atheta,phi,antenna.U)
rays.evaluateRays()
print("The HPBW of the antenna is:",rays.HPBW*180/np.pi,"°")
plot3 = plt.figure(3)
ax1 = plt.subplot(111, polar=True)
plt.plot(atheta, antenna.U,'b',label='U < Umax/2')
plt.plot(rays.thetaHPBW, antenna.U[np.nonzero(antenna.U>(np.amax(antenna.U))/2)],'r',label='U > Umax/2')
plt.legend(loc="center left")
plt.title('Dipole λ/2 - Radiation Intensity')

# Circular Scatterers

NSC = 1000
r = 0.05
scat = sc.CircularScatterers(NSC,r)
CSCx = scat.CSCx
CSCy = scat.CSCy
fig, ax = plt.subplots(1, 1)
ax.scatter(CSCx, CSCy, s=scat.radius)
plt.title('Circular Scatterers')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

# Try to find the intersection point between the Rays and the Scatterers
sum = 0
A = [0,0]                                                                       # All rays origin is on (0,0)
for i in range (len(rays.thetaHPBW)):
    B = [1,-np.tan(rays.thetaHPBW[i])]
    a = np.dot(B,B)
    for j in range (NSC):
        Cx = CSCx[j]
        Cy = CSCy[j]
        C = [Cx,Cy]
        b = 2*np.dot(B,np.subtract(A,C))
        c = np.dot(np.subtract(A,C),np.subtract(A,C))-r**2
        if (b**2-4*a*c)>=0:
            sum = sum+1

print(sum)



















# plt.show()

       

