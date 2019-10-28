import copy
import matplotlib.pyplot as plt
import numpy as np

from mylib.cartopy_plot import add_geoaxes, pcolormesh
from mylib.gbcwpry_map import gbcwpry_map
from mylib.pro_satellite import calculate_pixel_edge2
from mylib.trend_analysis import trend_analysis

from utilities import read_monthly_one_year

#######################
# Start user parameters
#

root_dir = '../data/'

start_year = 2012
end_year   = 2018

# staring and ending month index
im_st = 3
im_ed = -5


#
# End user parameters
#####################

# get AOD
AOD_list =[]
for yr in range(start_year, end_year+1):

    year = str(yr)

    filename = root_dir + 'MODIS_Terra_monthly_AOD_year_' + year  + '.nc'
    mo_lat, mo_lon, mo_AOD = read_monthly_one_year(filename)
    AOD_list.append(mo_AOD)

AOD = np.ma.concatenate(AOD_list)
AOD = AOD[im_st:im_ed,:,:]

# get latitude and longitude
lon_c, lat_c = np.meshgrid(mo_lon, mo_lat)
lat_e, lon_e = calculate_pixel_edge2(lat_c, lon_c)

#print(np.min(lat_c), np.max(lat_c))
#print(np.min(lon_c), np.max(lon_c))
#    
#print(np.min(lat_e), np.max(lat_e))
#print(np.min(lon_e), np.max(lon_e))

# fig
fig = plt.figure(figsize=(6,7))

# average of AOD
ave_AOD = np.mean(AOD, axis=0)
ax1 = add_geoaxes(fig, 211)
cb1_prop = dict()
cb1_prop['orientation'] = 'horizontal'
cb1_prop['shrink'] = 0.7
cb1_prop['aspect'] = 25
cb1_prop['pad'] = 0.12
cb1_prop['extend'] = 'max'
res1 = pcolormesh(ax1, lon_e, lat_e, ave_AOD, vmin=0.0, vmax=1.0, cbar=True, cbar_prop=cb1_prop)
cb1 = res1['cb']
cb1.set_label('Average AOD [unitless]')


# AOD trend
trend = np.zeros(ave_AOD.shape)
trend_sigma = np.zeros(ave_AOD.shape)
for i in range(ave_AOD.shape[0]):
    for j in range(ave_AOD.shape[1]):

        y = AOD[:,i,j]
        x = np.array(range(len(y))) / 12.0
        
        flag = np.logical_and(y>=-0.05, y<=5)
        y = y[flag]
        x = x[flag]

        if len(x) > 10:
            ta = trend_analysis(fit_model_index=4)
            ta.analysis(x,y)
            trend[i,j] = ta.popt[1]
            trend_sigma[i,j] = ta.trend_std
        else:
            trend[i,j] = np.nan
            trend_sigma[i,j] = np.nan

ax2 = add_geoaxes(fig, 212)
cb2_prop = copy.deepcopy(cb1_prop)
cb2_prop['extend'] = 'both'
ratio = trend / trend_sigma
flag_sig = np.absolute(ratio) >= 2.0
trend[np.logical_not(flag_sig)] = np.nan
res2 = pcolormesh(ax2, lon_e, lat_e, trend, vmin=-0.1, vmax=0.1, 
        cmap=gbcwpry_map, cbar=True, cbar_prop=cb2_prop)
cb2 = res2['cb']
cb2.set_label(r'AOD trend [year$^{-1}$]')

plt.savefig('AOD.png', format='png', dpi=300)
