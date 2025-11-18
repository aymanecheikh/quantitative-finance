from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue
from api_client import run_server


if __name__ == '__main__':
    app = run_server()
    
    subscription = ScannerSubscription()
    subscription.instrument = 'STK'
    subscription.locationCode = 'STK.US'
    subscription.scanCode = 'HIGH_OPEN_GAP'

    scan_data = app.reqScannerSubscription(1, subscription, [], [])
    print(scan_data)

    app.disconnect()
