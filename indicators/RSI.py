"""
RSI Calculation (Relative Strength Index)
Step 1: Calculating Up and Down Moves
Upmoves: Take the daily return if return is positive
         Take 0 if daily return is negative or zero
Downmoves: Absolute value of daily return if return is negative
           Zero if return is positive or zero
Step 2: Averaging up and down moves
        SMA or EMA
        Smooting factor.
Step 3: RS : Average Upmove / Average Downmove
        RSI: 100-100/(1+RS)
This code can open overlooping buy orders. That is not we want.
"""
import yfinance as yf
import matplotlib.pyplot as plt
import sqlalchemy
import pandas as pd
import numpy as np

def RSIcalc(df):
    df['MA200'] = df['close_price'].rolling(window=200).mean()
    df['Price Change'] = df['close_price'].pct_change()
    """Upmove is defined as take the price change of two timestamps, if it is positive then use it as same if it is 
    negative assign 0"""
    df['Upmove'] = df['Price Change'].apply(lambda x: x if x > 0 else 0)
    """Downmove is defined as take the price change of two timestamps, if it is negative then take absolute of it and 
    abs form, if it is positive assign 0"""
    df['Downmove'] = df['Price Change'].apply(lambda x: abs(x) if x < 0 else 0)
    """ exponential weighted (EW) functions : pandas.DataFrame.ewm is explained in 
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html#pandas-dataframe-ewm"""
    df['Avg Up'] = df['Upmove'].ewm(span=19).mean()
    df['Avg Down'] = df['Downmove'].ewm(span=19).mean()
    df = df.dropna()

    df['RS'] = df['Avg Up'] / df['Avg Down']
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))

    df.loc[(df['close_price'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
    df.loc[(df['close_price'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No'
    return df
#TODO: This part is problematic
def getSignals(df):
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)):
        """if there is the buy option as yes in that column"""
        if "Yes" in df['Buy'].iloc[i]:
            """This code is configured to sell the very next day of Buy signal at the opening of next day  """
            Buying_dates.append(df.iloc[i+1].name)
            """This loop checks if RSI value gets over 40 in following next 10 days. if the rsi gets over 40 after buy 
            day in the following 10 days we take next day of RSI over 40 day as selling date. Then we break the loop.
            And if RSI do not get over 40 following 10 days then we again get 11th day as sell day. This 10 number is 
            our choice"""
            for j in range(1 , 11):
                if df['RSI'].iloc[i + j] > 40:
                    Selling_dates.append(df.iloc[i+j+1].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i + j + 1].name)
    return Buying_dates, Selling_dates

def Profits():
    profits = (frame.loc[selldates].Open.values - frame.loc[buydates].Open.values)/frame.loc[buydates].Open.values
    wins = [i for i in profits if i > 0]
    winrate = len(wins) / len(profits)
    return profits, winrate

if __name__ == '__main__':
    pair = "BTCUSDT"
    interval = "1DAY"
    engine = sqlalchemy.create_engine('sqlite:///../history/DB/' + pair + '.db')
    prices = pd.read_sql('SELECT * FROM ' + pair + interval + '', engine)
    frame = RSIcalc(prices)
    buydates, selldates = getSignals(frame)

    #TODO: create a subplot to show them on same figure
    plt.figure(figsize=(30, 5))
    plt.scatter(frame.loc[buydates].index, frame.loc[buydates]['close_price'], marker='^', c='g')
    plt.scatter(frame.loc[selldates].index, frame.loc[selldates]['close_price'], marker='^', c='r')
    plt.plot(frame['close_price'], c='b', alpha=0.7)
    plt.show()

    plt.figure(figsize=(30, 5))
    plt.plot(frame['RSI'], c='r', alpha=0.7)
    plt.grid()
    plt.show()
    profits, winrate = Profits()
    print("Winning rate is :", winrate)

