# trades
import pandas as pd

def generate_trade_log(df, window, num_std, performance=None, save_csv=False, filename="trade_log.csv"):
    """
    Generate a trade log from a DataFrame and append strategy metadata.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'signal', 'exit', 'position', and 'close'.
    window : int
        Window used for Bollinger Bands.
    num_std : float
        Std dev multiplier used for bands.
    performance : dict, optional
        Dictionary containing Sharpe, drawdown, final return, etc.
    save_csv : bool
        If True, saves the log to CSV.
    filename : str
        CSV filename to save (if save_csv=True).

    Returns
    -------
    trade_log : pd.DataFrame
        Trade log DataFrame with metadata as attributes.
    """
    in_trade = False
    entry_price = None
    entry_index = None
    direction = None
    trades = []

    for i in range(len(df)):
        row = df.iloc[i]

        if not in_trade and row['signal'] != 0:
            in_trade = True
            entry_price = row['close']
            entry_index = df.index[i]
            direction = row['signal']

        elif in_trade and row['exit'] == 1:
            exit_price = row['close']
            exit_index = df.index[i]
            trade_return = (exit_price - entry_price) / entry_price if direction == 1 else (entry_price - exit_price) / entry_price
            duration = (exit_index - entry_index).days if isinstance(exit_index, pd.Timestamp) else exit_index - entry_index

            trades.append({
                'Entry Date': entry_index,
                'Exit Date': exit_index,
                'Direction': 'Long' if direction == 1 else 'Short',
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'Return': trade_return,
                'Duration': duration
            })

            in_trade = False

    trade_log = pd.DataFrame(trades)

    # Add metadata as new columns (broadcasted)
    meta = {
        'window': window,
        'num_std': num_std,
        'Sharpe': performance.get('sharpe') if performance else None,
        'Max Drawdown': performance.get('max_drawdown') if performance else None,
        'Final Return': performance.get('final_return') if performance else None,
        'Win Rate': None  # To be calculated below
    }

    if not trade_log.empty:
        win_rate = (trade_log['Return'] > 0).mean()
        meta['Win Rate'] = round(win_rate, 4)
        for key, val in meta.items():
            trade_log[key] = val

    if save_csv:
        trade_log.to_csv(filename, index=False)
        print(f"Trade log saved to {filename}")

    return trade_log