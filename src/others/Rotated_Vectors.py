# Code to calculate the reflected vector via rotated vectors (we find the angle of reflection a, 
# in respect to N, and we rotate the incident vector by 2a)

import numpy as np
import random
from numpy import sqrt,cos,sin
import math




def Rotate(Vec1,phi,axis):
    
    
    if axis=="X":
        base=[1,0,0]
        A=[[1,         0,            0],
           [0,np.cos(phi),-np.sin(phi)],
           [0,np.sin(phi),np.cos(phi) ]
            ]


    if axis=="Z":
        base=[0,0,1]
        A=np.zeros((3,3))
        A[0,:]=[np.cos(phi),-np.sin(phi), 0]
        A[1,:]=[np.sin(phi),np.cos(phi),  0]
        A[2,:]=[0,         0,             1 ]
        Vec2=[0,0,0]
        Vec2[0]=Vec1[0]*A[0,0] + Vec1[1]*A[0,1]+Vec1[2]*A[0,2]
        Vec2[1]=Vec1[0]*A[1,0] + Vec1[1]*A[1,1]+Vec1[2]*A[1,2]
        Vec2[2]=Vec1[0]*A[2,0] + Vec1[1]*A[2,1]+Vec1[2]*A[2,2]

    return Vec2


# Layout
A = [0,0]
theta = np.pi/4
C = [19,18]
r = 1  
B = [cos(theta),sin(theta)]

# Find the intersection point
L = np.subtract(A,C)
a = np.dot(B,B)
b = 2*np.dot(B,L)
c = np.dot(L,L)-r**2
delta = b*b-4*a*c
delta = round(delta,2)
t1 = (-b+sqrt(delta))/(2*a)
t2 = (-b-sqrt(delta))/(2*a)
t=t2
x = A[0] + t*B[0]
y = A[1] + t*B[1]
P = [x,y]
print("Intersection Point P =",P)

# Find the N vector
N = np.abs(np.subtract(P,C))
Nnorm = sqrt( (N[0])**2 + (N[1])**2 )
N /= Nnorm
print("Normal Vector N =",N)

# Define the Incident Ray
Ri = [B[0],B[1]]
Rinorm = sqrt(Ri[0]**2+Ri[1]**2)
print("Incident Ray: Ri=",Ri)

# Find the angle between the Ri,N --> a
dot = np.dot(N,Ri)
print("Dot Product:",dot)
rat = dot/(Nnorm*Rinorm)
print("rat",rat)
a = math.acos(rat)
print("a=",a*180/np.pi)

# # Ri = [A[0]*B[0],A[1]*B[1]]
# # print("Ri=",Ri)
# f = 2*(np.dot(Ri,N))*N 
# Rr = np.subtract(Ri,f)
# print("Rr=",Rr) 

# Rotate the Ri by 2a to find the Rr
print("-------------------")
Vec1=[Ri[0],Ri[1],0]
print(Vec1)
print(Rotate(Vec1,-2*a,"Z"))
print("--------------------")

print(delta)







