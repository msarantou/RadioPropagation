import numpy as np

class TransReceiver:
    #mode: 0=Tx, 1=Rx

    def __init__(self,mode,nAntennas,velocity,position,spacing,Nsamples,ts):
        self.mode = mode
        self.nAntennas = nAntennas
        self.position=position
        self.velocity=velocity
        self.spacing=spacing
        self.elementPositions = np.zeros((nAntennas,3))
        self.Nsamples=Nsamples
        self.ts=ts
        self.track=np.zeros((Nsamples,3))
        

    def elementSpacingCalc(self):

        halfWidth = self.nAntennas//2
        j=-halfWidth
        #only in Y
        for i in range (self.nAntennas):
            
            self.elementPositions[i,0]=self.position[0]
            self.elementPositions[i,1]=self.position[1]-j*self.spacing
            self.elementPositions[i,2]=self.position[2]
            j+=1
            
    def Track(self):
        
        px=self.position[0]
        py=self.position[1]
        pz=self.position[2]

        for i in range(self.Nsamples):
            self.track[i,:]=[px+self.velocity[0]*self.ts,
                    py+self.velocity[1]*self.ts,  pz+self.velocity[2]*self.ts]
            
            print(px,py,pz)
            px=self.track[i,0]
            py=self.track[i,1]
            pz=self.track[i,2]


    








tx=TransReceiver(0,3,[1,1,1],[0,0,0],0.15,100,1)
tx.elementSpacingCalc()
tx.Track()





