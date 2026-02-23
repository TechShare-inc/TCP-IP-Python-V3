# Tutorial: Feedback and Error Monitoring

Use:

1. `examples/03_feedback.py` — read feedback frames via `DobotRobot`
2. `examples/04_error_handling.py` — check and clear alarms

`DobotRobot` provides two feedback methods:

| Method | Return type | Best for |
|---|---|---|
| `feedback_data()` | `FeedbackData` | IDE autocomplete, type safety |
| `raw_feedback_data()` | `np.ndarray` | Zero-copy numeric pipelines |

```python
with DobotRobot("192.168.5.1") as robot:
    data = robot.feedback_data()
    if data is not None:
        print(data.robot_mode)
        print(data.tool_vector_actual)
```

For error monitoring, use `robot.check_errors()` or `robot.clear_and_recover()`.
