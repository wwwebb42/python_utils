# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:29:21 2018

@author: StephenWebb
"""
import numpy as np
import pandas as pd


def col_freqs(df, include_if_nunique_le=100, max_cats=10, print_output=True):
    """ Takes a dataframe, and outputs frequency tables of all object columns. 
        Only displays the top max_cats values in each column - values not in 
        the top max_cats are categorised as 'Other', and displayed at the bottom of the list. 
        (Fewer than max_cats categories may be displayed if there are tied ranks.)"""
    
    out = []
    
#     Include all object columns, and any other with fewer than xxx values, 
#     regardless of their type
    col_list = df.columns[(df.nunique() <= include_if_nunique_le) | (df.dtypes == 'object')]
    
#     for col in df.select_dtypes(include=['object']).columns:
    for col in col_list:
        
        # Calculate cumulative count of obs in each rank
        # This is a bit horrible, but I can't find an elegant way of doing it...
        
        # Value counts
        vc = df[col].value_counts()

        #Value counts, ranked
        vc_r = vc.rank(method='dense', ascending=False)

        # Value counts ranked, with cumulative number of records at each rank
        vc_r_cum = vc_r.value_counts().sort_index().cumsum()

        # Expand to shape of original series
        cum_rc = np.array([vc_r_cum[z] for z in vc_r])
            
        # Label any categories with a rank > max_cats as 'Other'
        cats_with_other = np.where(cum_rc <= max_cats, 
                                   [vc.index[i] for i, c in enumerate(cum_rc)], 'Other')
        
        # Calculate number of observations, and % of total
        f = pd.DataFrame({'category' : cats_with_other, 'obs' : vc})
        percs = f.groupby('category')['obs'].sum() / f['obs'].sum() * 100
        obs = f.groupby('category')['obs'].sum() 
        
        # Put them into a dataframe
        z = pd.concat([obs, percs], axis=1)
        z.columns = ['obs', '% of total']
         
        # Add ranks
        z['ranks'] = z['obs'].rank()

        # Set the rank of 'Other' to zero, ensuring it always appears at the bottom of the list
        if 'Other' in z.index:
            z.loc['Other', 'ranks'] = 0
 
        # Sort by rank
        z.sort_values(by='ranks', ascending=False, inplace=True)
        z.drop('ranks', axis=1, inplace=True)
 
        # Add the column name as the first level in the multi-index
        z = pd.concat([z], keys=[col], names=['column_name'])

        out.append(z)
    
    outdf = pd.concat(out)
    
    if print_output:
        for c in outdf.index.levels[0]:
            print('*** {} ***'.format(c))
            print('Number of unique values: ', df[c].nunique())
            print('Percent missing: {:5.2f}'.format((1- (df[c].count() / len(df[c]))) * 100 ), '\n')
            print(outdf.loc[c], '\n')

    return pd.concat(out)


if __name__ == '__main__':
    import seaborn as sns
    data = sns.load_dataset('titanic')
    data_stats = col_freqs(data)


