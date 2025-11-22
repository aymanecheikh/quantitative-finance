import asyncio

import pandas as pd
from lightweight_charts import Chart
from ib_insync import *
import nest_asyncio

nest_asyncio.apply()


def get_data(symbol: str, timeframe: str) -> pd.DataFrame:
    ib = IB()
    ib.connect('127.0.0.1', 4002, clientId=1)

    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='90 D',
        barSizeSetting=timeframe,
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )
    ib.disconnect()
    df = util.df(bars)
    df = df.rename(
        {
            'date': 'time',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        }
    )

    return df


class API:

    def __init__(self):
        self.chart: Chart | None = None

    async def on_search(
        self,
        chart: Chart,
        symbol: str
    ) -> None:
        self.chart = chart
        timeframe = chart.topbar['timeframe'].value
        df = get_data(symbol, timeframe)

        chart.set(df)
        chart.topbar['symbol'].set(symbol)

    async def on_timeframe(self, chart: Chart) -> None:
        self.chart = chart
        timeframe = chart.topbar['timeframe'].value
        symbol = chart.topbar['symbol'].value

        df = get_data(symbol, timeframe)
        chart.set(df)

async def main():
    api = API()

    with open('ticker_store.txt', 'r') as f:
        symbol = f.readlines()[0][:-1]
    timeframe = '15 mins'

    chart = Chart(
        title=f'{symbol} - {timeframe}',
        toolbox=True
    )
    api.chart = chart

    chart.topbar.textbox('symbol', symbol)
    chart.topbar.switcher(
        name='timeframe',
        options=('15 mins', '1 hour', '1 day'),
        default=timeframe,
        func=api.on_timeframe
    )

    chart.events.search += api.on_search

    df = get_data(symbol, timeframe)
    chart.set(df)

    await chart.show_async()

if __name__ == '__main__':
    asyncio.run(main())

