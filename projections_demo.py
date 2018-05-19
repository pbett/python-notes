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
          ccrs.PlateCarree(central_longitude=205),
          ccrs.AlbersEqualArea(central_longitude=10.0, central_latitude=52.0,
                               false_easting=0.0, false_northing=0.0, standard_parallels=(20.0, 50.0)),
          ccrs.Mollweide(  central_longitude= 10),
          ccrs.Mollweide(  central_longitude=205),
          ccrs.LambertAzimuthalEqualArea(central_longitude=10.0, central_latitude=52.0,
                                         false_easting=0.0, false_northing=0.0),	  
          ccrs.Robinson(   central_longitude= 10),
          ccrs.Robinson(   central_longitude=205),
          ccrs.Orthographic(central_longitude=0.0, central_latitude=50.0) ]


xlims_pairs = [ None, None, [-20,40],
                None, None, [-20,40],
                None, None, None     ]

ylims_pairs = [ None, None, [30,70],
                None, None, [30,70],
                None, None, None     ]

dxgrid  = 20
dygrid  = 20
gridcol = "grey"

cmsize = [25,16]  
fig = plt.figure(figsize=[x/2.54 for x in cmsize], dpi=96)

for i,proj in enumerate(projns):
    ax = fig.add_subplot(3,3,i+1, projection=proj)
    xlims = xlims_pairs[i]
    ylims = ylims_pairs[i]
    if (xlims is None) and (ylims is None):
        ax.set_global()
    else:
        ax.set_extent(xlims+ylims, crs=ccrs.Geodetic())
    #
    ax.stock_img()
    ax.coastlines("110m", linewidth=0.5, color="black")
    #
    # Doing the gridlines we want 
    # always takes more effort than anything else:
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
#-------------------

