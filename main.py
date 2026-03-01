import asyncio
from src.core.module_base import AIModule
from src.strategy.risk_manager import RiskManager


class ZerenEngine(AIModule):
    """
    Lite versiyonun ana yürütücü motoru.
    Modülleri ve risk kontrollerini koordine eder.
    """

    def __init__(self):
        super().__init__("ZerenEngine-Lite")
        self.risk_manager = RiskManager()

    async def _on_start(self):
        print(f"--- {self.module_id} Başlatılıyor ---")
        print("1. Konfigürasyonlar yüklendi.")
        print("2. Market bağlantıları simüle ediliyor...")
        await asyncio.sleep(1)
        print("3. Strateji motoru aktif.")

    async def run_cycle(self):
        """Ana işlem döngüsü."""
        while self.status.value == "running":
            print(f"[{self.sync_time()}] İşlem döngüsü taranıyor...")
            # Örnek bir sinyal kontrolü ve risk denetimi
            sample_signal = {"ticker": "BTCUSDT", "volatility": 0.02}
            risk_check = self.risk_manager.validate_trade_risk(sample_signal)

            if risk_check["is_valid"]:
                pos_size = self.risk_manager.calculate_kelly_position(0.55, 2.0)
                print(
                    f"✅ Uygun İşlem: {sample_signal['ticker']} | Önerilen Boyut: {pos_size:.4f}"
                )
            else:
                print(f"❌ Risk İhlali: {risk_check['reason']}")

            await asyncio.sleep(5)


async def main():
    engine = ZerenEngine()
    await engine.start()
    try:
        await engine.run_cycle()
    except KeyboardInterrupt:
        await engine.stop()


if __name__ == "__main__":
    asyncio.run(main())
