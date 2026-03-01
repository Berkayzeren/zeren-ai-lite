from src.strategy.risk_manager import RiskManager


def test_kelly_calculation():
    """Tests the accuracy of the Kelly Criterion calculation."""
    rm = RiskManager(max_risk_per_trade=0.10)

    # 55% win rate, 2.0 win/loss ratio (f* = (0.55*2 - 0.45)/2 = 0.65/2 = 0.325)
    # Half-kelly: 0.1625, Max Limit: 0.10
    kelly_pos = rm.calculate_kelly_position(win_prob=0.55, win_loss_ratio=2.0)

    assert kelly_pos <= rm.max_risk_per_trade
    assert kelly_pos > 0


def test_risk_validation():
    """Tests the risk validation logic."""
    rm = RiskManager()

    # Safe signal
    safe_signal = {"volatility": 0.02}
    assert rm.validate_trade_risk(safe_signal)["is_valid"] is True

    # Dangerous signal (Excessive volatility)
    risky_signal = {"volatility": 0.08}
    assert rm.validate_trade_risk(risky_signal)["is_valid"] is False
