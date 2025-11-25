import logging, logger

logging.info('Importing dependencies for fundamental data fetching')

from bs4 import BeautifulSoup as bs
from ib_async import IB, Stock

from constants import HOST, PORT, CLIENT_ID


logging.info('Connecting to broker')
ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID)


def fundamental_data(stock: str):
    logging.info('Fetching stock object')
    stock = Stock(stock, 'SMART', 'USD')
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
    fundamental_data('ALB')
