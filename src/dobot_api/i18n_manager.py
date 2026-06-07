"""Alarm i18n export."""

from __future__ import annotations

from ._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.i18n_manager import AlarmI18n  # noqa: E402

__all__ = ["AlarmI18n"]
