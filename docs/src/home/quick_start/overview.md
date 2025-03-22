bwaaa

4 modules for users:

1. User Config
    - Whenever you run code that requires a dataset, RedPlanet will (1) check if the file is in your local cache and has the correct hash, and if not then (2) download the file.
    - You can specify various options like where the data is stored, how file integrity is checked, etc.
2. Datasets
    - There are 2 general types of datasets:
        1. ^^Raster datasets^^ (i.e. regular 2D grids, or "pixels"), where you must `load` a model before using the `get` function to access points/swaths of data. For implementation details, see `src/redplanet/helper_functions/GriddedData.py`.
            - Topography / DEM (`Crust.topo`)
            - Mohorovičić Discontinuity / Crustal Thickness (`Crust.moho`)
            - Bouguer Anomaly (`Crust.boug`)
            - Spherical Harmonic Models (`Mag.sh`)
            - Gamma-Ray Spectrometer (`GRS`) — this is a special case where no `load` function is needed, it's loaded upon first access.
        2. ^^Point datasets^^, no need to `load` before use.
            - Craters (`Craters`)
            - Dichotomy (`Crust.dichotomy`)
            - Magnetic Source Depths (`Mag.depth`)
3. Analysis
    - Various analysis tools
4. Helper Functions
    - Miscellaneous convenience functions

