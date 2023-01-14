#!/sr/bin/env python

###############################################################################
# Program : 
# Authors  : Jesus
# Date	  : 22 January 2023
# Purpose : Work with NetCDF4 files
##############################################################################


"""
Working with NetCDF4 files:

(5) Function to find the index of the point closest to a specific lat/long.

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
import numpy as np
import shutil
import dateutil.parser

import xarray

import matplotlib.pyplot as plt    
import seaborn as sns

import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import gamma, norm
from scipy.signal import detrend
import xarray as xr
import numpy.ma as ma
from statsmodels.distributions.empirical_distribution import StepFunction

from sys import exit

print("All libraries imported")



#%%

# get folder location of script
cwd = os.path.dirname(__file__) 

folder = cwd+"/DATA"

os.chdir(folder)

#%% 

####################################################

##code 1 - Function to find the index of the point closest to a specific lat/long

####################################################

#READ - take core of long system (from 0-360 or -180-180)
data = Dataset(file, mode='r', format="NetCDF")


# extract lat/lon values (in degrees) to numpy arrays
lat, lon = data.variables['latitude0'], data.variables['longitude0']
latvals = lat[:]; lonvals = lon[:]

# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.

def getclosest_ij(lats,lons,latpt,lonpt):
  # find squared distance of every point on grid
  dist_sq1,dist_sq2 = (lats-latpt)**2, (lons-lonpt)**2
  # 1D index of minimum dist_sq element
  minindex_flattened1,minindex_flattened2 = dist_sq1.argmin(),dist_sq2.argmin()
  # Get 2D index for latvals and lonvals arrays from 1D index
  return np.unravel_index(minindex_flattened1, lats.shape), np.unravel_index(minindex_flattened2, lons.shape)

iy_min, ix_min = getclosest_ij(latvals, lonvals, 52.2, -1.70+360)    #Seville  37.39, -5.95+360 - #UK: 52.2, -1.70+360

print("Index of latitude :", iy_min)
print("Index of longidude :",ix_min)

