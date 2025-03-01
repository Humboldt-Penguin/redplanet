# Full Index of API Reference

## User Config

- [get_dirpath_datacache()](user_config/get_dirpath_datacache.md)
- [set_dirpath_datacache(...)](user_config/set_dirpath_datacache.md)
- [get_max_size_to_calculate_hash_GiB()](user_config/get_max_size_to_calculate_hash_GiB.md)
- [set_max_size_to_calculate_hash_GiB(...)](user_config/set_max_size_to_calculate_hash_GiB.md)
- [get_enable_stream_hash_check()](user_config/get_enable_stream_hash_check.md)
- [set_enable_stream_hash_check(...)](user_config/set_enable_stream_hash_check.md)


---
## Datasets

- Craters:
    - [get(...)](datasets/Craters/get.md)
- Crust:
    - Topography / DEM:
        - [load(...)](datasets/Crust/topo/load.md)
        - [get(...)](datasets/Crust/topo/get.md)
        - [get_metadata()](datasets/Crust/topo/get_metadata.md)
        - [get_dataset()](datasets/Crust/topo/get_dataset.md)
    - Dichotomy:
        - [get_coords()](datasets/Crust/dichotomy/get_coords.md)
        - [is_above(...)](datasets/Crust/dichotomy/is_above.md)
    - Mohorovičić Discontinuity / Crustal Thickness:
        - [get_registry()](datasets/Crust/moho/get_registry.md)
        - [load(...)](datasets/Crust/moho/load.md)
        - [get(...)](datasets/Crust/moho/get.md)
        - [get_metadata()](datasets/Crust/moho/get_metadata.md)
        - [get_dataset()](datasets/Crust/moho/get_dataset.md)
    - Bouguer Anomaly:
        - [load(...)](datasets/Crust/boug/load.md)
        - [get(...)](datasets/Crust/boug/get.md)
        - [get_metadata()](datasets/Crust/boug/get_metadata.md)
        - [get_dataset()](datasets/Crust/boug/get_dataset.md)
- Gamma-Ray Spectrometer (GRS):
    - [get(...)](datasets/GRS/get.md)
    - [get_metadata()](datasets/GRS/get_metadata.md)
    - [get_dataset()](datasets/GRS/get_dataset.md)
- Magnetic Field:
    - Spherical Harmonic Models:
        - [load(...)](datasets/Mag/sh/load.md)
        - [get(...)](datasets/Mag/sh/get.md)
        - [get_metadata()](datasets/Mag/sh/get_metadata.md)
        - [get_dataset()](datasets/Mag/sh/get_dataset.md)
    - Magnetic Source Depths:
        - [get_dataset(...)](datasets/Mag/depth/get_dataset.md)
        - [get_nearest(...)](datasets/Mag/depth/get_nearest.md)


---
## Analysis

- Radial Profile:
    - [get_concentric_ring_coords(...)](analysis/radial_profile/get_concentric_ring_coords.md)
    - [get_profile(...)](analysis/radial_profile/get_profile.md)
- Impact Demagnetization:
    - [compute_pressure(...)](analysis/impact_demag/compute_pressure.md)


---
## Helper Functions

- Coordinates:
    - [_plon2slon(...)](helper_functions/coordinates/_plon2slon.md)
    - [_slon2plon(...)](helper_functions/coordinates/_slon2plon.md)
- Geodesy:
    - [get_distance(...)](helper_functions/geodesy/get_distance.md)
    - [move_forward(...)](helper_functions/geodesy/move_forward.md)
    - [make_circle(...)](helper_functions/geodesy/make_circle.md)
- Misc:
    - [timer(...)](helper_functions/misc/timer.md)
