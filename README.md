# 🧠 Algotrading Project

This is a general-purpose algorithmic trading repository where I experiment with trading strategies, build custom backtesting engines, and develop tools for performance analysis and visualization.

---

## 🚀 Project Goals

- Prototype and test rule-based trading strategies (e.g. Bollinger Bands, momentum, mean reversion, etc.)
- Build a flexible and modular **backtesting engine** from scratch
- Develop robust **performance metrics and visual analytics**
- Explore cross-asset strategies across **equities, ETFs, FX, and rates**
- Create interactive dashboards using **Streamlit** and **Plotly**

---

## 🛠️ Tech Stack

- **Python 3.10**
- `pandas`, `numpy`, `scipy` for data analysis and vectorized computations  
- `yfinance`, `alpha_vantage`, `fredapi` for market data ingestion  
- `matplotlib`, `seaborn`, `plotly` for plotting  
- `streamlit`, `dash` for dashboard interfaces  
- `quantstats`, `empyrical`, `statsmodels` for performance metrics  
- `scikit-learn`, `optuna` for ML and parameter tuning (optional)

---

## 📁 Project Structure

```
bollinger_backtest/
├── prototyping.ipynb        # Notebook for prototyping
├── data/                          # Historical price data
├── strategies/                    # Strategy logic modules
├── backtests/                     # Backtest engine + performance metrics
├── plots/                         # Output figures (e.g., equity curves)
└── dashboard/                     # Streamlit app for visualization
```

---

## 📦 Getting Started

1. Clone the repo:
```bash
git clone https://github.com/yourusername/algotrading.git
cd algotrading
```

2. Set up the environment:
```bash
conda create --name algotrading python=3.10
conda activate algotrading
pip install -r requirements.txt
```

3. Run the notebook or dashboard:
```bash
jupyter lab
# or
cd dashboard
streamlit run app.py
```

---

## 📈 Example Strategies (WIP)

- [x] Bollinger Bands (mean reversion / breakout)
- [ ] Momentum based on moving average crossovers
- [ ] Pairs trading
- [ ] Carry strategies in FX/Rates
- [ ] Volatility targeting with regime switching

---

## 🧪 Upcoming Features

- Portfolio-level backtesting (multi-asset strategies)
- Trade simulation with slippage and execution lag
- Parameter optimization and walk-forward testing
- Live data hooks (for paper trading or sandboxed backtesting)

---

## 🧾 License

This project is licensed for personal and educational use. All code is open source and extensible.

---

### 📬 Contact

Built and maintained by Daniel Tompkins — feel free to reach out via GitHub or LinkedIn.
