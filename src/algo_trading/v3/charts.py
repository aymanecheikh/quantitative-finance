import pandas as pd
import talib
import yfinance as yf
from lightweight_charts import Chart


if __name__ == '__main__':
    chart = Chart()

    with open('ticker_store.txt', 'r') as text_file:
        ticker = text_file.readlines()[0]

    stock = yf.Ticker(ticker)
    df = stock.history(period='1y')[[
        'Open', 'High', 'Low', 'Close', 'Volume'
    ]]
 
    sma = talib.SMA(df.Close, timeperiod=20)
    sma = sma.reset_index()
    sma = sma.rename(columns={'Date': 'time', 0: 'value'})

    sma = sma.dropna()
    print(sma)

    df.reset_index()
    df.columns = df.columns.str.lower()
    chart.set(df)

    line = chart.create_line()
    line.set(sma)
    chart.watermark(ticker)
    chart.show(block=True)
