# Dobot API v3 Documentation

Use the sidebar to navigate The Basics, Tutorial, and Reference sections.

- The Basics: install, architecture, quick start
- Tutorial: step-by-step workflows from `examples/`
- Reference: generated API docs, response types, feedback fields, and
  compatibility notes
- Changelog: project release notes
- Dev Guide: contributor and testing notes

## Getting started

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()
```

