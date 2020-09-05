# Code to calculate the reflected vector using 
# https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector

import numpy as np
import random
from numpy import sqrt,cos,sin
import math

# theta = math.atan(-1/sqrt(3))
# A =[2,0]
A = [0,0]
theta = np.pi/4
C = [19,18]
r = 1  
B = [cos(theta),sin(theta)]


L = np.subtract(A,C)
a = np.dot(B,B)
b = 2*np.dot(B,L)
c = np.dot(L,L)-r**2
delta = b*b-4*a*c
delta = round(delta,2)

t1 = (-b+sqrt(delta))/(2*a)
t2 = (-b-sqrt(delta))/(2*a)
t = t1

x = A[0] + t*B[0]
y = A[1] + t*B[1]
P = [x,y]
print("Intersection Point P =",P)

N = np.abs(np.subtract(P,C))
Nnorm = sqrt( (N[0])**2 + (N[1])**2 )
N /= Nnorm
print("Normal Vector N =",N)

Rinorm = sqrt(B[0]**2+B[1]**2)
print("Incident Ray: Ri=",B)

dot = np.dot(N,B)
print("Dot Product:",dot)

# print("rat",dot/(Nnorm*Rinorm))
# a = math.acos(dot/(Nnorm*Rinorm))
# print("a=",a*180/np.pi)

Rr = np.subtract(B,2*(np.dot(B,N))*N )
print("Rr=",Rr) 

# if Rr[1]==Rr[0]:
#     a = np.pi/4
# elif Rr[0] == 0:
#     a = np.pi/2
# else:
#     a = math.atan(Rr[1]/Rr[0])
# print("a=",a*180/np.pi)

