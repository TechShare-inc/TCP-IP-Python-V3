# Quick Start

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
