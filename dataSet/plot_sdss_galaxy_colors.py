"""
SDSS Galaxy Colors
------------------
The function :func:`fetch_sdss_galaxy_colors` used below actually queries
the SDSS CASjobs server for the colors of the 50,000 galaxies.  Below we
extract the :math:`u - g` and :math:`g - r` colors for 5000 stars, and
scatter-plot the results
"""
# Author: Jake VanderPlas <vanderplas@astro.washington.edu>
# License: BSD
#   The figure is an example from astroML: see http://astroML.github.com
import numpy as np
from matplotlib import pyplot as plt

from sklearn.neighbors import KNeighborsRegressor

from astroML.datasets import fetch_sdss_galaxy_colors
from astroML.plotting import scatter_contour
import pandas as pd


#------------------------------------------------------------
# Download data
data = pd.read_csv("../Skyserver_SQL12-17-2017 8-08-16 AM.csv")

# Extract colors and spectral class
ug = data['u'] - data['g']
gr = data['g'] - data['r']
spec_class = data['camcol']

stars = (spec_class == 4)
qsos = (spec_class == 5)

#------------------------------------------------------------
# Prepare plot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)

ax.plot(ug[stars], gr[stars], '.', ms=4, c='b', label='stars')
ax.plot(ug[qsos], gr[qsos], '.', ms=4, c='r', label='qsos')

ax.legend(loc=2)

ax.set_xlabel('$u-g$')
ax.set_ylabel('$g-r$')

plt.show()
