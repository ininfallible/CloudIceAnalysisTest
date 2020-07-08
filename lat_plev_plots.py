import matplotlib as mpl
from netCDF4 import Dataset
import ncdump
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import numpy as np

# def colors
# TODO: auto-determine bounds
norm = mpl.colors.Normalize(vmin=1e-6, vmax=6e-5)
cmap = mpl.cm.rainbow

fig = plt.figure()

def gen_levels(lo, hi, n):
    out = []
    cur = lo
    for i in range(n):
        out.append(cur)
        cur += (hi-lo)/n
    return out


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
    #cf = ax.contourf(lat, plev, lonmean, cmap=cmap, norm=norm, levels=gen_levels(1e-9, 1e-4, 10))
    disp = ax.contourf(lat, plev, lonmean, cmap=cmap, levels=5, vmin=1e-6, vmax=6e-5)
    #cbar = plt.colorbar(disp, ax=ax, extend='both')
    return disp
    

am3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
am4 = Dataset("GFDL_am4_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")

ncdump.ncdump(am3)
ncdump.ncdump(am4)

plot_for_cbar = plot_lat_plev(am3, 211, "AM3 CLI by Latitude and Pressure")
plot_lat_plev(am4, 212, "AM4 CLI by Latitude and Pressure")

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(plot_for_cbar, cax=cbar_ax)



plt.show()
