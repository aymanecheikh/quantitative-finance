import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


def get_data(stock: Path) -> pd.DataFrame:
    df = pd.read_csv(stock)[['date', 'close', 'volume']]
    price_returns = df.close.pct_change().dropna()
    volume_returns = df.volume.pct_change().dropna()
    volume_returns[volume_returns == np.inf] = 0
    plt.hist(price_returns, bins=100, alpha=0.7, edgecolor='grey')
    plt.show()
    plt.hist(volume_returns, bins=100, alpha=0.7, edgecolor='grey')
    plt.show()


if __name__ == '__main__':
    historical_data = Path('historical_data')
    for stock in historical_data.iterdir():
        get_data(stock)
