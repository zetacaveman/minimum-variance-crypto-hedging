# Minimum-Variance Crypto Hedging

This demo follows the classical **minimum-variance hedging** framework developed in the futures literature by Johnson (1960) and Stein (1961), and given its standard empirical form by Ederington (1979), who uses the hedge ratio

$$
h^* = \frac{\operatorname{Cov}(r_s,r_f)}{\operatorname{Var}(r_f)}.
$$

The comparison between **static** and **dynamic** hedge ratios follows the later literature on time-varying hedging, especially Kroner and Sultan (1993) and related work on constant versus time-varying hedge ratios.

For the cryptocurrency setting, relevant applications include Sebastião and Godinho (2020) on Bitcoin futures as hedging instruments, and Deng et al. (2020) on minimum-variance hedging of Bitcoin futures.

## Structure
Concise BTC spot/futures hedging project with:
- one compute module
- one showcase notebook
- one executive summary
- data (optional, currently empty)

```text
minimum-variance-crypto-hedging/
├── executive_summary.md
├── presentation/
│   └── BTC_Hedging_Presentation.pptx
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_showcase.ipynb
├── src/
│   ├── __init__.py
│   └── hedge.py      
├── requirements.txt
├── LICENSE
└── README.md
```

## Executive Summary

See [executive_summary.md](executive_summary.md) for the presentation-oriented narrative, data period, methodology, and headline results.

## Math

- Static hedge ratio:
  $$
  h^*=\frac{\operatorname{Cov}(r^S,r^F)}{\operatorname{Var}(r^F)}
  $$
- Hedged return:
  $$
  r_t^P=r_t^S-h_t r_t^F
  $$
- Hedge effectiveness:
  $$
  HE=1-\frac{\operatorname{Var}(r^P)}{\operatorname{Var}(r^S)}
  $$

## API (`src/hedge.py`)

- `compute_returns(...)` (simple or log returns)
- `estimate_static_hedge_ratio(...)`
- `estimate_dynamic_hedge_ratio(...)` (rolling, lagged)
- `apply_hedge(...)`
- `compute_naive_hedged_returns(...)`
- `compute_static_hedged_returns(...)`
- `compute_dynamic_hedged_returns(...)`
- `hedge_effectiveness(...)`
- `build_hedge_comparison(...)` (naive/static/dynamic return series)

This module is computation-only and does not fetch data. You can pass returns from any source (Yahoo, exchange API, CSV, database, etc.).

## Minimal Usage

```bash
pip install -r requirements.txt
```

```python
import pandas as pd
from src.hedge import (
    compute_returns,
    compute_naive_hedged_returns,
    compute_static_hedged_returns,
    compute_dynamic_hedged_returns,
)

# prices must include spot and futures columns from your own source
prices = pd.read_csv("your_prices.csv", parse_dates=["date"]).set_index("date")
ret = compute_returns(prices, spot_col="spot", fut_col="fut", method="simple")

r_p_naive = compute_naive_hedged_returns(ret["r_s"], ret["r_f"])
r_p_static, h_static = compute_static_hedged_returns(ret["r_s"], ret["r_f"])
r_p_dynamic, h_t = compute_dynamic_hedged_returns(ret["r_s"], ret["r_f"], window=60, lag=1)
```

## Note on Data

`notebooks/01_showcase.ipynb` can still use `yfinance` for convenience, but the library code in `src/` is fully data-source-agnostic.

## References

### Core references

- Johnson, L. L. (1960). The theory of hedging and speculation in commodity futures.
- Stein, J. L. (1961). The simultaneous determination of spot and futures prices.
- Ederington, L. H. (1979). The hedging performance of the new futures markets.
- Kavussanos, M. G., and Nomikos, N. K. (2000). Constant vs. time-varying hedge ratios and hedging efficiency in the BIFFEX market.
- Alexander, C., and Barbosa, A. (2013). The (de)merits of minimum-variance hedging.

### Crypto / Bitcoin-related references

- Koutmos, D. (2021). Hedging uncertainty with cryptocurrencies: Is bitcoin your best bet?
- Wang, P. et al. (2021). Time and frequency dynamics of connectedness and hedging among Bitcoin and traditional hedges.
- Nekhili, R. (2022). Hedging Bitcoin with conventional assets.
- Xu, L. (2023). Hedging effectiveness of bitcoin and gold.
- Joo, Y. C. (2024). Hedging Bitcoin with commodity futures using dynamic hedge ratios.

## License

MIT. See `LICENSE`.
