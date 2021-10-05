# -*- coding: utf-8 -*-
"""
Write the script to prepare the data frame
"""

def Transform__test_data(pair, test_data):
    pair_selection_test = test_data[[pair[0],pair[1] ]]
    pair_selection_test.loc[:,"timestamp"] = pair_selection_test.index    
    pair_selection_test = pair_selection_test.reset_index(drop=True)
    #Data Frame Preparation
    enter1 = pair[0] + "_enter"
    enter2 = pair[1] + "_enter"
    close1 = pair[0] + "_close"
    close2 = pair[1] + "_close"
    pair_selection_test.loc[:,enter1] = 0
    pair_selection_test.loc[:,enter2] = 0
    pair_selection_test.loc[:,close1] = 0
    pair_selection_test.loc[:,close2] = 0
    
    return(pair_selection_test) 

