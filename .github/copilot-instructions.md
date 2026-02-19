# Dobot API – Naming Convention Rules for AI Agents

This document is the authoritative naming convention reference for the
`dobot_api_v3` package. AI coding agents **must** follow these rules for all
code generation, refactoring, and review tasks.

---

## 1. Module Names

| Rule                          | Convention   | Example                               |
| ----------------------------- | ------------ | ------------------------------------- |
| All module (`.py`) file names | `snake_case` | `error_monitor.py`, `i18n_manager.py` |

---

## 2. Class Names

| Rule                     | Convention                                  | Example                                                    |
| ------------------------ | ------------------------------------------- | ---------------------------------------------------------- |
| All class names          | `PascalCase`, one capital per word boundary | `DobotApiFeedback`, `RobotErrorMonitor`                    |
| **No mid-word capitals** | Treat compound words as single words        | `Feedback` **not** `FeedBack`; `Payload` **not** `PayLoad` |
| Acronyms ≤ 2 chars       | Keep uppercase                              | `DobotApi`, `MovJIO`                                       |
| Acronyms ≥ 3 chars       | Title-case in class names                   | `TcpSpeed` (not `TCPSpeed`)                                |

---

## 3. Method and Function Names

### 3a. Infrastructure / Internal Methods (non-protocol)

| Rule                                  | Convention                                                            | Example                                       |
| ------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| All public and private methods        | `snake_case`                                                          | `send_recv_msg`, `feedback_data`, `get_alarm` |
| Protected methods                     | `_snake_case` (single leading underscore)                             | `_build_cmd`, `_connect`                      |
| Avoid double-underscore name mangling | Only use `__name` when Python name mangling is intentionally required |                                               |

### 3b. Protocol Command Methods (Dobot TCP API)

These methods correspond directly to Dobot TCP protocol command names.

| Rule                                | Convention                                                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Primary method (implementation)** | `snake_case` — this is the canonical name to use in all new code                                                   |
| **Deprecated alias**                | Old PascalCase name preserved for backward compatibility only; emits `DeprecationWarning` via `warnings.warn(...)` |

Example:

```python
# PRIMARY — write new code against this
def enable_robot(self, load: float = 0.0, center_x: float = 0.0, ...) -> str: ...

# DEPRECATED ALIAS — do not use in new code
def EnableRobot(self, *args, **kwargs) -> str:
    import warnings
    warnings.warn("EnableRobot is deprecated, use enable_robot", DeprecationWarning, stacklevel=2)
    return self.enable_robot(*args, **kwargs)
```

**Mapping reference** (PascalCase protocol name → snake_case primary name):

