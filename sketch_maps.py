'''
Illustrating basic "sketch-maps", without gridded data.
e.g. http://scitools.org.uk/cartopy/docs/v0.13/matplotlib/intro.html
'''
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
#----------------------------------------------------

# Simplest:
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()  ;  plt.show()  ;  plt.close()


# A bit nicer:
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=10))
ax.coastlines()
plt.tight_layout()
plt.show()  ;  plt.close()


# With a stock image:
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=10))
ax.stock_img()
plt.tight_layout()
plt.show()  ;  plt.close()


# Just simple colouring of land and sea:
ax = plt.axes(projection=ccrs.Robinson(central_longitude=10))
ax.add_feature(cartopy.feature.LAND)
ax.add_feature(cartopy.feature.OCEAN)
ax.coastlines(color="grey")  # Or you could do:
#ax.add_feature(cartopy.feature.COASTLINE)
plt.tight_layout()
plt.show()  ;  plt.close()




# Final example:
proj = ccrs.Orthographic(central_longitude=0.0, central_latitude=50.0)
ax = plt.axes(projection=proj)
ax.add_feature(cartopy.feature.LAND)
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.COASTLINE) #, edgecolor="brown")
ax.gridlines()
plt.tight_layout()
plt.show()  ;  plt.close()

# Other cartopy features include BORDERS, LAKES, RIVERS.
# http://scitools.org.uk/cartopy/docs/v0.13/matplotlib/feature_interface.html
