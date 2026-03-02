"""Backward-compatible re-export shim for DobotApiDashboard.

The canonical implementation now lives in
:mod:`dobot_api_v3.commands.dashboard`.  This module re-exports
``DobotApiDashboard`` so that existing import paths continue to work::

    from dobot_api_v3.dashboard import DobotApiDashboard  # still valid
"""

from __future__ import annotations

from .commands.dashboard import DobotApiDashboard

__all__ = ["DobotApiDashboard"]
