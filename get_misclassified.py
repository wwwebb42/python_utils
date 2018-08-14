# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 09:15:08 2018

@author: StephenWebb

TODO:   Improve how we handle the concat of the dataframes 
        Remove duplicated code
"""
import numpy as np
import pandas as pd

def get_misclassified(X, y_true, y_score, 
                      y_classes=(0,1),
                      misclassification_thresholds=(0.5, 0.5)):
    """ Returns a dataframe conataining observations that are defined as
    misclassified: i.e. where estimated probability > high_threshold and
    true class is negative, or estimated probability < low_threshold and
    true class is positive. 
    misclassification_thresholds = a tuple, (low_threshold, high_threshold)
    y_classes = a tuple containing the values that indicate a negative or positive class"""

#   Flag the cases that are misclassified
    low_threshold = misclassification_thresholds[0]
    high_threshold = misclassification_thresholds[1]
    
    negative_class = y_classes[0]
    positive_class = y_classes[1]

    fp_flag = (y_score > high_threshold ) & (y_true == negative_class)
    fn_flag = (y_score < low_threshold) & (y_true == positive_class) 

#   False positives
    fp_y = pd.DataFrame({'y_true' : y_true[fp_flag], 
                           'y_score' : y_score[fp_flag],
                           'type' : 'FP'})
    fp_X = X[fp_flag]
    fp_X.reset_index(inplace=True)
    fp_out = pd.concat([fp_X, fp_y], axis=1)   
    
#   False negatives
    fn_y = pd.DataFrame({'y_true' : y_true[fn_flag], 
                           'y_score' : y_score[fn_flag],
                           'type' : 'FN'})
    fn_X = X[fn_flag]
    fn_X.reset_index(inplace=True)
    fn_out = pd.concat([fn_X, fn_y], axis=1)    

    return pd.concat([fp_out, fn_out], axis=0)    

 

