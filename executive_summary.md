# Executive Summary

This project implements a standard **minimum-variance hedging framework** to study whether **Bitcoin futures can reduce the risk of holding spot Bitcoin exposure**. Using daily BTC spot and futures data from January 2021 through December 2025, the project compares three common hedging strategies: a **naive hedge**, a **static minimum-variance hedge**, and a **dynamic minimum-variance hedge**. The purpose is not to propose a new trading strategy, but to evaluate how a well-known hedging framework behaves in the context of Bitcoin markets.

The analysis uses daily closing prices for **BTC-USD** as the spot series and **BTC=F** as the futures series. Returns are computed as log returns, and the hedged portfolio return is modeled as

$$
r_{p,t} = r_{s,t} - h_t r_{f,t},
$$

where $r_{s,t}$ denotes the spot return, $r_{f,t}$ denotes the futures return, and $h_t$ denotes the hedge ratio. Three hedge constructions are examined. The **naive hedge** sets $h_t = 1$, the **static hedge** estimates one full-sample minimum-variance hedge ratio, and the **dynamic hedge** re-estimates the hedge ratio over a rolling 60-day window, using a lagged implementation to avoid look-ahead bias.

Performance is evaluated primarily through **hedging effectiveness**, measured by the percentage reduction in return variance relative to the unhedged BTC spot position. The results show that all three hedging strategies reduce variance substantially. In this sample, the **static minimum-variance hedge** performs best, reducing variance by about **76.8%**. The **dynamic hedge** is slightly less effective, reducing variance by about **75.9%**, while the **naive hedge** reduces variance by about **74.5%**. The estimated static hedge ratio is approximately **0.85**, which suggests that a one-for-one hedge slightly over-hedges Bitcoin spot exposure in this sample.

Cumulative return comparisons highlight the tradeoff between **risk reduction** and **upside participation**. The unhedged BTC position captures the strongest gains during the post-2024 bull market, but it also experiences the largest volatility and drawdowns. By contrast, the hedged portfolios are much smoother. The naive hedge remains close to flat over time because it offsets most of the directional Bitcoin exposure, while the static and dynamic hedges preserve some residual upside while still providing substantial risk reduction. Among the hedged strategies, the dynamic hedge produces the strongest cumulative return path, even though the static hedge achieves the best variance reduction overall.

Overall, this project shows that **Bitcoin futures can serve as an effective instrument for hedging spot Bitcoin risk**. More broadly, the results illustrate the central tradeoff in hedging: investors seeking **volatility reduction and downside protection** may prefer to hedge, while investors seeking **full upside participation** may prefer to remain unhedged and instead focus on position sizing and leverage control.