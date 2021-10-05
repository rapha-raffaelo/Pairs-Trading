#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 14:35:01 2021

@author: raphaelmankopf
"""

import numpy as np
import pandas as pd

import statsmodels
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts

from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm

import matplotlib.pyplot as plt
from datetime import date
import time
from datetime import datetime
from datetime import timedelta
import pickle

def Cointegration_test(train_data):
    assessed_pairs = []
    for x in train_data.columns:
        for y in train_data.columns.drop(x):
            
            ### Compute Cointegration
            x_data = train_data[[x]].values
            y_data = train_data[[y]].values
            t,p,crit = coint(x_data,y_data)
            print(x,y,p)
            
            if p < 0.01:
                #print("Series " + str(x) + "and" + str(y) + " are cointegrated")
                ###Compute Spread
                spread = x_data - y_data
                pval_spread = adfuller(spread)[1]
                if pval_spread <0.01:
                    print(pval_spread,'Data is Cointegrated & stationary!')
                    plot = train_data[[x,y]][:]
                    plot["spread"] = spread
                    fig = plt.figure()
                    plot[x].plot(figsize=(15,5), legend = True)
                    plot[y].plot(figsize=(15,5), legend = True)
                    plot["spread"].plot(figsize=(15,5), legend = True)
                    assessed_pairs.append((x,y))
                    fig.savefig( "Output_files/" + x + " " + y +".png")
                else:
                    #print(pval_spread, 'Data is NOT Stationary!')
    return(assessed_pairs)