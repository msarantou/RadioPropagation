"""

 DESCRIPTION
 This class allocate random scatterers in x-y plane. For convinience, we consider that Scatterers are not 
 just points, but they have a small radius, since with that way, it would be easier to spot an intersection 
 point between the transmitted Rays and the Scatterers. 

 Inputs:
   NSC:            Number of point scatterers
   radius:         The radius of the circle for each Circular Scatterer
   n:              Reflection Coefficient for the scatterer
   


 Outputs:
   CSCx:            An array with the location of Scatterers' center on x-axis 
   CSCy:            An array with the location of Scatterers' center on y-axis
   
"""
 
import numpy as np
from random import uniform

class CircularScatterers():
    
    def __init__(self,NSC,radius,n):
        
        self.NSC = NSC
        self.radius = radius
        self.CSCx = np.zeros(NSC)
        self.CSCy = np.zeros(NSC)
        for i in range (self.NSC):
            self.CSCx[i] = uniform(2.0, 18.0)
            self.CSCy[i] = uniform(-15.0, 15.0)
        
                                   
