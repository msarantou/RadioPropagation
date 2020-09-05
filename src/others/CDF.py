import numpy as np
from numpy import hstack

def fCDF(A):
    a,b=np.histogram(A,100)
    
    #pad a
    c=np.zeros(len(a)+2)
    c[0]=0
    c[-1]=0
    c[1:-2]=a[0:-1]
    a=c
    step=b[1]-b[0]

    #pad x    
    x=np.zeros(len(b)+2)        
    x[0]=b[1]-step/2
    x[-1]=b[int(len(b)-1)]  +step/2
    x[1:-2]=b[0:-1]
    y=np.cumsum(a)

    return x,y
