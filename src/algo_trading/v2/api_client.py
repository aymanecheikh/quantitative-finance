from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

from dotenv import load_dotenv
import os
import threading
import time
from decimal import Decimal
load_dotenv()


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 2 and reqId == 1:
            print('The current ask price is: ', price)
    # Add output for historical data
    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFullPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice
    ):
        print(
            'orderStatus - orderid:', orderId,
            'status:', status,
            'filled:', filled,
            'remaining:', remaining,
            'lastFillPrice:', lastFillPrice
        )
    def openOrder(self, orderId, contract, order, orderState):
        print(
            'openOrder id:', orderId,
            contract.symbol, contract.secType, '@', contract.exchange, ':',
            order.action, order.orderType, order.totalQuantity,
            orderState.status
        )
    def execDetails(self, reqId, contract, execution):
        print(
            'Order Executed: ',
            reqId,
            contract.symbol,
            contract.secType,
            contract.currency,
            execution.execId,
            execution.orderId,
            execution.shares,
            execution.lastLiquidity
        )
    def pnl(
        self,
        reqId: int,
        dailyPnL: float,
        unrealizedPnL: float,
        realizedPnL: float
    ):
        print(
            "Daily PnL. ReqId:", reqId,
            "DailyPnL:", dailyPnL,
            "UnrealizedPnL:", unrealizedPnL,
            "RealizedPnL:", realizedPnL
        )
    def position(
        self,
        account: str,
        contract: Contract,
        position: Decimal,
        avgCost: float
    ):
        print(
            "Position.",
            "Account:", account,
            "Contract:", contract,
            "Position:", position,
            "Avg cost:", avgCost
        )


def run_loop():
    app.run()


def crypto_order(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'CRYPTO'
    contract.exchange = 'PAXOS'
    contract.currency = 'USD'
    return contract



app = IBapi()
app.connect('127.0.0.1', 4002, 0)
app.nextorderId = None


api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()


while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        break
    else:
        print('waiting for connection')
        time.sleep(1)

app.reqPnL(0, os.getenv('DEMO_ACCT'), '')
app.reqPositions()
'''
order = Order()
order.action = 'SELL'
order.totalQuantity = 0.47579184
order.orderType = 'MKT'
order.tif = 'IOC'


app.placeOrder(app.nextorderId, crypto_order('ETH'), order)
app.nextorderId += 1
time.sleep(2)

eth = Contract()
eth.symbol = 'ETH'
eth.secType = 'CRYPTO'
eth.exchange = 'PAXOS'
eth.currency = 'USD'

app.reqMktData(1, eth, '', False, False, [])
app.reqHistoricalData(1, eth, '', '2 D', '1 hour', 'BID', 0, 2, False, [])

'''
