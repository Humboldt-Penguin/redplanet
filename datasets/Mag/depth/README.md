- Paper: https://doi.org/10.1029/2020JE006690
    - "Depth of Martian Magnetization From Localized Power Spectrum Analysis" (Gong & Weiczorek, 2021)
- Dataset: https://doi.org/10.5281/zenodo.4686358


Directly from their README:

```
This archive contains the final inversion results for the employed magnetized caps model using a magnetic field that expanded to degree and order 134. For each localized analysis, the bandwidth and angular radius of the window were 17 and 20 degrees, respectively, which yields 8 localization windows that concentrated more than 70% of the power with the region of interest. The analyses were performed at 150 km altitude and on an equally spaced grid with a spacing corresponding to 10 degrees of latitude.

`20_17_8_134_150.dat`: This file contains the best fitting values and the corresponding reduced chi^2 value of the inversion. The first two columns correspond to the latitude and longitude, and the third to sixth columns correspond to the best fitting values of the angular radii (in km) of the magnetized caps, the magnetization depth (in km), the square root of the metric N<M^2>V^2 (in A m^2), and the reduced chi^2 value of the best fitting model at each location, respectively.

`20_17_8_134_150_lower.dat` & `20_17_8_134_150_upper.dat`: These two files contain the 1-sigma lower and upper limits of the parameters. For each file, the first two columns correspond to the latitude and longitude, and the third to fifth columns correspond to the 1-sigma lower or upper limits of the angular radii (in km) of the magnetized caps, the magnetization depth (in km), the square root of the metric N<M^2>V^2 (in A m^2), respectively. The last column corresponds to the 1-sigma confidence level of the reduced chi^2 that were obtained from Monte Carlo simulations. The 1-sigma lower and upper limits were set to -1e+100 when the minimum reduced chi^2 value of the best fitting model was above this 1-sigma confidence level.
```
