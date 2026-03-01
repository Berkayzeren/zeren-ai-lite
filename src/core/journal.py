import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger("ZerenAI.Core.Journal")


class Journal:
    """
    Zeren AI İşlem ve Karar Günlüğü.
    Tüm kararları (Onay/Red) kalıcı olarak JSON formatında saklar.
    """

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Günlük dosya adı (journal_2026-03-01.json)
        self.current_file = os.path.join(
            self.log_dir, f"journal_{datetime.now().strftime('%Y-%m-%d')}.json"
        )

    def log_decision(self, decision_data: Dict[str, Any]):
        """Bir kararı günlüğe kaydeder."""
        try:
            # Mevcut veriyi oku veya yeni liste oluştur
            records = []
            if os.path.exists(self.current_file):
                with open(self.current_file, "r") as f:
                    try:
                        records = json.load(f)
                    except json.JSONDecodeError:
                        records = []

            # Yeni kaydı ekle
            records.append({"ts": datetime.now().isoformat(), "data": decision_data})

            # Yaz
            with open(self.current_file, "w") as f:
                json.dump(records, f, indent=2, default=str)

            logger.info(
                f"Karar günlüğe kaydedildi: {decision_data.get('ticker')} - {decision_data.get('decision')}"
            )

        except Exception as e:
            logger.error(f"Günlük yazma hatası: {e}")
