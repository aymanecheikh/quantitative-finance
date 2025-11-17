from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue
from api_client import run_server


if __name__ == '__main__':
    app = run_server()
    subscription = ScannerSubscription()
    subscription.numberOfRows = 15
    subscription.instrument = 'STK'
    subscription.locationCode = 'STK.US'
    subscription.scanCode = 'MOST_ACTIVE'
    tagvalues = []
    tagvalues.append(
        TagValue('avgVolumeAbove', '10000')
    )

    app.reqScannerSubscription(0, subscription, [], tagvalues)
