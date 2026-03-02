# Command Patterns

<!-- Diátaxis type: Reference -->

Use this page as a quick guide for composing dashboard/move command arguments.

## Pattern 1: Positional Required Args

Use plain positional arguments for required protocol parameters.

```python
robot.mov_j(200, 0, 200, 0, 0, 0)
robot.speed_factor(40)
```

## Pattern 2: Optional Dynamic Parameters (`*dyn_params`)

Many motion/dashboard methods accept extra protocol arguments through
`*dyn_params`.

Typical forms:

- string fragments: `"SpeedJ=40"`, `"AccJ=40"`, `"User=0"`
- tuple payloads for parallel I/O: `(0, 50, 1, 1)`
- integer/float values where the protocol accepts scalar trailing args

Examples:

```python
robot.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40", "User=0")
robot.move.mov_l_io(250, 0, 180, 0, 0, 0, (0, 50, 1, 1))
```

## Pattern 3: Tool/User Relative Moves

For tool-relative helpers using `ToolDynParam`, pass optional tuples in the
form `(speed, acc, index)`.

```python
robot.move.rel_mov_j_tool(10, 0, 0, 0, 0, 0, 0, (40, 40, 0))
robot.move.rel_mov_l_tool(0, 0, -10, 0, 0, 0, 0, (30, 30, 0))
```

## Pattern 4: Lifecycle with `DobotRobot` (Recommended)

The `DobotRobot` class handles the standard startup/shutdown sequence:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)          # clear_error → power_on → enable → speed_factor
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()                 # disable_robot
```

`startup()` inspects current alarms and skips `clear_error`/`power_on` when
no errors are detected, reducing startup time on a clean controller.

## Pattern 5: Manual Lifecycle (Advanced)

If you need fine-grained control, use subsystem classes directly:

```python
from dobot_api_v3.commands import DobotApiDashboard, DobotApiMove

dashboard = DobotApiDashboard("192.168.5.1", 29999)
move = DobotApiMove("192.168.5.1", 30003)
try:
    dashboard.clear_error()
    dashboard.enable_robot()
    dashboard.speed_factor(40)
    move.mov_j(200, 0, 200, 0, 0, 0)
    move.sync()
    dashboard.disable_robot()
finally:
    move.close()
    dashboard.close()
```

## Pattern 6: Typed Responses

`DobotRobot` methods return typed frozen dataclasses:

```python
resp = robot.robot_mode()       # IntResponse
print(resp.value)               # e.g. 5

pose = robot.get_pose()         # PoseResponse
print(pose.x, pose.y, pose.z)

ack = robot.mov_j(200, 0, 200, 0, 0, 0)   # AckResponse
print(ack.command_id)
```

For raw string responses, use the subsystem objects directly
(`robot.dashboard`, `robot.move`).

## Pattern 7: Feedback + Error Monitoring

Use the unified `DobotRobot` for feedback and error access:

```python
with DobotRobot("192.168.5.1", language="en") as robot:
    data = robot.feedback_data()       # FeedbackData (typed)
    raw  = robot.raw_feedback_data()   # np.ndarray (zero-copy)
    has_errors = robot.check_errors()
```

Or use separate connections for advanced scenarios:

```python
from dobot_api_v3.commands import DobotApiDashboard, DobotApiMove
from dobot_api_v3 import DobotApiFeedback, RobotErrorMonitor

dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 30003)
feedback = DobotApiFeedback(ip, 30004)
monitor = RobotErrorMonitor(dashboard, language="en")
```

## Tips

- Prefer the `DobotRobot` wrapper for new code.
- Use `snake_case` API names exclusively — PascalCase aliases have been removed.
- Always close sockets in `finally` blocks or use `with` statements.
- Subsystem classes live in `dobot_api_v3.commands` (not the package root).

