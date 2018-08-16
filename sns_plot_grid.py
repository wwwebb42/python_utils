# Seaborn distribution plots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline

def sns_plot_grid(df, cols=3, split_vars=[],
                  g=None, sns_plot_fn = sns.boxplot, 
                  single_boxplot=False,
                  show_legend=True,
                  fg_kwargs=dict(), **kwargs ):
    
    """Plots various types of seaborn distribution plot on a grid, with one plot per column.
    Takes a dataframe, and returns a Seaborn FacetGrid object.
    split_vars = A list of one or two columns that split the output further. 
        For histograms, kde plots etc, this will give a different colour of 
        line, bar etc on each plot for each value of split_vars. For 
        boxplots, the first variable in split_vars will be the y axis of each
        plot, and the second with create groups within each y value.
    sns_plot_fn = the seaborn plotting function to use. So far, I've tested it with distplot, 
        kdeplot and boxplot.
    fg_kwargs are passed to sns.FacetGrid
    **kwargs are passed to sns.map"""

    df = df.copy()
    
#     Keep only numeric variables, apart from split_vars
    df_cols = list(df.select_dtypes('number').columns)
    
#    Add split vars to column list
    df_cols += [v for v in split_vars if v not in df_cols]
    
    df = df[df_cols]
    
#     Transpose the dataset
    df_t = df.melt(id_vars=split_vars) # Creates new columns called variable and value

    # For safety, convert the split variable to categorical
    for v in split_vars:
        df_t[v] = df_t[v].astype('category')

#     Select variables to plot
    plot_vars = ['value'] 
    facet_var='variable' 
    
#     Adjustments for different kinds of plot - especially the split variables
    if sns_plot_fn in [sns.boxplot, sns.violinplot]:
        hue=None    
        if single_boxplot:
            facet_var=None
            cols=None
            plot_vars.append('variable')
        elif len(split_vars) > 0:
            plot_vars += split_vars
    else:
        if len(split_vars) > 0:
            hue = split_vars.pop(0)

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



# A few tests...
if __name__ == "__main__":
    
    np.random.seed(123)
    df = pd.DataFrame(np.random.randn(500).reshape(100,5), columns=list('abcde'))
    group = pd.Series(np.random.choice([True, False], 100, replace=True, p=[0.5, 0.5]), name = 'group')
    group2 = pd.Series(np.random.choice([True, False], 100, replace=True, p=[0.5, 0.5]), name = 'group2')
    df = pd.concat([df, group, group2], axis=1)
    df.info()

#    sns_plot_grid(df)
#    plt.show()
#    
    g = sns_plot_grid(df, sns_plot_fn=sns.kdeplot, 
                  split_vars=['group'],
                  fg_kwargs=dict(sharex=False, sharey=False)
                 )

    g = sns_plot_grid(df, sns_plot_fn=sns.boxplot, 
                  split_vars=['group', 'group2'],
                  fg_kwargs=dict(sharex=False, sharey=False)
                 )

    g = sns_plot_grid(df, 
                  split_vars=['group'],
                  sns_plot_fn=sns.violinplot, 
                  fg_kwargs=dict(sharex=False, sharey=False),
                  inner='quart'
                 )