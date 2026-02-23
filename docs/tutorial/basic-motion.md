# Tutorial: Basic Motion

Follow these examples in order:

1. `examples/01_basic_connection.py` — connect, startup, query status, shutdown
2. `examples/02_basic_motion.py` — joint and relative motion with `sync()`

Both examples use the `DobotRobot` unified API:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()
```

`startup()` runs the full lifecycle sequence (clear errors, power on, enable,
set speed). All motion methods return typed `AckResponse` objects.
