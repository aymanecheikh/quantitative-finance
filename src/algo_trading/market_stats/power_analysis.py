from numpy import ndarray, array, var, mean
import pandas as pd
from itertools import combinations
from pathlib import Path




def stock_pairs(path: Path) -> tuple[str, str]:
    return combinations(
        (p.parts[-1].partition('.')[0] for p in directory.iterdir()), 2
    )

def get_data(path: Path, stock: str) -> pd.DataFrame:
    return pd.read_csv(directory / f'{stock}.csv')

def get_returns(df: pd.DataFrame) -> ndarray:
    return array(df.close.pct_change().dropna())

def consolidate_lengths(a: ndarray, b: ndarray) -> tuple[ndarray, ndarray]:
    shorter_array = min([len(a), len(b)])
    return a[:shorter_array], b[:shorter_array]

def cohens_d(a: np.ndarray, b: np.ndarray):
    n1, n2, s1, s2, u1, u2 = len(a), len(b), var(a), var(b), mean(a), mean(b)
    s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    return (u1 - u2) / s

def power_analysis(d):
    obj = TTestIndPower()
    return obj.solve_power(
        effect_size=d,
        alpha=0.05,
        power=0.8,
        ratio=1,
        alternative='two-sided'
    )

if __name__ == '__main__':
    directory = Path(
        '/home/aymane/Projects/algo_trading/src/algo_trading/historical_data'
    )
    print(type(stock_pairs(directory)))
    for i in stock_pairs(directory):
        print(i)
