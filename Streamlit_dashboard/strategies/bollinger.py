# bollinger strategy logic
import pandas as pd

def generate_signals(df, window=20, num_std=2):
    """
    Generate trading signals based on a Bollinger Band mean reversion strategy.

    Parameters:
    ----------
    df : pandas.DataFrame
        DataFrame containing at least a 'close' column.
    window : int
        Rolling window size for SMA and standard deviation.
    num_std : float
        Number of standard deviations for upper and lower Bollinger Bands.

    Returns:
    -------
    df : pandas.DataFrame
        DataFrame with added columns: 'sma', 'upper_band', 'lower_band',
        'signal', 'exit', and 'position'.
    """
    df = df.copy()

    # Calculate Bollinger Bands
    df['sma'] = df['close'].rolling(window=window).mean()
    df['std'] = df['close'].rolling(window=window).std()
    df['upper_band'] = df['sma'] + num_std * df['std']
    df['lower_band'] = df['sma'] - num_std * df['std']

    # Initialize columns
    df['signal'] = 0
    df['exit'] = 0
    df['position'] = 0

    # Define entry conditions
    buy_entry = df['close'] < df['lower_band']
    sell_entry = df['close'] > df['upper_band']

    # Simulate trade state
    in_trade = 0
    position = []

    for i in range(len(df)):
        price = df['close'].iloc[i]
        sma = df['sma'].iloc[i]
        prev_price = df['close'].shift(1).iloc[i]
        prev_sma = df['sma'].shift(1).iloc[i]

        # ENTRY
        if in_trade == 0:
            if buy_entry.iloc[i]:
                df.at[df.index[i], 'signal'] = 1
                in_trade = 1
            elif sell_entry.iloc[i]:
                df.at[df.index[i], 'signal'] = -1
                in_trade = -1

        # EXIT
        elif in_trade == 1 and price > sma and prev_price <= prev_sma:
            df.at[df.index[i], 'exit'] = 1
            in_trade = 0
        elif in_trade == -1 and price < sma and prev_price >= prev_sma:
            df.at[df.index[i], 'exit'] = 1
            in_trade = 0

        position.append(in_trade)

    df['position'] = position

    return df
