import logging, logger

logging.info('Importing dependencies for data_gateway')
from ib_async import IB, Stock, util
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd

from constants import HOST, PORT, CLIENT_ID


logging.info('Connecting to broker')
ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID)


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
    df.to_csv(f'historical_data/{stock.symbol}.csv')

def onPendingTicker(ticker):
    logging.info('ticker event received')
    print(ticker)

def real_time_market_data():
    logging.warning('This data is delayed by 15 mins')
    ib.reqMarketDataType(3)
    logging.debug('Fetching conid')
    ib.qualifyContracts(stock)[0]
    logging.info('requesting real time market data')
    market_data = (
        ib.reqMktData(stock, '', False,False)
    )
    logging.info('Waiting for response from broker')
    ib.pendingTickersEvent += onPendingTicker

def fundamental_data():
    logging.info('Requesting fundamental data on stock')
    fundamentals = ib.reqFundamentalData(
        stock, 'ReportSnapshot'
    )
    logging.info('Parsing xml response')
    content = bs(fundamentals, 'xml')
    logging.info('Finding all fundamental ratios')
    logging.warning(
        'You must eventually expand this towards building a full '
        'fundamental profile of the stock and find a way to persist it'
    )
    ratios = content.find_all('Ratio')
    logging.info('Printing all fundamental ratios')
    for ratio in ratios:
        print(ratio['FieldName'])
        print(ratio.text)


if __name__ == '__main__':
    df = pd.read_pickle('gapped_up_stocks.pkl')

    for ticker in df['symbol']:
        print(ticker)
        stock = Stock(ticker, 'SMART', 'USD')
        historical_data(stock)
