import logging
from typing import Dict, Any, List
import random

logger = logging.getLogger("ZerenAI.Strategy.PortfolioOptimizer")


class PortfolioOptimizer:
    """
    Lite Portfolio Optimizer.
    Simulates correlation analysis and sector-based diversification.
    """

    def __init__(self):
        # Example sector mappings
        self.sectors = {
            "THYAO.IS": "Transportation",
            "PGSUS.IS": "Transportation",
            "AKBNK.IS": "Banking",
            "EREGL.IS": "Steel",
            "BTCUSDT": "Crypto",
            "ETHUSDT": "Crypto",
        }

    def optimize_allocation(
        self, current_portfolio: Dict[str, float], new_signal: Dict[str, Any]
    ) -> float:
        """
        Calculates optimal weight for a new signal.
        Includes sector concentration checks.
        """
        ticker = new_signal.get("ticker")
        sector = self.sectors.get(ticker, "Other")

        # Sector concentration check
        sector_usage = sum(
            val for t, val in current_portfolio.items() if self.sectors.get(t) == sector
        )

        # Limit if sector weight exceeds 30%
        max_sector_weight = 0.30
        if sector_usage >= max_sector_weight:
            logger.warning(
                f"⚠️ SECTOR CONCENTRATION RISK: {sector} sector is already at {sector_usage * 100:.1f}% capacity."
            )
            return 0.0

        # Basic optimization (Simplified for Lite version)
        base_weight = 0.05  # Standard 5%
        confidence = new_signal.get("confidence", 0.5)

        optimized_weight = base_weight * (confidence * 2)
        return round(min(optimized_weight, max_sector_weight - sector_usage), 4)

    def calculate_portfolio_health(self, portfolio: Dict[str, float]) -> Dict[str, Any]:
        """Analyzes overall portfolio health and diversification."""
        return {
            "total_exposure": sum(portfolio.values()),
            "composition": {
                self.sectors.get(t, "Other"): sum(
                    v
                    for k, v in portfolio.items()
                    if self.sectors.get(k) == self.sectors.get(t)
                )
                for t in portfolio
            },
            "status": "Healthy" if len(portfolio) > 3 else "Concentrated",
        }
