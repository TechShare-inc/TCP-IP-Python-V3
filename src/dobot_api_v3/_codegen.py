"""Code generator — writes the AUTO-GENERATED section of robot.py.

Run as a module to regenerate the forwarding methods in robot.py::

    uv run python -m dobot_api_v3._codegen

The script rewrites the block between the markers::

    # --- BEGIN AUTO-GENERATED ---
    # --- END AUTO-GENERATED ---

inside ``dobot_api_v3/robot.py``.  Everything outside those markers is left
untouched.

No changes are written when the generated content is already up-to-date
(idempotent).
"""

from __future__ import annotations

import inspect
import pathlib
import re
from typing import Any

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

#: Methods inherited from DobotApi and _SerializationMixin that must NOT be
#: forwarded — they are either infrastructure or already defined on DobotRobot.
_EXCLUDE: frozenset[str] = frozenset(
    {
        "close",
        "reconnect",
        "send_data",
        "wait_reply",
        "send_recv_msg",
        "log",
        # _SerializationMixin internals (all private anyway, but be explicit)
        "_connect",
        "_recv_ack",
        "_recv_int",
        "_recv_pose",
        "_recv_error_ids",
        "_recv_int_list",
        "_recv_float_list",
        "_recv_str_list",
        "_fmt",
        "_build_cmd",
    }
)


def _call_args(sig: inspect.Signature) -> str:
    """Build the argument list string for the forwarding call.

    Given a signature ``(self, x: float, y: float, *dyn_params: DynParam) -> int``
    this returns ``"x, y, *dyn_params"`` — i.e. the part that goes inside the
    parentheses of the delegate call, without ``self``.
    """
    parts: list[str] = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            parts.append(f"*{name}")
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            parts.append(f"**{name}")
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            parts.append(f"{name}={name}")
        else:
            parts.append(name)
    return ", ".join(parts)


def _sig_str(method: Any) -> str:
    """Return the signature string with ``self`` included.

    Uses :func:`inspect.signature` directly.  When the source module uses
    ``from __future__ import annotations`` Python stores every annotation as
    a quoted string, so the raw ``str(sig)`` output looks like
    ``(self, speed: 'int') -> 'int'``.  This function strips those quotes so
    the generated code reads ``(self, speed: int) -> int``.
    """
    try:
        sig_str = str(inspect.signature(method))
    except (ValueError, TypeError):
        return "(*args: Any, **kwargs: Any) -> Any"
    # Strip quotes inserted by deferred annotation evaluation.
    sig_str = re.sub(r": '([^']+)'", r": \1", sig_str)
    sig_str = re.sub(r': "([^"]+)"', r": \1", sig_str)
    sig_str = re.sub(r"-> '([^']+)'", r"-> \1", sig_str)
    sig_str = re.sub(r'-> "([^"]+)"', r"-> \1", sig_str)
    return sig_str


def _collect_methods(cls: type, target_attr: str) -> list[str]:
    """Return sorted lines of forwarding stubs for *cls*.

    Args:
        cls: The class to introspect (``DobotApiDashboard`` or
            ``DobotApiMove``).
        target_attr: The ``DobotRobot`` attribute used to reach an instance
            of *cls* (``"dashboard"`` or ``"move"``).

    Returns:
        A list of code lines (already indented by 4 spaces), terminated by a
        blank line after each method.
    """
    lines: list[str] = []

    # Collect (name, method) in definition order across the MRO so that
    # methods from sub-classes override those from parent classes.
    seen: set[str] = set()
    ordered: list[tuple[str, Any]] = []
    for klass in reversed(cls.__mro__):
        for name, obj in vars(klass).items():
            if name in seen:
                continue
            seen.add(name)
            if callable(obj) and not isinstance(obj, (classmethod, staticmethod)):
                ordered.append((name, obj))

    # Sort alphabetically for stable output.
    for name, method in sorted(ordered, key=lambda t: t[0]):
        # Skip private, dunder, and excluded names.
        if name.startswith("_") or name in _EXCLUDE:
            continue

        sig = inspect.signature(method)
        sig_str = _sig_str(method)
        call = _call_args(sig)
        return_annotation = sig.return_annotation

        # Build a one-liner body or a void body (-> None methods).
        if (
            return_annotation is None
            or (
                isinstance(return_annotation, str)
                and return_annotation.strip() == "None"
            )
            or return_annotation is inspect.Parameter.empty
        ):
            body = f"self.{target_attr}.{name}({call})"
        else:
            body = f"return self.{target_attr}.{name}({call})"

        lines.append(f"    def {name}{sig_str}:")
        doc = inspect.getdoc(method)
        if doc:
            doc_lines = doc.splitlines()
            if len(doc_lines) == 1:
                lines.append(f'        """{doc_lines[0]}"""')
            else:
                lines.append(f'        """{doc_lines[0]}')
                for dline in doc_lines[1:]:
                    if dline:
                        lines.append(f"        {dline}")
                    else:
                        lines.append("")
                lines.append('        """')
        lines.append(f"        {body}")
        lines.append("")

    return lines


def generate() -> str:
    """Return the full text of the AUTO-GENERATED block.

    The block starts immediately after the ``# --- BEGIN AUTO-GENERATED ---``
    comment and ends just before ``# --- END AUTO-GENERATED ---``.
    """
    # Import here (not at module top) so the script fails fast with a clear
    # error if the package isn't installed rather than an ImportError on load.
    from .commands.dashboard import DobotApiDashboard  # noqa: PLC0415
    from .commands.move import DobotApiMove  # noqa: PLC0415

    parts: list[str] = []

    parts.append(
        "    # -- dashboard --------------------------------------------------------\n"
    )
    parts.extend(
        line + "\n" for line in _collect_methods(DobotApiDashboard, "dashboard")
    )

    parts.append(
        "    # -- move -------------------------------------------------------------\n"
    )
    parts.extend(line + "\n" for line in _collect_methods(DobotApiMove, "move"))

    return "".join(parts)


# ---------------------------------------------------------------------------
# Marker constants
# ---------------------------------------------------------------------------

_BEGIN = "    # --- BEGIN AUTO-GENERATED ---\n"
_END = "    # --- END AUTO-GENERATED ---\n"


def update_robot_py(robot_path: pathlib.Path | None = None) -> bool:
    """Rewrite the AUTO-GENERATED block in *robot_path*.

    Args:
        robot_path: Path to ``robot.py``.  Defaults to the ``robot.py``
            sibling of this file.

    Returns:
        ``True`` if the file was modified, ``False`` if it was already
        up-to-date.

    Raises:
        ValueError: If either marker is missing from the file.
    """
    if robot_path is None:
        robot_path = pathlib.Path(__file__).with_name("robot.py")

    original = robot_path.read_text(encoding="utf-8")

    begin_idx = original.find(_BEGIN)
    end_idx = original.find(_END)

    if begin_idx == -1 or end_idx == -1:
        raise ValueError(
            f"Could not find generation markers in {robot_path}.\n"
            f"Expected:\n  {_BEGIN.rstrip()}\n  {_END.rstrip()}"
        )

    new_content = generate()
    prefix = original[: begin_idx + len(_BEGIN)]
    suffix = original[end_idx:]
    updated = prefix + new_content + suffix

    if updated == original:
        return False

    robot_path.write_text(updated, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point: regenerate robot.py and report the result."""
    robot_path = pathlib.Path(__file__).with_name("robot.py")
    changed = update_robot_py(robot_path)
    if changed:
        print(f"Updated {robot_path}")
    else:
        print(f"No changes — {robot_path} is already up-to-date.")


if __name__ == "__main__":
    main()
