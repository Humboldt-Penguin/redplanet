Here's some boilerplate for making/configuring plots with `matplotlib`. We plan to add a plotting feature in the future.

For more info on making publication quality plots, we highly recommend the PySHTools documentation — see the "Plotting maps" section on [this page](https://shtools.github.io/SHTOOLS/python-examples.html) ([direct link](https://nbviewer.org/github/SHTOOLS/SHTOOLS/blob/master/examples/notebooks/plotting-maps.ipynb)).

&nbsp;

```py linenums="1"
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from redplanet import Crust





lon_bounds = [-180, 180]
lat_bounds = [-90 , 90]

lons = np.linspace(lon_bounds[0], lon_bounds[1], 1000)
lats = np.linspace(lat_bounds[0], lat_bounds[1], 1000)

Crust.topo.load('DEM_463m')
dat_topo = Crust.topo.get(lons, lats)





'''template for plotting stuff:'''
fig, ax = plt.subplots(figsize=(10, 10))

# ax.set_title('Bouguer Gravity Anomaly')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

im = ax.imshow(
    dat_topo / 1.e3,
    cmap   = 'RdBu_r',
    # cmap   = 'Greys',
    origin = 'lower',
    aspect = 'auto',  ## this makes pixels into squares; alternative is 'equal'
    extent = [lon_bounds[0], lon_bounds[1], lat_bounds[0], lat_bounds[1]],
)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.2)  ## `size` sets colorbar width to X% of main axes; `pad` sets separation between axes and colorbar to X inches
cbar = fig.colorbar(im, cax=cax)
cbar.set_label('Topography (km)')

plt.show()
```
