#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 14:14:39 2021

@author: raphaelmankopf
"""

import pandas as pd

import matplotlib.pyplot as plt
from datetime import date
import time
from datetime import datetime
from datetime import timedelta

def Backtesting(pair, pair1, pair2, pair_selection_test,full_data ):
    not_traded = []
    return_per_pair = []
    trades = pd.DataFrame(columns=['Trade_type', 'Trade_pair','BTC_balance','Token_1','Price_1','Token_2','Price_2','timestamp'])
    short_long = 0
    long_short = 0
    btc_balance = 1
    enter1 = pair1 + "_enter"
    enter2 = pair2 + "_enter"
    close1 = pair1 + "_close"
    close2 = pair2 + "_close"
    for i in range(0,len(pair_selection_test)):
        time_stamp = pair_selection_test.loc[i,"timestamp"]
        data_frame = full_data.loc[(time_stamp - timedelta(minutes=300*30)):time_stamp][[pair[0],pair[1] ]]        

        #Strategy Indicators
        data_frame.loc[:,"spread"] = data_frame.loc[:,pair[0]].values - data_frame.loc[:,pair[1]].values
        data_frame.loc[:,"std"] = data_frame.loc[:,"spread"].std()
        data_frame.loc[:,"mean"] = data_frame.loc[:,"spread"].mean()
        data_frame.loc[:,"upper"] = 2 * data_frame.loc[:,"std"] + data_frame.loc[:,"mean"]
        data_frame.loc[:,"lower"] = data_frame.loc[:,"mean"] - (2 * data_frame.loc[:,"std"])

        ###Signals
        data_frame.loc[:,"signal_short_long"] = data_frame.loc[:,"spread"]> data_frame.loc[:,"upper"]
        data_frame.loc[:,"signal_long_short"] = data_frame.loc[:,"spread"] < data_frame.loc[:,"lower"]

        try:

            if i == (len(pair_selection_test)-2) and short_long ==1:
                price_1 = pair_selection_test.at[(i + 1), pair1]
                price_2 = pair_selection_test.at[(i + 1), pair2]
                profit_1 = (position_short * price_1 + 0.5*btc_balance) + 0.5*btc_balance
                profit_2 = position_long * price_2
                btc_balance = profit_1 + profit_2
                short_long = 0
                pair_selection_test.at[(i), close1] = 1
                trades.loc[len(trades)] = ["forced_close_short_long",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]

            elif i == (len(pair_selection_test)-2) and long_short ==1:
                price_1 = pair_selection_test.at[(i + 1), pair1]
                price_2 = pair_selection_test.at[(i + 1), pair2]
                profit_1 = position_long * price_1
                profit_2 = (position_short * price_2 + 0.5*btc_balance) + 0.5*btc_balance

                btc_balance = profit_1 + profit_2
                long_short = 0
                short_enter_price = 0
                pair_selection_test.at[(i), close1] = 1
                trades.loc[len(trades)] = ["forced_close_long_short",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]

            else:
                if data_frame.at[time_stamp, "spread"] < data_frame.at[time_stamp, "mean"] and short_long == 1:
                    pair_selection_test.at[(i + 1), close1] = 1
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    profit_1 = (position_short * price_1 + 0.5*btc_balance) + 0.5*btc_balance
                    profit_2 = position_long * price_2
                    btc_balance = profit_1 + profit_2
                    short_long = 0
                    short_enter_price = 0
                    trades.loc[len(trades)] = ["exit_short_long",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]

                if data_frame.at[time_stamp, "spread"] > data_frame.at[time_stamp, "mean"] and long_short == 1:
                    pair_selection_test.at[(i + 1),close2] = 1
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    profit_1 = position_long * price_1
                    profit_2 = (position_short * price_2 + 0.5*btc_balance) + 0.5*btc_balance
                    btc_balance = profit_1 + profit_2
                    long_short = 0
                    short_enter_price = 0
                    trades.loc[len(trades)] = ["exit_long_short",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]
                    
                if data_frame.at[time_stamp, "signal_short_long"] == True and short_long == 0:
                    pair_selection_test.at[(i + 1), enter1] = -1
                    pair_selection_test.at[(i + 1), enter2] = 1
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    position_short = 0.5 * btc_balance*-1 / price_1
                    position_long = 0.5 * btc_balance / price_2
                    short_enter_price = price_1
                    short_long = 1
                    trades.loc[len(trades)] = ["enter_short_long",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]

                if data_frame.at[time_stamp, "signal_long_short"] == True and long_short == 0:
                    pair_selection_test.at[(i + 1), enter1] = 1
                    pair_selection_test.at[(i + 1), enter2] = -1
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    position_long = 0.5 * btc_balance  / price_1
                    position_short = 0.5 * btc_balance *-1 / price_2
                    short_enter_price = price_2
                    long_short = 1
                    trades.loc[len(trades)] = ["enter_long_short",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]
                    
                if long_short == 1 and (pair_selection_test.at[(i + 1), pair2]/short_enter_price-1)>0.2:
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    profit_1 = position_long * price_1
                    profit_2 = (position_short * price_2 + 0.5*btc_balance) + 0.5*btc_balance
                    btc_balance = profit_1 + profit_2
                    long_short = 0
                    short_enter_price = 0
                    pair_selection_test.at[(i), close1] = 1
                    trades.loc[len(trades)] = ["forced_liquidation_close_long_short",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]
                    
                if short_long == 1 and (pair_selection_test.at[(i + 1), pair1]/short_enter_price-1)>0.2:
                    price_1 = pair_selection_test.at[(i + 1), pair1]
                    price_2 = pair_selection_test.at[(i + 1), pair2]
                    profit_1 = (position_short * price_1 + 0.5*btc_balance) + 0.5*btc_balance
                    profit_2 = position_long * price_2
                    btc_balance = profit_1 + profit_2
                    short_long = 0
                    pair_selection_test.at[(i), close1] = 1
                    trades.loc[len(trades)] = ["forced_liquidation_close_short_long",(str(pair1) + "/" + str(pair2)), btc_balance, pair1, price_1,pair2 ,price_2, str(pair_selection_test.loc[(i+1), "timestamp"])]


        except:
            print("error",pair1,pair2, i)
    
    #Calculate overall return
    if len(trades) > 0:
        trades.loc[:,"returns"] = (trades.BTC_balance - trades.loc[0, "BTC_balance"]/trades.loc[0, "BTC_balance"])
    else:
        pass
        not_traded.append((pair1,pair2))
    #pair_selection[pair[0]].plot(figsize=(15,5), legend = True)
    #pair_selection[pair[1]].plot(figsize=(15,5), legend = True)
    fig = plt.figure()
    fig.suptitle((pair1 +"/" +pair2))    
    pair_selection_test.loc[:,"spread"] = pair_selection_test.loc[:,pair[0]].values - pair_selection_test.loc[:,pair[1]].values
    pair_selection_test.loc[:,"std"] = pair_selection_test.loc[:,"spread"].std()
    pair_selection_test.loc[:,"mean"] = pair_selection_test.loc[:,"spread"].mean()
    pair_selection_test.loc[:,"upper"] = 2 * pair_selection_test.loc[:,"std"] + pair_selection_test.loc[:,"mean"]
    pair_selection_test.loc[:,"lower"] = pair_selection_test.loc[:,"mean"] - (2 * pair_selection_test.loc[:,"std"])

    ###Signals
    pair_selection_test.loc[:,"signal_short_long"] = data_frame.loc[:,"spread"]> data_frame.loc[:,"upper"]
    pair_selection_test.loc[:,"signal_long_short"] = data_frame.loc[:,"spread"] < data_frame.loc[:,"lower"]
    pair_selection_test.index = pair_selection_test.timestamp.round('h')
    
    pair_selection_test.loc[:,"spread"].plot(figsize=(15,5), legend = True)
    pair_selection_test.loc[:,"upper"].plot(figsize=(15,5), legend = True)
    pair_selection_test.loc[:,"lower"].plot(figsize=(15,5), legend = True)
    pair_selection_test.loc[:,"mean"].plot(figsize=(15,5), legend = True)
    fig.savefig( "Output_files/" + pair1 + " " + pair2 +".png")
    plt.close(fig)    
    return_per_pair.append([(pair1,pair2),trades.at[(len(trades)-1),"returns"]] )

    return(trades, not_traded, return_per_pair)
