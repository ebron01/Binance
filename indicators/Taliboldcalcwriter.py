"""official sites for TA-Lib Technical Analysis Library- Indicator List
https://www.ta-lib.org/function.html
"""
import sqlalchemy
import pandas as pd
from data.coins import coin_details
from indics import indicator
import sqlite3

if __name__ == '__main__':
    symbol, intervals = coin_details()
    engine = sqlalchemy.create_engine('sqlite:///./../history/DBDEV/DEVSELECTED_15JAN.db')
    # timestamp = "2022-01-20 23:59:59.999000"
    for pair in symbol:
        for interval in intervals:
            prices = pd.read_sql('SELECT s.open_time , s.open_price, s.high_price, s.low_price, s.close_price, s.volume, s.close_time FROM ' + pair + interval +
                ' s', engine)
            # indexes = prices[prices['close_time'] > '2022-01-20 23:59:59.999000'].index
            # prices = prices.drop(indexes)
            """Does required calculations based on indicator types"""
            indicators = indicator.Indicators()
            result = indicator.Calculate.calculator(indicators, prices)
            result_keys = result.keys()
            """fills nan values with 0 to be able to write to database"""
            for i in range(len(result_keys)):
                try:
                    result_keys[i] = result_keys[i].fillna(0)
                except:
                    continue
            """inserts all calculated ta to the affiliated columns"""
            tablename = pair + interval
            connection = sqlite3.connect('./../history/DBDEV/DEVSELECTED_15JAN.db')  # creates a new database if there is none.
            cursor = connection.cursor()
            print(f'Started insert of {tablename}')
            for i in range(len(result.pricetime)):
                cursor.execute(f'''UPDATE {tablename} SET rsi=?, rsibasedma=?,  macd=?, macdsignal=?, macdhist=?, pricetime=?,
                        obv=?, kauf=?, obv_ema=?, chande=?, bbandupper=?, bbandmiddle=?, bbandlittle=?, dmi=?, dmineg=?, dmiplus=?, closeprice=? WHERE open_time=?''',
                               (result.rsi.iloc[i], result.rsibasedma.iloc[i],
                                result.macd.iloc[i],
                                result.macdsignal.iloc[i],
                                result.macdhist.iloc[i], result.pricetime.iloc[i],
                                result.obv.iloc[i], result.kauf.iloc[i],
                                result.obv_ema.iloc[i], result.chande.iloc[i],
                                result.bbandupper.iloc[i],
                                result.bbandmiddle.iloc[i], result.bbandlittle.iloc[i],
                                result.dmi.iloc[i],
                                result.dmineg.iloc[i], result.dmiplus.iloc[i],
                                result.closeprice.iloc[i],
                                result.pricetime.iloc[i]))
                connection.commit()
                if i % 10000 == 0 :
                    print(f'Done {i}')
            print(f'Done insert of {tablename}')


