# Dobot TCP-IP Python API (V3 Modernized)

Modern Python API for Dobot NOVA-series robots with modular TCP clients and V3 protocol semantics.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](https://github.com/TechShare-inc/TCP-IP-Python-V3)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Modular package: `base`, `dashboard`, `move`, `feedback`, `error_monitor`, `i18n_manager`
- Separate TCP connections by responsibility:
  - `DobotApiDashboard` on port `29999`
  - `DobotApiMove` on port `30003`
  - `DobotApiFeedback` on port `30004`
- Localized alarm metadata (`en`, `zh_CN`) via YAML locale files
- Error monitoring helper based on dashboard `get_error_id()`
- Structured logging with `loguru`

## Installation

```bash
git clone https://github.com/TechShare-inc/TCP-IP-Python-V3.git
cd TCP-IP-Python-V3
pip install -e .
```

Optional dependencies:

```bash
pip install -e .[dev]
pip install -e .[docs]
```

## Quick Start

```python
from dobot_api_v3 import DobotApiDashboard, DobotApiMove, DobotApiFeedback

ip = "192.168.5.1"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 30003)
feedback = DobotApiFeedback(ip, 30004)

try:
    print(dashboard.clear_error())
    print(dashboard.enable_robot())
    print(dashboard.speed_factor(40))

    print(move.mov_j(200, 0, 200, 0, 0, 0))
    print(move.sync())

    feedback_data = feedback.feedback_data()
    if feedback_data is not None:
        print("enable_status:", feedback_data["enable_status"][0])

    print(dashboard.disable_robot())
finally:
    feedback.close()
    move.close()
    dashboard.close()
```

## Core Components

- `DobotApiDashboard`: robot lifecycle, status, I/O, kinematics, safety, and scripting commands.
- `DobotApiMove`: point-to-point, linear, relative, servo, jog, trajectory, and sync commands.
- `DobotApiFeedback`: reads and parses the 1440-byte realtime feedback packet.
- `RobotErrorMonitor`: error query/log/clear helper using dashboard connection.
- `AlarmI18n`: alarm localization helper with `en` and `zh_CN` support.

## Example Scripts

Numbered examples are in `examples/`:

1. `01_basic_connection.py`
2. `02_basic_motion.py`
3. `03_feedback.py`
4. `04_error_handling.py`
5. `05_io_and_modbus.py`
6. `06_i18n_alarms.py`

## Documentation Workflow

Project docs use a hybrid workflow:

1. Sphinx + MyST generate API markdown pages
2. Manually authored markdown covers Basics/Tutorial/Development docs
3. VitePress builds the final static site

Generate API markdown:

```bash
sphinx-build -b markdown docs/sphinx docs/_autogen
```

Run docs site locally:

```bash
cd docs
npm install
npm run docs:dev
```

## Development

Run tests:

```bash
python -m pytest
```

Type-check and lint with your configured tools (`mypy`, `ruff`) in your local workflow or CI pipeline.

## Compatibility Notes

- New code should use `snake_case` method names.
- PascalCase command aliases are kept only for backward compatibility and emit `DeprecationWarning`.
- Keep robot/controller firmware and network configuration aligned with Dobot V3 expectations.

## License

MIT. See `LICENSE`.
