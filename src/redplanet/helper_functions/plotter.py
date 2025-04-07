import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from redplanet import Crust



def topo_to_hillshade(
    topography       : np.ndarray,
    meters_per_pixel : int = 1,
    azimuth          : int = 0,
    altitude         : int = 70,
) -> np.ndarray:
    """
    Azimuth is the horizontal angle of the sun (i.e. direction from which light is coming) measured clockwise from due north, in degrees. For example, 0° means light is coming from the north (default), 90° from the east, etc.

    Altitude is the vertical angle between the sun and the horizon, in degrees. For example, 0° means the sun is right on the horizon, while 90° means directly overhead. Default is 70.

    Return is in range 0-255 (uint8), where higher values are brighter.
    """
    ## scale so horizontal and vertical distances are the same (assuming it's not too intensely rectangular) — otherwise you get this lol: https://files.catbox.moe/8xnca0.png
    topography = topography / meters_per_pixel

    ## compute gradients along the latitude (dy) and longitude (dx)
    dy, dx = np.gradient(topography)

    ## compute slope in radians
    slope = np.pi/2. - np.arctan(np.sqrt(dx**2 + dy**2))

    ## compute aspect in radians
    aspect = np.arctan2(dx, dy)

    ## convert sun azimuth and altitude from degrees to radians.
    ## here we adjust the azimuth so that 0° corresponds to north.
    zenith = 90 - altitude
    azimuth_rad = np.radians(360 - azimuth)
    zenith_rad = np.radians(zenith)

    ## calculate the shaded relief
    shaded = (
        np.sin(zenith_rad) * np.sin(slope) +
        np.cos(zenith_rad) * np.cos(slope) *
        np.cos(azimuth_rad - aspect)
    )

    ## clip negative values and scale to 0-255
    hillshade = np.clip(shaded, 0, 1) * 255
    hillshade = 255 - hillshade
    return hillshade.astype(np.uint8)



