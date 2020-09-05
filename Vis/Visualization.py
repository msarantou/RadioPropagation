#!/usr/local/bin/python3
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import sys,re,os


if (len(sys.argv))<3:
    print("Usage: ./Visulation.py  <SimulationSetup.nc> <Timestep???.nc>")
    sys.exit()
filename = sys.argv[1] 
tsfilename = sys.argv[2] 

### Read SimulationSetUp.nc file
fh = nc.Dataset(filename, mode='r')

# BS Layout : BS Antennas Position
BSx = fh.variables['BSposx'][:]
BSy = fh.variables['BSposy'][:]
plot1 = plt.figure(1)
plt.plot(BSx,BSy,'k^')
plt.title('Scenario Layout')
plt.xlabel('x [m]')
plt.ylabel('y [m]')


# Dipole Antenna for Transmitter
theta = fh.variables['theta'][:]
P = fh.variables['P'][:]
plot2 = plt.figure(2)
plt.plot(theta*180/np.pi,P)
plt.title('Radiated Power versus Elevation Angle')
plt.xlabel('Theta [deg°]')
plt.ylabel('P [W]')
plt.grid()

# Transmitted Rays Interval
overalltheta = fh.variables['atheta'][:]
U = fh.variables['U'][:]
radiattedTheta = fh.variables['thetaInterval'][:]
plot3 = plt.figure(3)
ax1 = plt.subplot(111, polar=True)
plt.plot(overalltheta, U,'b',label='U < Umax/2')
plt.plot(radiattedTheta, U[np.nonzero(U>(np.amax(U))/2)],'r',label='U > Umax/2 - Radiation Interval')
plt.legend(loc="center left")
plt.title('Dipole λ/2 - Radiation Intensity')

# MS Layout: MS Antennas Position
MSx = fh.variables['MSposx'][:]
MSy = fh.variables['MSposy'][:]
N_Rx = (len(MSx))
plot1 = plt.figure(1)
plt.plot(MSx,MSy,'r^')

# MS Track
plot1 = plt.figure(1)
for i in range(N_Rx):
    plt.plot(fh.variables['MStrackx'+str(i)][:],fh.variables['MStracky'+str(i)][:])                          

# Scatterers Layout: Circular Scatterers position
SCx = fh.variables['SCposx'][:]
SCy = fh.variables['SCposy'][:]
plot1 = plt.figure(1)
plt.scatter(SCx, SCy, s=0.5)

fh.close()
### 

### Read Timestep???.nc file
tsfile = nc.Dataset(tsfilename, mode='r')

# Achieved Links
plot1 = plt.figure(1)
lx = tsfile.variables['lx'][:]
ly = tsfile.variables['ly'][:]
plt.plot(lx,ly,"r",linewidth= 0.1)
imagename = int(re.search(r'\d+', tsfilename).group(0)) # get the int part of a string (filename)
imagename = str(imagename).zfill(7)
# Create the Snaps Directory into Vis Directory if does not exist
if not os.path.exists("../Vis/Snaps"):
    os.makedirs("../Vis/Snaps")
plt.savefig("Snaps/"+imagename+".png",dpi=300)

###
plt.show()