# -*- coding: utf-8 -*-
'''
All the usual steps in making a nice plot.
This can become pretty massive,
and yes, it would be sensible to wrap all this sort of thing
into a function or functions!

I've separated out each step below, 
and put the user options at the top of each step
before they are used.
(Again, in practice, these could be function arguments
 rather than hard-coded and scattered throughout a script!)

'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm     as mpl_cm
import matplotlib.colors as mpl_col
import matplotlib.ticker as mticker ## for custom gridlines
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy
import cartopy.crs as ccrs
from   cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#=============================================================================


#--------------------------------------------
# Load some data:
fname = iris.sample_data_path('air_temp.pp')
acube = iris.load_cube(fname)
print acube.__repr__()
# <iris 'Cube' of air_temperature / (K) (latitude: 73; longitude: 96)>

# Makes it a bit more comprehensible:
acube.convert_units("Celsius")
#--------------------------------------------





#----------------------------------------------
# Set value range
vrange = [-30, 35]
vstep  = 5.0
vmid   = 0.0   # Needed if skewing the colour palette!

levels = np.arange(vrange[0], vrange[1]+vstep, vstep)
#----------------------------------------------


#----------------------------------------------
# Set colour palette:
cpal    = "RdBu_r"
extendcolbar = "both"
badcol  = "green"
undercol= "magenta"
overcol = "yellow"

ncols = len(levels) -1    # number of colours we actually want to use
if vmid is None:
    # Usual case.
    # (note that specifying the number of levels forces cmap to be discrete,
    #  but ensures consistency between contourf & pcolormesh)
    cmap = mpl_cm.get_cmap(cpal, ncols) 
    #    
else:
    # Explicit midpoint specified, make an off-centre (skewed) colourbar.
    # We create a palette that extends an equal distance either side of
    # the midpoint, but then crop it to the value range selected.
    #
    # First, get whichever is the biggest distance above or below vmid:
    deltamax = max(vrange[1]-vmid, vmid-vrange[0]) 
    vfull = [ vmid-deltamax, vmid+deltamax]  # Full range either side of vmid
    #
    # We'll map 0-1 to vfull[0]--vfull[1]   (size: 2*deltamax), 
    # so we need to know how far along vrange[0] and vrange[1] are.
    vlo_frac = (vrange[0]-vfull[0]) / (2.0*deltamax) # 0 or greater
    vhi_frac = (vrange[1]-vfull[0]) / (2.0*deltamax) # 1 or less
    # (one of these two must be 0 or 1)
    #    
    cmap_base = mpl_cm.get_cmap(cpal) # maps the range 0-1 to colours
    cols = cmap_base( np.linspace( vlo_frac, vhi_frac, ncols) )
    cmap = mpl_col.LinearSegmentedColormap.from_list('skewed',cols, N=ncols)

#cmap.set_bad(  color=badcol  )
cmap.set_over( color=overcol )
cmap.set_under(color=undercol)
#----------------------------------------------





#----------------------------------------------
# Start the plot:
cmsize = [15,10]
# A simple lat/lon projection, cutting at a sensible meridion:
proj = ccrs.PlateCarree(central_longitude=10)



fig = plt.figure(figsize=[x/2.54 for x in cmsize], dpi=96)

# Set up the Axes object as a cartopy GeoAxes object,
# i.e. one that is spatial-aware, so we can add coastlines etc later.)
# (just doing the iplt.contourf will also do this,
#  but we'd have to grab the gca() afterwards then)
ax = plt.axes(projection=proj)
#-----------------------------------------



#-----------------------------------------
# Set the domain of the plot, if necessary:
xlims = None
ylims = None

if xlims is None and ylims is None:
    ax.set_global()
else:
    # Get the x/y limits from the data if they're not specified:
    if not xlims:
        xlims = [dcube_masked.coord('longitude').points.min(),
                 dcube_masked.coord('longitude').points.max() ]
    if not ylims:
        ylims = [dcube_masked.coord('latitude').points.min(),
                 dcube_masked.coord('latitude').points.max() ]
    #
    # And set the Axes limits in lat/lon coordinates:
    ax.set_extent(xlims+ylims, crs=ccrs.Geodetic())
#-----------------------------------------




#-----------------------------------------
# Plot the data!
cont = False

if cont:
    # Filled contours
    # (always discrete colours, unless you cheat and have many colours)
    coldata = iplt.contourf(acube, axes=ax,  cmap=cmap, levels=levels, extend=extendcolbar)
else:
    # Shaded gridcells
    # (discrete colours if the number is given when setting up cmap,
    #  otherwise continuous colours)
    coldata = iplt.pcolormesh(acube, axes=ax, cmap=cmap,vmin=vrange[0],vmax=vrange[1])

# (We use the return value later when making the colorbar)
#-----------------------------------------


#-----------------------------------------
# Add contour lines highlighting some special value:
contlines = [-10.0, 10.0]
# Set the negative linestyle to be solid, like positive.
# (the default is 'dashed'; 'dotted' doesn't work)
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

cl = iplt.contour(acube, contlines, linewidths=1.5, 
                  colors="gold", alpha=0.5 )
#-----------------------------------------





#-----------------------------------------
# Add other annotations!

# Coastlines:
coastres = "50m" # or 10m (detailed) or 110m (simplified)
coastlw = 1
if coastlw > 0:
    ax.coastlines(coastres, linewidth=1, color="black")


# Country borders:
countryres = "10m"
countrylcol = "grey"
countrylw = 0

if countrylw > 0:
    if countryres is None:
        # Simple default:
        country_borders = cartopy.feature.BORDERS,
    else:
        # More explicit:
        country_borders = cartopy.feature.NaturalEarthFeature('cultural',
                                                              'admin_0_boundary_lines_land',
                                                              countryres) 
    ax.add_feature(country_borders, edgecolor=countrylcol,facecolor="",
                   linewidth=countrylw)
    # (Can use color and linestyle arguments too)


# Rivers:
riversres  = "10m"
riverslcol = "blue"
riverslw = 0

if riverslw > 0:
    if riversres is None:
        rivers_lines = cartopy.feature.RIVERS
    else:
        rivers_lines = cartopy.feature.NaturalEarthFeature('physical',
                                                           'rivers_lake_centerlines',
                                                           riversres)
    ax.add_feature(rivers_lines, color=riverscol, linewidth=riverslw)

#-----------------------------------------





#-----------------------------------------
# Grid lines!
dxgrid = 20
dygrid = 20
gridcol = "grey"
xgridax = [True, False] # Label x-axes: bottom,top
ygridax = [True, False] # Label y-axes: left,  right



# Create gridlines (and label them on the axes, IF we're in PlateCarree)
label_grid = ( proj==ccrs.PlateCarree() )
gl = ax.gridlines(crs=ccrs.Geodetic(), draw_labels=label_grid,
                  linewidth=0.5, color=gridcol)
if label_grid:
    # Options to switch on/off individual axes labels:
    gl.xlabels_bottom = xgridax[0]
    gl.xlabels_top    = xgridax[1]
    gl.ylabels_left   = ygridax[0]
    gl.ylabels_right  = ygridax[1]
    # And the axis titles themselves:
    ax.set_xlabel(r"Longitude")
    ax.set_ylabel(r"Latitude")


# Set limits for the grid separate to the plot's xlims/ylims:
# There are various fiddly ways of getting the x/y limits for the gridlines
# e.g. from the data (but needing them to be in lat/lon coords),
# but we'll just do something simple here:
xlims_for_grid = xlims   if xlims is not None   else  [-180,180]
ylims_for_grid = ylims   if ylims is not None   else  [ -90, 90]

# Now get the *actual* range we'll use, by rounding in units of the grid spacing:
xgridrange = [dxgrid*np.round(val/dxgrid) for val in xlims_for_grid]
ygridrange = [dygrid*np.round(val/dygrid) for val in ylims_for_grid]

# Now we can set up the gridlines arrays:
xgridpts = np.arange(xgridrange[0],xgridrange[1]+dxgrid,dxgrid)
ygridpts = np.arange(ygridrange[0],ygridrange[1]+dygrid,dygrid)
# Filter in case the rounding meant we went off-grid!
xgridpts = xgridpts[ np.logical_and(xgridpts>=-180, xgridpts<=360) ]
ygridpts = ygridpts[ np.logical_and(ygridpts>= -90, ygridpts<= 90) ]

gl.xlocator = mticker.FixedLocator(xgridpts)
gl.ylocator = mticker.FixedLocator(ygridpts)
if label_grid:
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

#----------------------------------------------------------------------




#----------------------------------------------------------------------
# Add colorbar Axes:
bar_pos = [0.05, 0.12, 0.9, 0.07]  # [l,b,w,h]
bar_orientation = "horizontal"  # or "vertical"  or "none" (to skip)
bar_ticklen  = 0
bar_ticklabs = None    # Use defaults
bar_label = u"Splendid temperature (°C)"


if bar_orientation.lower() != "none":
    bar_axes = fig.add_axes(bar_pos)
    bar = fig.colorbar(coldata, cax=bar_axes,
                       orientation=bar_orientation,
                       drawedges=False, extend=extendcolbar)
    #
    bar.ax.tick_params(length=bar_ticklen)
    bar.set_ticks(levels)
    #
    if bar_ticklabs is not None:
        bar.set_ticklabels(bar_ticklabs)
    #
    if bar_label is not None:
        bar.set_label(bar_label) 

#----------------------------------------------------------------------


#------------------------------------------------------------
# Finally, set the margins and make the plot!
marlft=0.03
marrgt=0.97
martop=0.99
marbot=0.20
marwsp=0
marhsp=0


fig.subplots_adjust(left  = marlft,  bottom = marbot,
                    right = marrgt,  top    = martop,
                    wspace= marwsp,  hspace = marhsp )
plt.show()
plt.close()
#======================================================================




