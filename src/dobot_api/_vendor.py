"""Helpers for importing protocol implementations from checked-in submodules."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_vendor_paths() -> None:
    """Put V3/V4 submodule source roots at the front of ``sys.path``."""
    root = Path(__file__).resolve().parents[2]
    vendor_roots = (
        root / "vendor" / "TCP-IP-Python-V3" / "src",
        root / "vendor" / "TCP-IP-Python-V4",
    )
    for vendor_root in reversed(vendor_roots):
        path = str(vendor_root)
        if vendor_root.exists() and path not in sys.path:
            sys.path.insert(0, path)
