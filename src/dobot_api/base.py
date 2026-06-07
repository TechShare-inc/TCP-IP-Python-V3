"""Shared DobotApi base -- union of V3+V4 port support with V4-quality features.

Provides a single ``DobotApi`` class that accepts all Dobot TCP ports
(29999, 30003, 30004, 30005, 30006) and includes V4's auto-reconnect,
graceful shutdown, and SO_RCVBUF tuning.  The underlying implementation
delegates to the V4 base after extending the port whitelist.
"""

from __future__ import annotations

from ._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.base import DobotApi as _V4DobotApi  # noqa: E402


class DobotApi(_V4DobotApi):
    """Shared TCP socket for all Dobot ports (29999, 30003-30006).

    Extends the V4 ``DobotApi`` base to also accept port 30003 (the V3
    motion port), so that both protocol families can share a single
    low-level transport class.  V4 features -- auto-reconnect in
    ``send_data``, ``__del__`` finaliser, ``SO_RCVBUF`` tuning, and
    graceful ``shutdown(SHUT_RDWR)`` -- are inherited unchanged.

    Typical usage is indirect (via ``DobotRobot`` or the feedback
    reader), but the class is public for advanced users who need raw
    socket access.
    """

    _ALLOWED_PORTS = {29999, 30003, 30004, 30005, 30006}


__all__ = ["DobotApi"]
