# Architecture

## Connections

- Dashboard commands: port `29999`
- Motion commands: port `30003`
- Feedback stream: ports `30004`, `30005`, `30006`

## Recommended entry point

`DobotRobot` is the unified high-level interface that composes all subsystem
connections. It is the recommended entry point for new code:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()
```

`DobotRobot` manages dashboard and move sockets eagerly on construction.
Feedback connections on ports 30004/30005/30006 are created lazily on first
access via `robot.feedback`, `robot.feedback_30005`, and `robot.feedback_30006`.

The individual subsystem objects are still accessible as public attributes
(`robot.dashboard`, `robot.move`, `robot.feedback`, `robot.errors`) for
advanced use cases.

## Package layout

```
dobot_api_v3/
├── __init__.py           ← public re-exports
├── base.py               ← DobotApi TCP socket base class
├── dtypes.py             ← FeedbackDtype, FeedbackData, PROTOCOL_FIELD_MAP
├── responses.py          ← AckResponse, IntResponse, PoseResponse, …
├── robot.py              ← DobotRobot unified entry point
├── feedback.py           ← DobotApiFeedback (binary packet reader)
├── error_monitor.py      ← RobotErrorMonitor (alarm polling)
├── i18n_manager.py       ← AlarmI18n (localized alarm metadata)
├── _forward.py           ← @forward_to decorator for DobotRobot
├── utils.py              ← DynParam, ToolDynParam, Pose type aliases
├── commands/
│   ├── __init__.py       ← re-exports DobotApiDashboard, DobotApiMove
│   ├── dashboard.py      ← DobotApiDashboard (composed from mixins)
│   ├── move.py           ← DobotApiMove (composed from mixins)
│   ├── _serialization.py ← _SerializationMixin (shared parse/build helpers)
│   ├── _system_mixin.py  ← enable/disable, power, speed, script control
│   ├── _config_mixin.py  ← speed/acc/jerk, coordinate, payload, collision
│   ├── _io_mixin.py      ← digital/analog I/O, DO groups, Modbus
│   ├── _query_mixin.py   ← pose/angle/error queries, kinematics, safety
│   ├── _basic_motion_mixin.py    ← mov_j, mov_l, arc, circle3, jump, …
│   ├── _relative_motion_mixin.py ← rel_mov_j, rel_mov_l, rel_*_tool/user
│   ├── _servo_jog_mixin.py       ← servo_j, servo_js, servo_p, move_jog
│   └── _trajectory_mixin.py      ← start_trace, start_path, sync
└── locales/
    ├── alarms.en.yml
    └── alarms.zh_CN.yml
```

## Subsystem classes

| Class | Port | Module | Purpose |
|---|---|---|---|
| `DobotApiDashboard` | 29999 | `commands.dashboard` | Robot status and control commands |
| `DobotApiMove` | 30003 | `commands.move` | Queued / real-time motion commands |
| `DobotApiFeedback` | 30004+ | `feedback` | 1440-byte binary feedback packet reader |
| `RobotErrorMonitor` | — | `error_monitor` | Alarm polling and logging (wraps dashboard) |
| `AlarmI18n` | — | `i18n_manager` | Localized alarm metadata helper |

### Mixin composition

`DobotApiDashboard` and `DobotApiMove` are assembled via multiple inheritance
from focused command-category mixins:

```
DobotApiDashboard                   DobotApiMove
  ├── _SystemMixin                    ├── _BasicMotionMixin
  ├── _IOMixin                        ├── _RelativeMotionMixin
  ├── _ConfigMixin                    ├── _ServoJogMixin
  ├── _QueryMixin                     ├── _TrajectoryMixin
  └── DobotApi (TCP base)             └── DobotApi (TCP base)
```

All mixins inherit from `_SerializationMixin` which provides the shared
`_fmt`, `_build_cmd`, `_recv_ack`, and `_recv_int` helpers.

## Typed responses

`DobotRobot` methods return typed frozen dataclasses instead of raw strings:

| Response type | Returned by |
|---|---|
| `AckResponse` | Lifecycle and motion commands (`enable_robot`, `mov_j`, `sync`, …) |
| `IntResponse` | Status queries (`robot_mode`) |
| `PoseResponse` | Pose/angle queries (`get_pose`, `get_angle`) |
| `ErrorIdResponse` | Alarm queries (`get_error_id`) |

## Feedback data

| API | Return type | Best for |
|---|---|---|
| `feedback_data()` | `FeedbackData` (dataclass) | Application code — IDE autocomplete, type safety |
| `raw_feedback_data()` | `np.ndarray` (structured array) | Numeric pipelines, zero-copy operations |

`FeedbackDtype` and `FeedbackData` are defined in `dtypes.py` and re-exported
from `base.py` for backward compatibility.

