# Changelog

## 3.0.0-alpha.2 (`41d0aac`)

### Added

- **`DobotRobot` high-level wrapper** — a single unified entry point that
  composes `DobotApiDashboard`, `DobotApiMove`, `DobotApiFeedback`, and
  `RobotErrorMonitor` behind one object.  Supports context-manager usage
  (`with DobotRobot(ip) as robot:`), lazy feedback connections, and a
  `startup()`/`shutdown()` lifecycle.
- **`responses` module** — typed frozen dataclasses for controller responses:
  `AckResponse`, `IntResponse`, `PoseResponse`, `ErrorIdResponse`, plus the
  `parse_response()` regex-based parser and `DobotApiError` exception.
  `DobotRobot` methods return these typed responses instead of raw strings.
- **`FeedbackData` dataclass** — immutable `@dataclass(frozen=True, slots=True)`
  snapshot of the 1440-byte feedback packet with full IDE autocompletion.
  Constructed via `FeedbackData.from_numpy()`.
- `feedback_data()` now returns a typed `FeedbackData` instance; the previous
  raw NumPy return is available as `raw_feedback_data()`.
- New example `07_drag_mode.py` — demonstrates drag (teach) mode.
- New utility `scripts/set_robot_ip.py` — configure static IP and DHCP for
  network interfaces.
- HIL test fixtures (`real_robot`) and initial hardware-in-the-loop tests.
- Unit tests for `DobotRobot` and `responses` module.

### Changed

- All examples updated to use the `DobotRobot` unified API.
- `startup()` now checks for controller errors first; skips `clear_error` and
  `power_on` when no alarms are present, reducing startup time.
- i18n alarm key structure changed to `alarms.{type}.{id}` (was `{type}.{id}`).
- Feedback fields documentation expanded with full field reference tables.

### Removed

- **All deprecated backward-compatibility aliases** — `DobotApiFeedBack`,
  `MyType`, `feedBackData()`, `RobotErrorMonitor.from_connection()`, and all
  PascalCase method aliases.  The API is now exclusively `snake_case`.
- Deleted `api.py` internal compatibility shim.
- Deleted `tests/unit/test_deprecations.py` and `tests/unit/test_utils.py`
  (covered by new tests).

---

## 3.0.0-alpha.1 (`304d6ba`)

- Initial modular `dobot_api_v3` package release
- Dashboard/move/feedback modules split by TCP connection role
- Alarm i18n and error monitoring utilities added
