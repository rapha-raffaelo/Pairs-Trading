#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 14:39:50 2021

@author: raphaelmankopf
"""

import numpy as np
import pandas as pd
from binance.client import Client
import time

def get_data(key, password, start_date, end_date):
    #Get all margin pairs
    client = Client(key, password)
    info = client.get_all_isolated_margin_symbols()
    data = pd.DataFrame.from_dict(info)
    data = data[data.quote == "BTC"]
    data.shape
    coins = data["symbol"].values
    
    #1. Get rowwise data
    #data = pd.DataFrame()
    #for x in coins[2:5]:
        #klines = client.get_historical_klines(x, Client.KLINE_INTERVAL_30MINUTE, "1 July, 2021", "1 Aug, 2021")
    #    price_data_1_hour = pd.DataFrame.from_dict(klines)
    #    price_data_1_hour=price_data_1_hour.rename(columns={0: "opentime", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume",
    #                                   6: "close time", 7: "quote asset volume", 8: "number of trades",
#                                    9: "Taker buy base asset volume", 10: "Taker buy quote asset volume",
#                                    11: "Ignore"})
#        price_data_1_hour.loc[:,"symbol"] = x
#        data = data.append(price_data_1_hour)
        #data = data.apply(pd.to_numeric)
        
    #2. Get Data Column-wise
    data = pd.DataFrame()
    for x in coins[0:100]:
        klines = client.get_historical_klines(x, Client.KLINE_INTERVAL_30MINUTE, start_date,end_date )
        price_data_1_hour = pd.DataFrame.from_dict(klines)
        price_data_1_hour=price_data_1_hour.rename(columns={0: "opentime", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume",
                                       6: "close time", 7: "quote asset volume", 8: "number of trades",
                                        9: "Taker buy base asset volume", 10: "Taker buy quote asset volume",
                                        11: "Ignore"})
        new_pair = price_data_1_hour[["close", "close time"]]
        newpair = new_pair.rename(columns ={"close": x})
        if data.shape[0]== 0:
            data = newpair
        else:
            data = data.merge(newpair, how = "left", on = "close time")
        time.sleep(5)
        print(x)
    data = data.apply(pd.to_numeric)
    data = data.fillna(0)
    
    return(data)
    
