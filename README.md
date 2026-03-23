# Minimum-Variance Crypto Hedging

This demo follows the classical **minimum-variance hedging** framework developed in the futures literature by Johnson (1960) and Stein (1961), and given its standard empirical form by Ederington (1979), who uses the hedge ratio

$$
h^* = \frac{\mathrm{Cov}(r_s,r_f)}{\mathrm{Var}(r_f)}.
$$

The comparison between **static** and **dynamic** hedge ratios follows the later literature on time-varying hedging, especially Kroner and Sultan (1993) and related work on constant versus time-varying hedge ratios.

For the cryptocurrency setting, relevant applications include Sebastião and Godinho (2020) on Bitcoin futures as hedging instruments, and Deng et al. (2020) on minimum-variance hedging of Bitcoin futures.

## Key Minimum-Variance References

These are the first references to look at for the hedge construction used in this project.

### Core minimum-variance hedging references

- Johnson, L. L. (1960). The theory of hedging and speculation in commodity futures.
- Stein, J. L. (1961). The simultaneous determination of spot and futures prices.
- Ederington, L. H. (1979). The hedging performance of the new futures markets.
- Kroner, K. F., and Sultan, J. (1993). Time-varying distributions and dynamic hedging with foreign currency futures.
- Kavussanos, M. G., and Nomikos, N. K. (2000). Constant vs. time-varying hedge ratios and hedging efficiency in the BIFFEX market.
- Alexander, C., and Barbosa, A. (2013). The (de)merits of minimum-variance hedging.

### Crypto / Bitcoin minimum-variance applications

- Sebastião, H., and Godinho, P. (2020). Bitcoin futures: An effective hedging instrument.
- Deng, Y. et al. (2020). Minimum-variance hedging of Bitcoin futures.
- Joo, Y. C. (2024). Hedging Bitcoin with commodity futures using dynamic hedge ratios.

## Structure
Concise BTC spot/futures hedging project with:
- one compute module
- one showcase notebook
- one presentation deck

```text
minimum-variance-crypto-hedging/
├── presentation/
│   └── BTC_Hedging_Presentation.pptx
├── notebooks/
│   └── 01_showcase.ipynb
├── src/
│   ├── __init__.py
│   └── hedge.py
├── tests/
│   └── test_hedge.py
├── requirements.txt
├── LICENSE
└── README.md
```

If you want to persist raw or processed market data, create a local `data/` directory yourself. The reusable code in `src/` does not rely on any bundled dataset.

## Math

- Static hedge ratio:
  $$
  h^*=\frac{\mathrm{Cov}(r^S,r^F)}{\mathrm{Var}(r^F)}
  $$
- Hedged return:
  $$
  r_t^P=r_t^S-h_t r_t^F
  $$
- Hedge effectiveness:
  $$
  HE=1-\frac{\mathrm{Var}(r^P)}{\mathrm{Var}(r^S)}
  $$

## API (`src/hedge.py`)

- `compute_returns(...)` (simple or log returns, with input validation)
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
ret = compute_returns(prices, spot_col="spot", fut_col="fut", method="log")

r_p_naive = compute_naive_hedged_returns(ret["r_s"], ret["r_f"])
r_p_static, h_static = compute_static_hedged_returns(ret["r_s"], ret["r_f"])
r_p_dynamic, h_t = compute_dynamic_hedged_returns(ret["r_s"], ret["r_f"], window=60, lag=1)
```

## Note on Data

`notebooks/01_showcase.ipynb` can still use `yfinance` for convenience, but the library code in `src/` is fully data-source-agnostic.

## Data Limitation

The showcase notebook downloads futures prices with `yf.download("BTC=F", ...)`, which appears to correspond to Yahoo Finance's rolling nearby CME Bitcoin futures symbol rather than one fixed-expiry futures contract. This does not change the minimum-variance hedging methodology implemented in `src/hedge.py`, but it can affect the reported hedge ratios, hedge effectiveness estimates, and cumulative return paths because contract-roll behavior is embedded in the downloaded series.

As a result, the project should be interpreted as a valid minimum-variance hedging demonstration using a convenient Yahoo/CME futures proxy. If you want tighter empirical control, replace `BTC=F` with explicit contract data or a self-constructed continuous futures series with documented roll rules.

## Additional References

### Other crypto / Bitcoin-related references

- Koutmos, D. (2021). Hedging uncertainty with cryptocurrencies: Is bitcoin your best bet?
- Wang, P. et al. (2021). Time and frequency dynamics of connectedness and hedging among Bitcoin and traditional hedges.
- Nekhili, R. (2022). Hedging Bitcoin with conventional assets.
- Xu, L. (2023). Hedging effectiveness of bitcoin and gold.

## License

MIT. See `LICENSE`.