| PascalCase (deprecated) | snake_case (primary)                      |
| ----------------------- | ----------------------------------------- |
| `EnableRobot`           | `enable_robot`                            |
| `DisableRobot`          | `disable_robot`                           |
| `ClearError`            | `clear_error`                             |
| `ResetRobot`            | `reset_robot`                             |
| `SpeedFactor`           | `speed_factor`                            |
| `User`                  | `set_user`                                |
| `Tool`                  | `set_tool`                                |
| `RobotMode`             | `robot_mode`                              |
| `PayLoad`               | `payload`                                 |
| `DO`                    | `do_output`                               |
| `DOExecute`             | `do_execute`                              |
| `ToolDO`                | `tool_do`                                 |
| `ToolDOExecute`         | `tool_do_execute`                         |
| `AO`                    | `ao`                                      |
| `AOExecute`             | `ao_execute`                              |
| `AccJ`                  | `acc_j`                                   |
| `AccL`                  | `acc_l`                                   |
| `SpeedJ`                | `speed_j`                                 |
| `SpeedL`                | `speed_l`                                 |
| `VelJ`                  | `vel_j`                                   |
| `VelL`                  | `vel_l`                                   |
| `Arch`                  | `arch`                                    |
| `CP`                    | `cp`                                      |
| `LimZ`                  | `lim_z`                                   |
| `SetArmOrientation`     | `set_arm_orientation`                     |
| `PowerOn`               | `power_on`                                |
| `RunScript`             | `run_script`                              |
| `StopScript`            | `stop_script`                             |
| `PauseScript`           | `pause_script`                            |
| `ContinueScript`        | `continue_script`                         |
| `GetHoldRegs`           | `get_hold_regs`                           |
| `SetHoldRegs`           | `set_hold_regs`                           |
| `GetErrorID`            | `get_error_id`                            |
| `SetPayload`            | `set_payload`                             |
| `PositiveSolution`      | `positive_solution`                       |
| `InverseSolution`       | `inverse_solution`                        |
| `SetCollisionLevel`     | `set_collision_level`                     |
| `GetAngle`              | `get_angle`                               |
| `GetPose`               | `get_pose`                                |
| `EmergencyStop`         | `emergency_stop`                          |
| `ModbusCreate`          | `modbus_create`                           |
| `ModbusClose`           | `modbus_close`                            |
| `SetSafeSkin`           | `set_safe_skin`                           |
| `SetObstacleAvoid`      | `set_obstacle_avoid`                      |
| `GetTraceStartPose`     | `get_trace_start_pose`                    |
| `GetPathStartPose`      | `get_path_start_pose`                     |
| `HandleTrajPoints`      | `handle_traj_points`                      |
| `GetSixForceData`       | `get_six_force_data`                      |
| `SetCollideDrag`        | `set_collide_drag`                        |
| `SetTerminalKeys`       | `set_terminal_keys`                       |
| `SetTerminal485`        | `set_terminal_485`                        |
| `GetTerminal485`        | `get_terminal_485`                        |
| `TCPSpeed`              | `tcp_speed`                               |
| `TCPSpeedEnd`           | `tcp_speed_end`                           |
| `GetInBits`             | `get_in_bits`                             |
| `GetInRegs`             | `get_in_regs`                             |
| `GetCoils`              | `get_coils`                               |
| `SetCoils`              | `set_coils`                               |
| `DI`                    | `di`                                      |
| `ToolDI`                | `tool_di`                                 |
| `DOGroup`               | `do_group`                                |
| `BrakeControl`          | `brake_control`                           |
| `StartDrag`             | `start_drag`                              |
| `StopDrag`              | `stop_drag`                               |
| `LoadSwitch`            | `load_switch`                             |
| `Continue`              | `resume` (`continue` is a Python keyword) |
| `MovJ`                  | `mov_j`                                   |
| `MovL`                  | `mov_l`                                   |
| `JointMovJ`             | `joint_mov_j`                             |
| `Jump`                  | `jump`                                    |
| `RelMovJ`               | `rel_mov_j`                               |
| `RelMovL`               | `rel_mov_l`                               |
| `MovLIO`                | `mov_l_io`                                |
| `MovJIO`                | `mov_j_io`                                |
| `Arc`                   | `arc`                                     |
| `Circle3`               | `circle3`                                 |
| `ServoJ`                | `servo_j`                                 |
| `ServoJS`               | `servo_js`                                |
| `ServoP`                | `servo_p`                                 |
| `MoveJog`               | `move_jog`                                |
| `StartTrace`            | `start_trace`                             |
| `StartPath`             | `start_path`                              |
| `StartFCTrace`          | `start_fc_trace`                          |
| `Sync`                  | `sync`                                    |
| `RelMovJTool`           | `rel_mov_j_tool`                          |
| `RelMovLTool`           | `rel_mov_l_tool`                          |
| `RelMovJUser`           | `rel_mov_j_user`                          |
| `RelMovLUser`           | `rel_mov_l_user`                          |
| `RelJointMovJ`          | `rel_joint_mov_j`                         |

---

## 4. Parameter Names

