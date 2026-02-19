# Command Patterns

Use this page as a quick guide for composing dashboard/move command arguments.

## Pattern 1: Positional Required Args

Use plain positional arguments for required protocol parameters.

```python
move.mov_j(200, 0, 200, 0, 0, 0)
dashboard.speed_factor(40)
```

## Pattern 2: Optional Dynamic Parameters (`*dyn_params`)

Many motion/dashboard methods accept extra protocol arguments through
`*dyn_params`.

Typical forms:

- string fragments: `"SpeedJ=40"`, `"AccJ=40"`, `"User=0"`
- tuple payloads for parallel I/O: `(0, 50, 1, 1)`
- integer/float values where the protocol accepts scalar trailing args

Examples:

```python
move.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40", "User=0")
move.mov_l_io(250, 0, 180, 0, 0, 0, (0, 50, 1, 1))
```

## Pattern 3: Tool/User Relative Moves

For tool-relative helpers using `ToolDynParam`, pass optional tuples in the
form `(speed, acc, index)`.

```python
move.rel_mov_j_tool(10, 0, 0, 0, 0, 0, 0, (40, 40, 0))
move.rel_mov_l_tool(0, 0, -10, 0, 0, 0, 0, (30, 30, 0))
```

## Pattern 4: Lifecycle + Motion Ordering

Recommended command ordering for most scripts:

1. `dashboard.clear_error()`
2. `dashboard.enable_robot()`
3. Configure speed/acceleration (for example `speed_factor`, `speed_j`)
4. Issue move commands (`mov_j`, `mov_l`, etc.)
5. `move.sync()`
6. `dashboard.disable_robot()`

## Pattern 5: Feedback + Error Monitoring

Use a separate feedback connection and keep dashboard ownership explicit.

```python
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 30003)
feedback = DobotApiFeedback(ip, 30004)
monitor = RobotErrorMonitor(dashboard, language="en")
```

## Tips

- Prefer `snake_case` API names in all new code.
- Keep deprecated PascalCase aliases only for migration compatibility.
- Always close sockets in `finally` blocks.
