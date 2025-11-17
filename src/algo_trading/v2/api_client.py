from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.scanner import ScanData
from ibapi.contract import *
from ibapi.order import Order

from dotenv import load_dotenv
from decimal import Decimal
import os
import threading
import time
load_dotenv()


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


    def scannerParameters(self, xml: str):
        open('log/scanner.xml', 'w').write(xml)
        print("ScannerParameters received.")

    def scannerData(
        self,
        reqId: int,
        rank: int,
        contractDetails: ContractDetails,
        distance: str,
        benchmark: str,
        projection: str,
        legsStr: str
    ):
        print(
            "ScannerData. ReqId:", reqId,
            ScanData(
                contractDetails.contract,
                rank,
                distance,
                benchmark,
                projection,
                legsStr
            )
        )

    def symbolSamples(
        self,
        reqId: int,
        contractDescriptions: ContractDescription
    ):
        print("Symbol Samples. Request Id: ", reqId)
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += " "
                derivSecTypes += derivSecType
                print(
                    "Contract: conId:%s, symbol:%s,"
                    "secType:%s primExchange:%s, "
                    "currency:%s, derivativeSecTypes:%s, description:%s, "
                    "issuerId:%s"
                    %
                    (
                        contractDescription.contract.conId,
                        contractDescription.contract.symbol,
                        contractDescription.contract.secType,
                        contractDescription.contract.primaryExchange,
                        contractDescription.contract.currency,
                        derivSecTypes,
                        contractDescription.contract.description,
                        contractDescription.contract.issuerId
                        )
                    )


def run_server():
    def run_loop():
        app.run()

    app = IBapi()
    app.connect('127.0.0.1', 4002, 0)

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(1)
    return app











































'''
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
