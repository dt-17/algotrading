import streamlit as st
import pandas as pd

from strategies.bollinger import generate_signals
from backtests.runner import run_backtest, compute_rolling_sharpe
from utils.plot import plot_equity_curve, plot_equity_with_rolling_sharpe
from backtests.trades import generate_trade_log

# ---- UI HEADER ----
st.title("📊 Bollinger Band Strategy Dashboard")
st.markdown("Upload data and run a backtest using Bollinger Band signals.")

# ---- DATA LOADING ----
uploaded_file = st.file_uploader("Upload a CSV file with 'close' prices", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=True)
    df.columns = df.columns.str.lower().str.strip()

    # Handle Alpha Vantage format (e.g., '4. close')
    if '4. close' in df.columns:
        df.rename(columns={'4. close': 'close'}, inplace=True)

    # Ensure there's a datetime index
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    elif not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # ---- STRATEGY INPUTS ----
    st.subheader("Strategy Parameters")

    window = st.slider("Rolling Window", 5, 60, 20)
    num_std = st.slider("Standard Deviations", 1.0, 3.0, 2.0, 0.1)
    start_date = st.date_input("Start Date", df.index.min().date())
    end_date = st.date_input("End Date", df.index.max().date())

    df = df.loc[str(start_date):str(end_date)]

    # ---- STRATEGY ----
    signals_df = generate_signals(df, window=window, num_std=num_std)
    results = run_backtest(signals_df)
    signals_df['rolling_sharpe'] = compute_rolling_sharpe(results['df'])

    st.subheader("Performance Summary")
    st.metric("Sharpe Ratio", f"{results['sharpe']:.2f}")
    st.metric("Max Drawdown", f"{results['max_drawdown']:.2%}")
    st.metric("Final Return", f"{results['final_return']:.2f}x")

    # ---- PLOTS ----
    st.subheader("Equity Curve")
    plot_equity_curve(results['df'])

    # ---- TRADE LOG ----
    st.subheader("Trade Log")
    trade_log = generate_trade_log(
        df=signals_df,
        window=window,
        num_std=num_std,
        performance=results,
        save_csv=False
    )
    st.dataframe(trade_log)

    # ---- DOWNLOAD ----
    csv = trade_log.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Trade Log",
        data=csv,
        file_name=f"trade_log_{window}_{num_std}.csv",
        mime="text/csv"
    )
