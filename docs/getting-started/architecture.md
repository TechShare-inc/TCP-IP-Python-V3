# Architecture

## Connections

- Dashboard commands: port `29999`
- Motion commands: port `30003`
- Feedback stream: port `30004`

## Main classes

- `DobotApiDashboard`: robot status and control commands
- `DobotApiMove`: queued/real-time motion commands
- `DobotApiFeedback`: 1440-byte status packet reader
- `RobotErrorMonitor`: alarm polling and logging helper
- `AlarmI18n`: localized alarm metadata helper
