# Seaborn distribution plots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def sns_plot_grid(df, cols=3, split_var=None,
                  g=None, sns_plot_fn = sns.boxplot, 
                  single_boxplot=False,
                  show_legend=True,
                  fg_kwargs=dict(), **kwargs ):
    
    """Plots various types of seaborn distribution plot on a grid, with one plot per column.
    Takes a dataframe, and returns a Seaborn FacetGrid object.
    split_var = A column which splits the output further. For histograms, kde plots etc, this will
        give a different colour of line, bar etc on each plot for each value of split_var. For 
        boxplots, split_var will be the y axis of each plot.
    sns_plot_fn is the seaborn plotting function to use. So far, I've tested it with distplot, 
        kdeplot and boxplot.
    fg_kwargs are passed to sns.FacetGrid
    **kwargs are passed to sns.map"""

    # Edited, 13:37, 15/08/2018

    df = df.copy()
    
#     Keep only numeric variables, apart from split_var
    df_cols = list(df.select_dtypes('number').columns)
    if (split_var is not None) and (split_var not in df_cols):
        df_cols.append(split_var)
    df = df[df_cols]
    
#     Transpose the dataset
    df_t = df.melt(id_vars=split_var) # Creates new columns called variable and value

    # For safety, convert the split variable to categorical
    if split_var is not None:
        df_t[split_var] = df_t[split_var].astype('category')

#     Select variables to plot
    plot_vars = ['value'] 
    facet_var='variable' 
    hue=split_var
    
#     Adjustments for boxplot
    if sns_plot_fn in [sns.boxplot, sns.violinplot]:
        hue=None    
        if single_boxplot:
            facet_var=None
            cols=None
            plot_vars.append('variable')
        elif split_var is not None:
            plot_vars.append(split_var)

    if g is None:
        g = sns.FacetGrid(df_t, col=facet_var, hue=hue, col_wrap=cols, legend_out=False, **fg_kwargs)
        
    g.map(sns_plot_fn, *plot_vars, **kwargs)
    
#     Fix the titles for each subplot
    axes = g.axes.flatten()
    for ax in axes:
        ax.set_title(ax.get_title().replace('variable = ', ''))
        ax.set_xlabel('')
        ax.set_ylabel('')
    
    if show_legend:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return g
