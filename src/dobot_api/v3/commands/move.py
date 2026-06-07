"""V3 DobotApiMove -- motion, servo, jog, and trajectory commands on port 30003."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v3.commands.move import DobotApiMove  # noqa: E402, F401

__all__ = ["DobotApiMove"]
