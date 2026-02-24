"""Backward-compatible re-export shim for DobotApiMove.

The canonical implementation now lives in
:mod:`dobot_api_v3.commands.move`.  This module re-exports
``DobotApiMove`` so that existing import paths continue to work::

    from dobot_api_v3.move import DobotApiMove  # still valid
"""

from __future__ import annotations

from .commands.move import DobotApiMove

__all__ = ["DobotApiMove"]
