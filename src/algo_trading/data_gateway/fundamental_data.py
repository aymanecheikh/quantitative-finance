import logging, logger

logging.info('Importing dependencies for fundamental data fetching')

from bs4 import BeautifulSoup as bs
from ib_async import IB, Stock

from constants import Fundamentals, IBAPI


logging.info('Connecting to broker')
ib = IB()
ib.connect(IBAPI.HOST, IBAPI.PORT, clientId=IBAPI.CLIENT_ID)


def fetch_stock_details(stock: str):
    logging.info('Fetching stock object')
    logging.warning(
        'Shouldn\'t you be setting \'SMART\' and \'USD\' as '
        'constants?'
    )
    return Stock(stock, 'SMART', 'USD')


def financial_summary(stock: str):
    logging.info('Requesting financial summary on stock')
    fundamentals = ib.reqFundamentalData(
        fetch_stock_details(stock),
        Fundamentals.FINANCIAL_SUMMARY.value
    )
    logging.info('Parsing xml response')
    content = bs(fundamentals, 'xml')
    return content

def company_ownership(stock: str):
    logging.info('Requesting ownership on stock')
    fundamentals = ib.reqFundamentalData(
        fetch_stock_details(stock),
        Fundamentals.COMPANY_OWNERSHIP.value
    )
    logging.info('Parsing xml response')
    content = bs(fundamentals, 'xml')
    return content

def company_financial_overview(stock: str):
    logging.info('Requesting financial overview on stock')
    fundamentals = ib.reqFundamentalData(
        fetch_stock_details(stock),
        Fundamentals.COMPANY_FINANCIAL_OVERVIEW.value
    )
    logging.info('Parsing xml response')
    content = bs(fundamentals, 'xml')
    return content
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

def company_financial_statements(stock: str):
    """
    Company data is unavailable
    """
    logging.info('Requesting financial statements on stock')
    fundamentals = ib.reqFundamentalData(
        fetch_stock_details(stock),
        Fundamentals.FINANCIAL_STATEMENTS.value
    )
    return fundamentals


if __name__ == '__main__':
    company_financial_overview('AAPL')
