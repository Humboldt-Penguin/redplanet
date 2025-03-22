Unfortunately, Python is notorious for lacking a simple, out-of-the-box solution for installing and managing your packages and environments *([relevant xkcd](https://www.explainxkcd.com/wiki/index.php/1987:_Python_Environment){target="_blank"})*. I hope this explanation can save you some time and frustration.(1)
{ .annotate }

1. When I was first learning Python in high school, I messed up my Python installation so badly I had to completely reinstall my operating system. This is the guide I wish I had back then.

If you're using Windows, I'd ^^HIGHLY recommend^^ using your built-in [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/about){target="_blank"}. It takes a few minutes to set up and will make every programming-related task exponentially easier, plus you can easily wipe/restore your environment without affecting your Windows installation at all in case anything ever goes wrong.


&nbsp;

---
## [1] Concepts/Motivation

The ^^core Python language^^ is occasionally updated to improve performance/security/features/bugs, and old versions are slowly deprecated according to a predetermined schedule. As such, it's highly recommended to use a recent version of Python which is still being monitored for security vulnerabilities. For an overview of which versions are currently supported, look [here](https://devguide.python.org/versions){target="_blank"} or [here](https://endoflife.date/python){target="_blank"} — for reference, RedPlanet currently supports Python 3.10 to 3.12.

^^Python packages^^ are external code libraries which extend the language's functionality (some ubiquitous examples are `numpy` for numerical computing, `pandas` for tabular data, `matplotlib` for plotting, and many more). The official "index" where Python packages are published/hosted/tracked/distributed is [PyPI (Python Package Index)](https://pypi.org/){target="_blank"} which is sufficient for most purposes. The official tool for installing packages on your computer is `pip` which is included with Python(1)— but don't go installing anything yet!
{ .annotate }

1. `pip` is a recursive acronym for "pip installs packages" — see the original 2008 blog post [here](https://ianbicking.org/blog/2008/10/pyinstall-is-dead-long-live-pip.html){target="_blank"}.

If you simply download Python from the official website and install packages with `pip`, there's a good chance you'd eventually run into some frustrating and unfixable issues. This is because by default, `pip` installs packages *globally* on your system, which can lead to conflicts between projects and unexpected behavior when different projects require different package versions.

To avoid these pitfalls, it's best practice to isolate your project's dependencies from the global Python installation by creating separate ^^virtual environments^^ (in software/security, this principle is known as *"sandboxing"*). This ensures that dependencies remain consistent/trackable/reproducible across different systems, and your system-wide Python installation remains unaffected by project-specific changes.


&nbsp;

---
## [2] Tools for Python/Package Management

Over the years, several tools have been developed to simplify the process of creating and managing virtual environments. Some popular options include:

- **`pip`/`venv`** — Python's built-in solution (available from Python 3.3 onwards) for creating lightweight virtual environments.
- **`virtualenv`/`pipenv`** — `virtualenv` predates `venv` and works with both Python 2 and 3, offering a flexible way to create isolated environments. `pipenv` build on this by integrating dependency management (via a `Pipfile`) with environment management, streamlining workflows and reducing the need for manual configuration.
- **Conda** — A package/environment manager with a broader scope than Python/`pip`, including support for multiple versions of Python, complex dependencies, and even programming languages other than Python. Conda has its own package index called [conda-forge](https://conda-forge.org/){target="_blank"}, but you still have access to everything on PyPI (just install `pip` in a Conda environment). Conda is only strictly necessary for tasks like GPU programming. In order to actually install/use Conda, choose one of the following:
    - [Anaconda](https://www.anaconda.com/download){target="_blank"} is popular for its user-friendly GUI and pre-installed packages, but it's quite large (4.4GB), slow to update, cumbersome, and encourages bad practices — I'd recommend staying away.
    - [`miniconda`](https://www.anaconda.com/docs/getting-started/miniconda/main){target="_blank"} is a smaller, more minimalistic version of Conda which only includes the essentials — this is a good options for beginners who want to minimize fuss while adhering to good practices.
    - [`mamba`](https://mamba.readthedocs.io/en/latest/index.html){target="_blank"} is a third-party drop-in replacement for `conda` which is much more fast/efficient — I recommend this if you're comfortable with the command line and want the best possible experience.
- **`poetry`/`pdm`/`flit`/`hatch`/`rye`** — Newer tools for Python developers which aim to simplify the process of managing dependencies and packaging projects.
- **`uv`** — A new tool which aims to unify the best features of all the above tools into a single, easy-to-use interface.


&nbsp;

---
## [3] My Recommendation

I started with `venv`, moved to `mamba` for about four years, and finally settled on [`uv` by Astral](https://docs.astral.sh/uv/){target="_blank"} since mid-2024. Although it's still under rapid development (it was first released in February 2024 as a drop-in `pip` replacement, and only began supporting [more advanced features](https://github.com/astral-sh/uv/blob/main/changelogs/0.3.x.md){target="_blank"} with v0.3.0 in August 2024), it's gained a ton of traction in the Python community and many have completely switched over(1). It's now my go-to recommendation for beginners and experienced users alike, whether you're doing simple scripting, data analysis, package development, or anything else.
{ .annotate }

1. see broader discussions/testimonials [here](https://www.google.com/search?hl=en&q=reddit%20astral%20uv){target="_blank"}

RedPlanet was fully developed and published with `uv`, it's been a joy to work with :)


&nbsp;

---
## [4] Editors

