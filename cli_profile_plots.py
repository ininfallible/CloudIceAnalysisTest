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

def gen_levels(lo, hi, n):
    out = []
    cur = lo
    for i in range(n):
        out.append(cur)
        cur += (hi-lo)/n
    return out


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
    ax.plot(plev, cli_profile, marker='o')
    

nc3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
nc4 = Dataset("GFDL_am4_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
ncdump.ncdump(nc3)
ncdump.ncdump(nc4)

plot_cli_profile(nc3, 211, "AM3 CLI profile")
plot_cli_profile(nc4, 212, "AM4 CLI profile")

plt.show()
