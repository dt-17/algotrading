# backtest runner
import pandas as pd
import numpy as np

def run_backtest(df, fee=0.0):
    """
    Run a vectorized backtest on a signal-enhanced DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        Must contain a 'close' column and a 'position' column (1, -1, 0).
    fee : float
        Transaction cost per position change (in decimal form, e.g., 0.0002 for 2bps).

    Returns:
    -------
    dict
        Contains updated DataFrame and performance metrics.
    """
    df = df.copy()
    
    # Step 1: Basic returns
    df['returns'] = df['close'].pct_change()

    # Step 2: Strategy returns
    df['strategy_returns'] = df['position'].shift(1) * df['returns']
    df['strategy_returns'] -= fee * df['position'].diff().abs().fillna(0)

    # Step 3: Cumulative returns
    df['cumulative_market'] = (1 + df['returns']).cumprod()
    df['cumulative_strategy'] = (1 + df['strategy_returns']).cumprod()

    # Step 4: Metrics
    strategy_returns = df['strategy_returns'].dropna()
    sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
    max_drawdown = (df['cumulative_strategy'] / df['cumulative_strategy'].cummax() - 1).min()
    final_return = df['cumulative_strategy'].iloc[-1]

    return {
        'df': df,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'final_return': final_return
    }

def compute_rolling_sharpe(df, window=252):
    """
    Compute rolling Sharpe ratio from strategy returns.

    Parameters
    ----------
    df : pd.DataFrame
        Must include 'strategy_returns' column.
    window : int
        Rolling window size (in trading days).

    Returns
    -------
    pd.Series
        Rolling Sharpe ratio (annualized).
    """
    rolling_mean = df['strategy_returns'].rolling(window).mean()
    rolling_std = df['strategy_returns'].rolling(window).std()
    rolling_sharpe = rolling_mean / rolling_std * np.sqrt(252)
    return rolling_sharpe