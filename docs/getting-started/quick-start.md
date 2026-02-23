# Quick Start

## Using `DobotRobot` (recommended)

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)

    print(robot.robot_mode())   # IntResponse(value=5)
    print(robot.get_pose())     # PoseResponse(x=..., y=..., ...)

    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()
```

`DobotRobot` manages all TCP connections and returns typed response
dataclasses (`AckResponse`, `IntResponse`, `PoseResponse`, `ErrorIdResponse`).

## Using individual subsystems

For advanced use cases you can still instantiate subsystem classes directly:

```python
from dobot_api_v3 import DobotApiDashboard, DobotApiMove

ip = "192.168.5.1"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 30003)

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

See the full scripts in the `examples/` directory for complete workflows.

