---
layout: home

hero:
  name: Dobot API v3
  text: Python SDK for Dobot Robots
  tagline: A modern, typed Python interface for controlling Dobot robots over TCP/IP.
  actions:
    - theme: brand
      text: Quick Start
      link: /getting-started/quick-start
    - theme: alt
      text: API Reference
      link: /reference/

features:
  - title: Unified Entry Point
    details: DobotRobot manages all TCP connections and returns typed response dataclasses — one object, full control.
  - title: Typed Responses
    details: AckResponse, IntResponse, PoseResponse, and ErrorIdResponse provide IDE autocomplete and type safety out of the box.
  - title: Feedback Streaming
    details: Read the 1440-byte binary feedback packet as a typed FeedbackData dataclass or as a zero-copy NumPy array.
  - title: Alarm I18n
    details: Built-in localized alarm messages in English and Chinese, enriched from YAML locale files.
---

## Getting Started

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
    robot.shutdown()
```

Explore the [Installation](./getting-started/installation.md) guide, work
through the [Tutorials](./tutorial/basic-motion.md), or jump straight to the
[API Reference](./reference/).

