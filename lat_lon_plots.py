import matplotlib as mpl
from netCDF4 import Dataset
import ncdump
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import numpy as np

# color/norm config
cmap = mpl.cm.rainbow
# norm = mpl.colors.Normalize(vmin=lo_cli, vmax = hi_cli)

# these values are overridden later
norm = mpl.colors.Normalize(vmin=8.3e-7, vmax = 3.2e-5)

#cbformat = mpl.ticker.ScalarFormatter()  
#cbformat.set_powerlimits((-2,2))
#mpl.ticker.set_powerlimits((-2,2))

# plot config
fig = plt.figure()

# because plevs aren't exact, find closest to each target
def find_closest_plev(target, plev):
    dist = 10000
    delta = 0
    i=0
    for i in range(plev.size):
        delta = abs(plev[i]-target) - dist
        dist = abs(plev[i]-target)
        if delta>0:
            break
    return i-1

# find min and max from all layers
lo_cli = 1000
hi_cli = 0
def pre_process(cli):
    global lo_cli
    global hi_cli
    print ("debug cli min:", np.nanmin(cli))
    print ("debug cli max:", np.nanmax(cli))
    lo_cli = min(lo_cli, np.nanmin(cli))
    hi_cli = max(hi_cli, np.nanmax(cli))
# debug
print("lo: ", lo_cli)
print("hi: ", hi_cli)


def plot_lat_lon(dataset, splt_param, title, target_plev):
    lat = dataset.variables['lat'][:] 
    lon = dataset.variables['lon'][:]
    plev = dataset.variables['plev'][:]
    time = dataset.variables['time'][:]
    cli = dataset.variables['cli'][:]

    ax = plt.subplot(splt_param, projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_extent([-180, 180, -90, 90])
    ax.set_title(title)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")

    ind = find_closest_plev(target_plev, plev)
    #disp = ax.pcolormesh(lon, lat, cli[ind], cmap=cmap, norm=norm, vmin=lo_cli, vmax=hi_cli)

    disp = ax.contourf(lon, lat, cli[ind], cmap=cmap, norm=norm, levels=8,\
            vmin = lo_cli, vmax = hi_cli)
    #cbar = plt.colorbar(disp, ax=ax, format='%.0e')
    return disp 


fig.suptitle("Cli at Different Altitudes")

am3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
am4 = Dataset("GFDL_am4_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")

ncdump.ncdump(am3)
ncdump.ncdump(am4)

pre_process(am3.variables['cli'])
pre_process(am4.variables['cli'])

plot_for_cb = \
plot_lat_lon(am3, 321, "am3 150 plev", 150)
plot_lat_lon(am3, 323, "am3 600 plev", 600)
plot_lat_lon(am3, 325, "am3 900 plev", 900)

plot_lat_lon(am4, 322, "am4 150 plev", 150)
plot_lat_lon(am4, 324, "am4 600 plev", 600)
plot_lat_lon(am4, 326, "am5 900 plev", 900)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(plot_for_cb, cax=cbar_ax)
cbar.set_label("cli (kg/kg)")

plt.show()

am3.close()
am4.close()

# lons = nc3.variables[][:]
