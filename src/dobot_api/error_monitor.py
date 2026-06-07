"""Protocol-aware robot error monitor."""

from __future__ import annotations

from typing import Literal


class RobotErrorMonitor:
    """Facade over V3 TCP and V4 HTTP error monitors."""

    def __init__(self, dashboard_or_ip, *, protocol: Literal["v3", "v4"]) -> None:
        self.protocol = protocol
        self._dashboard = None
        if protocol == "v3":
            from .v3 import RobotErrorMonitor as V3RobotErrorMonitor

            self._backend = V3RobotErrorMonitor(dashboard_or_ip)
        elif protocol == "v4":
            from .v4 import RobotErrorMonitor as V4RobotErrorMonitor

            ip = dashboard_or_ip if isinstance(dashboard_or_ip, str) else dashboard_or_ip.ip
            if not isinstance(dashboard_or_ip, str):
                self._dashboard = dashboard_or_ip
            self._backend = V4RobotErrorMonitor(ip)
        else:
            raise ValueError(f"Unknown protocol: {protocol}")

    def check_errors(self, language: str = "en") -> bool:
        return bool(self._backend.check_errors(language=language))

    def clear_robot_error(self, language: str = "en") -> bool:
        if hasattr(self._backend, "clear_robot_error"):
            return bool(self._backend.clear_robot_error(language=language))
        if self._dashboard is None:
            raise NotImplementedError("V4 error clearing requires a dashboard connection")
        self._dashboard.clear_error()
        return self.check_errors(language=language)

    def get_error_info(self, language: str = "en"):
        return self._backend.get_error_info(language=language)

    def monitor_errors(self, interval: int = 5, language: str = "en") -> None:
        self._backend.monitor_errors(interval=interval, language=language)

    def save_error_log(self, filename: str | None = None, language: str = "en") -> None:
        self._backend.save_error_log(filename=filename, language=language)
