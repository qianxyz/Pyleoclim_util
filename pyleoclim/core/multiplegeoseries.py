"""
A MultipleGeoSeries object is a collection (more precisely, a 
list) of GeoSeries objects. This is handy in case you want to apply the same method 
to such a collection at once (e.g. process a bunch of series in a consistent fashion).
Compared to its parent class MultipleSeries, MultipleGeoSeries opens new possibilites regarding mapping.
"""
from ..core.multipleseries import MultipleSeries
from ..utils import mapping as mp
import warnings

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from itertools import cycle
import matplotlib.lines as mlines
import numpy as np
#import warnings

#import matplotlib.pyplot as plt
#import matplotlib as mpl
#from matplotlib import cm
#from itertools import cycle
#import matplotlib.lines as mlines
#import copy


class MultipleGeoSeries(MultipleSeries):
    '''MultipleGeoSeries object.

    This object handles a collection of the type GeoSeries and can be created from a list of such objects.
    MultipleGeoSeries should be used when the need to run analysis on multiple records arises, such as running principal component analysis.
    Some of the methods automatically transform the time axis prior to analysis to ensure consistency.

    Parameters
    ----------

    series_list : list
    
        a list of pyleoclim.Series objects

    time_unit : str
    
        The target time unit for every series in the list.
        If None, then no conversion will be applied;
        Otherwise, the time unit of every series in the list will be converted to the target.

    label : str
   
        label of the collection of timeseries (e.g. 'Euro 2k')

    Examples
    --------
    .. jupyter-execute::
        
        from pylipd.utils.dataset import load_dir
        lipd = load_dir(name='Pages2k')
        df = lipd.get_timeseries_essentials()
        dfs = df.query("archiveType in ('tree','documents','coral','lake sediment')") 
        # place in a MultipleGeoSeries object
        ts_list = []
        for _, row in dfs.iterrows():
            ts_list.append(pyleo.GeoSeries(time=row['time_values'],value=row['paleoData_values'],
                                           time_name=row['time_variableName'],value_name=row['paleoData_variableName'],
                                           time_unit=row['time_units'], value_unit=row['paleoData_units'],
                                           lat = row['geo_meanLat'], lon = row['geo_meanLon'],
                                           archiveType = row['archiveType'], verbose = False, 
                                           label=row['dataSetName']+'_'+row['paleoData_variableName'])) 
    
        Euro2k = pyleo.MultipleGeoSeries(ts_list, label='Euro2k',time_unit='years AD')  
        Euro2k.map() 
    '''

    def __init__(self, series_list, time_unit=None, label=None):
        self.series_list = series_list
        from ..core.geoseries import GeoSeries
        # check that all components are GeoSeries
        if not all([isinstance(ts, GeoSeries) for ts in series_list]):
            raise ValueError('All components must be GeoSeries objects')
        
        super().__init__(series_list, time_unit, label)

    # ============ MAP goes here ================


    def map(self, marker='archiveType', hue='archiveType', size=None, cmap=None,
            edgecolor='k', projection='auto',
            proj_default=True, crit_dist=5000, colorbar=True,
            background=True, borders=False, coastline=True,rivers=False, lakes=False, land=True,ocean=True,
            figsize=None, fig=None, scatter_kwargs=None, gridspec_kwargs=None, legend=True, gridspec_slot=None,
            lgd_kwargs=None, savefig_settings=None, **kwargs):
        '''
        

        Parameters
        ----------
        hue : string, optional
            Grouping variable that will produce points with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            The default is 'archiveType'.

        size : string, optional
            Grouping variable that will produce points with different sizes. Expects to be numeric. Any data without a value for the size variable will be filtered out.
            The default is None.

        marker : string, optional
            Grouping variable that will produce points with different markers. Can have a numeric dtype but will always be treated as categorical.
            The default is 'archiveType'.

        edgecolor : color (string) or list of rgba tuples, optional
            Color of marker edge. The default is 'w'.

        projection : string
            the map projection. Available projections:
            'Robinson' (default), 'PlateCarree', 'AlbertsEqualArea',
            'AzimuthalEquidistant','EquidistantConic','LambertConformal',
            'LambertCylindrical','Mercator','Miller','Mollweide','Orthographic',
            'Sinusoidal','Stereographic','TransverseMercator','UTM',
            'InterruptedGoodeHomolosine','RotatedPole','OSGB','EuroPP',
            'Geostationary','NearsidePerspective','EckertI','EckertII',
            'EckertIII','EckertIV','EckertV','EckertVI','EqualEarth','Gnomonic',
            'LambertAzimuthalEqualArea','NorthPolarStereo','OSNI','SouthPolarStereo'
            By default, projection == 'auto', so the projection will be picked
            based on the degree of clustering of the sites.

        proj_default : bool, optional
            If True, uses the standard projection attributes.
            Enter new attributes in a dictionary to change them. Lists of attributes can be found in the `Cartopy documentation <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#eckertiv>`_.
            The default is True.

        crit_dist : float, optional
            critical radius for projection choice. Default: 5000 km
            Only active if projection == 'auto'

        background : bool, optional
            If True, uses a shaded relief background (only one available in Cartopy)
            Default is on (True).

        borders : bool or dict, optional
            Draws the countries border.
            If a dictionary of formatting arguments is supplied (e.g. linewidth, alpha), will draw according to specifications.
            Defaults is off (False).

        coastline : bool or dict, optional
            Draws the coastline.
            If a dictionary of formatting arguments is supplied (e.g. linewidth, alpha), will draw according to specifications.
            Defaults is on (True).

        land : bool or dict, optional
            Colors land masses.
            If a dictionary of formatting arguments is supplied (e.g. color, alpha), will draw according to specifications.
            Default is off (True). Overriden if background=True.

        ocean : bool or dict, optional
            Colors oceans.
            If a dictionary of formatting arguments is supplied (e.g. color, alpha), will draw according to specifications.
            Default is on (True). Overriden if background=True.

        rivers : bool or dict, optional
            Draws major rivers.
            If a dictionary of formatting arguments is supplied (e.g. linewidth, alpha), will draw according to specifications.
            Default is off (False).

        lakes : bool or dict, optional
            Draws major lakes.
            If a dictionary of formatting arguments is supplied (e.g. color, alpha), will draw according to specifications.
            Default is off (False).

        figsize : list or tuple, optional
            Size for the figure

        scatter_kwargs : dict, optional
            Dict of arguments available in `seaborn.scatterplot <https://seaborn.pydata.org/generated/seaborn.scatterplot.html>`_.
            Dictionary of arguments available in `matplotlib.pyplot.scatter <https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.scatter.html>`_.

        legend : bool, optional
            Whether to draw a legend on the figure.
            Default is True.

        colorbar : bool, optional
            Whether to draw a colorbar on the figure if the data associated with hue are numeric.
            Default is True.

        lgd_kwargs : dict, optional
            Dictionary of arguments for `matplotlib.pyplot.legend <https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.legend.html>`_.

        savefig_settings : dict, optional
            Dictionary of arguments for matplotlib.pyplot.saveFig.

             - "path" must be specified; it can be any existed or non-existed path,
               with or without a suffix; if the suffix is not given in "path", it will follow "format"
             - "format" can be one of {"pdf", "eps", "png", "ps"}

        extent : TYPE, optional
            DESCRIPTION.
            The default is 'global'.

        cmap : string or list, optional
            Matplotlib supported colormap id or list of colors for creating a colormap. See `choosing a matplotlib colormap <https://matplotlib.org/3.5.0/tutorials/colors/colormaps.html>`_.
            The default is None.

        fig : matplotlib.pyplot.figure, optional
            See matplotlib.pyplot.figure <https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib-pyplot-figure>_.
            The default is None.

        gs_slot : Gridspec slot, optional
            If generating a map for a multi-plot, pass a gridspec slot.
            The default is None.

        gridspec_kwargs : dict, optional
            Function assumes the possibility of a colorbar, map, and legend. A list of floats associated with the keyword `width_ratios` will assume the first (index=0) is the relative width of the colorbar, the second to last (index = -2) is the relative width of the map, and the last (index = -1) is the relative width of the area for the legend.
            For information about Gridspec configuration, refer to `Matplotlib documentation <https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.gridspec.GridSpec.html#matplotlib.gridspec.GridSpec>_. The default is None.

        kwargs: dict, optional
            - 'missing_val_hue', 'missing_val_marker', 'missing_val_label' can all be used to change the way missing values are represented ('k', '?',  are default hue and marker values will be associated with the label: 'missing').
            - 'hue_mapping' and 'marker_mapping' can be used to submit dictionaries mapping hue values to colors and marker values to markers. Does not replace passing a string value for hue or marker.


        Returns
        -------
        fig, ax_d
            Matplotlib figure, dictionary of ax objects which includes the as many as three items: 'cb' (colorbar ax), 'map' (scatter map), and 'leg' (legend ax)
            
        See also
        --------
        pyleoclim.utils.mapping.scatter_map: information-rich scatterplot on Cartopy map
            
        Examples
        --------
        .. jupyter-execute::
            
            from pylipd.utils.dataset import load_dir
            lipd = load_dir(name='Pages2k')
            df = lipd.get_timeseries_essentials()
            dfs = df.query("archiveType in ('tree','documents','coral','lake sediment','borehole')") 
            # place in a MultipleGeoSeries object
            ts_list = []
            for _, row in dfs.iterrows():
                ts_list.append(pyleo.GeoSeries(time=row['time_values'],value=row['paleoData_values'],
                                               time_name=row['time_variableName'],value_name=row['paleoData_variableName'],
                                               time_unit=row['time_units'], value_unit=row['paleoData_units'],
                                               lat = row['geo_meanLat'], lon = row['geo_meanLon'],
                                               elevation = row['geo_meanElev'], observationType = row['paleoData_proxy'],
                                               archiveType = row['archiveType'], verbose = False, 
                                               label=row['dataSetName']+'_'+row['paleoData_variableName'])) 
        
            Euro2k = pyleo.MultipleGeoSeries(ts_list, label='Euro2k',time_unit='years AD')  
            Euro2k.map() 
         
        By default, a projection is picked based on the degree of geographic clustering of the sites. To focus on Europe and use a more local projection, do:   
            
        .. jupyter-execute::     
            
            eur_coord = {'central_latitude':45, 'central_longitude':20}
            Euro2k.map(projection='Orthographic',proj_default=eur_coord) 
        
        By default, the shape and colors of symbols denote proxy archives; however, one can use either graphical device to convey other information. For instance, if elevation is available, it may be displayed by size, like so: 
        
        .. jupyter-execute::
            
            Euro2k.map(projection='Orthographic', size='elevation', proj_default=eur_coord) 
            
        Same with observationType:
            
        .. jupyter-execute::
            
            Euro2k.map(projection='Orthographic', hue = 'observationType', proj_default=eur_coord) 
        
        All three sources of information may be combined, but the figure height will need to be enlarged manually to fit the legend:
            
        .. jupyter-execute::
            
            Euro2k.map(projection='Orthographic',hue='observationType',
                       size='elevation', proj_default=eur_coord, figsize=[18, 8]) 

        '''

        fig, ax_d = mp.scatter_map(self, hue=hue, size=size, marker=marker,
                    edgecolor=edgecolor, projection=projection,
                                        proj_default=proj_default,
                                        crit_dist=crit_dist,
                                        background=background, borders=borders, rivers=rivers, lakes=lakes,
                                        ocean=ocean, coastline=coastline,
                                        land=land, gridspec_kwargs=gridspec_kwargs,
                                        figsize=figsize, scatter_kwargs=scatter_kwargs,
                                        lgd_kwargs=lgd_kwargs, legend=legend, colorbar=colorbar,
                                        cmap=cmap,
                                        fig=fig, gs_slot=gridspec_slot, **kwargs)
        return fig, ax_d

    def pca(self, weights=None,missing='fill-em',tol_em=5e-03, max_em_iter=100,**pca_kwargs):
        '''Principal Component Analysis (Empirical Orthogonal Functions)

        Decomposition of MultipleGeoSeries object in terms of orthogonal basis functions.
        Tolerant to missing values, infilled by an EM algorithm.

        Do make sure the time axes are aligned, however! (e.g. use `common_time()`)

        Algorithm from statsmodels: https://www.statsmodels.org/stable/generated/statsmodels.multivariate.pca.PCA.html

        Parameters
        ----------

        weights : ndarray, optional

            Series weights to use after transforming data according to standardize
            or demean when computing the principal components.

        missing : {str, None}

            Method for missing data.  Choices are:

            * 'drop-row' - drop rows with missing values.
            * 'drop-col' - drop columns with missing values.
            * 'drop-min' - drop either rows or columns, choosing by data retention.
            * 'fill-em' - use EM algorithm to fill missing value [ default].  ncomp should be
              set to the number of factors required.
            * `None` raises if data contains NaN values.

        tol_em : float

            Tolerance to use when checking for convergence of the EM algorithm.

        max_em_iter : int

            Maximum iterations for the EM algorithm.

        Returns
        -------

        res: MultivariateDecomp

            Resulting pyleoclim.MultivariateDecomp object

        See also
        --------

        pyleoclim.utils.tsutils.eff_sample_size : Effective Sample Size of timeseries y

        pyleoclim.core.multivardecomp.MultivariateDecomp : The multivariate decomposition object

        pyleoclim.core.mulitpleseries.MulitpleSeries.common_time : align time axes

        Examples
        --------

        .. jupyter-execute::

            from pylipd.utils.dataset import load_dir
            lipd = load_dir(name='Pages2k') # this loads a small subset of the PAGES 2k database
            lipd_euro = lipd.filter_by_geo_bbox(-20,20,40,80)
            df = lipd_euro.get_timeseries_essentials()
            dfs = df.query("archiveType in ('tree') & paleoData_variableName not in ('year')") 
            # place in a MultipleGeoSeries object
            ts_list = []
            for _, row in dfs.iterrows():
                ts_list.append(pyleo.GeoSeries(time=row['time_values'],value=row['paleoData_values'],
                                               time_name=row['time_variableName'],value_name=row['paleoData_variableName'],
                                               time_unit=row['time_units'], value_unit=row['paleoData_units'],
                                               lat = row['geo_meanLat'], lon = row['geo_meanLon'],
                                               elevation = row['geo_meanElev'], observationType = row['paleoData_proxy'],
                                               archiveType = row['archiveType'], verbose = False,
                                               label=row['dataSetName']+'_'+row['paleoData_variableName']))

            Euro2k = pyleo.MultipleGeoSeries(ts_list, label='Euro2k',time_unit='years AD')

            res = Euro2k.common_time().pca() # carry out PCA
            type(res) # the result is a MultivariateDecomp object

        To plot the eigenvalue spectrum:
            
        .. jupyter-execute::
            
            res.screeplot() 
            
        To plot the first mode, equivalent to `res.modeplot(index=0)`:
            
        .. jupyter-execute::
            
            res.modeplot() 
            
        To plot the second (note the zero-based indexing):
            
        .. jupyter-execute::    
            
            res.modeplot(index=1)  
            
        One can use map semantics to display the observation type as well:
            
        .. jupyter-execute::    
            
            res.modeplot(index=1, marker='observationType', size='elevation')

        There are many ways to configure the map component. As a simple example, specifying the projection:

        .. jupyter-execute::

            res.modeplot(index=1, marker='observationType', size='elevation',
                map_kwargs={'projection':'Robinson'})

        Or dive into the nuances of gridspec and legend configurations:

        .. jupyter-execute::

            res.modeplot(index=1, marker='observationType', size='elevation',
                        map_kwargs={'projection':'Robinson',
                                    'gridspec_kwargs': {'width_ratios': [.5, 1,14, 4], 'wspace':-.065},
                                    'lgd_kwargs':{'bbox_to_anchor':[-.015,1]}})

        '''
        # apply PCA fom parent class
        pca_res = super().pca(weights=weights,missing=missing,tol_em=tol_em,
                           max_em_iter=max_em_iter,**pca_kwargs)
        pca_res.orig = self  # add original object for plotting purposes

        return pca_res
        