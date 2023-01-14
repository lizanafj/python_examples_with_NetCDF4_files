#!/sr/bin/env python

###############################################################################
# Program : 
# Authors  : Jesus
# Date	  : 22 January 2023
# Purpose : Work with NetCDF4 files
##############################################################################


"""
Working with NetCDF4 files:

(a) read, analysis and plot ensemble of netCDF4 files using xarray

"""   

  
#%%

##########################################################################
##########################################################################

#INPUT DATA 

#*.nc file     
file ="item3236_6hrly_mean_h000_2006-10_2006-11.nc"
ensemble = "item3236_6hrly*.nc" #or "*.nc"

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

##code 1 - read ensemble of netCDF4 files 

####################################################


model = xarray.open_mfdataset("item3236*.nc",combine = "nested",concat_dim="new_dim",decode_times=False)['item3236_6hrly_mean'][:,:,0,:,:]
print(model)



#%%   

####################################################

##code 2 - print data distribution

####################################################

model_csv = model[:,:,68,430].values-273.15

sns.distplot(model[:,:,68,430].values-273.15, hist=False, kde_kws={"color": "r", "lw": 2, "label": "model",'linestyle':'--'})

plt.legend()
plt.xlabel("Temperature ºC")
#plt.xlim(-20, 50)
plt.title(f'Data distribution')
plt.show()
plt.clf()

model.close()




