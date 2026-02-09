# Dobot TCP-IP Python API (V3 Modernized)

Modern Python API for Dobot NOVA-series robots with a modular architecture and V3 protocol semantics.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-4.0.0-green.svg)](https://github.com/TechShare-inc/TCP-IP-Python-V3)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Note: This repository is based on `Dobot-Arm/TCP-IP-Python-V3` and maintained for TechShare usage with a modular API surface.

## Features

- Modular package design: `base`, `dashboard`, `move`, `feedback`, `error_monitor`, `i18n_manager`
- Separate TCP connections: `DobotApiDashboard` (port 29999) for control, `DobotApiMove` (port 30003) for movement
- V3 protocol behavior retained for existing supported commands
- Local alarm i18n support (`en`, `zh_CN`) through YAML locale files
- Optional HTTP alarm monitor (`RobotErrorMonitor`)
- Structured logging via `loguru`

---

## Quick Start

### Installation

```bash
git clone https://github.com/TechShare-inc/TCP-IP-Python-V3.git
cd TCP-IP-Python-V3
pip install -e .
```

### Basic Example

```python
from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

ip = "192.168.5.1"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 30003)
feed = DobotApiFeedBack(ip, 30004)

# Enable and configure
print(dashboard.EnableRobot())
print(dashboard.ClearError())
print(dashboard.SpeedFactor(50))

# Motion command (on move port)
print(move.MovJ(200, 0, 200, 0, 0, 0))

# Feedback
data = feed.feedBackData()
if data is not None:
    print(data["enable_status"][0])

# Cleanup
dashboard.DisableRobot()
dashboard.close()
move.close()
feed.close()
```

---

## Core Components

### 1. `DobotApiDashboard`

Main control entry for dashboard commands (connects to port 29999).

```python
from dobot_api import DobotApiDashboard

dashboard = DobotApiDashboard("192.168.5.1", 29999)

# Robot control
dashboard.EnableRobot()
dashboard.DisableRobot()
dashboard.ClearError()
dashboard.ResetRobot()

# I/O
dashboard.DO(index, status)
dashboard.DI(index)
dashboard.AO(index, value)

# Speed/acceleration settings
dashboard.SpeedFactor(50)
dashboard.SpeedJ(50)
dashboard.SpeedL(50)
dashboard.AccJ(50)
dashboard.AccL(50)
```

### 2. `DobotApiMove`

Movement commands (connects to port 30003).

```python
from dobot_api import DobotApiMove

move = DobotApiMove("192.168.5.1", 30003)

# Motion
move.MovJ(x, y, z, rx, ry, rz)
move.MovL(x, y, z, rx, ry, rz)
move.Arc(x1, y1, z1, rx1, ry1, rz1, x2, y2, z2, rx2, ry2, rz2)

# Relative motion
move.RelMovJUser(dx, dy, dz, drx, dry, drz, user)
move.RelMovLUser(dx, dy, dz, drx, dry, drz, user)

# Servo motion
move.ServoJ(j1, j2, j3, j4, j5, j6)
move.ServoP(x, y, z, a, b, c)
```

Notes:
- V4-style aliases are available for common names: `VelJ`, `VelL`, `Pause`, `Stop`.
- Command strings preserve V3 behavior for supported methods.

### 3. `DobotApiFeedBack`

Real-time robot state feedback via TCP.

```python
from dobot_api import DobotApiFeedBack

feed = DobotApiFeedBack("192.168.5.1", 30004)
data = feed.feedBackData()
if data is not None:
    print(data["q_actual"])          # Joint feedback
    print(data["robot_mode"])        # Robot mode
    print(data["digital_input_bits"]) # Digital inputs
```

Feedback packet size is 1440 bytes and parsed by `MyType`.

### 4. `RobotErrorMonitor`

Optional HTTP alarm polling interface (port `22000`) with localized output.

```python
from dobot_api import RobotErrorMonitor

monitor = RobotErrorMonitor("192.168.5.1")
info = monitor.get_error_info(language="en")
if info and info.get("errMsg"):
    for err in info["errMsg"]:
        print(err["id"], err["description"])
```

### 5. `AlarmI18n`

Local alarm translation manager.

```python
from dobot_api import AlarmI18n

i18n = AlarmI18n(default_language="en")
print(i18n.get_controller_alarm(16))

i18n.set_language("zh_CN")
print(i18n.format_alarm(16))
```

Supported languages:
- `en`
- `zh_CN`

---

## Import Paths

Primary package:

```python
from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack, RobotErrorMonitor, AlarmI18n
```

Alias package:

```python
from dobot_api_v3 import DobotApiDashboard, DobotApiMove, DobotApiFeedBack
```

---

## Breaking Changes (from legacy monolithic V3)

- Movement methods have been restored to `DobotApiMove` class (separate TCP port 30003).
- `DobotApiDashboard` now handles only dashboard/control commands (TCP port 29999).
- `alarmAlarmJsonFile` is removed from public exports.
- `dobot_api/api.py` is no longer the primary API entry.

See `MIGRATION.md` for migration mapping and examples.

---

## Project Structure

```text
TCP-IP-Python-V3/
  dobot_api/
    __init__.py
    base.py
    dashboard.py
    move.py
    feedback.py
    error_monitor.py
    i18n_manager.py
    locales/
      alarms.en.yml
      alarms.zh_CN.yml
    files/
      alarm_controller.json
      alarm_servo.json
  dobot_api_v3/
    __init__.py
    base.py
    dashboard.py
    move.py
    feedback.py
    error_monitor.py
    i18n_manager.py
  examples/
    basic_demo.py
    i18n_demo.py
    error_handling.py
    main.py
  tests/
  MIGRATION.md
  pyproject.toml
```

---

## Development

Run tests:

```bash
pytest -q
```

Install dev dependencies:

```bash
pip install -e .[dev]
```

---

## Compatibility Notes

- Robot/controller firmware support remains aligned to V3 series usage expectations.
- Network setup must be in the same subnet as the controller.
- Common control ports: `29999` (dashboard), `30003` (move), `30004` (feedback).

---

## License

MIT. See `LICENSE`.
