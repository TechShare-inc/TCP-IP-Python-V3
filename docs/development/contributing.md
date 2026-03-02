# Contributing

## Setup

```powershell
uv venv
uv pip install -e .[dev]
```

## Running checks

```powershell
uv run ruff check .
uv run ruff format .
uv run mypy dobot_api_v3
uv run pytest
```

## Coding style

- Use `snake_case` for methods, parameters, and variables
- Use `PascalCase` for class names
- All new public APIs must use Google-style docstrings
- Boolean parameters prefixed with `is_`, `has_`, `should_`, or `can_`
- Constants in `UPPER_SNAKE_CASE`
- No deprecated PascalCase aliases — the API is exclusively `snake_case`

See `.github/copilot-instructions.md` for the complete naming convention
reference.

## Package structure

Dashboard and move command implementations live in the `commands/` sub-package,
organized as mixin classes:

- **`_system_mixin.py`** — lifecycle, script, motion-flow
- **`_config_mixin.py`** — speed/acc/jerk, coordinate, payload
- **`_io_mixin.py`** — digital/analog I/O, DO groups, Modbus
- **`_query_mixin.py`** — pose/angle/error queries, kinematics
- **`_basic_motion_mixin.py`** — `mov_j`, `mov_l`, `arc`, `circle3`, …
- **`_relative_motion_mixin.py`** — `rel_mov_j`, `rel_mov_l`, tool/user
- **`_servo_jog_mixin.py`** — `servo_j`, `servo_js`, `servo_p`, `move_jog`
- **`_trajectory_mixin.py`** — `start_trace`, `start_path`, `sync`
- **`_serialization.py`** — shared `_fmt`, `_build_cmd`, `_recv_ack` helpers

Data types (`FeedbackDtype`, `FeedbackData`, `PROTOCOL_FIELD_MAP`) live in
`dtypes.py`.  Response dataclasses live in `responses.py`.
