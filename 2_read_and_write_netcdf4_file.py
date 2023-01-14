#!/sr/bin/env python

###############################################################################
# Program : 
# Authors  : Jesus
# Date	  : 22 January 2023
# Purpose : Work with NetCDF4 files
##############################################################################


"""
Working with NetCDF4 files:

(2) Read, modify and write netCDF4 file - using netCDF4 library. 

"""   

  
#%%

##########################################################################
##########################################################################

#INPUT DATA 

#*.nc file     
file ="item3236_6hrly_mean_h000_2006-10_2006-11.nc"
ensemble = "*.nc"

#variables
lat = "latitude0"
long = "longitude0"
temp = "item3236_6hrly_mean"
time = "time0"

##########################################################################
##########################################################################


#%%

import os
import glob

print("....importing libraries")

import netCDF4
from netCDF4 import Dataset,num2date # or from netCDF4 import Dataset as NetCDFFile

import xarray

import numpy as np
import numpy.ma as ma
import pandas as pd

import dateutil.parser

from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import gamma, norm
from scipy.signal import detrend

from statsmodels.distributions.empirical_distribution import StepFunction

import matplotlib.pyplot as plt    
import seaborn as sns

print("All libraries imported")



#%%

# get folder location of script
cwd = os.path.dirname(__file__) 

folder = cwd+"/DATA"

os.chdir(folder)

#%%
###########################################################

#Basic function for netCDF4 files: 
    
###########################################################

def print_variables(data):
    """prints variables in netcdf Dataset
    only works if have assigned attributes!"""
    for i in data.variables:
        print(i, data.variables[i].units, data.variables[i].shape)
        


#%%   

####################################################

##code 1 - read netCDF4 file

####################################################

#Open using netCDF library: 
    
data = Dataset(file, mode='r', format="NetCDF")

data_temp = data.variables[temp][:,0,:,:]
data_lat = data.variables["latitude0"][:]
data_long = data.variables["longitude0"][:]
data_time = data.variables["time0"][:]


#%%   

####################################################

##code 2 - change lon from (0-360) to (-180-180)

####################################################

######To change lon values to plot with Spain in centre
#lon[lon>180]-=360
def long_change(temp,long):
    ###  Section added ################
    # map lon values to -180..180 range
    f = lambda x: ((x+180) % 360) - 180
    lon = f(long)
    # rearange data
    ind = np.argsort(lon)
    long1 = lon[ind]
    temp1 = temp[:,:,ind]     #check how many indices - temp[:,:,ind] or - temp[:,ind]
    return temp1, long1

#Change long for normal projection 
data_temp1, data_long1 = long_change(data_temp,data_long)

#%%  

####################################################

##code 3 - convert from K to ºC

####################################################

#Convert from Kelvin to Degree C
data_temp1 = data_temp1[:,:,:] - 273.15


#%%

####################################################

##code 4 - Save file with new long format and temperature value in ºC

####################################################

data = Dataset(file, mode='r', format="NetCDF")

##### create dimensions for new file ####
input_lat_dim = data.dimensions["latitude0"]
input_lon_dim = data.dimensions["longitude0"]
input_time_dim = data.dimensions["time0"]

##### read variables ####
lat_v = data.variables['latitude0']
lon_v = data.variables['longitude0']
time_v = data.variables['time0'] #[st_idx:et_idx+1]
#temp_v = data.variables['item3236_6hrly_mean']
temp_v = data.variables[temp]



#CREATION OF NEW FILE WITH SELECTED PERIOD AND VARIABLES FROM RAW ERA5
New_file = "new_file_created.nc"

#### open filestreams and create new filestream for pvout ######
output_stream = Dataset(New_file, "w", format = "NETCDF4")

##### create dimensions for new file ####
output_stream.createDimension("latitude0", len(input_lat_dim))
output_stream.createDimension("longitude0", len(input_lon_dim))
output_stream.createDimension("time0", None)

##### create variables ####
output_lat_var = output_stream.createVariable("latitude0",lat_v.datatype,("latitude0",))
output_lat_var.units = 'degrees_north'

output_lon_var = output_stream.createVariable("longitude0",lon_v.datatype,("longitude0",))
output_lon_var.units = 'degrees_east'

output_time_var = output_stream.createVariable("time0",time_v.datatype,("time0",))
output_time_var.units = 'days since 2005-12-01 00:00:00'
output_time_var.calendar = time_v.calendar

output_temp_var = output_stream.createVariable(temp,temp_v.datatype,("time0","latitude0","longitude0"), zlib = True, complevel = 4) #compression #compresion 
output_temp_var.units = "C"

#### writing data ###
output_lat_var[:] = lat_v[:]
output_lon_var[:] = data_long1  #lon[:]
output_time_var[:] = time_v[:]
output_temp_var[:] = data_temp1

print_variables(data)
print_variables(output_stream)

###### close filestreams #####
output_stream.close()
data.close()

print("file corrected")



#%%

