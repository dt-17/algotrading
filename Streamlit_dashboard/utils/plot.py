# plotting utilities
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from backtests.runner import compute_rolling_sharpe

def plot_equity_curve(df):
    """
    Plot the equity curve for strategy and market.

    Parameters:
    ----------
    df : pandas.DataFrame
        Must contain 'cumulative_market' and 'cumulative_strategy' columns.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['cumulative_market'], label='Market', color='grey', linestyle='--')
    plt.plot(df['cumulative_strategy'], label='Strategy', color='blue')
    plt.title('EURUSD Bollinger Band Strategy vs Market')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)


def plot_equity_with_rolling_sharpe(df, sharpe_window=252):
    """
    Plot cumulative strategy return and rolling Sharpe ratio on dual y-axes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'strategy_returns' and 'cumulative_strategy'.
    sharpe_window : int
        Window size in days for rolling Sharpe calculation.
    """
    df = df.copy()
    df['rolling_sharpe'] = compute_rolling_sharpe(df, window=sharpe_window)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot equity curve
    ax1.plot(df.index, df['cumulative_strategy'], label='Equity Curve', color='blue')
    ax1.set_ylabel("Cumulative Return", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot rolling Sharpe on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['rolling_sharpe'], label=f'Rolling Sharpe ({sharpe_window}d)', color='green', alpha=0.7)
    ax2.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.9)
    ax2.set_ylabel("Rolling Sharpe Ratio", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Add titles and layout
    plt.title(f"Equity Curve and Rolling Sharpe Ratio ({sharpe_window}-day)")
    fig.tight_layout()
    plt.grid(True)
    plt.show()