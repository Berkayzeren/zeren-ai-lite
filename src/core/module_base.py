import asyncio
import logging
import time
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Log yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ZerenAI.Core")

class ModuleStatus(Enum):
    """Modül durumlarını temsil eden Enum."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class AIModule:
    """
    Zeren AI projesindeki tüm servisler için temel sınıf.
    Asenkron çalışma, durum yönetimi ve zaman senkronizasyonu sağlar.
    """
    
    def __init__(self, module_id: str):
        self.module_id = module_id
        self.status = ModuleStatus.STOPPED
        self.error_message: Optional[str] = None
        self._sync_timestamp: Optional[float] = None
        logger.info(f"Modül başlatıldı: {self.module_id}")

    async def start(self):
        """Modülü asenkron olarak başlatır."""
        self.status = ModuleStatus.INITIALIZING
        logger.info(f"[{self.module_id}] Başlatılıyor...")
        try:
            await self._on_start()
            self.status = ModuleStatus.RUNNING
        except Exception as e:
            self.status = ModuleStatus.ERROR
            self.error_message = str(e)
            logger.error(f"[{self.module_id}] Başlatma hatası: {e}")

    async def stop(self):
        """Modülü durdurur."""
        logger.info(f"[{self.module_id}] Durduruluyor...")
        await self._on_stop()
        self.status = ModuleStatus.STOPPED

    async def _on_start(self):
        """Alt sınıflar tarafından override edilmelidir."""
        pass

    async def _on_stop(self):
        """Alt sınıflar tarafından override edilmelidir."""
        pass

    def sync_time(self, master_timestamp: Optional[float] = None) -> float:
        """
        SWISS WATCH ANALOGY: Tüm modüller için zaman senkronizasyonu.
        Tüm modüllerin aynı zaman referansı ile çalışmasını sağlar.
        """
        if master_timestamp is None:
            master_timestamp = time.time()
        self._sync_timestamp = master_timestamp
        return master_timestamp

    def get_status_report(self) -> Dict[str, Any]:
        """Modül durumunu raporlar."""
        return {
            "module_id": self.module_id,
            "status": self.status.value,
            "error": self.error_message,
            "sync_time": self._sync_timestamp
        }
