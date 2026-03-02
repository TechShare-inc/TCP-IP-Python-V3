# Dobot TCP-IP Python API (V3 Modernized)

Modern Python API for Dobot NOVA-series robots with modular TCP clients and V3 protocol semantics.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-3.0.0--alpha.2-green.svg)](https://github.com/TechShare-inc/TCP-IP-Python-V3)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- **`DobotRobot` unified entry point** — manages all TCP connections behind
  a single context-manager interface with `startup()`/`shutdown()` lifecycle.
- Modular package organized by responsibility:
  - `commands/dashboard` — `DobotApiDashboard` (port `29999`) composed from
    system, I/O, config, and query mixins
  - `commands/move` — `DobotApiMove` (port `30003`) composed from basic motion,
    relative motion, servo/jog, and trajectory mixins
  - `feedback` — `DobotApiFeedback` (ports `30004`–`30006`)
  - `error_monitor` — `RobotErrorMonitor`
  - `i18n_manager` — `AlarmI18n` with `en` and `zh_CN` locale files
- **Typed responses** — `AckResponse`, `IntResponse`, `PoseResponse`,
  `ErrorIdResponse` frozen dataclasses instead of raw strings
- **`FeedbackData` dataclass** — immutable typed snapshot of the 1440-byte
  feedback packet with full IDE autocompletion
- Structured logging with `loguru`

## Installation

```powershell
git clone https://github.com/TechShare-inc/TCP-IP-Python-V3.git
cd TCP-IP-Python-V3
uv venv
uv pip install -e .
```

Development dependencies:

```powershell
uv pip install -e .[dev]
```

> **Note:** Always use `uv` for environment and package management.

## Quick Start

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)

    print(robot.robot_mode())   # IntResponse(value=5)
    print(robot.get_pose())     # PoseResponse(x=..., y=..., ...)

    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()

    data = robot.feedback_data()
    if data is not None:
        print("enable_status:", data.enable_status)

    robot.shutdown()
```

For advanced use cases, subsystem classes are accessible directly:

```python
from dobot_api_v3.commands import DobotApiDashboard, DobotApiMove
```

## Core Components

| Class | Module | Purpose |
|---|---|---|
| `DobotRobot` | `robot` | Unified high-level entry point (recommended) |
| `DobotApiDashboard` | `commands.dashboard` | Lifecycle, status, I/O, config, and query commands |
| `DobotApiMove` | `commands.move` | Point-to-point, linear, relative, servo, jog, trajectory |
| `DobotApiFeedback` | `feedback` | 1440-byte realtime feedback packet reader |
| `RobotErrorMonitor` | `error_monitor` | Error query/log/clear helper |
| `AlarmI18n` | `i18n_manager` | Alarm localization (`en`, `zh_CN`) |

## Example Scripts

Numbered examples are in `examples/`:

1. `01_basic_connection.py` — connect, startup, query status, shutdown
2. `02_basic_motion.py` — joint and relative motion with `sync()`
3. `03_feedback.py` — read feedback frames via `DobotRobot`
4. `04_error_handling.py` — check and clear alarms
5. `05_io_and_modbus.py` — digital I/O and Modbus operations
6. `06_i18n_alarms.py` — alarm localization
7. `07_drag_mode.py` — drag (teach) mode

## Development

```powershell
uv run ruff check .
uv run ruff format .
uv run mypy dobot_api_v3
uv run pytest
```

See `docs/` for full documentation including architecture, tutorials, and
API reference.

## Compatibility Notes

- The API is exclusively `snake_case` — all PascalCase aliases have been removed.
- `DobotApiDashboard` and `DobotApiMove` have moved from the package root to
  the `commands` sub-package.
- `FeedbackDtype` and `FeedbackData` are now defined in `dtypes.py`
  (re-exported from `base.py` for backward compatibility).
- For new code, prefer `DobotRobot` over direct subsystem instantiation.

## License

MIT. See `LICENSE`.
