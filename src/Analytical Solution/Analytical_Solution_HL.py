"""
Capacity Analytical Solution:

3x3 MIMO at 2GHz using Clarke's model. Antenna arrays are allocated along y-axis with spacing = λ. BS is stable 
[-500,0,0](m) and MT moves along x-axis with initial position [-2,0,0](m), making a straight line journey of total length 
5(m) and constant velocity 10(m/s). 100 Scatterers are randomly distributed in the 2D space (x,y) over a circle 
of radius 100 (m) and center [0,0]. Assuming SNR equal to 20[dB] the Channel Capacity is calculated and plotted 
with time. The "Uninformed Channel Capacity" approach is assumed.

"""

import Simulation_Parameters as sp
import Transceiver as tr
import Scatterers as sc
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt
import cmath

# Basic parameters for the simulation 

parameters = sp.SimulationParameters(2e9,0,8,[10,0,0],5)     
snapshots = parameters.Nsamples                                                 # Number of snapshots along MT's track

# Transmitter Topology

tx = tr.Transceceiver(0,3,parameters.lamda,[-500,0,0],parameters)               # Call for Transceiver.py class                  
tx.elementPositionsCalc()                                                       # Allocate BS antennas in space 
BSx = tx.elementPositions[:,0]       
BSy = tx.elementPositions[:,1]  
N_Tx = tx.nAntennas                                                             # Number of Tx antennas
plot1 = plt.figure(1)
plt.plot(BSx,BSy,'k^')
plt.title('BS Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

# Receiver Topology

rx = tr.Transceceiver(1,3,parameters.lamda,[-2,0,0],parameters)                 # Call for Transceiver.py class             
rx.elementPositionsCalc()                                                       # Allocate MT antennas in space  
MTx = rx.elementPositions[:,0]                                                  
MTy = rx.elementPositions[:,1]       
N_Rx = rx.nAntennas                                                             # Number of Rx antennas     
plot2 = plt.figure(2)                           
plt.plot(MTx,MTy,'r^')
plt.title('MT Antennas Position')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

rx.Track()                                                                      # MT's Track 
plot3 = plt.figure(3)
for i in range(N_Rx):
    plt.plot(rx.track[i,:,0],rx.track[i,:,1])                                   # Track of each MT's antenna in x,y axis
plt.title('MT Track')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

# Point Scatterers over a circle

scat = sc.PointScatterers(100,100,parameters.avPower)                           # Call for Scatterers.py class
SCx = scat.SCx                                                                  # Scaterrers location in x-axis
SCy = scat.SCy                                                                  # Scaterrers location in y-axis
NSC = scat.NSC                                                                  # Total number of point scatterers
plot4 = plt.figure(4)
plt.plot(SCx,SCy,'k*')
plt.title('Point Scatterers')
plt.xlabel('x [m]')
plt.ylabel('y [m]')

# Distance Matrix and Channel Matrix Calculation

distBS_SC = np.zeros((N_Tx,NSC))                                                # Distance between each BS antenna and each Scatterer
for i in range (N_Tx):
    for j in range (NSC):
        distBS_SC[i,j] = sqrt(((BSx[i]-SCx[j])**2) + ((BSy[i]-SCy[j])**2))


distSC_MT = np.zeros((N_Rx,NSC,snapshots))                                      # Distance between each MT antenna and each Scatterer for each snapshot
for i in range (N_Rx):
    for j in range (NSC):
        for k in range (snapshots):
            distSC_MT[i,j,k] = sqrt(((rx.track[i,k,0]-SCx[j])**2) + ((rx.track[i,k,1]-SCy[j])**2))


distBS_SC_MT = np.zeros((N_Rx,N_Tx,NSC,snapshots))
ray = np.zeros((N_Rx,N_Tx,NSC,snapshots),dtype=complex)
for i in range (N_Rx):
    for j in range (N_Tx):
        for k in range (NSC):
            for p in range (snapshots):
                distBS_SC_MT[i,j,k,p] = distBS_SC[j,k] + distSC_MT[i,k,p]       # Overall distance BS-MT through each Scatterer for each snapshot 
                ray[i,j,k,p] = scat.a * cmath.exp(-1j*k*distBS_SC_MT[i,j,k,p])  # Signal's Complex Envelope

H = np.sum(ray,axis=2)                                                          # Sum along axis 2 (Scatterers) which gives the overall signal                              
                                                                                # corresponds to each path, for each snapshot
                                                                                # r(N_Rx,N_Tx,snapshots)
# Eigenvalues and Capacity Calculation

Neigens = min(N_Rx,N_Tx)                                                        
eigens = np.zeros((Neigens,snapshots))
for j in range (snapshots):
    s = np.linalg.svd(H[:,:,j], full_matrices=False,compute_uv=False)           # Singular values for each snapshot
    eigens[:,j] = s
eigens = eigens**2                                                              # Eigenvalues

timeaxis = np.zeros(snapshots)
for i in range (snapshots):
    timeaxis[i] = parameters.ts*i
plot5 = plt.figure(5)
plt.plot(timeaxis,10*np.log(eigens[0,:]),'b') 
plt.plot(timeaxis,10*np.log(eigens[1,:]),'r')
plt.plot(timeaxis,10*np.log(eigens[2,:]),'y')
plt.title('Eigenvalues with time')
plt.xlabel('Time [s]')
plt.ylabel('Eigenvalues [dB]')
plt.grid()

SNR = 20                                                                        # Signal to Noise Ratio in [dB]
snr = 10**(SNR/10)                                                              # Linear scale SNR
CSISO = np.log2(1+snr*(H[1,1,:]**2))                                            # SISO Ergodic Capacity using only the first channel
CMIMO = sum(np.log2(1+(snr/Neigens)*eigens))                                    # MIMO Capacity 

plot6 = plt.figure(6)
CapS, = plt.plot(timeaxis,CSISO,label="SISO Capacity")
first_legend = plt.legend(handles=[CapS], loc='lower right')
ax = plt.gca().add_artist(first_legend)
CapM, = plt.plot(timeaxis,CMIMO,label='MIMO Capacity')
plt.legend(handles=[CapM], loc='upper right')
plt.title('Channel Capacity with time')
plt.xlabel('Time [s]')
plt.ylabel('Capacity [bits/sec/Hz]')
plt.grid()


plt.show()

