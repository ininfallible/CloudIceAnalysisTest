import matplotlib as mpl
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import numpy as np

import ncdump
import adjustfont

# def colors
norm = mpl.colors.Normalize(vmin=1e-6, vmax=6e-5)
cmap = mpl.cm.rainbow

adjustfont.adjfont()

fig = plt.figure()
fig.suptitle("CLI Profile")

def plot_cli_profile(dataset, splt_param, title):
    # get data from netcdf file
    lat = dataset.variables['lat'][:] 
    lon = dataset.variables['lon'][:]
    plev = dataset.variables['plev'][:]
    time = dataset.variables['time'][:]
    cli = dataset.variables['cli'][:]

    ax = plt.subplot(splt_param)
    ax.set_title(title)
    plt.xlabel("Pressure (hPa)")
    plt.ylabel("Cloud ice level (kg/kg)")

    # will be an array [plev] -> avg 
    cli_profile=[]
    # calc mean for lons 
    for i in range(plev.size):
        cli_profile.append(np.mean(cli[i]))
    plt.gca().invert_yaxis()
    ax.plot(cli_profile, plev, marker='o')
    

nc3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
nc4 = Dataset("GFDL_am4_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
ncdump.ncdump(nc3)
ncdump.ncdump(nc4)

plot_cli_profile(nc3, 121, "AM3 CLI profile")
plot_cli_profile(nc4, 122, "AM4 CLI profile")

fig.tight_layout()

plt.show()
