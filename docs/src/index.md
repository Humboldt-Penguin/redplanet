---
title: "RedPlanet"
# hide:
#   - toc
---


<!-- Hide title in favor of logo (but keep the "title" metadata in yaml or else page title becomes "index") -->
<style>
  .md-typeset h1 {
    display: none;
  }
</style>



<!-- Logo -->
<figure markdown="span">
  ![](.assets/logo/transparent_withtext.png){ style="width:700px; height:auto;" }
</figure>

<!-- Logo aligned to the left like SciPy's GH readme: https://github.com/scipy/scipy/blob/main/README.rst
![](.assets/logo/transparent_withtext.png){ style="width:300px; height:auto; float:left; padding-right:20px;" }
-->



<!-- Badges (useful: https://naereen.github.io/badges/ ) -->
<div align="center">

  <a href="https://pypi.org/project/redplanet/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/pypi/v/redplanet.svg?color=blue"/>
  </a>

  <a href="https://github.com/Humboldt-Penguin/redplanet/actions/workflows/test.yml" target="_blank" rel="noopener noreferrer">
    <img src="https://github.com/Humboldt-Penguin/redplanet/actions/workflows/test.yml/badge.svg?branch=main"/>
  </a>

  <a href="https://humboldt-penguin.github.io/redplanet/home/about/contact/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg"/>
  </a>

  <!-- Template:
  <a href="" target="_blank" rel="noopener noreferrer">
    <img src=""/>
  </a>
  -->
</div>



<!-- Content -->

*RedPlanet* is an open-source Python library for working with various Mars geophysical datasets. We aim to streamline data analysis/visualization workflows for beginners and experts alike, so you spend less time hunting/wrangling data and more time doing cool science! :) (1)
{ .annotate }

1. Fun story: I recently spent 6 hours on a Saturday trying to find/compute a high-resolution (greater than 1x1 degree) Bouguer anomaly dataset. <br><br>
I have intermediate knowledge of search engine techniques, and I like to think I'm not completely incompetent (you can judge for yourself based on my work on this package/website) — but I was still tearing my hair out on what should have been a simple task. <br><br>
Resources such as [pyshtools](https://github.com/SHTOOLS/SHTOOLS){target="_blank"} (both the software and documentation website) and [Zenodo](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Wieczorek%2C%20Mark%22&l=list&p=1&s=10&sort=bestmatch){target="_blank"} are shining examples of how we can make our analysis workflows more accessible/reproducible and increase our scientific productivity. I hope RedPlanet can contribute to that ecosystem. <br><br>



&nbsp;

---
## Key Features

(citations are missing from here until I figure out how I'm handling that)

- ^^Crater database^^ which unifies [1] comprehensive database of craters D>=1km, [2] crater ages from both Hartmann and Neukum isochron-fitting, and [3] official/up-to-date IAU crater names.
- ^^Digital elevation models^^ up to 200m resolution with memory-mapping, parallelization, and chunking for high-performance.
- ^^Mohorovičić discontinuity^^ (crust-mantle interface) models and derived ^^crustal thickness^^ maps — models are parameterized by north/south crustal density, reference interior models, and crustal thickness beneath the InSight lander with a total of ~20,000 valid combinations.
- ^^Magnetic source depth^^ data from spherical harmonic inversions.
- ^^Heat flow^^ and ^^Curie depth^^ calculations from ^^gamma-ray spectroscopy (GRS)^^ data.
- (Planned for future) MAVEN magnetometer data, filtered for nighttime and low-altitude.

&nbsp;

Here's a sample plot generated with RedPlanet:

[![](https://files.catbox.moe/geubr5.png)](https://files.catbox.moe/geubr5.png){target="_blank"}



&nbsp;

---
## Online Demo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1b66gQ54S5wnjLP9p-wk3X7mMpWHqsA8H?usp=sharing){target="_blank"}

Whether you're a beginner who's never installed Python before or an advanced user who'd like a demo before installing, *Google Colab* is a great way to try all the features of RedPlanet completely in your browser without installing anything! Just open the link above.
