import netCDF4 as nc
import numpy as np

# OpenFile function opens a new NetCDF4 file for writing
def OpenFile(filename):
    ncout = nc.Dataset(filename,'w',format='NETCDF4')
    ncout.close()
    return True

""" Save and SaveTimesteps functions write on the NetCDF4 file. Each time, it creats a new dimension with 2 variables.
Inputs:
   filename:       The name of the NetCDF4 file that the user wants to write on
   name1:          The name of the dimension (string)
   var1:           The name of the first variable (string) that corresponds to the former dimension
   var2:           The name of the second variable (string) that corresponds to the former dimension
   value1:         The value that corresponds to the first variable (float)
   value2:         The value that corresponds to the second variable (float)

"""
def Save(filename,name1,var1,var2,value1,value2):

    name = name1
    namedata1 = var1
    namedata2 = var2
    ncout = nc.Dataset(filename,'r+',format='NETCDF4')
    ncout.createDimension(name,len(value1))
    data1 = ncout.createVariable(namedata1,'f4',(name,))
    data1[:] = value1
    data2 = ncout.createVariable(namedata2,'f4',(name,))
    data2[:] = value2
    ncout.close()
    return True 


def SaveTimesteps(filename,name1,var1,var2,value1,value2):
    
     name = name1
     namedata1 = var1
     namedata2 = var2
     ncout = nc.Dataset(filename,'w',format='NETCDF4')
     ncout.createDimension(name,len(value1))
     data1 = ncout.createVariable(namedata1,'f4',(name,))
     data1[:] = value1
     data2 = ncout.createVariable(namedata2,'f4',(name,))
     data2[:] = value2
     ncout.close()
     return True 
