Start here: https://humboldt-penguin.github.io/redplanet/

---

NOTE: I completely rewrote this project in 2024 September, erasing the entire git history and restarting from scratch. See an archive of the old repo here: https://github.com/Humboldt-Penguin/redplanet_archive-240910

---
# Get Started:

RedPlanet is an open-source Python library for working with various Mars geophysical datasets. We aim to streamline data analysis/visualization workflows for beginners and experts alike, so you spend less time hunting/wrangling data and more time doing cool science! :)

(TODO: add key features from docs page once that's finalized)

---
# Links:

- Repo/package links:
    - GitHub: https://github.com/Humboldt-Penguin/redplanet
        - Legacy/archived code: https://github.com/Humboldt-Penguin/redplanet_archive-240910
    - PyPI (out of date / non-functional at the moment, pending update): https://pypi.org/project/redplanet/
- Useful resources:
    - [Mars QuickMap](https://mars.quickmap.io/layers?prjExtent=-16435210.8833828%2C-8021183.5691341%2C12908789.1166172%2C7866816.4308659&showGraticule=true&layers=NrBMBoAYvBGcQGYAsA2AHHGkB0BOcAOwFcAbU8AbwCIAzUgSwGMBrAUwCdqAuWgQ1IBnNgF8AumKrixQA&proj=3&time=2024-11-11T07%3A09%3A37.723Z) (this is an incredible resource for everyone, from beginners to advanced users — big props to [Applied Coherent Technology (ACT) Corporation](https://www.actgate.com/) :)

---
# SELF NOTE / TODO:

- Make a list of all modules/functions and "internal"/"public" annotation like the "Submodules" section on this package's doc website: https://mrjean1.github.io/PyGeodesy/
- consider cleaning up dependencies like axing scipy (nvm pyshtools needs it lols) & pandas (does anyone else need it? check!) since it's bloated!!! use `rclone ncdu .` to explore venv folder to see what's bloated, and use `uv tree` to see if it'd even help to remove the dep.
