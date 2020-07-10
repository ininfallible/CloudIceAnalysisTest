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

def plot_lat_plev(dataset, splt_param, title):
    # get data from netcdf file
    lat = dataset.variables['lat'][:] 
    lon = dataset.variables['lon'][:]
    plev = dataset.variables['plev'][:]
    time = dataset.variables['time'][:]
    cli = dataset.variables['cli'][:]

    ax = plt.subplot(splt_param)
    ax.set_title(title)
    plt.xlabel("Latitude")
    plt.ylabel("Pressure (hPa)")

    # will be a 2d array [plev, lat]
    lonmean = []
    # calc mean for lons 
    for i in range(plev.size):
        tmp = []
        for j in range(lat.size):
            tmp.append(np.mean(cli[i][j]))
        lonmean.append(tmp)
    plt.gca().invert_yaxis()

    """
    # Unified Colorbar
    disp = ax.contourf(lat, plev, lonmean, cmap=cmap, levels=5, vmin=1e-6, vmax=6e-5)
    """

    # Individual colorbar
    disp = ax.contourf(lat, plev, lonmean, cmap=cmap, levels=5)
    cbar = plt.colorbar(disp, ax=ax, extend='both', format='%.0e')

    return disp
    

am3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
am4 = Dataset("GFDL_am4_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")

ncdump.ncdump(am3)
ncdump.ncdump(am4)

plot_for_cbar = plot_lat_plev(am3, 121, "AM3 CLI by Latitude and Pressure")
plot_lat_plev(am4, 122, "AM4 CLI by Latitude and Pressure")

"""
# Unified colorbar
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(plot_for_cbar, cax=cbar_ax, format='%.0e')
"""

fig.tight_layout()
plt.show()
