import asyncio
import random
from src.core.module_base import AIModule
from src.strategy.risk_manager import RiskManager
from src.strategy.signal_generator import SignalGenerator
from src.strategy.neural_risk_guard import NeuralRiskGuard


class ZerenEngine(AIModule):
    """
    Lite versiyonun ana yürütücü motoru.
    Modülleri, sinyal üretimini ve hibrit risk yönetimini koordine eder.
    """

    def __init__(self):
        super().__init__("ZerenEngine-Lite")
        self.risk_manager = RiskManager()
        self.signal_gen = SignalGenerator()
        self.neural_guard = NeuralRiskGuard()

    async def _on_start(self):
        print(f"--- {self.module_id} Başlatılıyor ---")
        print("1. Konfigürasyonlar ve i18n sistemleri yüklendi.")
        print("2. NeuralRiskGuard anomali modelleri (Lite) yüklendi.")
        print("3. Market veri akışı simüle ediliyor...")
        await asyncio.sleep(1)
        print("4. Strateji motoru ve Sinyal Üretici aktif.")

    async def run_cycle(self):
        """Ana işlem döngüsü: Veri -> Sinyal -> Risk Denetimi -> Karar"""
        tickers = ["BTCUSDT", "ETHUSDT", "THYAO.IS"]

        while self.status.value == "running":
            selected_ticker = random.choice(tickers)
            print(f"\n[{self.sync_time()}] İşlem döngüsü taranıyor: {selected_ticker}")

            # --- 1. VERİ SİMÜLASYONU ---
            sim_data = {
                "rsi": random.uniform(20, 80),
                "macd_trend": random.choice(["bullish", "bearish", "neutral"]),
                "volatility": random.uniform(0.01, 0.06),
            }

            # --- 2. SİNYAL ÜRETİMİ ---
            signals = await self.signal_gen.generate_signals(selected_ticker, sim_data)
            if not signals["signals"]:
                print(f"ℹ️ {selected_ticker}: Güçlü bir sinyal tespit edilemedi.")
            else:
                print(self.signal_gen.format_signal_report(signals))

                # --- 3. RİSK DENETİMİ (HİBRİT) ---
                # Kural tabanlı denetim
                rule_check = self.risk_manager.validate_trade_risk(sim_data)
                # Sinirsel (Neural) denetim
                # Not: RiskManager'daki volatiliteyi 10 ile çarparak technical_risk simüle ediyoruz
                neural_check = self.neural_guard.evaluate_risk_hybrid(
                    selected_ticker, sim_data["volatility"] * 10
                )

                print(
                    f"🛡️ Risk Durumu: Rules={rule_check['reason']} | Neural={neural_check['status']}"
                )

                # --- 4. KARAR MEKANİZMASI ---
                if rule_check["is_valid"] and neural_check["level"] < 3:
                    pos_size = self.risk_manager.calculate_kelly_position(0.60, 1.5)
                    print(
                        f"🚀 İŞLEM ONAYLANDI: {selected_ticker} | Boyut: {pos_size:.4f}"
                    )
                else:
                    print(
                        f"⚠️ İŞLEM REDDEDİLDİ: Risk limitleri aşıldı! (Action: {neural_check['action']})"
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
