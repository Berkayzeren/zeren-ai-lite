import asyncio
import logging
from typing import Dict, Any, List, Callable
from collections import defaultdict

logger = logging.getLogger("ZerenAI.Core.EventBus")


class EventBus:
    """
    Lite Etkinlik Veriyolu (Event Bus).
    Modüller arası asenkron iletişimi ve 'Loose Coupling' mimarisini sağlar.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._queue: asyncio.Queue = asyncio.Queue()

    def subscribe(self, event_type: str, callback: Callable):
        """Bir etkinlik tipine abone olur."""
        self._subscribers[event_type].append(callback)
        logger.info(f"Yeni abone: {event_type} -> {callback.__name__}")

    async def publish(self, event_type: str, data: Any):
        """Bir etkinlik yayınlar (kuyruğa ekler)."""
        await self._queue.put((event_type, data))

    async def start_listening(self):
        """Kuyruğu dinlemeye başlar ve aboneleri tetikler."""
        logger.info("EventBus dinlemeye başladı...")
        while True:
            event_type, data = await self._queue.get()
            if event_type in self._subscribers:
                tasks = []
                for callback in self._subscribers[event_type]:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(data))
                    else:
                        callback(data)

                if tasks:
                    await asyncio.gather(*tasks)

            self._queue.task_done()
