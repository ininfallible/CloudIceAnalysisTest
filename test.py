from netCDF4 import Dataset
import ncdump
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs

nc3 = Dataset("GFDL_am3_cli_2009_01.nc", "r", format="NETCDF3_CLASSIC")
print(nc3.data_model)

lat = nc3.variables['lon'][:] 
lon = nc3.variables['lat'][:]
plev = nc3.variables['plev'][:]
time = nc3.variables['time'][:]
cli = nc3.variables['cli'][:]

# Debug 
print("lon size:", lon.size)
for i in lon: 
    print(i,end=" ")
print("lat size: ", lat.size)
for i in lat: 
    print(i,end=" ")
print("plev size: ", plev.size)
#for i in plev: print(i,end=" ")
print(cli[20][20][20])
ncdump.ncdump(nc3)

# =====================================================
# PLOTTING
# =====================================================
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.set_extent([-180, 180, -90, 90])

# min and max of the data set
hi=0
lo=1000000
for i in range(lon.size):
    for j in range(lat.size):
        lo = min(cli[0][i][j], lo)
        hi = max(cli[0][i][j], hi)
print("lo: ", lo)
print("hi: ", hi)

# color config
cmap = plt.cm.rainbow
norm = mpl.colors.Normalize(vmin=lo, vmax = hi)

# Save the plot by calling plt.savefig() BEFORE plt.show()
# plt.savefig('coastlines.pdf')
# plt.savefig('coastlines.png')

"""
for i in range(lon.size):
    for j in range(lat.size):
        plt.plot(lat[j],lon[i], marker='o',\
            color=cmap(norm(cli[0][i][j])), \
            transform = ccrs.PlateCarree(),
        )
"""
#pcm = ax.pcolormesh(lat, lon, cli[0], cmap=cmap, norm=norm)
#plt.colorbar(pcm, ax=ax)

print(ax.get_extent())

#plt.show()


nc3.close()

# lons = nc3.variables[][:]
