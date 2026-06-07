"""Shared base export for the unified Dobot API."""

from __future__ import annotations

from ._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.base import DobotApi  # noqa: E402

__all__ = ["DobotApi"]
