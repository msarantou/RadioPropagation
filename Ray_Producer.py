"""

 DESCRIPTION
 This class produces the Transmitted Rays interval for the tracing and check if there are Intersection Points 
 with the Circular Scatterers. We assume that Rays are generated only throughout the HPBW interval. 
 

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
   

   * Function intersection(A,B,scat)
     This function is called for each Transmitted Ray, and check if it has Intersection Points with all the Scatterers.
     The Ray-Sphere Intersection method is applied. It receives as input the Ray's origin (A), the Ray's direction vector (B) 
     and all the Circular_Scatterers parameters.
        nPoints:        How many Intercection Points a single Ray hitted with all the Scatterers. 
   
"""

import numpy as np

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


    def intersection(self,A,B,scat):
          
          NSC = scat.NSC
          a = np.dot(B,B)
          nPoints = 0
          for jj in range (NSC):
                
                Cx = scat.CSCx[jj]
                Cy = scat.CSCy[jj]
                # x-y coordinates for the Center of each Circular Scatterer
                C = [Cx,Cy]
                b = 2*np.dot(B,np.subtract(A,C))
                c = np.dot(np.subtract(A,C),np.subtract(A,C))-scat.radius**2
                if (b**2-4*a*c)>=0:
                      nPoints+= 1
          return(nPoints)
          
                      
                
                      
                      

          
