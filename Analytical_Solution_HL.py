# Capacity Analytical Solution 

import Simulation_Parameters as sp
import Transceiver as tr
import Scatterers as sc
import matplotlib.pyplot as plt

# Basic parameters for the simulation 

# parameters = sp.SimulationParameters(2e9,0,8,[10,0,0],5)     


# # Transmitter Topology

# tx = tr.Transceceiver(0,3,parameters.lamda,[-500,0,0],parameters)               # Call for Transceiver.py class                  
# tx.elementPositionsCalc()                                                       # Allocate BS antennas in space                                            
# plt.plot(tx.elementPositions[:,0],tx.elementPositions[:,1],'k^')
# plt.title('BS Antennas Position')
# plt.xlabel('x [m]')
# plt.ylabel('y [m]')


# # Receiver Topology

# rx = tr.Transceceiver(1,3,parameters.lamda,[-2,0,0],parameters)                 # Call for Transceiver.py class             
# rx.elementPositionsCalc()                                                       # Allocate MT antennas in space                                            
# plt.plot(rx.elementPositions[:,0],rx.elementPositions[:,1],'r^')
# plt.title('MT Antennas Position')
# plt.xlabel('x [m]')
# plt.ylabel('y [m]')

# rx.Track()                                                                      # MT's Track 
# plt.plot(rx.track[:,0],rx.track[:,1])
# plt.title('MT Track')
# plt.xlabel('x [m]')
# plt.ylabel('y [m]')


# Point Scatterers over a circle

scat = sc.PointScatterers(100,100)
plt.plot(scat.SCx,scat.SCy,'k*')
plt.title('Point Scatterers')
plt.xlabel('x [m]')
plt.ylabel('y [m]')











plt.show()   
