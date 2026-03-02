"""Utility helpers for Dobot API."""

from __future__ import annotations

from typing import Union

# ---------------------------------------------------------------------------
# Variadic parameter type aliases used by move/dashboard command methods.
# ---------------------------------------------------------------------------

# Pattern A — Generic dynamic parameters converted via str().
# Callers may pass individual ints, floats, strings, or tuples/lists that
# will be serialised as-is into the TCP command string.
DynParam = Union[int, float, str, tuple]  # type: ignore[type-arg]

# Pattern B — Structured (speed, acc, coord_index) tuples expected by
# RelMovJTool and RelMovLTool when optional parameters are provided.
ToolDynParam = tuple[int, int, int]

# ---------------------------------------------------------------------------
# Return type aliases
# ---------------------------------------------------------------------------

# Six-degree-of-freedom pose or joint-angle vector returned by query commands
# such as ``get_pose``, ``get_angle``, ``positive_solution``, etc.
Pose = tuple[float, float, float, float, float, float]
Joints = tuple[float, float, float, float, float, float]
