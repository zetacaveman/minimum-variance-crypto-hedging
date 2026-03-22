from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "compute_returns",
    "estimate_static_hedge_ratio",
    "estimate_dynamic_hedge_ratio",
    "apply_hedge",
    "compute_naive_hedged_returns",
    "compute_static_hedged_returns",
    "compute_dynamic_hedged_returns",
    "hedge_effectiveness",
    "build_hedge_comparison",
]


def _align_two_series(
    left: pd.Series,
    right: pd.Series,
    left_name: str = "left",
    right_name: str = "right",
) -> tuple[pd.Series, pd.Series]:
    aligned = pd.concat([left.rename(left_name), right.rename(right_name)], axis=1).dropna()
    if aligned.empty:
        raise ValueError("No overlapping non-null observations between input series")
    return aligned[left_name], aligned[right_name]


def _validate_price_columns(df: pd.DataFrame, columns: set[str], method: str) -> None:
    non_finite = sorted(
        col for col in columns if not np.isfinite(df[col].dropna().to_numpy()).all()
    )
    if non_finite:
        raise ValueError(f"Price columns contain non-finite values: {non_finite}")

    if method == "log":
        non_positive = sorted(col for col in columns if (df[col].dropna() <= 0).any())
        if non_positive:
            raise ValueError(
                "Log returns require strictly positive prices in columns: "
                f"{non_positive}"
            )


def compute_returns(
    df: pd.DataFrame,
    spot_col: str = "spot",
    fut_col: str = "fut",
    method: str = "simple",
) -> pd.DataFrame:
    required = {spot_col, fut_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if method not in {"simple", "log"}:
        raise ValueError("method must be 'simple' or 'log'")

    _validate_price_columns(df, required, method)

    out = df.copy()
    if method == "simple":
        out["r_s"] = out[spot_col].pct_change()
        out["r_f"] = out[fut_col].pct_change()
    elif method == "log":
        out["r_s"] = np.log(out[spot_col] / out[spot_col].shift(1))
        out["r_f"] = np.log(out[fut_col] / out[fut_col].shift(1))

    invalid_returns = sorted(
        col for col in ("r_s", "r_f") if np.isinf(out[col].dropna().to_numpy()).any()
    )
    if invalid_returns:
        raise ValueError(
            "Computed returns contain infinite values; check for zero prices in columns: "
            f"{invalid_returns}"
        )

    return out.dropna(subset=["r_s", "r_f"])


def estimate_static_hedge_ratio(spot_ret: pd.Series, fut_ret: pd.Series) -> float:
    spot_ret, fut_ret = _align_two_series(spot_ret, fut_ret, left_name="r_s", right_name="r_f")
    var_f = fut_ret.var()
    if pd.isna(var_f) or var_f == 0:
        raise ValueError("Cannot estimate hedge ratio: futures return variance is zero")
    return float(spot_ret.cov(fut_ret) / var_f)


def estimate_dynamic_hedge_ratio(
    spot_ret: pd.Series,
    fut_ret: pd.Series,
    window: int = 60,
    lag: int = 1,
) -> pd.Series:
    spot_ret, fut_ret = _align_two_series(spot_ret, fut_ret, left_name="r_s", right_name="r_f")
    if window < 2:
        raise ValueError("window must be >= 2")
    if lag < 0:
        raise ValueError("lag must be >= 0")

    rolling_cov = spot_ret.rolling(window).cov(fut_ret)
    rolling_var_f = fut_ret.rolling(window).var()
    hedge_ratio = (rolling_cov / rolling_var_f).replace([np.inf, -np.inf], np.nan)
    return hedge_ratio.shift(lag)


def apply_hedge(
    spot_ret: pd.Series,
    fut_ret: pd.Series,
    hedge_ratio: float | pd.Series,
) -> pd.Series:
    spot_ret, fut_ret = _align_two_series(spot_ret, fut_ret, left_name="r_s", right_name="r_f")
    if isinstance(hedge_ratio, pd.Series):
        hedge_ratio = hedge_ratio.reindex(spot_ret.index)
    return spot_ret - hedge_ratio * fut_ret


def compute_naive_hedged_returns(
    spot_ret: pd.Series,
    fut_ret: pd.Series,
    hedge_ratio: float = 1.0,
) -> pd.Series:
    return apply_hedge(spot_ret, fut_ret, hedge_ratio)


def compute_static_hedged_returns(spot_ret: pd.Series, fut_ret: pd.Series) -> tuple[pd.Series, float]:
    h_static = estimate_static_hedge_ratio(spot_ret, fut_ret)
    return apply_hedge(spot_ret, fut_ret, h_static), h_static


def compute_dynamic_hedged_returns(
    spot_ret: pd.Series,
    fut_ret: pd.Series,
    window: int = 60,
    lag: int = 1,
) -> tuple[pd.Series, pd.Series]:
    h_t = estimate_dynamic_hedge_ratio(spot_ret, fut_ret, window=window, lag=lag)
    return apply_hedge(spot_ret, fut_ret, h_t), h_t


def hedge_effectiveness(spot_ret: pd.Series, hedged_ret: pd.Series) -> float:
    spot_ret, hedged_ret = _align_two_series(
        spot_ret,
        hedged_ret,
        left_name="r_s",
        right_name="r_p",
    )
    var_spot = spot_ret.var()
    if pd.isna(var_spot) or var_spot == 0:
        raise ValueError("Cannot compute hedge effectiveness: spot return variance is zero")
    return float(1 - hedged_ret.var() / var_spot)


def build_hedge_comparison(
    returns_df: pd.DataFrame,
    window: int = 60,
    lag: int = 1,
) -> tuple[pd.DataFrame, float]:
    required = {"r_s", "r_f"}
    missing = required - set(returns_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = returns_df.copy()
    out["r_p_naive"] = compute_naive_hedged_returns(out["r_s"], out["r_f"], hedge_ratio=1.0)
    out["r_p_static"], h_static = compute_static_hedged_returns(out["r_s"], out["r_f"])
    out["r_p_dynamic"], out["h_t"] = compute_dynamic_hedged_returns(
        out["r_s"],
        out["r_f"],
        window=window,
        lag=lag,
    )
    return out, h_static
