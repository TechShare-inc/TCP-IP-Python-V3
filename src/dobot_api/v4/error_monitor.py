"""V4 RobotErrorMonitor -- HTTP-based error backend on port 22000."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.error_monitor import RobotErrorMonitor  # noqa: E402, F401

__all__ = ["RobotErrorMonitor"]
