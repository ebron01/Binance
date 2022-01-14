"""
Crossover strategy: Buy an asset if short term moving average(last 20 days) crosses above long term(last 50 days) moving
average. Sell an asset if short term moving average crosses below long term moving average.
If 50 days short term moving average crosses over 200 days long term moving average it is calles "GOLDEN CROSS", if vice
versa, it is called "DEATH CROSS".
"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy

pair = "ETHUSDT"
interval = "1DAY"
engine = sqlalchemy.create_engine('sqlite:///C:/Users/a/PycharmProjects/Binance/history/DB/'+pair+'.db')

prices = pd.read_sql('SELECT * FROM ' + pair + interval + '', engine)

prices['MA20'] = prices['close_price'].rolling(20).mean()
prices['MA50'] = prices['close_price'].rolling(50).mean()

"""Because MA20 will not be available for first 19 and MA50 for first 49 rows we drop them."""
prices = prices.dropna()
prices = prices[['close_price', 'MA20', 'MA50', 'close_time']]

Buy = []
Sell = []
for i in range(len(prices)):
    if i == 0:
        continue
    if prices.MA20.iloc[i] > prices.MA50.iloc[i] and prices.MA20.iloc[i-1] < prices.MA50.iloc[i-1]:
        Buy.append(i)
    elif prices.MA20.iloc[i] < prices.MA50.iloc[i] and prices.MA20.iloc[i-1] > prices.MA50.iloc[i-1]:
        Sell.append(i)
print(f"buy days: {Buy}")

print(f"sell days: {Sell}")

"""This plot shows the buy and sell signal"""
plt.figure(figsize=(12, 5))
plt.plot(prices['close_price'], label='Asset Price', c='blue', alpha=0.5)
plt.plot(prices['MA20'], label='MA20', c='black', alpha=0.9)
plt.plot(prices['MA50'], label='MA50', c='magenta', alpha=0.9)
plt.scatter(prices.iloc[Buy].index, prices.iloc[Buy]['MA20'], marker='^', color='g', s=100)
plt.scatter(prices.iloc[Sell].index, prices.iloc[Sell]['MA20'], marker='v', color='r', s=100)
plt.legend()
plt.show()


