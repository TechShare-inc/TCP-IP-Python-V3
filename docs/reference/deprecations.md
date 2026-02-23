# Deprecations

## Removed in 3.0.0-alpha.2

All deprecated backward-compatibility aliases have been **removed**. The API is
now exclusively `snake_case`.

### Removed aliases

| Removed name | Replacement |
|---|---|
| `DobotApiFeedBack` | `DobotApiFeedback` |
| `MyType` | `FeedbackDtype` |
| `feedBackData()` | `raw_feedback_data()` (NumPy) or `feedback_data()` (`FeedbackData`) |
| `RobotErrorMonitor.from_connection()` | Construct `DobotApiDashboard` and pass to `RobotErrorMonitor(dashboard)` |
| All PascalCase method aliases (e.g. `EnableRobot`) | `snake_case` equivalents (e.g. `enable_robot`) |

### Removed modules

| Removed module | Notes |
|---|---|
| `dobot_api_v3.api` | Internal compatibility shim — import from `dobot_api_v3` directly |

### Migration

If you are upgrading from an older version, replace any PascalCase method calls
with their `snake_case` equivalents (e.g. `EnableRobot()` → `enable_robot()`,
`MovJ()` → `mov_j()`). The full mapping is documented in the
[copilot-instructions](../../.github/copilot-instructions.md) protocol name
table under **Section 3b**.

For new code, prefer `DobotRobot` over direct subsystem instantiation.