def plot(
    lons       : np.ndarray,
    lats       : np.ndarray,
    dat        : np.ndarray,
    ax         : None | plt.Axes = None,
    figsize    : float | tuple[float, float] = (7, 7),
    xlabel     : str = 'Longitude',
    ylabel     : str = 'Latitude',
    title      : None | str = None,
    cmap       : str = 'RdBu_r',
    cbar       : bool = True,
    cbar_label : None | str = None,
    cbar_units : None | str | tuple[str, float ] = None,
    limits     : tuple[ None|float, None|float ] = [None, None],
    hillshade  : bool = False,
    topo_model : str = 'DEM_463m',
    azimuth    : int = 0,
    altitude   : int = 70,
    alpha_hs   : float = 1,
    alpha_dat  : float = 0.6,
    show       : bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plots a 2D dataset with optional hillshade underlay.

    Parameters
    ----------
    lons : np.ndarray
        1D array of longitudes, likely the ones used to create the data array.
    lats : np.ndarray
        1D array of latitudes, likely the ones used to create the data array.
    dat : np.ndarray
        2D array of data values to be visualized. Shape should be `(len(lats), len(lons))`.
    ax : None | plt.Axes, optional
        Existing Matplotlib Axes object on which to plot the data, e.g. if you're using subplots to put multiple plots on the same figure. If None, a new figure and axes are created. Default is None.
    figsize : float | tuple[float, float], optional
        Width, height of the figure in inches. If a single number is provided, it is used for both width and height. Default is (7, 7).
    xlabel : str, optional
        Label for the x-axis. Default is 'Longitude'.
    ylabel : str, optional
        Label for the y-axis. Default is 'Latitude'.
    title : None | str, optional
        Title of the plot. If None, no title is set. Default is None.
    cmap : str, optional
        Colormap used to display the data. Default is 'RdBu_r'.
    cbar : None | bool, optional
        Whether to display a colorbar alongside the plot. Default is True.
    cbar_label : None | str, optional
        Label for the colorbar. Default is None.
    cbar_units : str | tuple[str, float ], optional
        Units to display on the colorbar. If a tuple is provided, it should be in the form `(unit_name, scale)` where the data is scaled by the given factor before plotting. Default is None.
    limits : tuple[ None|float, None|float ], optional
        Tuple specifying the (minimum, maximum) limits for the data colormap scaling. If you only want to set one limit, use None for the other. Default is [None, None].
    hillshade : bool, optional
        If True, underlays a hillshade generated from topographic data. Default is False.
    topo_model : str, optional
        (For hillshade) Identifier for the topographic model used to generate the hillshade. See `Crust.topo.load(...)` for options. Default is 'DEM_463m'.
    azimuth : int, optional
        (For hillshade) Azimuth angle (in degrees) representing the horizontal direction of the light source (measured clockwise from north). Default is 0.
    altitude : int, optional
        (For hillshade) Altitude angle (in degrees) representing the vertical angle of the light source above the horizon. Default is 70.
    alpha_hs : float, optional
        (For hillshade) Opacity for the hillshade underlay (range 0 to 1). Default is 1.
    alpha_dat : float, optional
        (For hillshade) Opacity for the data overlay (range 0 to 1). If hillshade is disabled, this is set to 1. Default is 0.6.
    show : bool, optional
        If True and a new figure is created (i.e. `ax` is not provided), displays the plot immediately. Default is True.

    Returns
    -------
    tuple[plt.Figure, plt.Axes]
        A tuple containing the matplotlib Figure and Axes objects for the created plot.
    """

    if isinstance(figsize, int | float):
        figsize = (figsize, figsize)


    # If no axis is provided, create a new figure and axis.
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        created_new_fig = True
    else:
        fig = ax.figure
        created_new_fig = False

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if title:
        ax.set_title(title)


    '''compute hillshade & plot hillshade if necessary'''

    if hillshade:

        ## temporarily offshore the user's topo model (in order to load the requested model for hillshade), then restore it later on — plotting something shouldn't change external state (the user's topo model), that's horrible and anti-user design !!!
        user_topo = Crust.topo.loader._dat_topo

        if (user_topo is None) or (user_topo.metadata['short_name'] != topo_model):
            Crust.topo.load(topo_model)

        ## account for the fact that input data arrays might be super low-res (e.g. GRS), but we still want high-res hillshade
        hs_lons = np.linspace(lons[0], lons[-1], 1000)
        hs_lats = np.linspace(lats[0], lats[-1], 1000)

        dat_hs = topo_to_hillshade(
            topography       = Crust.topo.get(hs_lons, hs_lats),
            meters_per_pixel = Crust.topo.get_metadata()['meters_per_pixel'],
            azimuth          = azimuth,
            altitude         = altitude,
        )

        Crust.topo.loader._dat_topo = user_topo

        im_hs = ax.imshow(
            dat_hs,
            cmap = 'Greys_r',
            origin = 'lower',
            aspect = 'equal',
            extent = [hs_lons[0], hs_lons[-1], hs_lats[0], hs_lats[-1]],
            alpha = alpha_hs,
        )

    else:
        alpha_dat = 1


    '''plot data'''

    if isinstance(cbar_units, (tuple, list)):
        cbar_units_name, scale = cbar_units
        dat = dat * scale
    else:
        cbar_units_name = cbar_units

    im_dat = ax.imshow(
        dat,
        cmap = cmap,
        origin = 'lower',
        aspect = 'equal',
        extent = [lons[0], lons[-1], lats[0], lats[-1]],
        alpha = alpha_dat,
        vmin = limits[0],
        vmax = limits[1],
    )


    '''plot colorbar'''

    if cbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.2)  ## `size` sets colorbar width to X% of main axes; `pad` sets separation between axes and colorbar to X inches
        cbar = fig.colorbar(im_dat, cax=cax)
        label = ''
        if cbar_label:
            label += cbar_label
        if cbar_units_name:
            label += f' [{cbar_units_name}]'
        cbar.set_label(label)

    if show and created_new_fig:
        plt.show()

    return fig, ax
