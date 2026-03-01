import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger("ZerenAI.Strategy.RiskManager")


class RiskManager:
    """
    Zeren AI Risk Management Center.
    Manages position sizing, volatility controls, and protection guards.
    """

    def __init__(self, max_risk_per_trade: float = 0.02):
        self.max_risk_per_trade = max_risk_per_trade  # Max risk per trade (e.g., 2%)

    def calculate_kelly_position(self, win_prob: float, win_loss_ratio: float) -> float:
        """
        Kelly Criterion ($f^* = \frac{bp - q}{b}$) for optimal position sizing.

        Args:
            win_prob: Probability of winning (p)
            win_loss_ratio: Average win / Average loss (b)
        """
        if win_loss_ratio <= 0:
            return 0.0

        loss_prob = 1 - win_prob
        kelly_f = (win_loss_ratio * win_prob - loss_prob) / win_loss_ratio

        # Risk constraints: Half-Kelly and system max limit
        safe_kelly = max(0.0, kelly_f * 0.5)
        return min(safe_kelly, self.max_risk_per_trade)

    def check_opening_bell_buffer(self, ticker: str) -> float:
        """
        Opening Volatility Protection:
        Reduces position size by 50% during the first 15 minutes of market opening.
        """
        multiplier = 1.0
        now = datetime.now()

        # Example for market opening (10:00 - 10:15)
        if now.hour == 10 and now.minute < 15:
            logger.warning(
                f"🔔 OPENING BELL BUFFER: Reducing size by 50% for {ticker}."
            )
            multiplier = 0.5

        return multiplier

    def validate_trade_risk(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates if a trade meets risk standards.
        """
        # Basic control logic for Lite version
        is_valid = True
        reason = "OK"

        if signal_data.get("volatility", 0) > 0.05:
            is_valid = False
            reason = "Excessive volatility detected."

        return {
            "is_valid": is_valid,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
