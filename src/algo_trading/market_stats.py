import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import itertools
from math import sqrt
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
    sample_sizes_needed = []
    corrcoefs = []
    corrcoef_p_values = []
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
                    [
                        df,
                        df_sub[
                            ['symbol', 'price_returns', 'volume_returns']
                        ].dropna()
                    ]
                    )
                .reset_index(drop=True)
            )
        # Code unique to this function
        a = np.array(df[df.symbol == list(set(df.symbol))[0]].price_returns)
        b = np.array(df[df.symbol == list(set(df.symbol))[1]].price_returns)
        shorter_array = np.min([len(a), len(b)])
        a = a[:shorter_array]
        b = b[:shorter_array]
        # Effect Size | Cohen's d
        n1, n2 = len(a), len(b)
        s1, s2 = np.var(a), np.var(b)
        s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
        u1, u2 = np.mean(a), np.mean(b)
        d = (u1 - u2) / s
        # print(f'Effect size: {d}')
        
        # Power Analysis
        alpha = 0.05
        power = 0.8
        obj = TTestIndPower()
        n = obj.solve_power(
            effect_size=d,
            alpha=alpha,
            power=power,
            ratio=1,
            alternative='two-sided'
        )
        # print(f'Samples size/Number needed in each group: {n:.3f}')
        sample_sizes_needed.append(n)
        
        # p-values
        t_stat, p_val = stats.ttest_rel(a, b)
        p_values.append(p_val)
        m = np.mean(a - b)
        s = np.std(a - b, ddof=1)
        n = len(b)
        t_manual = m / (s / np.sqrt(n))

        # Correlation
        pearson_corr, pearson_p = stats.pearsonr(a, b)
        spearman_corr, spearman_p = stats.spearmanr(a, b)
        kendalltau_corr, kendalltau_p = stats.kendalltau(a, b)

        corrs = np.array([pearson_corr, spearman_corr, kendalltau_corr])
        corr_p_values = np.array([pearson_p, spearman_p, kendalltau_p])
        if corr_p_values < 0.05:
            print(
                f'Pearson\'s Correlation for {label}: {pearson_corr} '
                f'w/ p-value of: {pearson_p}'
            )
            print(
                f'Spearman Rank Correlation for {label}: {spearman_corr} '
                f'w/ p-value of: {spearman_p}'
            )
            print(
                f'Kendall Tau Correlation for {label}: {kendalltau_corr} '
                f'w/ p-value of: {kendalltau_p}'
            )
            print(f'Average Correlation for {label}: {corrs.mean()}')
            print(f'Average p-value for {label}: {corr_p_values.mean()}')
        corrcoefs.append(corrs.mean())
        corrcoef_p_values.append(corr_p_values.mean())
        print()

        '''
        decision = "Reject" if p_val <= alpha else "Fail reject"
        concl = (
            "Significant difference."
            if decision == "Reject"
            else "No significant difference."
        )
        print(f"For pair: {label}")
        print("T:", t_stat)
        print("P:", p_val)
        print("T manual:", t_manual)
        print(f"Decision: {decision} H0 at α={alpha}")
        print("Conclusion:", concl)
        print("\n-------------------------------------\n")
        '''
    adjusted_p_values = stats.false_discovery_control(p_values, method="bh")
    print(f'Max correlation: {np.min(corrcoefs)}')
    print(f'Min correlation: {np.max(corrcoefs)}')
    '''
    print(f"Minimum sample size needed: {np.min(sample_sizes_needed)}")
    print(f"Minimum p-value: {np.min(p_values)}")
    print(f"Minimum adjusted p-value: {np.min(adjusted_p_values)}")
    '''
    return p_values


if __name__ == '__main__':
    '''
    historical_data = Path('historical_data')
    for stock in historical_data.iterdir():
        price_volume_hists(stock)
    hollistic_scatterplots()
    '''
    stats = price_returns_hypothesis_test()
