#!/sr/bin/env python

###############################################################################
# Program : 
# Authors  : Jesus
# Date	  : 22 January 2023
# Purpose : Work with NetCDF4 files
##############################################################################


"""
Working with NetCDF4 files:

(3) Read, modify and write netCDF4 file - using xarray library. 

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

####################################################

##code 1 - open and save using xarray

####################################################

#open new file
member = xarray.open_dataset(file)      

member_check = member[temp][:]    #member['item3236_6hrly_mean'][:,0,:,:]

print("before operations :", member_check[0,0,68,430].values)

#add operations
#Convert from Kelvin to Degree C
member_check = member_check - 273.15

print("after operations :", member_check[0,0,68,430].values)

#implement new values in the member
member[temp][:] = member_check[:]

#save
new_name = "new_name.nc"
member.to_netcdf(new_name)

print(new_name," Done!")
    
print(member)




#%%


