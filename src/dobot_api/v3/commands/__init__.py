"""V3 command adapters."""

from __future__ import annotations

from .dashboard import DobotApiDashboard  # noqa: F401
from .move import DobotApiMove  # noqa: F401

__all__ = ["DobotApiDashboard", "DobotApiMove"]
