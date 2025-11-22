from ib_async import IB, Stock, util
from bs4 import BeautifulSoup as bs
import pandas as pd
HOST, PORT, CLIENT_ID = '127.0.0.1', 4002, 1

ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID)


def historical_data(stock: str):
    bars = ib.reqHistoricalData(
        stock,
        endDateTime='',
        durationStr='10 Y',
        barSizeSetting='2 hours',
        whatToShow='TRADES',
        useRTH=True
    )

    df = util.df(bars)
    print(df)
    df.to_csv(f'historical_data/{stock.symbol}.csv')

def onPendingTicker(ticker):
    print('ticker event received')
    print(ticker)

def real_time_market_data():
    ib.reqMarketDataType(3)
    ib.qualifyContracts(stock)[0]
    market_data = (
        ib.reqMktData(stock, '', False,False)
    )
    ib.pendingTickersEvent += onPendingTicker

def fundamental_data():
    fundamentals = ib.reqFundamentalData(
        stock, 'ReportSnapshot'
    )
    content = bs(fundamentals, 'xml')
    ratios = content.find_all('Ratio')
    for ratio in ratios:
        print(ratio['FieldName'])
        print(ratio.text)


if __name__ == '__main__':
    df = pd.read_pickle('gapped_up_stocks.pkl')

    for ticker in df['symbol']:
        print(ticker)
        stock = Stock(ticker, 'SMART', 'USD')
        historical_data(stock)
