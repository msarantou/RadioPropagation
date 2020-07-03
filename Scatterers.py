"""

 DESCRIPTION
 This class allocate random scatterers over a circle of a choosen radius. 

 Inputs:
   NSC:            Number of point scatterers
   radius:         The radius of the circle 
   


 Outputs:
   SCx:            An array with the location of Scatterers x-axis
   SCy:            An array with the location of Scatterers y-axis 
   
"""
 
import numpy as np
from random import randrange
from numpy import sin ,cos ,sqrt


class PointScatterers():

    def __init__(self,NSC,radius):
        
        self.NSC = NSC
        self.radius = radius
        theta = np.zeros(self.NSC) 
        for i in range (self.NSC):
            theta[i] = randrange(0, 360)
        self.SCx = self.radius * cos(np.radians(theta)) 
        self.SCy = self.radius * sin(np.radians(theta)) 
         
                                   
