# Tutorial: I/O and Modbus

Use `examples/05_io_and_modbus.py` to run basic I/O and Modbus calls.

Recommended sequence with `DobotRobot`:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot(ip) as robot:
    robot.startup(speed=40)
    # Access I/O through the dashboard subsystem
    robot.dashboard.do_execute(1, 1)    # set DO1 high
    robot.dashboard.di(1)               # read DI1
    # Modbus operations
    robot.dashboard.modbus_create(...)   # create slave
    robot.dashboard.get_hold_regs(...)   # read registers
    robot.shutdown()
```

The `DobotRobot.dashboard` attribute exposes the full `DobotApiDashboard` API
for I/O and Modbus commands not directly forwarded by `DobotRobot`.

I/O and Modbus commands are defined in the `_IOMixin` class
(`dobot_api_v3/commands/_io_mixin.py`).
