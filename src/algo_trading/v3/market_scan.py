import asyncio
from ib_async import IB, ScannerSubscription, TagValue
from ib_async.contract import Contract

# Note: Make sure ushmds is on


TOP_N = 10
HOST, PORT, CLIENT_ID = "127.0.0.1", 4002, 1

async def calc_gap_pct_async(ib: IB, contract: Contract):
    # ask only for what we need
    bars = await ib.reqHistoricalDataAsync(
        contract,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=False
    )
    if len(bars) < 2:
        return None
    today, prev = bars[-1], bars[-2]
    if prev.close and today.open:
        return (today.open - prev.close) / prev.close * 100.0
    return None

async def calc_since_open_pct(ib: IB, contract: Contract):
    bars = await ib.reqHistoricalDataAsync(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=False
    )
    if not bars:
        return None, None

    open_price = bars[0].open
    last_close = bars[-1].close
    day_high = max(b.high for b in bars)

    if open_price and last_close:
        since_open = (last_close - open_price) / open_price * 100.0
        max_run = (day_high - open_price) / open_price * 100.0
        return since_open, max_run
    return None, None


async def main():
    ib = IB()
    await ib.connectAsync(HOST, PORT, clientId=CLIENT_ID)

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


    scan_data = await ib.reqScannerDataAsync(
        sub,
        scannerSubscriptionFilterOptions=filters
    )
    rows = scan_data[:TOP_N]

    async def worker(d):
        c = d.contractDetails.contract

        gap = await calc_gap_pct_async(ib, c)
        since_open, max_run = await calc_since_open_pct(ib, c)
        return d.rank, c.symbol, gap, since_open, max_run

    results = await asyncio.gather(*(worker(d) for d in rows))

    for rank, sym, gap, since_open, max_run in results:
        gap_txt = f"{gap:.2f}%" if gap is not None else "n/a"
        since_open_txt = (
            f"{since_open:.2f}%" if since_open is not None else "n/a"
        )
        max_run_txt = f"{max_run:.2f}%" if max_run is not None else "n/a"
        
        print(
            f'Rank {rank:2d}: {sym:<6} gap {gap_txt} | '
            f'since-open {since_open_txt} | max-run {max_run_txt}'
        )


    ib.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
