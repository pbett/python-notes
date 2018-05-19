'''
Illustrating quick-and-easy ways of plotting gridded data,
using the iris package and its quickplot module.
https://scitools.org.uk/iris/docs/latest/userguide/plotting_a_cube.html
https://scitools.org.uk/iris/docs/latest/iris/iris/quickplot.html

'''
import iris
import iris.quickplot as qplt
#---------------------------------


#--------------------------------------------
# Load some data:
fname = iris.sample_data_path('air_temp.pp')
acube = iris.load_cube(fname)
print acube.__repr__()
# <iris 'Cube' of air_temperature / (K) (latitude: 73; longitude: 96)>

# Makes it a bit more comprehensible:
acube.convert_units("Celsius")
#--------------------------------------------


#--------------------------------------------
# The simplest plot possible:
qplt.contourf(acube)  ; qplt.show()
#--------------------------------------------


#--------------------------------------------
# But we need to add coastlines really.
# (contourf has discrete levels by default,
#  whereas pcolormesh defaults to a continuous range.)
qplt.contourf(acube)    ; qplt.plt.gca().coastlines()  ;  qplt.show()
qplt.pcolormesh(acube)  ; qplt.plt.gca().coastlines()  ;  qplt.show()
#--------------------------------------------


#--------------------------------------------
# In fact, qplt plots are still pretty customizable 
# without having to use other plotting packages:
import numpy as np

# 10 levels:
qplt.contourf(acube, 10)    ; qplt.plt.gca().coastlines()  ;  qplt.show()

# Using an explicit set of levels:
qplt.contourf(acube, np.arange(-30, 35+5, 5)) ; qplt.plt.gca().coastlines()  ;  qplt.show()


# What we mean by that, more clearly, is:
vrange = [-35,35]
vstep  = 5.0
levels = np.arange(vrange[0], vrange[1]+vstep, vstep)
# Let's use a more intuitive, diverging colour scheme while we're at it:
qplt.contourf(acube, levels, cmap="RdBu") ; qplt.plt.gca().coastlines()  ;  qplt.show()
#--------------------------------------------


