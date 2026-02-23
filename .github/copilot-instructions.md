# Dobot API – Constitutive Rules for AI Agents

This document is the **authoritative reference** governing how AI coding agents
must operate within the `dobot_api_v3` project. It covers tooling, workflows,
scripting, and naming conventions. **All rules are mandatory** for code
generation, refactoring, review, and automation tasks.

---

# Part A — Project Tooling & Workflow Rules

## A1. Python Environment — `uv` Only

| Rule                  | Detail                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| Virtual-env creation  | `uv venv` (creates `.venv/` in project root). **Never** use `python -m venv`, `virtualenv`, or `conda`.  |
| Package installation  | `uv pip install -e .[dev]` for development. **Never** use bare `pip install`.                            |
| Dependency resolution | All dependency metadata lives in `pyproject.toml`. No `requirements.txt` files.                          |
| Lock file             | When lock-file support is used, use `uv lock` / `uv.lock`.                                               |
| Running tools         | Prefer `uv run <tool>` (e.g. `uv run pytest`, `uv run ruff check .`) to ensure the correct venv is used. |
| Python version        | ≥ 3.9 as declared in `pyproject.toml`.                                                                   |

**Setup command (canonical):**

```powershell
uv venv
uv pip install -e .[dev]
```

## A2. Shell & Scripting — PowerShell Only

| Rule              | Detail                                                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Script language   | All automation scripts **must** be PowerShell (`.ps1`). **Never** write Bash (`.sh`) or Batch (`.bat`/`.cmd`) scripts. |
| Script location   | `scripts/` directory at the project root.                                                                              |
| Naming convention | `Verb-Noun.ps1` using PowerShell approved verbs (e.g. `Setup-Dev.ps1`, `Run-Tests.ps1`).                               |
| Shebang / header  | Start each `.ps1` file with `#Requires -Version 5.1` and a brief comment block.                                        |
| Execution         | Users run scripts via `pwsh ./scripts/Verb-Noun.ps1` or `.\scripts\Verb-Noun.ps1` from the repo root.                  |
| CI compatibility  | CI pipelines should invoke PowerShell with `pwsh -NoProfile -File scripts/Verb-Noun.ps1`.                              |

**Available scripts:**

| Script                   | Purpose                                           |
| ------------------------ | ------------------------------------------------- |
| `scripts/Setup-Dev.ps1`  | Create venv, install dev dependencies             |
| `scripts/Run-Tests.ps1`  | Run pytest with optional marker filter            |
| `scripts/Run-Lint.ps1`   | Run ruff + mypy checks                            |
| `scripts/Build-Docs.ps1` | Generate Sphinx API docs and build VitePress site |

## A3. Code Quality Tools

| Tool           | Purpose              | Command                                        |
| -------------- | -------------------- | ---------------------------------------------- |
| **ruff**       | Linting + formatting | `uv run ruff check .` / `uv run ruff format .` |
| **mypy**       | Static type checking | `uv run mypy dobot_api_v3`                     |
| **pytest**     | Testing              | `uv run pytest`                                |
| **pytest-cov** | Coverage reporting   | `uv run pytest --cov`                          |

Configuration for all tools lives in `pyproject.toml`. Do **not** create
standalone config files (e.g. `.flake8`, `setup.cfg`, `tox.ini`).

## A4. File & Editor Settings

- An `.editorconfig` at the project root governs indentation, line endings,
  and trailing whitespace. AI agents must respect these settings.
- Indent with **4 spaces** for Python, **2 spaces** for YAML/JSON/Markdown.
- Line endings: `LF` (Unix-style) everywhere.
- Final newline: always present.

## A5. Pre-commit Hooks

A `.pre-commit-config.yaml` is provided. AI agents that create or modify
source files should ensure the changes pass the configured hooks:

- `ruff` (lint + format)
- `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`

## A6. Project Structure Invariants

```
TCP-IP-Python-V3/
├── .github/
│   └── copilot-instructions.md   ← THIS FILE (agent rules)
├── dobot_api_v3/                  ← package source
├── tests/
│   ├── unit/                      ← fast tests, no I/O
│   ├── integration/               ← loopback stub-server tests
│   └── hil/                       ← hardware-in-the-loop tests
├── scripts/                       ← PowerShell automation (.ps1 only)
├── examples/                      ← numbered example scripts
├── docs/                          ← documentation source
├── pyproject.toml                 ← single source of project metadata
├── .editorconfig
└── .pre-commit-config.yaml
```

