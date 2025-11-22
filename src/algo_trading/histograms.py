import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


def price_volume_hists(stock: Path):
    df = pd.read_csv(stock)[['date', 'close', 'volume']]
    price_returns = df.close.pct_change().dropna()
    volume_returns = df.volume.pct_change().dropna()
    volume_returns[volume_returns == np.inf] = 0
    plt.hist(price_returns, bins=100, alpha=0.7, edgecolor='grey')
    plt.show()
    plt.hist(volume_returns, bins=100, alpha=0.7, edgecolor='grey')
    plt.show()

def hollistic_scatterplots():
    df = pd.DataFrame(columns=['symbol', 'price_returns', 'volume_returns'])
    labels = [
        path.parts[-1].partition('.')[0]
        for path in Path('historical_data').iterdir()
    ]
    for label in labels:
        df_sub = pd.read_csv(
            f'historical_data/{label}.csv'
        )[['date', 'close', 'volume']]
        df_sub['symbol'] = label
        df_sub['price_returns'] = df_sub.close.pct_change().dropna()
        df_sub['volume_returns'] = df_sub.volume.pct_change().dropna()
        df = (
            pd.concat(
                [df, df_sub[['symbol', 'price_returns', 'volume_returns']].dropna()]
            )
            .reset_index(drop=True)
        )
    width = 0.4
    fig, ax = plt.subplots()
    for index, i in enumerate(labels):
        sample = np.array(df[df['symbol'] == i].price_returns)
        x = (
            np.ones(sample.shape[0]) * index
            + (np.random.rand(sample.shape[0]) * width-width/2)
        )
        ax.scatter(x, sample, s=0.1)
        mean = sample.mean()
        ax.plot([index-width/2, index+width/2], [mean, mean], color='k')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    plt.show()
    fig, ax = plt.subplots()
    for index, i in enumerate(labels):
        sample = np.array(df[df['symbol'] == i].volume_returns)
        x = (
            np.ones(sample.shape[0]) * index
            + (np.random.rand(sample.shape[0]) * width-width/2)
        )
        ax.scatter(x, sample, s=1)
        mean = sample.mean()
        ax.plot([index-width/2, index+width/2], [mean, mean], color='k')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    plt.show()


if __name__ == '__main__':
    historical_data = Path('historical_data')
    for stock in historical_data.iterdir():
        price_volume_hists(stock)
    hollistic_scatterplots()
