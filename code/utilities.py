import calendar
import glob
import numpy as np
from netCDF4 import Dataset

def read_MxD08_M3(filename, var_names):
    """
    """

    print('reading ' + filename)

    f = Dataset(filename, 'r')

    # latitude and longitude
    lat = f.variables['YDim'][:]
    lon = f.variables['XDim'][:]

    # all variables
    var_list = []
    for varne in var_names:
        var = f.variables[varne][:]
        var_list.append(var)

    f.close()

    return lat, lon, var_list

def read_one_year(inDir, year, varname, prefix='MOD08_M3', version='061'):
    """
    """

    # the starting julian day of every month
    if not calendar.isleap( int(year) ):
        month_julain = np.array([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335])
    else:
        month_julain = np.array([1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336])

    var_all = []
    for i in range(len(month_julain)):

        month_jd = str(month_julain[i]).zfill(3)

        # find file
        filename = glob.glob(inDir + '/' + prefix + '.A' + year + month_jd + '.' + version + '.*.hdf')
        if len(filename) == 1:
            filename = filename[0]
        else:
            print('read_one_year: ERROR')
            exit()

        # read data
        lat, lon, var_list = read_MxD08_M3(filename, (varname,))
        var_month = var_list[0]
        var_all.append(var_month)

    var_all = np.array(var_all)

    return lat, lon, var_all

def read_monthly_one_year(filename):
    """
    """

    print(' - save_monthly_one_year: read ' + filename)

    f = Dataset(filename, 'r')

    AOD = f.variables['AOD_550_DT_DB'][:]
    lat = f.variables['Latitude'][:]
    lon = f.variables['Longitude'][:]

    f.close()

    return lat, lon, AOD

def save_monthly_one_year(filename, lat, lon, var, year):
    """
    """

    f = Dataset(filename, 'w', format='NETCDF4')

    # Dimensions of a netCDF file 
    nlat = lat.shape[0]
    nlon = lon.shape[0]
    nmon = 12

    dim_lat = f.createDimension('Latitude',  nlat)
    dim_lon = f.createDimension('Longitude', nlon)
    dim_mon = f.createDimension('month',     nmon)

    # Create variables in a netCDF file
    Latitude_v  = f.createVariable( 'Latitude',      'f4', ('Latitude',  ) )
    Longitude_v = f.createVariable( 'Longitude',     'f4', ('Longitude', ) )
    month_v     = f.createVariable( 'month',         str,  ('month',     ) )
    var_v       = f.createVariable( 'AOD_550_DT_DB', 'f4', ('month', 'Latitude', 'Longitude'), fill_value=-9999.0 )

    # add addtributes
    Latitude_v.unit  = 'degree'
    Longitude_v.unit = 'degree'
    var_v.longname   = 'Monthly mean of combined dark target and deep blue AOD at 550 nm'
    var_v.valid_range = np.array([0.0, 5.0])

    # write variables
    Latitude_v[:]  = lat
    Longitude_v[:] = lon
    var_v[:,:]    = var

    month = []
    for i in range(nmon):
        month.append(year + '-' + str(i+1).zfill(2))
    month = np.array(month)
    month_v[:] = month

    f.close()

def save_annual_mean(filename, lat, lon, var, years):
    """
    """
    f = Dataset(filename, 'w', format='NETCDF4')

    # Dimensions of a netCDF file 
    nlat  = lat.shape[0]
    nlon  = lon.shape[0]
    nyear = years.shape[0]

    dim_lat  = f.createDimension('Latitude',  nlat )
    dim_lon  = f.createDimension('Longitude', nlon )
    dim_year = f.createDimension('year',      nyear)

    # Create variables in a netCDF file
    Latitude_v  = f.createVariable( 'Latitude',      'f4', ('Latitude',  ) )
    Longitude_v = f.createVariable( 'Longitude',     'f4', ('Longitude', ) )
    year_v      = f.createVariable( 'year',          str,  ('year',      ) )
    var_v       = f.createVariable( 'AOD_550_DT_DB', 'f4', ('year', 'Latitude', 'Longitude'), fill_value=-9999.0 )

    # add addtributes
    Latitude_v.unit  = 'degree'
    Longitude_v.unit = 'degree'
    var_v.longname   = 'Annual mean of combined dark target and deep blue AOD at 550 nm'
    var_v.valid_range = np.array([0.0, 5.0])

    # write variables
    Latitude_v[:]  = lat
    Longitude_v[:] = lon
    var_v[:,:]    = var
    year_v[:] = years

    f.close()














