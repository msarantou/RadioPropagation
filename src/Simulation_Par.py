"""

 DESCRIPTION
 This class controls the simulation options and calculates basic constants.

 Inputs:
   fc:             Center Frequency in [Hz]
   F:              Sampling rate as a fraction of wavelength for the MT's track
                     Sampling rate describes the number of samples per wavelenght. 
                     To fulfill the sampling theorem the minimum sample desnity must be 2.
   V:              The vector for the velocity of the MT [Vx,Vy] in [m/s] 
   dist:           The total length of MT track in [m]  


 Outputs:
   lamda:          Wavelength in [m]
   k:              Wavenumber in [m^-1]
   Dx:             Sampling spacing in [m]
   ts:             Time sampling interval in [s]   
   fs:             Sampling frequency in [Hz]
   Nsamples:       Number of samples along the MT track 


"""

import numpy as np

class SimulationParameters:

    
    def __init__(self,fc,F,V,dist):

        c = 3e8                                                     # Speed of light [m/s] 
        self.fc = fc                                                                                                       
        self.lamda = c/self.fc                                      
        self.k = 2 * np.pi/self.lamda   
        self.F = F                                                       
        self.V = V  
        self.dist = dist
        self.speed = np.sqrt(self.V[0]**2+self.V[1]**2)                                                      
        self.Dx = self.lamda/self.F                                      
        self.ts = self.Dx/self.speed                                         
        self.fs = 1/self.ts                                              
        self.Nsamples = int(self.dist/self.Dx)                                      
                                   
                              



    
