# Capacity Analytical Solution 

import numpy as np
from numpy import sin ,cos ,sqrt
import matplotlib.pyplot as plt
from random import randrange
import math
import cmath

## Basic Inputs
fc =  2e9                                                             # Carrier grequency 
NSC = 100                                                             # Number of Scatterers
c = 3e8                                                               # Speed of light [m/s] 
avPower = 0                                                           # 
F = 8                                                                 # Sampling rate: fraction of wavelength
V = 10                                                                # m/s MT speed
Nsamples = 200                                                        # Number of samples

## Computed Parameters
lamda =  c/fc                                                         # Wavelength [m]
k = 2*np.pi/lamda                                                     # Wavenumber [m^-1]
a = sqrt(10**(avPower/10)/NSC)                                        # Magnitude of echoes
Dx = lamda/F                                                          # m sampling spacing
ts = Dx/V                                                             # s time sampling interval
fs = 1/ts                                                             # Hz sampling frequency
fm = V/lamda                                                          # Max Doppler shift
timeaxis = np.zeros(Nsamples)
for i in range (Nsamples):
    timeaxis = ts * i 
spaceaxis = V * timeaxis

## Topology Inputs

# Transmitter
dBS = 500
angleBS = 180;       
BSx = dBS*cos(np.radians(angleBS))                                    # Location of Transmitter x-axis
BSy = dBS*sin(np.radians(angleBS))                                    # Location of Transmitter y-axis
N_Tx = 3                                                              # Number of Tx antennas
d_Tx = lamda                                                          # Spacing between Tx antennas

BS_antenna = np.zeros(N_Tx)
j = 0
for i in range (-1,2):
    BS_antenna[j] = ((N_Tx-abs(i))*i)/2*d_Tx
    j += 1

BSxi = (BS_antenna * sin(np.radians(180))) + BSx                      # Allocate BS antennas along y axis
BSyi = (BS_antenna * cos(np.radians(180))) + BSy

# Receiver 
dMT = 200
angleMT = 0;       
MTx = dMT*cos(np.radians(angleMT))                                    # Location of Receiver x-axis
MTy = dMT*sin(np.radians(angleMT))                                    # Location of Receiver y-axis
N_Rx = 3                                                              # Number of Rx antennas
d_Rx = lamda                                                          # Spacing between Rx antennas

MT_antenna = np.zeros(N_Rx)
j = 0                                                      
for i in range (-1,2):
    MT_antenna[j] = ((N_Rx-abs(i))*i)/2*d_Rx
    j += 1

MTxi0 = (MT_antenna * sin(np.radians(180))) + MTx                     # Allocate MT antennas along y axis. MTxi0 is the initial location of the MT route
MTyi = (MT_antenna * cos(np.radians(180))) + MTy

MTxi = 
# MTxi = MTxi * spaceaxis
# MTyi = np.zeros(Nsamples)

plt.plot(BSxi,BSyi/lamda,'k^')
plt.plot(MTxi,MTyi/lamda,'r^')
plt.title('BS and MT Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [λ]')
plt.show()


# Point Scatterers : Allocate NSC random point scatterers around a circle
radius = 100

theta = np.zeros(NSC)
for x in range (NSC):
 theta[x] = randrange(0, 360)

SCx = radius * cos(np.radians(theta))                                 # Location of Scatterers x-axis
SCy = radius * sin(np.radians(theta))                                 # Location of Scatterers y-axis

plt.plot(SCx,SCy,'k*')
plt.title('Point Scatterers Allocation')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


## Distance Matrix

distBS_SC = np.zeros((N_Tx,NSC))                                      # Distance between each BS antenna and each Scatterer
for i in range (N_Tx):
    for j in range (NSC):
        distBS_SC[i,j] = sqrt(((BSxi[i]-SCx[j])**2) + ((BSyi[i]-SCy[j])**2))

distSC_MT = np.zeros((N_Rx,NSC))                                      # Distance between each MT antenna and each Scatterer
for i in range (N_Rx):
    for j in range (NSC):
        distSC_MT[i,j] = sqrt(((MTxi[i]-SCx[j])**2) + ((MTyi[i]-SCy[j])**2))

distBS_SC_MT = np.zeros((NSC,N_Rx,N_Tx))
for k in range (NSC):
    for i in range (N_Rx):
        for j in range (N_Tx):
            distBS_SC_MT[k,i,j] = distBS_SC[j,k] + distSC_MT[i,k]     # Overall distance BS-MT through each Scatterer


## Complex Envelope Calculation 

ray = np.zeros((NSC,N_Rx,N_Tx),dtype=complex)    
for k in range (NSC):
    for i in range (N_Rx):
        for j in range (N_Tx):
            ray[k,i,j] = a * cmath.exp(-1j*k*distBS_SC_MT[k,i,j])
         
r = np.sum(ray,axis=0)                                                # Sum along axis 0 (Scatterers) --> derive the overall signal corresponds to each path 


        


