'''
Demonstrating using cartopy on some map projections.
https://scitools.org.uk/cartopy/docs/latest/crs/projections.html

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
import cartopy.crs as ccrs
#------------------------------------------------------------


projns = [ccrs.PlateCarree(central_longitude= 10),
          ccrs.PlateCarree(central_longitude=210),
          ccrs.Mollweide(  central_longitude= 10),
          ccrs.Robinson(   central_longitude= 10),
          ccrs.AlbersEqualArea(central_longitude=10.0, central_latitude=52.0,
                               false_easting=0.0, false_northing=0.0, standard_parallels=(20.0, 50.0)),
          ccrs.LambertAzimuthalEqualArea(central_longitude=10.0, central_latitude=52.0,
                                         false_easting=0.0, false_northing=0.0) ]


cmsize = [19,16]  # Fits my screen!
fig = plt.figure(figsize=[x/2.54 for x in cmsize], dpi=96)

for i,proj in enumerate(projns):
    ax = fig.add_subplot(3,2,i+1, projection=proj)
    if i < 4:
        ax.set_global()
    else:
        xlims = [-20,40]
        ylims = [ 30,70]
        ax.set_extent(xlims+ylims, crs=ccrs.Geodetic())
    #
    ax.stock_img()
    ax.coastlines("110m", linewidth=1, color="black")
    #ax.coastlines("10m", linewidth=1, color="black")
    #
    dxgrid = 20
    dygrid = 20
    gridcol = "grey"
    gl = ax.gridlines(crs=ccrs.Geodetic(), draw_labels=False,
                      linewidth=0.5, color="grey")
    xlims_for_grid = [-180,180]
    ylims_for_grid = [ -90, 90]
    xgridrange = [dxgrid*np.round(val/dxgrid) for val in xlims_for_grid]
    ygridrange = [dygrid*np.round(val/dygrid) for val in ylims_for_grid]
    xgridpts = np.arange(xgridrange[0],xgridrange[1]+dxgrid,dxgrid)
    ygridpts = np.arange(ygridrange[0],ygridrange[1]+dygrid,dygrid)
    # Filter in case the rounding meant we went off-grid!
    xgridpts = xgridpts[ np.logical_and(xgridpts>=-180, xgridpts<=360) ]
    ygridpts = ygridpts[ np.logical_and(ygridpts>= -90, ygridpts<= 90) ]
    gl.xlocator = mticker.FixedLocator(xgridpts)
    gl.ylocator = mticker.FixedLocator(ygridpts)

plt.tight_layout()
plt.show()
plt.close()
#---------------------------------------------------

