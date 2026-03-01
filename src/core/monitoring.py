import time
import os
import json
import logging
from datetime import datetime

logger = logging.getLogger("ZerenAI.Core.Monitoring")


class Monitoring:
    """
    Sistem Sağlık İzleme (Heartbeat).
    Modüllerin hayatta olduğunu ve gecikmelerini takip eder.
    """

    def __init__(self, heartbeat_dir: str = "temp/heartbeats"):
        self.heartbeat_dir = heartbeat_dir
        if not os.path.exists(self.heartbeat_dir):
            os.makedirs(self.heartbeat_dir)

    def send_heartbeat(self, component_name: str, status: str = "ALIVE"):
        """Bileşen için nabız (heartbeat) sinyali gönderir."""
        file_path = os.path.join(self.heartbeat_dir, f"{component_name}.json")
        try:
            data = {
                "ts": time.time(),
                "time_human": datetime.now().isoformat(),
                "status": status,
                "pid": os.getpid(),
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.warning(f"Heartbeat gönderilemedi ({component_name}): {e}")

    def get_system_status(self) -> dict:
        """Checks the status of all components."""
        report = {}
        if not os.path.exists(self.heartbeat_dir):
            return report

        for file in os.listdir(self.heartbeat_dir):
            if file.endswith(".json"):
                comp_name = file.replace(".json", "")
                try:
                    with open(os.path.join(self.heartbeat_dir, file), "r") as f:
                        data = json.load(f)
                        latency = time.time() - data.get("ts", 0)
                        report[comp_name] = "OK" if latency < 60 else "DEAD"
                except Exception:
                    report[comp_name] = "UNKNOWN"
        return report
