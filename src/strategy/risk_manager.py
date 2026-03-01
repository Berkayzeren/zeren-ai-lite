import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger("ZerenAI.Strategy.RiskManager")


class RiskManager:
    """
    Zeren AI Risk Yönetim Merkezi.
    Pozisyon büyüklüğü, volatilite kontrolü ve koruma kalkanlarını yönetir.
    """

    def __init__(self, max_risk_per_trade: float = 0.02):
        self.max_risk_per_trade = max_risk_per_trade  # Tek işlemde max risk (%2)

    def calculate_kelly_position(self, win_prob: float, win_loss_ratio: float) -> float:
        """
        Kelly Kriteri ($f^* = \frac{bp - q}{b}$) optimal pozisyon boyutlandırma.

        Args:
            win_prob: Kazanma olasılığı (p)
            win_loss_ratio: Ortalama kazanç / Ortalama kayıp (b)
        """
        if win_loss_ratio <= 0:
            return 0.0

        loss_prob = 1 - win_prob
        kelly_f = (win_loss_ratio * win_prob - loss_prob) / win_loss_ratio

        # Risk kısıtlamaları: Kelly'nin yarısı (half-kelly) ve sistem max limiti
        safe_kelly = max(0.0, kelly_f * 0.5)
        return min(safe_kelly, self.max_risk_per_trade)

    def check_opening_bell_buffer(self, ticker: str) -> float:
        """
        Açılış Volatilitesi Koruması:
        Borsa açılışının ilk 15 dakikasında pozisyon büyüklüğünü %50 azaltır.
        """
        multiplier = 1.0
        now = datetime.now()

        # BIST açılış saati örnek (10:00 - 10:15)
        if now.hour == 10 and now.minute < 15:
            logger.warning(
                f"🔔 OPENING BELL BUFFER: {ticker} için boyut %50 azaltılıyor."
            )
            multiplier = 0.5

        return multiplier

    def validate_trade_risk(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bir işlemin risk standartlarına uygunluğunu denetler.
        """
        # Lite versiyon için temel kontrol mantığı
        is_valid = True
        reason = "OK"

        if signal_data.get("volatility", 0) > 0.05:
            is_valid = False
            reason = "Aşırı volatilite tespit edildi."

        return {
            "is_valid": is_valid,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
