# This file initialize all the parameters for the simulation

import numpy as np
import Simulation_Par as sp

# Simulation_Par
fc = 2e9
F = 8
V = [10,0]
dist = 5
parameters = sp.SimulationParameters(fc,F,V,dist)                        
lamda = parameters.lamda

# Transceivers: Α Transmitter with 1 antenna element which is located to the coodinates origin
Tmode = 0
TnAntennas = 3
Tspacing = lamda
Tposition = [0,0,0]

# Antenna_Pattern: A Half- Wavelength Verical Dipole with Scanning interval for theta (atheta), phi=0 and 
#  r=(2*D^2)/λ as the minimum limit for the Far Field.
type = 0
length = 1/2
I0 = 1
mode = 0
thetaStep = 0.1
atheta = np.arange((-np.pi/2)+1e-10,np.pi/2,thetaStep*np.pi/180.0)
r = (2*(lamda/2)**2)/lamda
phi = 0

# Transceivers: Α Receiver with 1 antenna element which is located to the coodinates origin
Rmode = 1
RnAntennas = 3
Rspacing = lamda
Rposition = [20,0,0]

# Circular_Scatterers: 1000 Circular Scatterers of radius=0.05 and Scattering Coefficient=-1
NSC = 1000
radius = 0.05
n = -1

