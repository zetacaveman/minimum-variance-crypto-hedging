from __future__ import annotations

from dataclasses import dataclass
import time

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class HedgeSummary:
    hedge_ratio: float
    spot_variance: float
    hedged_variance: float
    hedge_effectiveness: float


def _extract_close(downloaded: pd.DataFrame, ticker: str) -> pd.Series:
    if downloaded.empty:
        raise ValueError(f"No data returned for {ticker}")

    if isinstance(downloaded.columns, pd.MultiIndex):
        if "Close" not in downloaded.columns.get_level_values(0):
            raise ValueError(f"Close column not found for {ticker}")
        close = downloaded["Close"]
        if isinstance(close, pd.DataFrame):
            close = close[ticker] if ticker in close.columns else close.iloc[:, 0]
    else:
        if "Close" not in downloaded.columns:
            raise ValueError(f"Close column not found for {ticker}")
        close = downloaded["Close"]

    close = pd.to_numeric(close, errors="coerce").dropna()
    close.name = ticker
    return close


def download_close(
    ticker: str,
    start: str = "2021-01-01",
    end: str = "2026-01-01",
    interval: str = "1d",
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> pd.DataFrame:
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        downloaded = yf.download(
            ticker,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

        try:
            close = _extract_close(downloaded, ticker)
            return close.to_frame(name=ticker)
        except ValueError as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(retry_delay * attempt)

    raise ValueError(
        f"Could not download usable close prices for {ticker} after {max_retries} attempts"
    ) from last_error


def load_spot_and_futures(
    spot_ticker: str = "BTC-USD",
    futures_ticker: str = "BTC=F",
    start: str = "2021-01-01",
    end: str = "2026-01-01",
) -> pd.DataFrame:
    spot = download_close(spot_ticker, start=start, end=end).rename(
        columns={spot_ticker: "spot_close"}
    )
    fut = download_close(futures_ticker, start=start, end=end).rename(
        columns={futures_ticker: "fut_close"}
    )
    df = spot.join(fut, how="inner").dropna()
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    required = {"spot_close", "fut_close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["spot_ret"] = out["spot_close"].pct_change()
    out["fut_ret"] = out["fut_close"].pct_change()
    return out.dropna(subset=["spot_ret", "fut_ret"])


def estimate_static_hedge_ratio(spot_ret: pd.Series, fut_ret: pd.Series) -> float:
    var_f = fut_ret.var()
    if pd.isna(var_f) or var_f == 0:
        raise ValueError("Cannot estimate hedge ratio: futures return variance is zero")
    h_star = spot_ret.cov(fut_ret) / var_f
    return float(h_star)


def add_static_hedged_returns(df: pd.DataFrame, hedge_ratio: float) -> pd.DataFrame:
    required = {"spot_ret", "fut_ret"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["hedged_ret"] = out["spot_ret"] - hedge_ratio * out["fut_ret"]
    return out


def add_dynamic_hedge(
    df: pd.DataFrame,
    window: int = 60,
    lag: int = 1,
    ratio_col: str = "h_t",
    output_col: str = "hedged_ret_dyn",
) -> pd.DataFrame:
    required = {"spot_ret", "fut_ret"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if window < 2:
        raise ValueError("window must be >= 2")
    if lag < 0:
        raise ValueError("lag must be >= 0")

    out = df.copy()
    cov_sf = out["spot_ret"].rolling(window).cov(out["fut_ret"])
    var_f = out["fut_ret"].rolling(window).var()
    out[ratio_col] = (cov_sf / var_f).shift(lag)
    out[output_col] = out["spot_ret"] - out[ratio_col] * out["fut_ret"]
    return out


def hedge_effectiveness(spot_ret: pd.Series, hedged_ret: pd.Series) -> float:
    var_spot = spot_ret.var()
    if pd.isna(var_spot) or var_spot == 0:
        raise ValueError("Cannot compute hedge effectiveness: spot return variance is zero")
    he = 1 - (hedged_ret.var() / var_spot)
    return float(he)


def run_static_hedge(
    spot_ticker: str = "BTC-USD",
    futures_ticker: str = "BTC=F",
    start: str = "2021-01-01",
    end: str = "2026-01-01",
) -> tuple[pd.DataFrame, HedgeSummary]:
    df = load_spot_and_futures(
        spot_ticker=spot_ticker,
        futures_ticker=futures_ticker,
        start=start,
        end=end,
    )
    df = compute_returns(df)
    h_star = estimate_static_hedge_ratio(df["spot_ret"], df["fut_ret"])
    df = add_static_hedged_returns(df, h_star)

    spot_var = float(df["spot_ret"].var())
    hedged_var = float(df["hedged_ret"].var())
    he = hedge_effectiveness(df["spot_ret"], df["hedged_ret"])
    summary = HedgeSummary(
        hedge_ratio=h_star,
        spot_variance=spot_var,
        hedged_variance=hedged_var,
        hedge_effectiveness=he,
    )
    return df, summary
