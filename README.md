# Minimum-Variance Crypto Hedging

A Python project on hedging cryptocurrency spot exposure with futures using minimum-variance hedge ratios. The project studies static and time-varying hedging strategies, evaluates hedge effectiveness on historical data, and examines the role of volatility and basis risk in crypto markets.

## Overview

This repository implements a standard futures-hedging framework for cryptocurrency markets. The main idea is to hold a spot exposure and offset part of its risk with a futures position. The hedge ratio is chosen to reduce portfolio variance.

The project focuses on four benchmark portfolios:

- **Unhedged exposure**
- **Naive hedge** with hedge ratio \(h = 1\)
- **Static minimum-variance hedge**
- **Dynamic minimum-variance hedge**

The goal is to compare how well these approaches reduce risk in practice.

## Project Structure

```text
minimum-variance-crypto-hedging/
├── data/
│   ├── raw/                  # original downloaded data
│   └── processed/            # cleaned and merged datasets
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_static_hedge.ipynb
│   ├── 03_dynamic_hedge.ipynb
│   └── 04_evaluation.ipynb
├── src/
│   ├── data_utils.py         # loading, cleaning, aligning data
│   ├── hedge.py              # hedge ratio estimation and hedged returns
│   ├── metrics.py            # volatility, drawdown, hedge effectiveness
│   └── plots.py              # reusable plotting functions
├── results/
│   ├── figures/
│   └── tables/
├── README.md
├── requirements.txt
└── .gitignore
```

## Mathematical Framework

Let

- \(S_t\): spot price at time \(t\)
- \(F_t\): futures price at time \(t\)

We define simple returns by

\[
r_t^S = \frac{S_t - S_{t-1}}{S_{t-1}}, \qquad
r_t^F = \frac{F_t - F_{t-1}}{F_{t-1}}.
\]

If we hold one unit of spot exposure and hedge with \(h_t\) units of futures, then the hedged portfolio return is

\[
r_t^P = r_t^S - h_t r_t^F.
\]

The objective is to choose \(h_t\) so that the hedged portfolio has lower variance than the unhedged spot position.

### Minimum-Variance Hedge Ratio

The standard minimum-variance hedging problem is

\[
\min_{h_t} \operatorname{Var}(r_t^S - h_t r_t^F).
\]

Expanding the variance gives

\[
\operatorname{Var}(r_t^S - h_t r_t^F)
=
\operatorname{Var}(r_t^S)
- 2 h_t \operatorname{Cov}(r_t^S, r_t^F)
+ h_t^2 \operatorname{Var}(r_t^F).
\]

Differentiating with respect to \(h_t\) and setting the derivative equal to zero yields

\[
-2\operatorname{Cov}(r_t^S, r_t^F)
+ 2 h_t \operatorname{Var}(r_t^F) = 0,
\]

so the optimal hedge ratio is

\[
h_t^\star = \frac{\operatorname{Cov}(r_t^S, r_t^F)}{\operatorname{Var}(r_t^F)}.
\]

This is the **minimum-variance hedge ratio**.

### Static Hedge

A static hedge uses one constant hedge ratio estimated from a training sample:

\[
\hat h_{\text{static}} =
\frac{\widehat{\operatorname{Cov}}(r^S, r^F)}
{\widehat{\operatorname{Var}}(r^F)}.
\]

That value is then held fixed throughout the evaluation period.

### Dynamic Hedge

A dynamic hedge allows the hedge ratio to vary over time. A simple implementation uses a rolling window of length \(W\):

\[
\hat h_t =
\frac{\widehat{\operatorname{Cov}}_{t-W:t-1}(r^S, r^F)}
{\widehat{\operatorname{Var}}_{t-W:t-1}(r^F)}.
\]

This allows the hedge to adapt when volatility and correlation change.

### Basis Risk

A hedge with futures is not perfect because spot and futures prices do not move identically at every date. Define the basis by

\[
B_t = F_t - S_t,
\]

or the normalized basis by

\[
b_t = \frac{F_t - S_t}{S_t}.
\]

Changes in the basis create **basis risk**, which is one of the main sources of hedging error.

### Hedge Effectiveness

A standard measure of performance is

\[
\text{HE} = 1 - \frac{\operatorname{Var}(r^P)}{\operatorname{Var}(r^S)}.
\]

If \(\text{HE}\) is close to 1, the hedge reduces variance substantially. If it is close to 0, the hedge provides little risk reduction.

## Methods

The workflow of the project is:

1. Collect spot and futures price data
2. Clean and align the time series
3. Compute returns and basis
4. Estimate hedge ratios
5. Construct hedged portfolio returns
6. Compare unhedged, naive, static, and dynamic strategies
7. Evaluate performance using risk metrics

## Evaluation Metrics

Typical metrics include:

- annualized volatility
- hedge effectiveness
- cumulative return
- maximum drawdown
- downside tail quantiles
- basis behavior over time

## Code Modules

### `src/data_utils.py`

Functions for:

- loading spot and futures data
- merging on date
- computing returns
- handling missing values

### `src/hedge.py`

Functions for:

- static hedge-ratio estimation
- rolling hedge-ratio estimation
- constructing hedged returns

### `src/metrics.py`

Functions for:

- annualized volatility
- hedge effectiveness
- drawdown
- summary performance tables

### `src/plots.py`

Functions for:

- price charts
- return series visualization
- rolling hedge-ratio plots
- basis plots
- cumulative performance plots

## Example Workflow

```python
from src.data_utils import load_and_merge_data, compute_returns
from src.hedge import estimate_static_hedge_ratio, compute_hedged_returns
from src.metrics import hedge_effectiveness

df = load_and_merge_data("data/processed/spot.csv", "data/processed/futures.csv")
df = compute_returns(df)

h = estimate_static_hedge_ratio(df["spot_ret"], df["fut_ret"])
df["hedged_ret"] = compute_hedged_returns(df["spot_ret"], df["fut_ret"], h)

he = hedge_effectiveness(df["spot_ret"], df["hedged_ret"])
print("Static hedge ratio:", h)
print("Hedge effectiveness:", he)
```

## Potential Extensions

Possible extensions include:

- exponentially weighted covariance estimation
- regime-based analysis under high- and low-volatility periods
- comparison across different cryptocurrencies
- analysis of different futures maturities
- stress testing under large basis movements

## Requirements

Typical Python packages:

- `pandas`
- `numpy`
- `matplotlib`
- `scipy`
- `statsmodels`
- `jupyter`

Install with:

```bash
pip install -r requirements.txt
```

## Notes

This project is an empirical implementation of standard hedging ideas in a cryptocurrency setting. It is intended as a quantitative finance portfolio project and a practical study of derivative-based risk management.
