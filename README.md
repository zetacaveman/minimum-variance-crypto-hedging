# Minimum-Variance Crypto Hedging (Concise)

This project implements a clean, minimal workflow for hedging BTC spot exposure with BTC futures using the minimum-variance hedge ratio.

Current scope:
- Static hedge (ready to run)
- Dynamic hedge helper (rolling window, ready for extension)

## Project Layout

```text
minimum-variance-crypto-hedging/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_showcase.ipynb
├── src/
│   ├── hedge.py              # core functions (data load, returns, static/dynamic hedge)
│   └── run_static.py         # executable static hedge script
├── requirements.txt
└── README.md
```

## Math Used

With spot return \(r_t^S\) and futures return \(r_t^F\):

- Static minimum-variance hedge ratio:
  \[
  h^\* = \frac{\operatorname{Cov}(r^S, r^F)}{\operatorname{Var}(r^F)}
  \]

- Hedged return:
  \[
  r_t^P = r_t^S - h^\* r_t^F
  \]

- Hedge effectiveness:
  \[
  HE = 1 - \frac{\operatorname{Var}(r^P)}{\operatorname{Var}(r^S)}
  \]

This is exactly what the static pipeline computes.

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run static hedge:

```bash
python src/run_static.py
```

3. Output dataset is saved to:

`data/processed/btc_static_hedge_daily.csv`

## Core API (`src/hedge.py`)

- `download_close(...)`
- `load_spot_and_futures(...)`
- `compute_returns(...)`
- `estimate_static_hedge_ratio(...)`
- `add_static_hedged_returns(...)`
- `hedge_effectiveness(...)`
- `add_dynamic_hedge(...)` (rolling \(h_t\), lagged to avoid look-ahead)
- `run_static_hedge(...)`

## Dynamic Hedge (Room Left Open)

`add_dynamic_hedge(df, window=60, lag=1)` is already included.  
It computes a rolling hedge ratio and dynamic hedged returns:

\[
h_t = \frac{\widehat{\operatorname{Cov}}_{t-W:t-1}(r^S, r^F)}
{\widehat{\operatorname{Var}}_{t-W:t-1}(r^F)}
\]

with lag applied so only past information is used.

## Data Note

The example uses Yahoo tickers:
- Spot: `BTC-USD`
- Futures: `BTC=F`

`BTC=F` is a front-month futures series, so roll behavior can influence return statistics and hedge estimates.

## License

MIT. See [LICENSE](LICENSE).
