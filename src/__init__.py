"""Core hedging utilities."""

from .hedge import (
    apply_hedge,
    build_hedge_comparison,
    compute_dynamic_hedged_returns,
    compute_naive_hedged_returns,
    compute_returns,
    compute_static_hedged_returns,
    estimate_dynamic_hedge_ratio,
    estimate_static_hedge_ratio,
    hedge_effectiveness,
)

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
