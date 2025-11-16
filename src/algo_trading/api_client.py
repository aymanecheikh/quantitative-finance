from pprint import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import numpy as np


class MarketSession:
    def __init__(self):
        self.BASE_URL = 'https://localhost:5000/v1/api'
        self.ISERVER_BASE = f'{self.BASE_URL}/iserver'
        self.session = requests.Session()
        self.session_init # Defined below

    @property
    def session_init(self) -> dict:
        self.session.verify = False
        session_init = self.session.post(
            url=f'{self.ISERVER_BASE}/auth/ssodh/init',
            json={'publish': True, 'compete': True}
        )
        session_init_details = session_init.json()
        assert session_init.status_code == 200
        assert session_init_details['authenticated'] == True
        assert session_init_details['connected'] == True
        return session_init_details

    @property
    def account(self) -> str:
        account_info = self.session.get(
            url=f'{self.BASE_URL}/portfolio/accounts'
        )
        assert account_info.status_code == 200
        return account_info.json()[0]['accountId']

class AssetEcosystem:
    def __init__(self):
        self.s = MarketSession()
        self.scope: dict = self.s.session.get(
            url=f'{self.s.ISERVER_BASE}/secdef/search',
            params={'symbol': 'BTC', 'name': True}
        ).json()


if __name__ == '__main__':
    ae = AssetEcosystem()
    details = ae.scope
    company_names = np.array([detail['companyName'] for detail in details])
    print(np.nonzero(company_names == None))


'''
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


order_status = session.get(f'{BASE_URL}/iserver/account/order/status/474467663')
pprint(order_status.json())

positions = (
    session.get(
        url=f'{BASE_URL}/portfolio2/{account}/positions',
    )
)


print(f'\nFETCHING ACCOUNT: {account}\n')



print(f'---- FETCHING PORTFOLIO ----\n')
pprint(portfolio)


print(f'---- FETCHING POSITIONS ----\n')
print(f'Positions endpoint response code: {positions.status_code}')
pprint(positions.json())
'''
