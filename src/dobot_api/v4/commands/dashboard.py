"""V4 DobotApiDashboard -- all commands on port 29999 (lifecycle, motion, force, I/O, etc.)."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.commands.dashboard import DobotApiDashboard  # noqa: E402, F401

__all__ = ["DobotApiDashboard"]
