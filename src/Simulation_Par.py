"""

 DESCRIPTION
 This class controls the simulation options and calculates basic constants.

 Inputs:
   fc:             Center Frequency in [Hz]
   


 Outputs:
   lamda:          Wavelength in [m]
   k:              Wavenumber in [m^-1]
 
"""

import numpy as np

class SimulationParameters:

    
    def __init__(self,fc):

        c = 3e8                                                     # Speed of light [m/s] 
        self.fc = fc                                                                                                       
        self.lamda = c/self.fc                                      
        self.k = 2 * np.pi/self.lamda                                    
                                   



    
