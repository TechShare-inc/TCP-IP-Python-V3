# Deprecations

<!-- Diátaxis type: Reference -->

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
| `dobot_api_v3.dashboard` | Moved to `dobot_api_v3.commands.dashboard` |
| `dobot_api_v3.move` | Moved to `dobot_api_v3.commands.move` |

### Relocated modules

| Old import path | New import path |
|---|---|
| `from dobot_api_v3 import DobotApiDashboard` | `from dobot_api_v3.commands import DobotApiDashboard` |
| `from dobot_api_v3 import DobotApiMove` | `from dobot_api_v3.commands import DobotApiMove` |
| `from dobot_api_v3.base import FeedbackDtype` | `from dobot_api_v3.dtypes import FeedbackDtype` (re-exported from `base` for compat) |
| `from dobot_api_v3.base import FeedbackData` | `from dobot_api_v3.dtypes import FeedbackData` (re-exported from `base` for compat) |

### Migration

If you are upgrading from an older version, replace any PascalCase method calls
with their `snake_case` equivalents (e.g. `EnableRobot()` → `enable_robot()`,
`MovJ()` → `mov_j()`). The full mapping is documented in the project's
`.github/copilot-instructions.md` protocol name table under **Section 3b**.

Update imports for `DobotApiDashboard` and `DobotApiMove` to use the
`dobot_api_v3.commands` sub-package.

For new code, prefer `DobotRobot` over direct subsystem instantiation.

