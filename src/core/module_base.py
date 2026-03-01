import asyncio
import logging
import time
from enum import Enum
from typing import Optional, Dict, Any

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ZerenAI.Core")


class ModuleStatus(Enum):
    """Enum representing module states."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class AIModule:
    """
    Base class for all services in the Zeren AI project.
    Provides asynchronous execution, state management, and time synchronization.
    """

    def __init__(self, module_id: str):
        self.module_id = module_id
        self.status = ModuleStatus.STOPPED
        self.error_message: Optional[str] = None
        self._sync_timestamp: Optional[float] = None
        logger.info(f"Module initialized: {self.module_id}")

    async def start(self):
        """Starts the module asynchronously."""
        self.status = ModuleStatus.INITIALIZING
        logger.info(f"[{self.module_id}] Starting...")
        try:
            await self._on_start()
            self.status = ModuleStatus.RUNNING
        except Exception as e:
            self.status = ModuleStatus.ERROR
            self.error_message = str(e)
            logger.error(f"[{self.module_id}] Start-up error: {e}")

    async def stop(self):
        """Stops the module."""
        logger.info(f"[{self.module_id}] Stopping...")
        await self._on_stop()
        self.status = ModuleStatus.STOPPED

    async def _on_start(self):
        """Should be overridden by subclasses."""
        pass

    async def _on_stop(self):
        """Should be overridden by subclasses."""
        pass

    def sync_time(self, master_timestamp: Optional[float] = None) -> float:
        """
        SWISS WATCH ANALOGY: Time synchronization for all modules.
        Ensures all modules operate with the same time reference.
        """
        if master_timestamp is None:
            master_timestamp = time.time()
        self._sync_timestamp = master_timestamp
        return master_timestamp

    def get_status_report(self) -> Dict[str, Any]:
        """Reports the status of the module."""
        return {
            "module_id": self.module_id,
            "status": self.status.value,
            "error": self.error_message,
            "sync_time": self._sync_timestamp,
        }
