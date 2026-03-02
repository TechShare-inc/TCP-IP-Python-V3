# Feedback Fields

## Overview

The Dobot controller streams a 1440-byte binary feedback packet on ports 30004, 30005, and 30006. There are two ways to access this data:

| API | Return type | Best for |
|---|---|---|
| `feedback_data()` | `FeedbackData` (dataclass) | Application code — IDE autocomplete, type safety |
| `raw_feedback_data()` | `np.ndarray` (structured array) | Numeric pipelines, zero-copy operations |

---

## `FeedbackData` — typed access (recommended)

`FeedbackData` is an immutable `@dataclass(frozen=True, slots=True)`. All scalar fields are plain Python `int` or `float`; multi-element fields are `tuple[float, ...]` or `tuple[int, ...]`.

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    data = robot.feedback_data()
    if data is not None:
        print(data.robot_mode)             # int
        print(data.tool_vector_actual)     # tuple[float, ...] — 6 values
        print(data.enable_status)          # int
        print(data.q_actual)              # tuple[float, ...] — 6 joints
```

### Field reference

#### Header
| Field | Python type | Description |
|---|---|---|
| `len` | `int` | Total packet length in bytes |

#### I/O bitmasks
| Field | Python type | Description |
|---|---|---|
| `digital_input_bits` | `int` | Digital input bitmask |
| `digital_output_bits` | `int` | Digital output bitmask |

#### Mode and timing
| Field | Python type | Description |
|---|---|---|
| `robot_mode` | `int` | Current robot mode code |
| `time_stamp` | `int` | Controller timestamp |
| `time_stamp_reserve_bit` | `int` | Reserved timestamp bits |
| `test_value` | `int` | Internal test value |
| `test_value_keep_bit` | `float` | Internal test keep bit |

#### Dynamics — scalars
| Field | Python type | Description |
|---|---|---|
| `speed_scaling` | `float` | Global speed scaling factor (0–1) |
| `linear_momentum_norm` | `float` | Linear momentum magnitude |
| `v_main` | `float` | Main voltage (V) |
| `v_robot` | `float` | Robot voltage (V) |
| `i_robot` | `float` | Robot current (A) |
| `i_robot_keep_bit1` | `float` | Reserved current field 1 |
| `i_robot_keep_bit2` | `float` | Reserved current field 2 |

#### Tool and elbow vectors (3-element tuples)
| Field | Python type | Description |
|---|---|---|
| `tool_accelerometer_values` | `tuple[float, ...]` | Tool accelerometer XYZ |
| `elbow_position` | `tuple[float, ...]` | Elbow Cartesian position XYZ |
| `elbow_velocity` | `tuple[float, ...]` | Elbow Cartesian velocity XYZ |

#### Joint target state (6-element tuples)
| Field | Python type | Description |
|---|---|---|
| `q_target` | `tuple[float, ...]` | Target joint angles (rad) |
| `qd_target` | `tuple[float, ...]` | Target joint velocities (rad/s) |
| `qdd_target` | `tuple[float, ...]` | Target joint accelerations (rad/s²) |
| `i_target` | `tuple[float, ...]` | Target joint currents |
| `m_target` | `tuple[float, ...]` | Target joint torques (N·m) |

#### Joint actual state (6-element tuples)
| Field | Python type | Description |
|---|---|---|
| `q_actual` | `tuple[float, ...]` | Actual joint angles (rad) |
| `qd_actual` | `tuple[float, ...]` | Actual joint velocities (rad/s) |
| `i_actual` | `tuple[float, ...]` | Actual joint currents |

#### TCP force, pose, speed (6-element tuples)
| Field | Python type | Description |
|---|---|---|
| `actual_tcp_force` | `tuple[float, ...]` | Actual TCP force/torque |
| `tool_vector_actual` | `tuple[float, ...]` | Actual TCP pose [x, y, z, rx, ry, rz] |
| `tcp_speed_actual` | `tuple[float, ...]` | Actual TCP speed vector |
| `tcp_force` | `tuple[float, ...]` | TCP force sensor reading |
| `tool_vector_target` | `tuple[float, ...]` | Target TCP pose |
| `tcp_speed_target` | `tuple[float, ...]` | Target TCP speed vector |

#### Thermal and mode per joint (6-element tuples)
| Field | Python type | Description |
|---|---|---|
| `motor_temperatures` | `tuple[float, ...]` | Motor temperatures (°C) |
| `joint_modes` | `tuple[float, ...]` | Joint mode codes |
| `v_actual` | `tuple[float, ...]` | Actual joint voltages |

#### Hand and coordinate flags
| Field | Python type | Description |
|---|---|---|
| `hand_type` | `tuple[int, ...]` | Hand type flags (4 bytes) |
| `user` | `int` | Active user coordinate index |
| `tool` | `int` | Active tool coordinate index |
| `run_queued_cmd` | `int` | Queued command running flag |
| `pause_cmd_flag` | `int` | Pause command flag |

#### Ratio flags
| Field | Python type | Description |
|---|---|---|
| `velocity_ratio` | `int` | Joint velocity ratio (%) |
| `acceleration_ratio` | `int` | Joint acceleration ratio (%) |
| `jerk_ratio` | `int` | Joint jerk ratio (%) |
| `xyz_velocity_ratio` | `int` | Cartesian velocity ratio (%) |
| `r_velocity_ratio` | `int` | Rotational velocity ratio (%) |
| `xyz_acceleration_ratio` | `int` | Cartesian acceleration ratio (%) |
| `r_acceleration_ratio` | `int` | Rotational acceleration ratio (%) |
| `xyz_jerk_ratio` | `int` | Cartesian jerk ratio (%) |
| `r_jerk_ratio` | `int` | Rotational jerk ratio (%) |

#### Status flags
| Field | Python type | Description |
|---|---|---|
| `brake_status` | `int` | Brake status bitmask |
| `enable_status` | `int` | Robot enable status (1 = enabled) |
| `drag_status` | `int` | Drag mode status |
| `running_status` | `int` | Motion running flag |
| `error_status` | `int` | Error flag (non-zero = fault) |
| `jog_status` | `int` | Jog mode status |
| `robot_type` | `int` | Robot model type code |
| `drag_button_signal` | `int` | Physical drag button signal |
| `enable_button_signal` | `int` | Physical enable button signal |
| `record_button_signal` | `int` | Physical record button signal |
| `reappear_button_signal` | `int` | Physical reappear button signal |
| `jaw_button_signal` | `int` | Jaw button signal |
| `six_force_online` | `int` | Six-axis force sensor online flag |
| `reserve2` | `tuple[int, ...]` | Reserved (82 bytes) |

#### Torques, payload, coordinate frames
| Field | Python type | Description |
|---|---|---|
| `m_actual` | `tuple[float, ...]` | Actual joint torques (N·m) |
| `load` | `float` | Payload mass (kg) |
| `center_x` | `float` | Payload CoM X offset (mm) |
| `center_y` | `float` | Payload CoM Y offset (mm) |
| `center_z` | `float` | Payload CoM Z offset (mm) |
| `user_coords` | `tuple[float, ...]` | Active user frame [x, y, z, rx, ry, rz] |
| `tool_coords` | `tuple[float, ...]` | Active tool frame [x, y, z, rx, ry, rz] |
| `trace_index` | `float` | Current trace index |

#### Six-force and quaternions
| Field | Python type | Description |
|---|---|---|
| `six_force_value` | `tuple[float, ...]` | Force sensor readings (6 values) |
| `target_quaternion` | `tuple[float, ...]` | Target TCP quaternion [w, x, y, z] |
| `actual_quaternion` | `tuple[float, ...]` | Actual TCP quaternion [w, x, y, z] |
| `reserve3` | `tuple[int, ...]` | Reserved (24 bytes) |

---

## `FeedbackDtype` — raw NumPy access

`FeedbackDtype` is the NumPy structured dtype for the 1440-byte packet.  It is
defined in `dobot_api_v3.dtypes` and re-exported from `dobot_api_v3.base` for
backward compatibility.  Use it with `raw_feedback_data()` when you need
zero-copy array operations.

```python
raw = robot.raw_feedback_data()
if raw is not None:
    # direct NumPy indexing
    angles = raw[0]["q_actual"]        # np.ndarray shape (6,)
    mode   = int(raw[0]["robot_mode"]) # np.uint64 → int
```

### Building from bytes directly

```python
import numpy as np
from dobot_api_v3 import FeedbackDtype, FeedbackData

arr = np.frombuffer(buf, dtype=FeedbackDtype)   # decode
data = FeedbackData.from_numpy(arr)              # convert to typed snapshot
```

---

## Protocol field name mapping

Use `PROTOCOL_FIELD_MAP` when you need the original Dobot protocol documentation names:

| `FeedbackData` / `FeedbackDtype` field | Protocol documentation name |
|---|---|
| `actual_tcp_force` | `actual_TCP_force` |
| `tcp_speed_actual` | `TCP_speed_actual` |
| `tcp_force` | `TCP_force` |
| `tool_vector_target` | `Tool_vector_target` |
| `tcp_speed_target` | `TCP_speed_target` |
| `user_coords` | `user[6]` |
| `tool_coords` | `tool[6]` |
