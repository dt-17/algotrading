import streamlit as st
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange

from strategies.bollinger import generate_signals
from backtests.runner import run_backtest, compute_rolling_sharpe
from utils.plot import plot_equity_curve, plot_equity_with_rolling_sharpe
from backtests.trades import generate_trade_log

# ---- UI HEADER ----
st.title("📊 Bollinger Band Strategy Dashboard")
st.markdown("Select a currency pair and run a backtest using Bollinger Band signals.")

# ---- FX PAIR SELECTION ----
currency_pairs = {
    "EUR/USD": ("EUR", "USD"),
    "GBP/USD": ("GBP", "USD"),
    "USD/JPY": ("USD", "JPY"),
    "AUD/USD": ("AUD", "USD"),
    "USD/CAD": ("USD", "CAD")
}

selected_pair = st.selectbox("Currency Pair", list(currency_pairs.keys()))
from_symbol, to_symbol = currency_pairs[selected_pair]

api_key = "DK3F3HB19R3IX4C3"


@st.cache_data
def fetch_fx_data(api_key: str, from_symbol: str, to_symbol: str) -> pd.DataFrame:
    """
    Fetch daily FX data from Alpha Vantage, rename the '4. close' column to 'close',
    parse the index as datetime, and sort by date ascending.
    Because of @st.cache_data, this will only run once per unique (api_key, from_symbol, to_symbol).
    """
    fx = ForeignExchange(key=api_key, output_format="pandas")
    data, _ = fx.get_currency_exchange_daily(
        from_symbol=from_symbol,
        to_symbol=to_symbol,
        outputsize="full"
    )
    data = data.rename(columns={"4. close": "close"})
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    return data


# ------------------------------
# Maintain session_state for the DataFrame and last selected pair
# ------------------------------
if "last_pair" not in st.session_state:
    st.session_state.last_pair = None

# If the user changed currency_pair, clear the cached DF in session_state
if st.session_state.last_pair != selected_pair:
    st.session_state.df = None
    st.session_state.last_pair = selected_pair

# If there's no DataFrame in session_state yet, show a button to fetch
if st.session_state.df is None:
    if st.button("Fetch Data"):
        try:
            # This call is cached; only makes an HTTP call on first fetch for this pair
            df = fetch_fx_data(api_key, from_symbol, to_symbol)  # :contentReference[oaicite:0]{index=0}
            st.session_state.df = df
            st.success(f"Loaded {selected_pair} exchange rate data.")
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            st.stop()

# If df is in session_state, proceed to show strategy controls & results
if st.session_state.df is not None:
    df = st.session_state.df.copy()

    # ---- STRATEGY INPUTS ----
    st.subheader("Strategy Parameters")
    window = st.slider("Rolling Window", 5, 60, 20)
    num_std = st.slider("Standard Deviations", 1.0, 3.0, 2.0, 0.1)

    # ---- DATE RANGE ----
    st.subheader("Select Date Range")
    earliest = df.index.min().date()
    latest = df.index.max().date()
    start_date = st.date_input("Start Date", earliest, min_value=earliest, max_value=latest)
    end_date   = st.date_input("End Date", latest,   min_value=earliest, max_value=latest)

    # Filter the DataFrame to the selected window
    df = df.loc[str(start_date) : str(end_date)]

    # ---- STRATEGY CALCULATIONS ----
    signals_df = generate_signals(df, window=window, num_std=num_std)
    results = run_backtest(signals_df)
    signals_df["rolling_sharpe"] = compute_rolling_sharpe(results["df"])

    # ---- PERFORMANCE SUMMARY ----
    st.subheader("Performance Summary")
    st.metric("Sharpe Ratio", f"{results['sharpe']:.2f}")
    st.metric("Max Drawdown", f"{results['max_drawdown']:.2%}")
    st.metric("Final Return", f"{results['final_return']:.2f}×")

    # ---- PLOTS ----
    st.subheader("Equity Curve")
    plot_equity_curve(results["df"])

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

    # ---- DOWNLOAD TRADE LOG BUTTON ----
    csv = trade_log.to_csv(index=False).encode("utf-8")
    filename = f"trade_log_{selected_pair.replace('/', '')}_{window}_{num_std}.csv"
    st.download_button(
        "📥 Download Trade Log",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )
