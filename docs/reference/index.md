# API Reference

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
| `DobotApiDashboard` | `dashboard` | Dashboard command connection |
| `DobotApiMove` | `move` | Motion command connection |
| `DobotApiFeedback` | `feedback` | Feedback stream reader |
| `FeedbackData` | `base` | Typed feedback packet snapshot (frozen dataclass) |
| `FeedbackDtype` | `base` | NumPy structured dtype for raw feedback |
| `AckResponse` | `responses` | Ack from lifecycle/motion commands |
| `IntResponse` | `responses` | Single integer value response |
| `PoseResponse` | `responses` | 6-DOF pose/angle response |
| `ErrorIdResponse` | `responses` | Active alarm code list |
| `parse_response` | `responses` | Regex parser for controller response strings |
| `DobotApiError` | `responses` | Exception for controller errors |
| `RobotErrorMonitor` | `error_monitor` | Alarm polling and logging |
| `AlarmI18n` | `i18n_manager` | Localized alarm metadata |

## Generated API docs

Generate and sync with:

```bash
npm run docs:sync-api
```

This command writes Sphinx markdown output to `_autogen` and syncs it into
`docs/reference/api/` for VitePress routing.
