from ibapi.contract import Contract
import time
import threading
from api_client import IBapi

# contract_map_id is the list index
contract_map = [
    {
        'symbol': 'BTC',
        'secType': 'CRYPTO',
        'exchange': 'PAXOS'
    },
    {
        'symbol': 'ETH',
        'secType': 'CRYPTO',
        'exchange': 'PAXOS'
    },
    {
        'symbol': 'AAPL',
        'secType': 'STK',
        'exchange': 'SMART'
    }
]


# Map symbol to security type and exchange
def contract_profile(contract_map_id: int):
    contract = Contract()
    focus = contract_map[contract_map_id]
    contract.symbol = focus['symbol']
    contract.secType = focus['secType']
    contract.exchange = focus['exchange']
    contract.currency = 'USD'
    return contract


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 4002, 0)


api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)

# Get a full list of symbols to run through the search - maybe persist
# offline and figure out how to systemically pull candidates for trading?
# !!!!!!!!!!!!!!! Or use the market scanner? !!!!!!!!!!!!!!!!!!
# LATEST :: We have an xml file with all thescanner params. Next session I
# will parse it and and figure out how to get a list of tickers



# Once candidates are selected, we fetch historical prices, which is then
# processed downstream

# We also need to make it such that we trigger live market feed for crypto
# and delayed for anything that's blocked by the market data subscription

### app.reqMatchingSymbols(0, 'NVDA')

'''
for i in range(len(contract_map)):
    app.reqContractDetails(0, contract_profile(i))
    time.sleep(1)
'''
