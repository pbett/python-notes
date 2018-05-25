# -*- coding: utf-8 -*-
'''
Animating a rotating globe, 
with the stock image.

'''
import datetime as dt
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
import matplotlib.animation as mplanim
#
# Useful links:
# https://matplotlib.org/api/animation_api.html
# https://matplotlib.org/api/_as_gen/matplotlib.animation.FuncAnimation.html
#--------------------------------------------------------------------



#-------------------------------------------------
# Set up the figure:
cmsize=[6.5, 6.5]
fig = plt.figure(figsize=[aside/2.54 for aside in cmsize], dpi=96) 

#---------------------------------------------------
# Set the initial Axes:
cent_lat = 50.0
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0.0,
                                           central_latitude=cent_lat))
ax.stock_img()

gl = ax.gridlines(crs=ccrs.Geodetic(), draw_labels=False,
                  linewidth=0.5, color="grey",alpha=0.5)
xgridpts = np.arange(-180,180+20, 20)
ygridpts = np.arange( -80, 80+20, 20)
gl.xlocator = mticker.FixedLocator(xgridpts)
gl.ylocator = mticker.FixedLocator(ygridpts)

fig.set_tight_layout(True)
#---------------------------------------------------





#---------------------------------------------------
# Create the updating function to call during the animation:
def update(i):
    '''
    Update the plot for each frame.
    Needs to return tuple of the artists 
    that will be redrawn for each frame.
    '''
    print  'timestep {0}'.format(i)
    ax.projection = ccrs.Orthographic(central_longitude=i,
                                      central_latitude=cent_lat)
    ax.stock_img()
    # Just return the Axes object itself in this case:
    return ax

#---------------------------------------------------
  

# Set up the animation:
fps = 20
interval = 1000.0/float(fps)  # in ms



# FuncAnimation will call the update() function for each frame:
print "Creating animation..."
anim = mplanim.FuncAnimation(fig, update, frames=np.arange(0,360),
                             interval=interval, blit=False)





# Set up the animation writing function,
# here using the ImageMagickWriter.
# This pipes the frames straight to ImageMagick to create a gif:

writer = mplanim.ImageMagickWriter(fps=fps)
# https://matplotlib.org/api/_as_gen/matplotlib.animation.ImageMagickWriter.html


# Alternatives are the ImageMagickFileWriter(),
# which saves out each frame before calling ImageMagick convert:
# https://matplotlib.org/api/_as_gen/matplotlib.animation.ImageMagickFileWriter.html
# and FFMpegWriter, FFMpegFileWriter equivalently:
# https://matplotlib.org/api/_as_gen/matplotlib.animation.FFMpegWriter.html
# https://matplotlib.org/api/_as_gen/matplotlib.animation.FFMpegFileWriter.html




# Finally, save using that writer:
# (this is the stage when it is actually generated,
#  and takes time - about 40 mins on my laptop!)
print "About to save animation:" 
anim.save('animated_globe.gif', dpi=96, writer=writer)


# Alternatively, you can display the animation
# (but in this particular case, it will be really slow!)
#plt.show()
#========================================================