| Rule               | Convention                                      | Example                          |
| ------------------ | ----------------------------------------------- | -------------------------------- |
| All parameters     | `snake_case`                                    | `center_x`, `offset_z`, `is_rtu` |
| Boolean parameters | Prefix with `is_`, `has_`, `should_`, or `can_` | `is_rtu`, `is_enabled`           |
| Never camelCase    | `centerX` → `center_x`, `isRTU` → `is_rtu`      |                                  |

---

## 5. Variable Names

| Category                   | Convention                                                          | Example                               |
| -------------------------- | ------------------------------------------------------------------- | ------------------------------------- |
| Local variables            | `snake_case`                                                        | `enable_status`, `robot_mode`         |
| Instance variables         | `snake_case`                                                        | `self.last_recv_time`                 |
| Private instance variables | `_snake_case` (single underscore)                                   | `self._feedback_dtype`                |
| Module-level globals       | `snake_case`                                                        | `current_actual`, `global_lock_value` |
| **Never camelCase**        | `robotMode` → `robot_mode`, `globalLockValue` → `global_lock_value` |                                       |

---

## 6. Constants

| Rule                        | Convention         | Example                               |
| --------------------------- | ------------------ | ------------------------------------- |
| Module-level constants      | `UPPER_SNAKE_CASE` | `SERVO_ID_MIN`, `SUPPORTED_LANGUAGES` |
| Protocol field mapping dict | `UPPER_SNAKE_CASE` | `PROTOCOL_FIELD_MAP`                  |

---

## 7. Type Aliases

| Rule            | Convention                            | Example                                     |
| --------------- | ------------------------------------- | ------------------------------------------- |
| Type aliases    | `PascalCase`, descriptive             | `FeedbackDtype`, `DynParam`, `ToolDynParam` |
| Not vague names | Name must describe the type's purpose | `FeedbackDtype` **not** `MyType`            |

---

## 8. NumPy Dtype Field Names

The `FeedbackDtype` (formerly `MyType`) dtype in `base.py` represents the
1440-byte binary feedback packet from the Dobot controller. Field names use
`snake_case` internally; the `PROTOCOL_FIELD_MAP` dictionary in `base.py`
provides the mapping to the original Dobot protocol documentation names.

| Rule                    | Convention                                  |
| ----------------------- | ------------------------------------------- | ----------------------------------------------------- |
| All dtype fields        | `snake_case`                                | `tcp_force`, `tool_vector_target`, `actual_tcp_force` |
| Original protocol names | Available via `PROTOCOL_FIELD_MAP` constant |                                                       |

---

## 9. Deprecation Pattern

When renaming a public symbol, always preserve the old name as a deprecated
alias:

```python
import warnings

# For methods (in class body):
def OldName(self, *args, **kwargs):
    warnings.warn(
        "OldName is deprecated, use new_name instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.new_name(*args, **kwargs)

# For module-level names / re-exports (in __init__.py):
# Keep old name as alias, but mark in __all__ docstring as deprecated.
OldClassName = NewClassName  # deprecated alias
```

---

## 10. Quick-Check Checklist for AI Agents

Before submitting any code touching this package, verify:

- [ ] No camelCase method, parameter, or variable names (except inside string literals sent to the robot protocol)
- [ ] No `__PascalCase` private members — use `_snake_case` instead
- [ ] Class names use `PascalCase` with correct word boundaries (`Feedback`, not `FeedBack`)
- [ ] All new protocol command methods use `snake_case` as the primary implementation
- [ ] Deprecated PascalCase aliases call the snake_case implementation and emit `DeprecationWarning`
- [ ] Boolean variables/parameters prefixed with `is_`, `has_`, `should_`, or `can_`
- [ ] Constants are `UPPER_SNAKE_CASE`
- [ ] Type aliases are `PascalCase` and descriptive
- [ ] Dtype field references use the snake_case names from `FeedbackDtype`
