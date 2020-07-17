"""

 DESCRIPTION
 This class produce the transmitted rays for the tracing. We assume that rays are generated only throughout 
 the HPBW interval.

 Inputs:
   r:                   The choosen radius, the r-compontent of the sperical coodinates in [m]
   theta:               The 1D array for the theta scanning interval: contains all theta values
   phi:                 The choosen value for the azimuth angle in [rad]
   U:                   The 1D array for the Radiation Intensity (U) in [W/unit solid angle], as it evaluated 
                        in "Antenna_Pattern" class for the given r, theta interval, phi  
   

 Outputs:
   * Function evaluateRays()
        thetaHPBW:      The angle (theta) interval where rays are generated. Since the U(theta) 
                        represents the power pattern, to find the half-power beamwidth we have 
                        to find the anglular interval in which U > Umax/2.
        HPBW:           The Half Power BeamWidth in [rad]
   
"""

import numpy as np

class Ray():

    def __init__(self,r,theta,phi,U):

        self.theta = theta
        self.U = U
    

    def evaluateRays (self):

        maxU = np.amax(self.U)
        self.thetaHPBW = (self.theta[np.nonzero(self.U>maxU/2)])                               # Find the indices in which U > Umax/2
        self.HPBW = (np.amax(self.thetaHPBW)+np.abs(np.amin(self.thetaHPBW)))

