# Feedback and Error Monitoring

<!-- Diátaxis type: Tutorial -->

In this tutorial, we will read real-time feedback from the robot's 1440-byte
binary packet and inspect the error monitoring workflow. By the end you will
know how to poll feedback fields and check/clear alarms.

## Prerequisites

- Completed the [Basic Motion](./basic-motion.md) tutorial.
- Robot is connected and powered on.

## Step 1 — Read a feedback frame

We connect to the robot and access the `feedback` property. The port-30004
connection is created lazily on first access:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    data = robot.feedback_data()
    if data is not None:
        print("Robot mode:", data.robot_mode)
        print("TCP pose:", data.tool_vector_actual)
        print("Joint angles:", data.q_actual)
        print("Enabled:", data.enable_status == 1)
```

**Expected output:**

> ```
> Robot mode: 5
> TCP pose: (200.0, 0.0, 200.0, 0.0, 0.0, 0.0)
> Joint angles: (-11.53, 4.64, 87.16, -2.84, -77.71, 0.01)
> Enabled: True
> ```
>
> Exact values vary with the robot's current state.

## Step 2 — Choose the right feedback API

The library offers two feedback methods — pick the one that fits your use case:

| Method | Return type | Best for |
|---|---|---|
| `feedback_data()` | `FeedbackData` (dataclass) | Application code — IDE autocomplete, type safety |
| `raw_feedback_data()` | `np.ndarray` (structured array) | Numeric pipelines, zero-copy operations |

For NumPy-level access:

```python
    raw = robot.raw_feedback_data()
    if raw is not None:
        angles = raw[0]["q_actual"]         # np.ndarray shape (6,)
        mode = int(raw[0]["robot_mode"])     # np.uint64 → int
```

See [Feedback Fields](../reference/feedback-fields.md) for the complete field
reference.

## Step 3 — Poll feedback in a loop

For time-critical applications, we can read feedback at a fixed cycle time
(e.g., 8 ms):

```python
import time

with DobotRobot("192.168.5.1") as robot:
    feedback = robot.feedback
    for i in range(100):
        data = feedback.feedback_data()
        if data is not None:
            print(f"[{i}] mode={data.robot_mode}")
        time.sleep(0.008)
```

**Expected output:**

> ```
> [0] mode=5
> [1] mode=5
> ...
> [99] mode=5
> ```

## Step 4 — Check and clear errors

We use `check_errors()` and `clear_and_recover()` for alarm management:

```python
with DobotRobot("192.168.5.1", language="en") as robot:
    has_errors = robot.check_errors(language="en")
    if has_errors:
        error_info = robot.errors.get_error_info(language="en")
        print("Errors:", error_info)

        is_cleared = robot.clear_and_recover(language="en")
        print("Cleared:", is_cleared)
    else:
        print("No errors found.")
```

**Expected output (no errors):**

> ```
> No errors found.
> ```

## Next steps

- [I/O and Modbus](./io-and-modbus.md) — control digital/analog I/O and
  Modbus registers.
- [Alarm I18n](./i18n.md) — format alarm messages in multiple languages.