**Rules:**

- **No `setup.py` or `setup.cfg`** — all metadata in `pyproject.toml`.
- **No `requirements*.txt`** — dependencies declared in `pyproject.toml`.
- **No Bash/Batch scripts** — only `.ps1` in `scripts/`.

## A7. Git & Version Control

| Rule            | Detail                                                                                                                             |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Commit messages | Use [Conventional Commits](https://www.conventionalcommits.org/) format: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`. |
| Branch naming   | `feature/<description>`, `fix/<description>`, `chore/<description>`.                                                               |
| PR scope        | Keep PRs focused — one logical change per PR.                                                                                      |

---

# Part B — Naming Convention Rules

This section is the authoritative naming convention reference for the
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

| Rule                             | Convention                                               |
| -------------------------------- | -------------------------------------------------------- |
| **All protocol command methods** | `snake_case` — always use these in new and existing code |

**Protocol name → Python method name mapping:**

| Protocol Name (wire format) | Python Method Name                        |
| --------------------------- | ----------------------------------------- |
| `EnableRobot`               | `enable_robot`                            |
| `DisableRobot`              | `disable_robot`                           |
| `ClearError`                | `clear_error`                             |
| `ResetRobot`                | `reset_robot`                             |
| `SpeedFactor`               | `speed_factor`                            |
| `User`                      | `set_user`                                |
| `Tool`                      | `set_tool`                                |
| `RobotMode`                 | `robot_mode`                              |
| `PayLoad`                   | `payload`                                 |
| `DO`                        | `do_output`                               |
| `DOExecute`                 | `do_execute`                              |
| `ToolDO`                    | `tool_do`                                 |
| `ToolDOExecute`             | `tool_do_execute`                         |
| `AO`                        | `ao`                                      |
| `AOExecute`                 | `ao_execute`                              |
| `AccJ`                      | `acc_j`                                   |
| `AccL`                      | `acc_l`                                   |
| `SpeedJ`                    | `speed_j`                                 |
| `SpeedL`                    | `speed_l`                                 |
| `VelJ`                      | `vel_j`                                   |
| `VelL`                      | `vel_l`                                   |
| `Arch`                      | `arch`                                    |
| `CP`                        | `cp`                                      |
| `LimZ`                      | `lim_z`                                   |
| `SetArmOrientation`         | `set_arm_orientation`                     |
| `PowerOn`                   | `power_on`                                |
| `RunScript`                 | `run_script`                              |
| `StopScript`                | `stop_script`                             |
| `PauseScript`               | `pause_script`                            |
| `ContinueScript`            | `continue_script`                         |
| `GetHoldRegs`               | `get_hold_regs`                           |
| `SetHoldRegs`               | `set_hold_regs`                           |
| `GetErrorID`                | `get_error_id`                            |
| `SetPayload`                | `set_payload`                             |
| `PositiveSolution`          | `positive_solution`                       |
| `InverseSolution`           | `inverse_solution`                        |
| `SetCollisionLevel`         | `set_collision_level`                     |
| `GetAngle`                  | `get_angle`                               |
| `GetPose`                   | `get_pose`                                |
| `EmergencyStop`             | `emergency_stop`                          |
| `ModbusCreate`              | `modbus_create`                           |
| `ModbusClose`               | `modbus_close`                            |
| `SetSafeSkin`               | `set_safe_skin`                           |
| `SetObstacleAvoid`          | `set_obstacle_avoid`                      |
| `GetTraceStartPose`         | `get_trace_start_pose`                    |
| `GetPathStartPose`          | `get_path_start_pose`                     |
| `HandleTrajPoints`          | `handle_traj_points`                      |
| `GetSixForceData`           | `get_six_force_data`                      |
| `SetCollideDrag`            | `set_collide_drag`                        |
| `SetTerminalKeys`           | `set_terminal_keys`                       |
| `SetTerminal485`            | `set_terminal_485`                        |
| `GetTerminal485`            | `get_terminal_485`                        |
| `TCPSpeed`                  | `tcp_speed`                               |
| `TCPSpeedEnd`               | `tcp_speed_end`                           |
| `GetInBits`                 | `get_in_bits`                             |
| `GetInRegs`                 | `get_in_regs`                             |
| `GetCoils`                  | `get_coils`                               |
| `SetCoils`                  | `set_coils`                               |
| `DI`                        | `di`                                      |
| `ToolDI`                    | `tool_di`                                 |
| `DOGroup`                   | `do_group`                                |
| `BrakeControl`              | `brake_control`                           |
| `StartDrag`                 | `start_drag`                              |
| `StopDrag`                  | `stop_drag`                               |
| `LoadSwitch`                | `load_switch`                             |
| `Continue`                  | `resume` (`continue` is a Python keyword) |
| `MovJ`                      | `mov_j`                                   |
| `MovL`                      | `mov_l`                                   |
| `JointMovJ`                 | `joint_mov_j`                             |
| `Jump`                      | `jump`                                    |
| `RelMovJ`                   | `rel_mov_j`                               |
| `RelMovL`                   | `rel_mov_l`                               |
| `MovLIO`                    | `mov_l_io`                                |
| `MovJIO`                    | `mov_j_io`                                |
| `Arc`                       | `arc`                                     |
| `Circle3`                   | `circle3`                                 |
| `ServoJ`                    | `servo_j`                                 |
| `ServoJS`                   | `servo_js`                                |
| `ServoP`                    | `servo_p`                                 |
| `MoveJog`                   | `move_jog`                                |
| `StartTrace`                | `start_trace`                             |
| `StartPath`                 | `start_path`                              |
| `StartFCTrace`              | `start_fc_trace`                          |
| `Sync`                      | `sync`                                    |
| `RelMovJTool`               | `rel_mov_j_tool`                          |
| `RelMovLTool`               | `rel_mov_l_tool`                          |
| `RelMovJUser`               | `rel_mov_j_user`                          |
| `RelMovLUser`               | `rel_mov_l_user`                          |
| `RelJointMovJ`              | `rel_joint_mov_j`                         |

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

The `FeedbackDtype` dtype in `base.py` represents the
1440-byte binary feedback packet from the Dobot controller. Field names use
`snake_case` internally; the `PROTOCOL_FIELD_MAP` dictionary in `base.py`
provides the mapping to the original Dobot protocol documentation names.

| Rule                    | Convention                                  |
| ----------------------- | ------------------------------------------- | ----------------------------------------------------- |
| All dtype fields        | `snake_case`                                | `tcp_force`, `tool_vector_target`, `actual_tcp_force` |
| Original protocol names | Available via `PROTOCOL_FIELD_MAP` constant |                                                       |

---

## 9. Docstring Style

All new or updated public APIs must use **Google-style docstrings**.

| Rule                        | Convention                                                           | Example                         |
| --------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| Public classes/methods      | Google-style sections (`Args:`, `Returns:`, `Raises:` as applicable) | `def enable_robot(...): ...`    |
| Include usage where helpful | Add concise `Example:` blocks for high-traffic API methods           | `mov_j`, `speed_factor`, `sync` |

Template:

```python
def speed_factor(self, speed: int) -> str:
    """Set global speed factor.

    Args:
        speed: Rate value in range 1-100.

    Returns:
        Robot response string.

    Example:
        >>> dashboard.speed_factor(40)
    """
```

---

## 10. Quick-Check Checklist for AI Agents

Before submitting any code touching this package, verify:

**Tooling & Workflow:**

- [ ] Environment created with `uv venv`, packages installed with `uv pip install`
- [ ] No `requirements.txt`, `setup.py`, or `setup.cfg` files created
- [ ] Any new automation scripts are PowerShell `.ps1` files (no `.sh` or `.bat`)
- [ ] Tool configuration added to `pyproject.toml`, not standalone config files
- [ ] Terminal commands use `uv run <tool>` instead of invoking tools directly

**Naming & Style:**

- [ ] No camelCase method, parameter, or variable names (except inside string literals sent to the robot protocol)
- [ ] No `__PascalCase` private members — use `_snake_case` instead
- [ ] Class names use `PascalCase` with correct word boundaries (`Feedback`, not `FeedBack`)
- [ ] All new protocol command methods use `snake_case`
- [ ] Boolean variables/parameters prefixed with `is_`, `has_`, `should_`, or `can_`
- [ ] Constants are `UPPER_SNAKE_CASE`
- [ ] Type aliases are `PascalCase` and descriptive
- [ ] Dtype field references use the snake_case names from `FeedbackDtype`
- [ ] New/updated public APIs use Google-style docstrings (`Args:`, `Returns:`, and `Raises:` when needed)
