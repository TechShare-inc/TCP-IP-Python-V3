# API Reference

<!-- Diátaxis type: Reference -->

This section contains generated API reference pages from Sphinx and curated
reference notes.

## Quick links

- [Generated API Overview](./api/index.md)
- [Generated API Modules](./api/modules.md)
- [Command Patterns](./command-patterns.md)
- [Deprecations](./deprecations.md)
- [Feedback Fields](./feedback-fields.md)

## Key public API

| Symbol | Module | Description |
|---|---|---|
| `DobotRobot` | `robot` | Unified high-level entry point (recommended) |
| `DobotApi` | `base` | Base TCP socket class (low-level) |
| `DobotApiDashboard` | `commands.dashboard` | Dashboard command connection (mixin-composed) |
| `DobotApiMove` | `commands.move` | Motion command connection (mixin-composed) |
| `DobotApiFeedback` | `feedback` | Feedback stream reader |
| `FeedbackData` | `dtypes` | Typed feedback packet snapshot (frozen dataclass) |
| `FeedbackDtype` | `dtypes` | NumPy structured dtype for raw feedback |
| `PROTOCOL_FIELD_MAP` | `dtypes` | Snake_case → protocol name mapping |
| `AckResponse` | `responses` | Ack from lifecycle/motion commands |
| `IntResponse` | `responses` | Single integer value response |
| `PoseResponse` | `responses` | 6-DOF pose/angle response |
| `ErrorIdResponse` | `responses` | Active alarm code list |
| `parse_response` | `responses` | Regex parser for controller response strings |
| `DobotApiError` | `responses` | Exception for controller errors |
| `RobotErrorMonitor` | `error_monitor` | Alarm polling and logging |
| `AlarmI18n` | `i18n_manager` | Localized alarm metadata |
| `DynParam` | `utils` | Type alias for dynamic command parameters |
| `ToolDynParam` | `utils` | Type alias for tool relative move params |
| `Pose` | `utils` | 6-DOF pose/joint-angle tuple alias |

## Generated API docs

Generate and sync with:

```powershell
npm run docs:sync-api
```

This command writes Sphinx markdown output to `_autogen/` and syncs it into
`docs/reference/api/` for VitePress routing.
