"""V3-specific FeedbackDtype (binary feedback packet layout)."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v3.dtypes import FeedbackDtype  # noqa: E402

__all__ = ["FeedbackDtype"]
