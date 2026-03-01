import logging
from typing import Dict, Any, List
import random

logger = logging.getLogger("ZerenAI.Strategy.PortfolioOptimizer")


class PortfolioOptimizer:
    """
    Lite Portföy Optimizatörü.
    Korelasyon analizi ve sektör bazlı çeşitlendirme simülasyonu yapar.
    """

    def __init__(self):
        # Örnek sektör eşleştirmeleri
        self.sectors = {
            "THYAO.IS": "Ulaşım",
            "PGSUS.IS": "Ulaşım",
            "AKBNK.IS": "Bankacılık",
            "EREGL.IS": "Demir-Çelik",
            "BTCUSDT": "Kripto",
        }

    def optimize_allocation(
        self, current_portfolio: Dict[str, float], new_signal: Dict[str, Any]
    ) -> float:
        """
        Yeni bir sinyal için optimal ağırlığı hesaplar.
        Sektör yoğunlaşması kontrolü içerir.
        """
        ticker = new_signal.get("ticker")
        sector = self.sectors.get(ticker, "Diğer")

        # Sektör yoğunlaşması kontrolü
        sector_usage = sum(
            val for t, val in current_portfolio.items() if self.sectors.get(t) == sector
        )

        # Eğer sektör ağırlığı %30'u geçiyorsa yeni alımı kısıtla
        max_sector_weight = 0.30
        if sector_usage >= max_sector_weight:
            logger.warning(
                f"⚠️ SEKTÖR YOĞUNLAŞMA RİSKİ: {sector} sektörü zaten %{sector_usage * 100} ağırlığında."
            )
            return 0.0

        # Temel optimizasyon (Lite sürüm için basitleştirilmiş)
        base_weight = 0.05  # Standart %5
        confidence = new_signal.get("confidence", 0.5)

        optimized_weight = base_weight * (confidence * 2)
        return round(min(optimized_weight, max_sector_weight - sector_usage), 4)

    def calculate_portfolio_health(self, portfolio: Dict[str, float]) -> Dict[str, Any]:
        """Portföyün genel sağlık ve çeşitlendirme durumunu analiz eder."""
        return {
            "total_exposure": sum(portfolio.values()),
            "composition": {
                self.sectors.get(t, "Diğer"): sum(
                    v
                    for k, v in portfolio.items()
                    if self.sectors.get(k) == self.sectors.get(t)
                )
                for t in portfolio
            },
            "status": "Healthy" if len(portfolio) > 3 else "Concentrated",
        }
