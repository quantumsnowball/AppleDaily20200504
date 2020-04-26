import pandas as pd
import numpy as np

def get_close(ticker):
    df = pd.read_csv(f'./prices/{ticker}.csv', index_col=0, parse_dates=True)
    close = df['Adj Close']
    return close

def main():
    df = pd.DataFrame()

    df['index'] = get_close('^GSPC')
    df['pct_chgs'] = df['index'].pct_change()
    df['log_returns'] = np.log(df['index']).diff()
    df['ma50'] = df['index'].rolling(50).mean()
    df['ma200'] = df['index'].rolling(200).mean()
    df['bull'] = df['ma50']>=df['ma200']
    df['bear'] = df['ma50']< df['ma200']

    bull_stats = df[df['bull']]['log_returns'].describe().rename('bull')
    bear_stats = df[df['bear']]['log_returns'].describe().rename('bear')

    stats = pd.concat([
        bull_stats,
        bear_stats
    ], axis=1).T

    stats_ann = pd.concat([
        stats['count'],
        stats['mean']*252,
        stats['std']*252**.5,
    ], axis=1)
    stats_ann['sharpe'] = stats_ann['mean']/stats_ann['std']

    print(stats_ann)


if __name__ == '__main__':
    main()