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
import sys,os
from Output import Save, OpenFile, SaveTimesteps
import netCDF4 as nc
import cmath

# Create the Output Directory if does not exist
if not os.path.exists("../Output"):
    os.makedirs("../Output")

# The file in which outputs related to the simulation layout are stored
file = "../Output/SimulationSetUp.nc"

## Basic parameters for the simulation: Call for Simulation_Par Class 
parameters = sp.SimulationParameters(config.fc,config.F,config.V,config.dist)                        
lamda = parameters.lamda
k = parameters.k

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
lx=[]
ly=[]
bounce = False 
Nsnapshots = parameters.Nsamples 
# Channel Matrix H:
H = np.zeros((Nsnapshots,N_Tx,N_Rx),dtype=complex)
for ts in tqdm(range(Nsnapshots)):
    for t in range (N_Tx):
        for r in range (N_Rx):
            # Signal's complex envelope:
            ray = []
            for i in range (len(P[t].data)):
                xx,yy = rays.intersection(P[t].data[i].get(),Br[t].data[i].get(),[rx.C[r,ts,0],rx.C[r,ts,1]],rx.r,bounce)
                if (xx!=False):
                    hitX,hitY = P[t].data[i].get()
                    distSC_MT = (sqrt(((hitX-MSx[r])**2) + ((hitY-MSy[r])**2)))
                    totDist = distBS_SC[t].data[i].get()[0]+distSC_MT 
                    ray.append(cmath.exp(-1j*k*totDist))
                    lx.append(BSx[t])
                    ly.append(BSy[t])                
                    lx.append(hitX)
                    ly.append(hitY)
                    lx.append(MSx[r])
                    ly.append(MSy[r])
            H[ts,t,r] = sum(ray)    
    # The file in which outputs for each snapshot are stored
    file = "../Output/Timestep"+str(ts).zfill(7)+".nc" 
    SaveTimesteps(file,"Links","lx","ly",lx,ly)
    lx.clear()
    ly.clear()
            
# Eigenvalues and Capacity Calculation
Neigens = min(N_Rx,N_Tx)                                                        
eigens = np.zeros((Neigens,Nsnapshots))
for j in range (Nsnapshots):
    # Singular values for each snapshot
    s = np.linalg.svd(H[j,:,:], full_matrices=False,compute_uv=False)           
    eigens[:,j] = s
# Eigenvalues
eigens = eigens**2 
eigens[:]+=1e-13   
timeaxis = np.zeros(Nsnapshots)
for i in range (Nsnapshots):
    timeaxis[i] = parameters.ts*i
plot1 = plt.figure(1)
plt.plot(timeaxis,10*np.log(eigens[0,:]),'b') 
plt.plot(timeaxis,10*np.log(eigens[1,:]),'r')
plt.plot(timeaxis,10*np.log(eigens[2,:]),'y')

plt.title('Eigenvalues versus time')
plt.xlabel('Time [s]')
plt.ylabel('Eigenvalues [dB]')
plt.grid()
plt.savefig("Eigenvalues1.png",dpi=300)
SNR = 20                                                                        # Signal to Noise Ratio in [dB]
snr = 10**(SNR/10)                                                              # Linear scale SNR
CSISO = np.log2(1+snr*(H[:,1,1]**2))                                                 # SISO Ergodic Capacity using only the first channel
CMIMO = sum(np.log2(1+(snr/Neigens)*eigens))                                    # MIMO Capacity 

plot2 = plt.figure(2)
CapS, = plt.plot(timeaxis,CSISO,label="SISO Capacity")
first_legend = plt.legend(handles=[CapS], loc='lower right')
ax = plt.gca().add_artist(first_legend)
CapM, = plt.plot(timeaxis,CMIMO,label='MIMO Capacity')
plt.legend(handles=[CapM], loc='upper right')
plt.title('Channel Capacity versus time')
plt.xlabel('Time [s]')
plt.ylabel('Capacity [bits/sec/Hz]')
plt.grid()
plt.savefig("Capacity1.png",dpi=300)


plt.show()

