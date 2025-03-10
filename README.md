NOTE: I completely rewrote this project in 2024 September, erasing the entire git history and restarting from scratch. See an archive of the old repo here: https://github.com/Humboldt-Penguin/redplanet_archive-240910

---
# Links:

- Repo/package links:
    - GitHub: https://github.com/Humboldt-Penguin/redplanet
        - Legacy/archived code: https://github.com/Humboldt-Penguin/redplanet_archive-240910
    - PyPI (out of date / non-functional at the moment, pending update): https://pypi.org/project/redplanet/
- Useful resources:
    - [Mars QuickMap](https://mars.quickmap.io/layers?prjExtent=-16435210.8833828%2C-8021183.5691341%2C12908789.1166172%2C7866816.4308659&showGraticule=true&layers=NrBMBoAYvBGcQGYAsA2AHHGkB0BOcAOwFcAbU8AbwCIAzUgSwGMBrAUwCdqAuWgQ1IBnNgF8AumKrixQA&proj=3&time=2024-11-11T07%3A09%3A37.723Z) (this is an incredible resource for everyone, from beginners to advanced users — big props to [Applied Coherent Technology (ACT) Corporation](https://www.actgate.com/) :)

---
# Get Started:

1. What kind of science can I do with `redplanet`. [TODO: add link to docs]
1. In-depth documentation for `redplanet`. [TODO: add link to docs]

---
# SELF NOTE / TODO:

- Make a list of all modules/functions and "internal"/"public" annotation like the "Submodules" section on this package's doc website: https://mrjean1.github.io/PyGeodesy/
- I REALLY like how these docs allow you to jump straight to source code for each function: https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.geodesic.Geodesic.html
- consider cleaning up dependencies like axing scipy (nvm pyshtools needs it lols) & pandas (does anyone else need it? check!) since it's bloated!!! use `rclone ncdu .` to explore venv folder to see what's bloated, and use `uv tree` to see if it'd even help to remove the dep.
- nice readme thingie:
    - "RamanSPy streamlines the entire Raman spectroscopic data analysis lifecycle by providing accessible, easy-to-use tools for loading, preprocessing, analysing and visualising diverse Raman spectroscopic data. All functionalities of RamanSPy are completely application-agnostic and work equally well on any data loaded into the framework, regardless of their spectroscopic modality (single-point spectra, imaging, volumetric) and instrumental origin. This allows users to construct entire analysis workflows with minimal software requirements which are out-of-the-box transferable across different datasets and projects."
