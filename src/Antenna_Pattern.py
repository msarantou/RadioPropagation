"""

 DESCRIPTION
 This class define the antenna type for the BS. Currently, only Finite Dipole Antennas are available 
 and the simulation is 2D. That means that only polar radiation patterns are allowed: only the elevation 
 angle θ is varied, when phi and r are constant.

 Inputs:
   type:           0 for Dipole Antenna
   length:         The total length of the Dipole as a fraction of wavelength (e.g length=1/2 corresponds to l=λ/2)
   I0:             Μax current in antenna structure in [A]
   mode:           0 for Vertical, 1 for Horizontal Polarized Dipole
   theta:          An 1D array for the theta scanning interval: contains all theta values in [rad]
   phi:            A value for the azimuth angle (e.g. phi=0) in [rad]
   r:              The radius, the r-compontent of the sperical coodinates (r>=(2*D^2)/λ) in [m]
   lamda:          Wavelength in [m]
   
   

 Outputs:
   * Function radiationPattern()
     Evaluate the Radiation Intensity (U) in [W/unit solid angle] and the Radiated Power (Prad) in [W] 
     for any antenna length for the above theta interval, phi, r (spherical coordinates).

"""

import numpy as np
from numpy import sin ,cos ,sqrt,arccos,arctan
import matplotlib.pyplot as plt

class Antenna():

    def __init__(self,type,length,I0,mode,r,theta,phi,lamda):

        self.type = type
        self.length = length
        self.I0 = I0
        self.mode = mode
        self.theta = theta
        self.lamda = lamda
        self.l = self.lamda*self.length                                                 
        self.r = r
        self.phi = phi
        self.U = np.zeros(len(theta))
        self.P = np.zeros(len(theta))
    

    # Mode 0: Finite Dipole Antenna
    # A function to evaluate Radiation Intensity (U) and Radiated Power (Prad) for the Far Field

    def radiationPattern(self):

        if (self.r ==0):
            print("??? Error: Rho cannot be zero")
            return nan
        n = 120*np.pi                                                                 # Eta: Intrinsic Impedance of the medium (air) n = (μο/εο)^0.5
        B0 = (n*self.I0**2)/(8*np.pi**2)
        if self.mode == 0 :
            theta0 = np.pi/2
        else:
            theta0 = 0   
        f = (2*np.pi)
        self.U = B0*(((cos(np.pi*cos(theta0-self.theta)*self.l/self.lamda)-cos(np.pi*self.l/self.lamda)))/sin(theta0-self.theta))**2        
        self.P = self.U/(self.r**2)                                                                  

    





