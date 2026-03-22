import unittest

import pandas as pd

from src.hedge import build_hedge_comparison, compute_returns, estimate_static_hedge_ratio


class HedgeTests(unittest.TestCase):
    def test_compute_returns_simple(self) -> None:
        prices = pd.DataFrame(
            {
                "spot": [100.0, 110.0, 121.0, 108.9],
                "fut": [100.0, 120.0, 144.0, 115.2],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        returns = compute_returns(prices, method="simple")

        self.assertEqual(list(returns.columns), ["spot", "fut", "r_s", "r_f"])
        self.assertEqual(len(returns), 3)
        self.assertAlmostEqual(estimate_static_hedge_ratio(returns["r_s"], returns["r_f"]), 0.5)

    def test_compute_returns_log_rejects_non_positive_prices(self) -> None:
        prices = pd.DataFrame(
            {
                "spot": [100.0, 0.0, 110.0],
                "fut": [101.0, 102.0, 103.0],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "Log returns require strictly positive prices",
        ):
            compute_returns(prices, method="log")

    def test_compute_returns_simple_rejects_infinite_returns(self) -> None:
        prices = pd.DataFrame(
            {
                "spot": [100.0, 0.0, 110.0],
                "fut": [100.0, 100.0, 110.0],
            }
        )

        with self.assertRaisesRegex(
            ValueError,
            "Computed returns contain infinite values",
        ):
            compute_returns(prices, method="simple")

    def test_build_hedge_comparison_adds_expected_columns(self) -> None:
        returns = pd.DataFrame(
            {
                "r_s": [0.01, 0.02, -0.01, 0.03, 0.01, -0.02],
                "r_f": [0.015, 0.01, -0.005, 0.025, 0.005, -0.01],
            },
            index=pd.date_range("2024-01-01", periods=6, freq="D"),
        )

        comparison, h_static = build_hedge_comparison(returns, window=3, lag=1)

        self.assertIn("r_p_naive", comparison.columns)
        self.assertIn("r_p_static", comparison.columns)
        self.assertIn("r_p_dynamic", comparison.columns)
        self.assertIn("h_t", comparison.columns)
        self.assertGreater(h_static, 0)
        self.assertEqual(comparison["r_p_dynamic"].notna().sum(), 3)


if __name__ == "__main__":
    unittest.main()
