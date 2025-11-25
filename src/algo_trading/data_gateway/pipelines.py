from data_gateway.market_scan import get_gapped_up_stocks
from data_gateway.historical_data import get_historical_data


def gapped_up_to_historicals():
    df = get_gapped_up_stocks()
    df.pipe(get_historical_data)


if __name__ == '__main__':
    gapped_up_to_historicals()

