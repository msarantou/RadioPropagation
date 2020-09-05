"""

 DESCRIPTION
 This class controls the Transmitter/Receiver topology. 
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
        elementPositions: a vector [x,y] which contains the position of each array's antenna allocated along y axis
    
   * Function Track()
     Calculates the MT's track.
        track: a vector [x,y] which contains the positions of the MT along its track for each antenna element
    
"""

import numpy as np

class Transceiver():

    def __init__(self,mode,nAntennas,spacing,position,simulation_par):

        self.mode = mode
        self.nAntennas = nAntennas
        self.spacing = spacing
        self.position = position
        self.lamda = simulation_par.lamda
        self.Nsamples = simulation_par.Nsamples
        self.velocity = simulation_par.V
        self.ts = simulation_par.ts
        self.elementPositions = np.zeros((self.nAntennas,2))
        if (self.mode == 1):
            self.C = np.zeros((self.nAntennas,self.Nsamples,2))        

  
    def elementPositionsCalc(self):                                    
                                                                       
        halfWidth = self.nAntennas//2
        j = -halfWidth

        for i in range (self.nAntennas):
            # Allocate MT's antennas along y axis
            self.elementPositions[i,:] = [self.position[0],self.position[1]-j*self.spacing]
            j+=1

        if (self.mode == 1):

          self.r = (2*(self.lamda/2)**2)/self.lamda
          
    
    def Track(self):
    
        if (self.mode == 1): 
          
          for i in range (self.nAntennas):
                # Initial Position of each MT's antenna element 
                self.C[i,0,:] = [self.elementPositions[i,0],self.elementPositions[i,1]]
            
          for i in range (self.nAntennas):
                for j in range (1,self.Nsamples):
                      # Update Position of each MT's antenna element  
                      self.C[i,j,:] = [self.C[i,j-1,0]+self.velocity[0]*self.ts,self.C[i,j-1,1]+self.velocity[1]*self.ts]
                  

        else:
            print ("??? Error: A moving BS is not supported!")
    