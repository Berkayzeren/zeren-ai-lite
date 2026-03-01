import random
import logging
from typing import Dict, Any

logger = logging.getLogger("ZerenAI.Strategy.Sentiment")


class SentimentAnalyzer:
    """
    Lite Haber ve Sosyal Medya Duygu Analizörü.
    Piyasa duyarlılığını simüle ederek stratejiye ek bir doğrulama katmanı ekler.
    """

    def __init__(self):
        self.keywords = {
            "bullish": ["launch", "partnership", "growth", "buyback", "profit"],
            "bearish": ["lawsuit", "hack", "dump", "regulation", "loss"],
        }

    def analyze_ticker(self, ticker: str) -> float:
        """
        Bir sembol için duygu skoru üretir (-1.0 ile 1.0 arası).
        Lite versiyon: İstatistiksel ağırlıklı rastgele simülasyon.
        """
        # Genelde piyasa %55 boğa (bullish) eğilimlidir simülasyonu
        base_sentiment = random.uniform(-0.5, 0.7)

        # Bazı özel durum simülasyonları
        if "BTC" in ticker:
            base_sentiment += 0.1  # BTC hype faktörü

        return round(max(-1.0, min(1.0, base_sentiment)), 2)

    def get_sentiment_mitigation(self, sentiment_score: float) -> float:
        """Duygu skoruna göre işlem boyutunu etkileyen çarpan döndürür."""
        if sentiment_score < -0.5:
            return 0.0  # Çok negatif, işlem yapma
        elif sentiment_score < 0:
            return 0.5  # Negatif, boyutu yarılatt
        return 1.0  # Pozitif veya nötr
