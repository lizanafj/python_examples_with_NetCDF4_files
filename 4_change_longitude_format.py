#!/sr/bin/env python

###############################################################################
# Program : 
# Authors  : Jesus
# Date	  : 22 January 2023
# Purpose : Work with NetCDF4 files
##############################################################################


"""
Working with NetCDF4 files:

(4) Function to find the index of the point closest to a specific lat/long.

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

##code 1 - read netCDF4 file, and analysis data

####################################################


#Open using netCDF library: 
    
data = Dataset(file, mode='r', format="NetCDF")

data_temp = data.variables[temp][:,0,:,:]
data_lat = data.variables["latitude0"][:]
data_long = data.variables["longitude0"][:]
data_time = data.variables["time0"][:]


#%%   

####################################################

##code 3 - change lon from (0-360) to (-180-180)

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

