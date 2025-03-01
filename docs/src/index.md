<!-- ---
hide:
  - toc
--- -->

# RedPlanet

RedPlanet is an open-source Python library for working with various Mars geophysical datasets. We aim to streamline data analysis/visualization workflows for beginners and experts alike, so you spend less time hunting/wrangling data and more time doing cool science! :) (1)
{ .annotate }

1. Fun story: I recently spent 6 hours on a Saturday trying to find/compute a high-resolution (greater than 1x1 degree) Bouguer anomaly dataset. <br><br>
I have intermediate knowledge of search engine techniques, and I like to think I'm not completely incompetent (you can judge for yourself based on my work on this package/website) — but I was still tearing my hair out on what should have been a simple task. <br><br>
Resources such as [pyshtools](https://github.com/SHTOOLS/SHTOOLS){target="_blank"} (both the software and documentation website) and [Zenodo](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Wieczorek%2C%20Mark%22&l=list&p=1&s=10&sort=bestmatch){target="_blank"} are shining examples of how we can make our analysis workflows more accessible/reproducible and increase our scientific productivity. I hope RedPlanet can contribute to that ecosystem. <br><br>



&nbsp;

---
## Key Features

(citations are missing from here until I figure out how I'm handling that)

- **Crater database** which unifies [1] comprehensive database of craters D>=1km, [2] crater ages from both Hartmann and Neukum isochron-fitting, and [3] official/up-to-date IAU crater names.
- **Digital elevation models** up to 200m resolution with memory-mapping, parallelization, and chunking for high-performance.
- **Mohorovičić discontinuity** (crust-mantle interface) models and derived **crustal thickness** maps — models are parameterized by north/south crustal density, reference interior models, and crustal thickness beneath the InSight lander with a total of ~20,000 valid combinations.
- **Magnetic source depth** data from spherical harmonic inversions.
- **Heat flow** and **Curie depth** calculations from **gamma-ray spectroscopy (GRS)** data.
- MAVEN magnetometer data, filtered for nighttime and low-altitude (COMING SOON).



&nbsp;

---
## Online Demo (no installation necessary!)

TODO: GOOGLE COLAB



&nbsp;

---
## Get Started

TODO: INTERNAL LINKS
