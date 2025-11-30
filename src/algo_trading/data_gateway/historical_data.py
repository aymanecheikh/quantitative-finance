import logging, logger

logging.info('Importing dependencies for data_gateway')
from ib_async import IB, Stock, util
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd

from cloud.storage import upload_blob
from constants import IBAPI, CloudStorage


logging.info('Connecting to broker')
ib = IB()
ib.connect(IBAPI.HOST, IBAPI.PORT, clientId=IBAPI.CLIENT_ID)


def historical_data(stock: str):
    logging.info('Fetching historical data')
    bars = ib.reqHistoricalData(
        stock,
        endDateTime='',
        durationStr='10 Y',
        barSizeSetting='2 hours',
        whatToShow='TRADES',
        useRTH=True
    )
    
    logging.info('Converting historical data response to dataframe')
    df = util.df(bars)
    #df['price_returns'] = df.volume.pct_change().dropna()
    #df['volume_returns'] = df.volume.pct_change().dropna()
    #df.price_returns[df.price_returns == np.inf] = 0
    #df.volume_returns[df.volume_returns == np.inf] = 0
    logging.info('Printing dataframe')
    print(df)
    logging.info('Persisting dataframe to disk as csv')
    logging.warning('Is this the best method for persistence?')
    if df is None:
        return None
    file_name = f"{stock.symbol}.csv"
    df.to_csv(f'historical_data/{file_name}')
    upload_blob(
        CloudStorage.BUCKET_NAME,
        f'historical_data/{file_name}',
        file_name
    )


def get_historical_data():
    # Remember to swap this out for param in pipelines.py
    df = pd.read_pickle('gapped_up_stocks.pkl')
    for ticker in df['symbol']:
        print(ticker)
        stock = Stock(ticker, 'SMART', 'USD')
        historical_data(stock)


if __name__ == '__main__':
    get_historical_data()
