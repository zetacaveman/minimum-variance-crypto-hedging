from __future__ import annotations

from pathlib import Path

try:
    from .hedge import run_static_hedge
except ImportError:
    from hedge import run_static_hedge


def main() -> None:
    try:
        df, summary = run_static_hedge()
    except ValueError as exc:
        raise SystemExit(f"Static hedge run failed: {exc}") from exc

    print(f"Estimated hedge ratio h*: {summary.hedge_ratio:.6f}")
    print(f"Variance of spot returns: {summary.spot_variance:.8f}")
    print(f"Variance of hedged returns: {summary.hedged_variance:.8f}")
    print(f"Hedging effectiveness: {summary.hedge_effectiveness:.4%}")

    output_path = Path("data/processed/btc_static_hedge_daily.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index_label="date")
    print(f"Saved merged dataset with returns to: {output_path}")


if __name__ == "__main__":
    main()
