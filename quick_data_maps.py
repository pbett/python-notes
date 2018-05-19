'''
Illustrating quick-and-easy ways of plotting gridded data,
using the iris package and its quickplot module.

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
# But we need to add coastlines really:
qplt.contourf(acube)    ; qplt.plt.gca().coastlines()  ;  qplt.show()
qplt.pcolormesh(acube)  ; qplt.plt.gca().coastlines()  ;  qplt.show()
#--------------------------------------------


#--------------------------------------------
# Actually, qplt plots are still pretty customizable on their own:
import numpy as np

# 10 levels:
qplt.contourf(acube, 10)    ; qplt.plt.gca().coastlines()  ;  qplt.show()

# Using an explicit set of levels:
qplt.contourf(acube, np.arange(-30, 35+5, 5)) ; qplt.plt.gca().coastlines()  ;  qplt.show()


# What we mean by that, more clearly, is:
vrange = [-35,35]
vstep  = 5.0
levels = np.arange(vrange[0], vrange[1]+vstep, vstep)
qplt.contourf(acube, levels, cmap="RdBu") ; qplt.plt.gca().coastlines()  ;  qplt.show()
#--------------------------------------------


