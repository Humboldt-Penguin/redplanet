# Index of Supplemental Materials:

We try to provide full explanations and citations in the [documentation for each individual function](../usage/index.md){target="_blank"}, but some topics need a bit more space to explain. This section is for those topics.

&nbsp;

---

- [Impact Demagnetization](impact_demagnetization.md)
    - Explaining and deriving our analytical model for calculating subsurface impact pressures.
    - Used in:
        - [`redplanet.analysis.impact_demag.compute_pressure(...)`](../usage/analysis/impact_demag/compute_pressure.md){target="_blank"}.
- [Radial Profile](radial_profile.md)
    - Visual explanation of how we compute radial/cross-sectional averages while respecting geodesic distances.
    - Used in:
        - [`redplanet.analysis.radial_profile.get_concentric_ring_coords(...)`](../usage/analysis/radial_profile/get_concentric_ring_coords.md){target="_blank"}
        - [`redplanet.analysis.radial_profile.get_profile(...)`](../usage/analysis/radial_profile/get_profile.md){target="_blank"}
- [Plotting](plotting.md)
    - Tips, code snippets, and resources on plotting data with `matplotlib` (unfortunately it's less straightforward than you might expect — we plan on adding a plotting feature to RedPlanet in the future, but it will always be helpful to know how to do it yourself).
