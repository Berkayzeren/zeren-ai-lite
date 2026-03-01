import asyncio
import random
from src.core.module_base import AIModule
from src.core.event_bus import EventBus
from src.strategy.risk_manager import RiskManager
from src.strategy.signal_generator import SignalGenerator
from src.strategy.neural_risk_guard import NeuralRiskGuard
from src.strategy.portfolio_optimizer import PortfolioOptimizer


class ZerenEngine(AIModule):
    """
    Lite versiyonun ana yürütücü motoru.
    EventBus tabanlı haberleşme ve çok katmanlı karar mekanizması.
    """

    def __init__(self):
        super().__init__("ZerenEngine-Lite")
        self.bus = EventBus()
        self.risk_manager = RiskManager()
        self.signal_gen = SignalGenerator()
        self.neural_guard = NeuralRiskGuard()
        self.portfolio_opt = PortfolioOptimizer()

        # Simüle edilmiş portföy
        self.current_portfolio = {}  # ticker: weight

    async def handle_trade_execution(self, trade_data: dict):
        """İşlem gerçekleştiğinde tetiklenen callback."""
        ticker = trade_data["ticker"]
        weight = trade_data["weight"]
        self.current_portfolio[ticker] = self.current_portfolio.get(ticker, 0) + weight
        print(
            f"💰 PORTFÖY GÜNCELLENDİ: {ticker} (+%{weight * 100}) | Yeni Portföy: {self.current_portfolio}"
        )

    async def _on_start(self):
        print(f"--- {self.module_id} Başlatılıyor ---")
        # EventBus abonelikleri
        self.bus.subscribe("TRADE_EXECUTED", self.handle_trade_execution)

        # EventBus'ı arka planda başlat
        asyncio.create_task(self.bus.start_listening())

        print("1. EventBus ve Dinleyiciler Aktif.")
        print("2. PortfolioOptimizer ve Sektör Analiz Modülleri Yüklendi.")
        print("3. Strateji motoru ve Sinyal Üretici hazır.")
        await asyncio.sleep(1)

    async def run_cycle(self):
        """Ana işlem döngüsü: Veri -> Sinyal -> Risklar -> Optimizasyon -> Karar"""
        tickers = ["BTCUSDT", "THYAO.IS", "EREGL.IS", "AKBNK.IS", "PGSUS.IS"]

        while self.status.value == "running":
            selected_ticker = random.choice(tickers)
            print(f"\n[{self.sync_time()}] Döngü: {selected_ticker}")

            # --- 1. VERİ SİMÜLASYONU ---
            sim_data = {
                "rsi": random.uniform(20, 80),
                "macd_trend": random.choice(["bullish", "bearish", "neutral"]),
                "volatility": random.uniform(0.01, 0.06),
                "ticker": selected_ticker,
            }

            # --- 2. SİNYAL ÜRETİMİ ---
            signals = await self.signal_gen.generate_signals(selected_ticker, sim_data)
            if not signals["signals"]:
                print(f"ℹ️ {selected_ticker}: Güçlü bir sinyal yok.")
            else:
                print(self.signal_gen.format_signal_report(signals))

                # Sinyal içindeki en güçlü güven skorunu al
                max_conf = max(s["confidence"] for s in signals["signals"].values())

                # --- 3. ÇOK KATMANLI RİSK DENETİMİ ---
                rule_check = self.risk_manager.validate_trade_risk(sim_data)
                neural_check = self.neural_guard.evaluate_risk_hybrid(
                    selected_ticker, sim_data["volatility"] * 10
                )

                # --- 4. PORTFÖY OPTİMİZASYONU (Sektör Kontrolü) ---
                opt_weight = self.portfolio_opt.optimize_allocation(
                    self.current_portfolio,
                    {"ticker": selected_ticker, "confidence": max_conf},
                )

                print(
                    f"🛡️ Risk: Rules={rule_check['reason']} | Neural={neural_check['status']}"
                )
                print(
                    f"📊 Optimizasyon: Önerilen Sektörel Ağırlık = %{opt_weight * 100}"
                )

                # --- 5. SON KARAR ---
                if (
                    rule_check["is_valid"]
                    and neural_check["level"] < 3
                    and opt_weight > 0
                ):
                    print(f"🚀 ONAY: {selected_ticker} işleme gönderiliyor...")
                    # EventBus üzerinden duyur
                    await self.bus.publish(
                        "TRADE_EXECUTED",
                        {"ticker": selected_ticker, "weight": opt_weight},
                    )
                else:
                    reason = (
                        "Risk Limitleri"
                        if not rule_check["is_valid"] or neural_check["level"] >= 3
                        else "Sektörel Limitler"
                    )
                    print(f"⚠️ RED: {selected_ticker} - Neden: {reason}")

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
