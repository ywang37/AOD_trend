import numpy as np
from utilities import read_one_year
from utilities import save_monthly_one_year
from utilities import save_annual_mean

# generate year
start_year = 2015
end_year   = 2018
years = np.arange(start_year, end_year+1)
years = np.array(years, dtype=str)

# directories
inDir = '/Dedicated/jwang-data/shared_satData/MODIS_L3/MOD08_M3'
outDir = '../data'

varname = 'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'

######################################
# begin process data
######################################

###################################
# save monthly data for every year
# and calculate annual mean
###################################

annual_mean = []
for i in range(len(years)):

    year = years[i]

    # read one year data
    lat, lon, var_all = read_one_year(inDir, year, varname, prefix='MOD08_M3', version='061')

    # read monthly data for one year
    out_file = outDir + '/MODIS_Terra_monthly_AOD_year_' + year + '.nc' 
    save_monthly_one_year(out_file, lat, lon, var_all, year)

    # calculate annual mean
    mask_var_all = np.ma.masked_array(var_all, np.logical_or(var_all<0.0, var_all>5.0))
    var_mean = np.mean(mask_var_all, axis=0)
    annual_mean.append(var_mean)

# output annual mean
annual_mean = np.array(annual_mean)
flag = annual_mean <= 0.0
annual_mean[flag] = -9999.0
year_file = outDir + '/MODIS_Terra_annual_AOD_year_' + years[0] + '-' + years[-1] + '.nc'
save_annual_mean(year_file, lat, lon, annual_mean, years)

