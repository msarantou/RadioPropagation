import netCDF4 as nc
import numpy as np

def OpenFile(filename):
    ncout = nc.Dataset(filename,'w',format='NETCDF4')
    ncout.close()
    return True

def Save(filename,name1,value1,value2):

    name = name1
    ncout = nc.Dataset(filename,'r+',format='NETCDF4')
    ncout.createDimension(name,len(value1))
    data1 = ncout.createVariable(name+"x",'f4',(name,))
    data1[:] = value1
    data2 = ncout.createVariable(name+"y",'f4',(name,))
    data2[:] = value2
    ncout.close()
    return True 
