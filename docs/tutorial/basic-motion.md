# Basic Motion

<!-- Diátaxis type: Tutorial -->

In this tutorial, we will connect to a Dobot robot, run the startup sequence,
execute basic joint motions, and shut down cleanly. By the end you will
understand the `DobotRobot` lifecycle and the `sync()` pattern for queued
motion.

## Prerequisites

- The `dobot_api_v3` package is [installed](../getting-started/installation.md).
- Your PC can reach the robot controller at its IP address (default
  `192.168.5.1`).
- The robot is powered on and in a safe workspace.

## Step 1 — Connect and start up

We use the `DobotRobot` context manager to open TCP connections and run the
standard startup sequence (clear errors → power on → enable → set speed):

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)
    print("Robot is ready.")
```

**Expected output:**

> ```
> Robot is ready.
> ```

::: tip
`startup()` inspects current alarms and skips `clear_error` / `power_on` when
no errors are detected, reducing startup time on a clean controller.
:::

## Step 2 — Query robot status

Let's read the current robot mode, joint angles, and TCP pose:

```python
    print("Mode:", robot.robot_mode())    # IntResponse(value=5)
    print("Angle:", robot.get_angle())    # PoseResponse(x=..., ...)
    print("Pose:", robot.get_pose())      # PoseResponse(x=..., ...)
```

**Expected output:**

> ```
> Mode: IntResponse(value=5)
> Angle: PoseResponse(x=-11.53, y=4.64, z=87.16, rx=-2.84, ry=-77.71, rz=0.01)
> Pose: PoseResponse(x=200.00, y=0.00, z=200.00, rx=0.00, ry=0.00, rz=0.00)
> ```
>
> Exact values depend on the robot's current position.

## Step 3 — Execute a joint move

We issue a joint-interpolated move and call `sync()` to block until the motion
queue is empty:

```python
    robot.mov_j(200, 0, 200, 0, 0, 0)
    robot.sync()
```

`mov_j()` returns a typed `AckResponse` containing the queued command ID.
`sync()` blocks the calling thread until all queued motions have completed.

## Step 4 — Relative joint movement

For small offsets, we can use `rel_joint_mov_j` through the move subsystem:

```python
    robot.move.rel_joint_mov_j(15, 0, 0, 0, 0, 0)
    robot.sync()
```

## Step 5 — Shut down

Finally we disable the robot. Connections are closed automatically when the
`with` block exits:

```python
    robot.shutdown()
```

## Complete script

See [examples/01_basic_connection.py](https://github.com/user/repo/blob/main/examples/01_basic_connection.py)
and [examples/02_basic_motion.py](https://github.com/user/repo/blob/main/examples/02_basic_motion.py)
for the full runnable scripts.

## Next steps

- [Feedback and Monitoring](./feedback-monitoring.md) — read real-time robot
  state.
- [Command Patterns](../reference/command-patterns.md) — understand optional
  dynamic parameters (`*dyn_params`).
