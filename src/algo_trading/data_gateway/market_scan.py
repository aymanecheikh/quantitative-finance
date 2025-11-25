import asyncio
import pandas as pd
from ib_async import IB, ScannerSubscription, TagValue
from ib_async.contract import Contract
from constants import *
import logging, logger


async def calc_gap_pct_async(ib: IB, contract: Contract):
    # ask only for what we need
    logging.info('Requesting historical data for calculating gap size.')
    bars = await ib.reqHistoricalDataAsync(
        contract,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=False
    )
    logging.debug(
        'Checking that there are more than two data points in '
        'historical data.'
    )
    if len(bars) < 2:
        logging.warning(
            'There is insufficient data to calculate gap size '
            'for this stock.'
        )
        return None
    logging.debug('Fetching last two data points.')
    today, prev = bars[-1], bars[-2]
    logging.debug('Checking that open price is available for last data point.')
    logging.debug(
        'Checking that close price is available for penultimate '
        'data point'
    )
    if prev.close and today.open:
        logging.info('Calculating gap size.')
        return (today.open - prev.close) / prev.close * 100.0
    logging.warning(
        'There is insufficient data to calculate gap size for '
        'this project.'
    )
    return None

async def calc_since_open_pct(ib: IB, contract: Contract):
    logging.info(
        'Requesting historical data for the day for calculating post gap run '
        'size.'
    )
    bars = await ib.reqHistoricalDataAsync(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=False
    )
    logging.debug('Checking if historical data has been returned.')
    if not bars:
        logging.warning(
            'There is insufficient data to calculate post gap '
            'run size.'
        )
        return None, None
    
    logging.info('Fetching first open price for the day.')
    open_price = bars[0].open
    logging.info('Fetching latest closing price.')
    last_close = bars[-1].close
    logging.info('Fetching max price for the day.')
    day_high = max(b.high for b in bars)
    
    logging.debug('Checking if open price for the day is available.')
    logging.debug('Checking if latest close for the day is available.')
    if open_price and last_close:
        logging.info('Calculating percentage change since open.')
        since_open = (last_close - open_price) / open_price * 100.0
        logging.info(
            'Calculating percentage change between open price for '
            'the day and highest price.'
        )
        max_run = (day_high - open_price) / open_price * 100.0
        logging.info(
            'Returning pct change since open and pct change '
            'between open and highest price point.'
        )
        return since_open, max_run
    logging.warning(
        'There is insufficient data to calculate pct changes '
        'between open and close vs open and highest price point.'
    )
    return None, None


async def main():
    logging.info('Connecting to broker.')
    ib = IB()
    await ib.connectAsync(HOST, PORT, clientId=1)
    
    logging.info(
        'Subscribing to high open gap scanner for Major US Stocks\n'
        '@ mkt cap over 10,000,000,000\n'
        '@ USD Price > 10\n'
        '@ Volume > 1,000,000\n'
        '@ Pct Change Since Open > 3%\n'
    )
    sub = ScannerSubscription()
    sub.instrument   = 'STK'
    sub.locationCode = 'STK.US.MAJOR'
    sub.scanCode     = 'HIGH_OPEN_GAP'

    filters = [
        TagValue('marketCapAbove1e6', '10000'),
        TagValue('usdPriceAbove', '10'),
        TagValue('volumeAbove', '1000000'),
        TagValue('changeOpenPercAbove', '3')
    ]

    logging.info('Requesting data from scaner subscription')
    scan_data = await ib.reqScannerDataAsync(
        sub,
        scannerSubscriptionFilterOptions=filters
    )
    logging.info(
        'Filtering data to top N scanner results using const from '
        'constants.py'
    )
    rows = scan_data[:TOP_N_SCANNER_RESULTS]
    
    logging.info(
        'Defining async worker to call historical data fetches, gap '
        'sizes, and post gap runs'
    )
    async def worker(d):
        logging.info('Fetching contract details for corresponding stock')
        c = d.contractDetails.contract
        
        logging.info('Calculating gap size')
        gap = await calc_gap_pct_async(ib, c)
        logging.info('Calculating post gap run size from open and from highest price')
        since_open, max_run = await calc_since_open_pct(ib, c)
        logging.info(
            'Returning scanner rank, ticker, gap size, post gap run '
            'since open, and post gap run from highest'
        )
        return d.rank, c.symbol, gap, since_open, max_run
    
    logging.info(
        'Calling asynchronous workers to run the gap size and post '
        'gap run calcs for each stock asynchronously'
    )
    results = await asyncio.gather(*(worker(d) for d in rows))
    
    logging.info('Initializing list to store resulting data from scanner subscription')
    entries = []  
    for rank, sym, gap, since_open, max_run in results:
        logging.info(
            'Initializing dict to store resulting details per entry '
            'to be appended to initialized list above'
        )
        entry = {}
        logging.info('Adding ticker to entry')
        entry['symbol'] = sym
        logging.info('Adding gap size to entry')
        entry['gap'] = gap
        logging.info('Adding post gap run since open')
        entry['since_open'] = since_open
        logging.info('Adding post gap run from highest point')
        entry['max_run'] = max_run
        logging.info('Submitting entry to scanner result list')
        entries.append(entry)
        logging.info('Formatting output for logging purposes')
        gap_txt = f"{gap:.2f}%" if gap is not None else "n/a"
        since_open_txt = (
            f"{since_open:.2f}%" if since_open is not None else "n/a"
        )
        max_run_txt = f"{max_run:.2f}%" if max_run is not None else "n/a"
        
        logging.info(
            f'Rank {rank:2d}: {sym:<6} gap {gap_txt} | '
            f'since-open {since_open_txt} | max-run {max_run_txt}'
        )

    logging.info('Disconnecting from broker')
    ib.disconnect()
    logging.info('Returning entries')
    return entries


def get_gapped_up_stocks():
    logging.info('Running pipeline')
    x = asyncio.run(main())
    logging.info('Persisiting output to pkl file')
    df = pd.DataFrame.from_dict(x)
    df.to_pickle('gapped_up_stocks.pkl')
    return df


if __name__ == '__main__':
    get_gapped_up_stocks()
