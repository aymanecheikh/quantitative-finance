import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import itertools
from pathlib import Path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


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

def price_returns_hypothesis_test():
    # Standard repeatable steps
    labels = [
        path.parts[-1].partition('.')[0]
        for path in Path('historical_data').iterdir()
        ]
    stock_pairs = list(itertools.combinations(labels, 2))
    
    p_values = []
    for label in stock_pairs:
        df = pd.DataFrame(columns=['symbol', 'price_returns', 'volume_returns'])
        for pair_element in label:
            df_sub = pd.read_csv(
                f'historical_data/{pair_element}.csv'
            )[['date', 'close', 'volume']]
            df_sub['symbol'] = pair_element
            df_sub['price_returns'] = df_sub.close.pct_change().dropna()
            df_sub['volume_returns'] = df_sub.volume.pct_change().dropna()
            df = (
                pd.concat(
                    [df, df_sub[['symbol', 'price_returns', 'volume_returns']].dropna()]
                    )
                .reset_index(drop=True)
            )
        # Code unique to this function
        a = np.array(df[df.symbol == list(set(df.symbol))[0]].price_returns)
        b = np.array(df[df.symbol == list(set(df.symbol))[1]].price_returns)
        shorter_array = np.min([len(a), len(b)])
        a = a[:shorter_array]
        b = b[:shorter_array]
        alpha = 0.05
        t_stat, p_val = stats.ttest_rel(a, b)
        m = np.mean(a - b)
        s = np.std(a - b, ddof=1)
        n = len(b)
        t_manual = m / (s / np.sqrt(n))
    
        decision = "Reject" if p_val <= alpha else "Fail reject"
        concl = "Significant difference." if decision == "Reject" else "No significant difference."
        if concl == "Significant difference.":
            print(f"For pair: {label}")
            print("T:", t_stat)
            print("P:", p_val)
            print("T manual:", t_manual)
            print(f"Decision: {decision} H0 at α={alpha}")
            print("Conclusion:", concl)
            print("\n-------------------------------------\n")
        p_values.append(p_val)
    return p_values


if __name__ == '__main__':
    '''
    historical_data = Path('historical_data')
    for stock in historical_data.iterdir():
        price_volume_hists(stock)
    hollistic_scatterplots()
    '''
    stats = price_returns_hypothesis_test()
    print('\n\n')
    print(np.min(stats))
