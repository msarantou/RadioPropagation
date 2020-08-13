"""

 DESCRIPTION
 This class controls the Transmitter topology. 
 Currently, the array antennas could be allocated only along y axis.

 Inputs:
   mode:           0 for Transmitter, 1 for Receiver
   nAntennas:      Number of array antennas 
   spacing:        The spacing between the array antennas 
   position:       The vector for the BS position or the MT's initial position in cartesian coordinates [x,y,z] in [m]
   simulation_par  The parameters calculated in the class "Simulation_Parameters.py"


 Outputs:
   * Function elementPositionsCalc()
     Allocate the array's antennas (only along y axis) in the 3D cartesian space for the Tx/Rx, 
     in respect to the antenna spacing and Tx/Rx initial position.
        elementPositions: a vector [x,y,z] which contains the position of each array's antenna allocated along y axis

"""

import numpy as np

class Transceiver():

    def __init__(self,mode,nAntennas,spacing,position,simulation_par):

        self.mode = mode
        self.nAntennas = nAntennas
        self.spacing = spacing
        self.position = position
        lamda = simulation_par.lamda
        self.elementPositions = np.zeros((self.nAntennas,3))
        

  
    def elementPositionsCalc(self):                                    
                                                                       
        halfWidth = self.nAntennas//2
        j = -halfWidth

        for i in range (self.nAntennas):
            # Allocate MT's antennas along y axis
            self.elementPositions[i,:] = [self.position[0],self.position[1]-j*self.spacing,self.position[2]]
            j+=1

        if (self.mode == 1):
              # self.r = (2*(lamda/2)**2)/lamda
          self.r = 11
          self.C = self.elementPositions
