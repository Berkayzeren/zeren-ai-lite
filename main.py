import asyncio
import random
import logging

# Core Imports
from src.core.module_base import AIModule
from src.core.event_bus import EventBus
from src.core.journal import Journal
from src.core.monitoring import Monitoring
from src.core.data_models import SignalData, RiskReport, TradeDecision

# Strategy Imports
from src.strategy.risk_manager import RiskManager
from src.strategy.signal_generator import SignalGenerator
from src.strategy.neural_risk_guard import NeuralRiskGuard
from src.strategy.portfolio_optimizer import PortfolioOptimizer
from src.strategy.sentiment_analyzer import SentimentAnalyzer

# Log ayarları
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ZerenEngine(AIModule):
    """
    Zeren AI Lite - Gelişmiş Otonom Karar Motoru.
    Duygu analizi, çok katmanlı risk ve şeffaf günlükleme özelliklerini birleştirir.
    """

    def __init__(self):
        super().__init__("ZerenEngine-Lite")
        self.bus = EventBus()
        self.journal = Journal()
        self.monitor = Monitoring()

        # Servisler
        self.risk_manager = RiskManager()
        self.signal_gen = SignalGenerator()
        self.neural_guard = NeuralRiskGuard()
        self.portfolio_opt = PortfolioOptimizer()
        self.sentiment = SentimentAnalyzer()

        self.current_portfolio = {}

    async def handle_trade_execution(self, trade_data: dict):
        ticker = trade_data["ticker"]
        weight = trade_data["weight"]
        self.current_portfolio[ticker] = self.current_portfolio.get(ticker, 0) + weight
        print(f"💰 PORTFÖY GÜNCELLENDİ: {ticker} (+%{weight * 100})")

    async def _on_start(self):
        self.bus.subscribe("TRADE_EXECUTED", self.handle_trade_execution)
        asyncio.create_task(self.bus.start_listening())

        # Periodic Heartbeat TASK
        asyncio.create_task(self._heartbeat_loop())

        print("\n" + "=" * 50)
        print("🚀 ZEREN AI LITE ENGINE V2 - AKTİF")
        print("Mimari: Event-Driven & Sub-Component Hybrid")
        print("Özellikler: Journaling, Monitoring, Sentiment Focus")
        print("=" * 50)
        await asyncio.sleep(1)

    async def _heartbeat_loop(self):
        """Sistemin hayatta olduğunu raporlar."""
        while self.status.value == "running":
            self.monitor.send_heartbeat("Engine")
            await asyncio.sleep(30)

    async def run_cycle(self):
        tickers = ["BTCUSDT", "ETHUSDT", "THYAO.IS", "EREGL.IS", "AKBNK.IS", "PGSUS.IS"]

        while self.status.value == "running":
            selected_ticker = random.choice(tickers)
            print(f"\n[{self.sync_time()}] --- ANALİZ BAŞLADI: {selected_ticker} ---")

            # --- 1. DUYGU ANALİZİ (Sentiment) ---
            sentiment_score = self.sentiment.analyze_ticker(selected_ticker)
            sentiment_mult = self.sentiment.get_sentiment_mitigation(sentiment_score)
            print(f"🌍 Sentiment: {sentiment_score} (Multiplier: {sentiment_mult})")

            # --- 2. VERİ VE SİNYAL ---
            sim_data = {
                "rsi": random.uniform(20, 80),
                "macd_trend": random.choice(["bullish", "bearish", "neutral"]),
                "volatility": random.uniform(0.01, 0.06),
                "ticker": selected_ticker,
            }
            signals = await self.signal_gen.generate_signals(selected_ticker, sim_data)

            if not signals["signals"] or sentiment_mult == 0:
                reason = (
                    "Zayıf Sinyal" if not signals["signals"] else "Negatif Haber Akışı"
                )
                print(f"ℹ️ {selected_ticker}: Pas geçildi ({reason})")
                continue

            # Standardize Signal Data
            max_strategy = max(
                signals["signals"], key=lambda k: signals["signals"][k]["confidence"]
            )
            sig_obj = SignalData(
                ticker=selected_ticker,
                action=signals["signals"][max_strategy]["signal"],
                confidence=signals["signals"][max_strategy]["confidence"],
                strategy_name=max_strategy,
            )

            # --- 3. HİBRİT RİSK DENETİMİ ---
            rule_check = self.risk_manager.validate_trade_risk(sim_data)
            neural_check = self.neural_guard.evaluate_risk_hybrid(
                selected_ticker, sim_data["volatility"] * 10
            )

            risk_report = RiskReport(
                is_valid=rule_check["is_valid"],
                risk_level=neural_check["level"],
                status=neural_check["status"],
                reason=rule_check["reason"],
            )

            # --- 4. PORTFÖY OPTİMİZASYONU ---
            opt_weight = self.portfolio_opt.optimize_allocation(
                self.current_portfolio,
                {"ticker": selected_ticker, "confidence": sig_obj.confidence},
            )
            final_weight = opt_weight * sentiment_mult

            # --- 5. KARAR VE GÜNLÜKLEME ---
            decision = "REJECT"
            final_reason = "Risk/Sektör Kısıtı"

            if risk_report.is_valid and risk_report.risk_level < 3 and final_weight > 0:
                decision = "EXECUTE"
                final_reason = "Tüm protokoller onayladı."
                await self.bus.publish(
                    "TRADE_EXECUTED",
                    {"ticker": selected_ticker, "weight": final_weight},
                )

            # Create Decision Object
            trade_decision = TradeDecision(
                ticker=selected_ticker,
                decision=decision,
                signal=sig_obj,
                risk=risk_report,
                weight=final_weight,
                reason=final_reason,
            )

            # JOURNALING (Kayıt)
            self.journal.log_decision(trade_decision.dict())

            # Konsol Raporu
            print(f"🛡️ Risk: Rules={risk_report.reason} | Neural={risk_report.status}")
            print(
                f"📊 Karar: {decision} (%{final_weight * 100}) - Neden: {final_reason}"
            )

            await asyncio.sleep(4)


async def main():
    engine = ZerenEngine()
    await engine.start()
    try:
        await engine.run_cycle()
    except KeyboardInterrupt:
        await engine.stop()


if __name__ == "__main__":
    asyncio.run(main())
