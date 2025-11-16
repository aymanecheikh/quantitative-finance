import requests, time, os
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


BASE_URL = 'https://localhost:5000/v1/api'
session = requests.Session()
session.verify = False


session_init = session.post(
    url=f'{BASE_URL}/iserver/auth/ssodh/init',
    json={'publish': True, 'compete': True}
)
account = (
    session.get(url=f'{BASE_URL}/portfolio/accounts').json()[0]['accountId']
)
bitcoin_id = session.get(
    url=f'{BASE_URL}/iserver/secdef/search',
    params={'symbol': 'BTC', 'name': True}
).json()[0]

'''
market_order = session.post(
    url=f'{BASE_URL}/iserver/account/{account}/orders',
    headers={'Content-Type': 'application/json'},
    json={
        'orders': [
            {
                'conid': int(bitcoin_id['conid']),
                'orderType': 'MKT',
                'side': 'BUY',
                'tif': 'IOC',
                'cashQty': float(100),
                'secType': 'CRYPTO',
                'listingExchange': 'PAXOS'
            }
        ]
    }
)

pprint(market_order.json())
'''

order_status = session.get(f'{BASE_URL}/iserver/account/order/status/474467663')
pprint(order_status.json())

positions = (
    session.get(
        url=f'{BASE_URL}/portfolio2/{account}/positions',
    )
)


print(f'\nFETCHING ACCOUNT: {account}\n')


'''
print(f'---- FETCHING PORTFOLIO ----\n')
pprint(portfolio)
'''

print(f'---- FETCHING POSITIONS ----\n')
print(f'Positions endpoint response code: {positions.status_code}')
pprint(positions.json())
