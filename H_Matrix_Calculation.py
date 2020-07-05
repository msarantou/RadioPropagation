"""

 DESCRIPTION
 This class calculates the signal's complex envelope and produces the channel matrix H. 
 
 
    
"""

import numpy as np

class Channel():

    def __init__(self,NSC,N_Rx,N_Tx,snapshots,distBS_SC_MT):

        self.NSC = NSC
        self.N_Rx = N_Rx
        self.N_Tx = N_Tx
        self.snapshots = snapshots
        self.distBS_SC_MT = distBS_SC_MT
    

    def Envelope(self):

        self.ray = np.zeros(self.N_Rx,self.N_Tx,self.NSC,self.snapshots)
        for i in range (self.N_Rx):
            for j in range (self.N_Tx):
                for k in range ()



