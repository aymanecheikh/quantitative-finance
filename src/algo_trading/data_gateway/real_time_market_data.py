import logging, logger

from ib_async import IB, Stock

from constants import HOST, PORT, CLIENT_ID

logging.info('Connecting to broker')
ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID)


def onPendingTicker(ticker):
    logging.info('ticker event received')
    print(ticker)

def real_time_market_data(stock: str):
    stock = Stock(stock, 'SMART', 'USD')
    logging.warning('This data is delayed by 15 mins')
    ib.reqMarketDataType(3)
    logging.debug('Fetching conid')
    ib.qualifyContracts(stock)[0]
    logging.info('requesting real time market data')
    market_data = (
        ib.reqMktData(stock, '', False, False)
    )
    logging.info('Waiting for response from broker')
    ib.pendingTickersEvent += onPendingTicker
    logging.info('Streaming prices')
    ib.run()


if __name__ == '__main__':
    real_time_market_data('ALB')
