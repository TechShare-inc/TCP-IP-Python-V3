"""V3 DobotApiDashboard -- lifecycle, I/O, config, and query commands on port 29999."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v3.commands.dashboard import DobotApiDashboard  # noqa: E402, F401

__all__ = ["DobotApiDashboard"]
