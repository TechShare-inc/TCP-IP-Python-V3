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

## Subsystem classes

| Class | Port | Purpose |
|---|---|---|
| `DobotApiDashboard` | 29999 | Robot status and control commands |
| `DobotApiMove` | 30003 | Queued / real-time motion commands |
| `DobotApiFeedback` | 30004+ | 1440-byte binary feedback packet reader |
| `RobotErrorMonitor` | — | Alarm polling and logging (wraps dashboard) |
| `AlarmI18n` | — | Localized alarm metadata helper |

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

