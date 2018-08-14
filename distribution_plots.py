# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:48:02 2018

@author: StephenWebb

TODO: Histograms can display different bin widths if overlaying datasets 
    with different ranges. This is annoying but doesn't really affect 
    interpretation of the chart. 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def distribution_plots(df, ax=None, by=None, ncols=5, title='Distributions', 
                       describe=True,
                       plot_type='kde',
                       describe_df=True,
                       subplots_kwargs=dict(figsize = (8,6)), 
                       ax_kwargs={}):
    """Plots distribution of each column of a dataframe, optionally split by a by-variable. 
        It doesn't seem that any of the 'automatic' plotting options in pandas or seaborn give us the
        level of control that we want, so we have to control the sub-plots manually. 
        This is a bit hacky at the moment, bit it works..."""

#    print('Edited')
    
#   Keep only the numeric columns in the dataframe, and the by-variable
    keep_cols = list(df.select_dtypes('number').columns) 
    if by is not None:
        keep_cols += [by]
        
    df = df[keep_cols]
    
#   Print summary stats for df
    if describe_df:
        df.describe()
    
    df = df.loc[:, df.count() > 0] # Remove columns with all missing values
    
    #   For kde plots, remove any columns with only zero or 1 values
    if plot_type == 'kde':
        df = df.loc[:, df.std() > 0] # Remove any columns with std of zero
    else:
        pass #TODO: boxplots?...
    
    varlist = list(df.columns)
    nvars = len(varlist)
            
    # If we are using a by-variable, then group the dataframe
    if by is not None:
        varlist.remove(by) # Remove the by-variable from this list of columns we want to plot
        nvars += -1
    
    if (by is not None) & (plot_type != 'box'):
        df_to_plot = df.groupby(by)
    else:
        df_to_plot = df
    
    # How many rows do we need?
    nrows = int(np.ceil(nvars / ncols))
    
    if ax is None:
        fig, ax = plt.subplots(nrows, ncols, **subplots_kwargs) #squeeze=False, 
    
    # Special case for when we only have one row or column 
    if ncols == 1:
        ax = ax[:, np.newaxis]
    elif nrows == 1:
        ax = ax[np.newaxis, :]
        
    for i, c in enumerate(varlist):
        
        this_row = int(np.floor(i/ncols))
        this_col = int(i % ncols)
        this_ax = ax[this_row, this_col]
        
#       Plot it
#       TODO: include option for histogram overlaid with kde
        try:
            if plot_type == 'hist':
                df_to_plot[c].plot.hist(ax=this_ax, **ax_kwargs)
            elif plot_type == 'kde':
                df_to_plot[c].plot.kde(ax=this_ax, **ax_kwargs)
            elif plot_type == 'box':
                df_to_plot[[c, by]].boxplot(ax=this_ax, vert=False, by=by, **ax_kwargs) #TODO: may remove vert=False...
        except (TypeError, ValueError):
            print('Type error...')
            print('Column = ', c)
        
        # Control axis labels, ticks, etc
        if plot_type != 'box':
            pass
#            this_ax.set_ylabel('')
#            this_ax.set_yticks([])
        elif plot_type == 'box':
            this_ax.set_xlabel('')

        this_ax.set_title(c)
        
        # If we are on the last plot, and we are using a by-variable, 
        # then add a single legend outside the main plot area.
        # TODO: Add parameter to control the legend position
        if (i == nvars-1) and (by is not None) and (plot_type != 'box'):
            handles, labels = this_ax.get_legend_handles_labels()
            fig.legend(handles, labels, loc='center right')

#     Remove unused axes (must be a more elegant way of doing this...)
    for i, a in enumerate(ax.flatten()):
        if i >= nvars:
            fig.delaxes(a)
    
    # Add main title, and adjust the subplots area so it does not overlap the title or legend
    fig.suptitle(title)
    fig.tight_layout()
    
    adjust_params = dict(top=0.9)
    if by is not None:
        adjust_params['right'] = 0.85
    fig.subplots_adjust(**adjust_params)
    return ax


