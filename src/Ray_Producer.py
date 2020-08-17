"""

 DESCRIPTION
 This class produces the Transmitted Rays interval for the tracing and check if there are Intersection Points 
 with the Circular Scatterers and/or the Receiver. We assume that Rays are generated only throughout the HPBW 
 interval and only one bounce via a Scatterer is feasible. 
 

 Inputs:
   r:                   The choosen radius, the r-compontent of the sperical coodinates in [m]
   theta:               The 1D array for the theta scanning interval: contains all theta values
   phi:                 The choosen value for the azimuth angle in [rad]
   U:                   The 1D array for the Radiation Intensity (U) in [W/unit solid angle], as it evaluated 
                        in "Antenna_Pattern" class for the given r, theta interval, phi  
   

 Outputs:
   * Function evaluateRays()
     This function define the anglular (theta) interval in which rays will be generated, and calculate the HPBW for the antenna.
        thetaHPBW:      The angle (theta) interval where rays are generated. 
        HPBW:           The Half Power BeamWidth in [rad]. Since the U(theta) represents the power pattern, 
                        to find the half-power beamwidth we have to find the anglular interval in which U > Umax/2.
   

   * Function intersection(A,B,C,radius,bounce)
     This function is called to check for Intersection Points between a line (a Ray) and a circle (Scatterer or Receiver).
     The Ray-Circle Intersection method is applied. It receives as input the Ray's origin (A), the Ray's direction vector (B) 
     and the center, radius of each Circular object. If there are two Intersection Points, we choose one of those randomly. 
     If there is an Intersection Point between the Transmitted Ray - Scatterer, the function returns (bounce=True):
        x,y,Rr:        The x,y components of the Intersection Point and the Direction vector of the Reflected Ray.
     If there is an Interection Point between the Scatterer - Receiver, the function returns (bounce=False):
        x,y:           The x,y components of the Intersection Point
   
        
    

   
"""

import numpy as np
import random
from numpy import sqrt

class Ray():

    def __init__(self,r,theta,phi,U):
        
        self.r = r
        self.theta = theta
        self.phi = phi
        self.U = U
    

    def evaluateRays(self):

        maxU = np.amax(self.U)
        # Find all theta values for the indices in which U > Umax/2
        self.thetaHPBW = (self.theta[np.nonzero(self.U>maxU/2)])                               
        self.HPBW = (np.amax(self.thetaHPBW)+np.abs(np.amin(self.thetaHPBW)))


    def intersection(self,A,B,C,radius,bounce):
          
          L = np.subtract(A,C)
          a = np.dot(B,B)
          b = 2*np.dot(B,L)
          c = np.dot(L,L)-radius**2
          delta = b*b-4*a*c
          delta = round(delta,2)
          if (delta)>=0:
                # Calculate the Intersection Point P[x,y] (hit point)
                t1 = (-b+sqrt(delta))/(2*a)
                t2 = (-b-sqrt(delta))/(2*a)
                t = random.choice([t1, t2]) 
                x = A[0] + t*B[0]
                y = A[1] + t*B[1]
                # Calculate the Reflected Direction Vector Rr 
                if (bounce == True):
                      P = [x,y]
                      N = np.abs(np.subtract(P,C))
                      Nnorm = sqrt( (N[0])**2 + (N[1])**2 )
                      N /= Nnorm
                      Rinorm = sqrt(B[0]**2+B[1]**2)
                      dot = np.dot(N,B)
                      Rr = np.subtract(B,2*(np.dot(B,N))*N)
                      return x,y,Rr
                else:
                      return x,y
          else:
                if (bounce == True):
                      return(False, False, False)
                else:
                      return (False,False)

       
               
                
                      
                      

          
