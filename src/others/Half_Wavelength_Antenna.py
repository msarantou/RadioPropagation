import numpy as np
from numpy import sin ,cos ,sqrt,arccos,arctan
import matplotlib.pyplot as plt

# A function to convert Cartesian to Sperical Coordinates 

def Cart2Sph(X,Y,Z):
   
    R= sqrt(X**2 + Y**2 + Z**2)
    THETA= arccos(Z/R)
    if X > 0:
        PHI = arctan(Y/X)   
    elif  X<0 and Y>=0 :
        PHI = arctan(Y/X) + np.pi
    elif X<0 and Y<0 :
        PHI = arctan(Y/X) - np.pi
    elif X==0 and Y>0 :
        PHI = np.pi/2
    elif X==0 and Y<0 :
        PHI = - np.pi/2
    elif X==0 and Y==0:
        PHI = 0
    return R,THETA,PHI

# A function to convert Sperical to Cartesian Coordinates 

def Sph2Cart(r,theta,phi):

    x = r * sin(theta) * cos(phi)                                      #
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return x,y,z


# A function to evaluate Radiation Intensity (U) and Radiated Power (Prad) for a Half-Wavelength Dipole in the Far Field

def RadiationPattern(r,theta,phi):

    if (r ==0):
        print("??? Error: Rho cannot be zero")
        return nan
    n = 120*np.pi                                                       # Eta: Intrinsic Impedance of the medium (air) n = (μο/εο)^0.5
    I0 = 1                                                              # Μax current in antenna structure
    B0 = (n*I0*I0)/(8*np.pi*np.pi)
    theta0 = np.pi/2
    U = B0*(cos(np.pi*cos(theta0-theta)/2)/sin(theta0-theta))**2        # Vertical polarized half-wave dipole Radiation Intensity (U)
    P = U/(r**2)                                                        # Radiated Power (P)
    return P,U 





















## PLOT POLAR
# theta = np.arange(-np.pi,np.pi,0.001)
# ax = plt.subplot(111, polar=True)
# plt.plot(theta, RadiationIntensity(theta, np.pi))
# plt.show()


# P=RadiationPattern(Cart2Sph(5,4,3))