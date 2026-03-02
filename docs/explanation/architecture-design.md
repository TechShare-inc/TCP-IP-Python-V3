# About the Architecture

<!-- Diátaxis type: Explanation -->

This page explains the design decisions behind the `dobot_api_v3` package
architecture. For quick-start usage, see the
[Architecture overview](../getting-started/architecture.md).

## Why a unified `DobotRobot` entry point?

The Dobot V3 protocol requires multiple TCP connections — dashboard (port
29999), motion (port 30003), and feedback (ports 30004–30006). Managing these
manually is error-prone: forgetting to close a socket, mixing up port
assignments, or getting the startup sequence wrong are common mistakes.

`DobotRobot` was introduced to encapsulate this complexity behind a single
context-managed object. It opens dashboard and move connections eagerly on
construction, while feedback connections are created **lazily** on first access
to avoid unnecessary network traffic for users who do not need real-time
feedback.

## Why mixin composition?

`DobotApiDashboard` and `DobotApiMove` each expose dozens of protocol commands.
Placing all methods in a single class would create files exceeding 1000 lines
with no logical grouping.

The mixin pattern groups commands by category (system, config, I/O, query,
motion, trajectory, etc.), where each mixin file is small, focused, and
independently testable. The concrete `DobotApiDashboard` and `DobotApiMove`
classes then compose the appropriate mixins through multiple inheritance, with
`_SerializationMixin` at the base providing shared helpers (`_build_cmd`,
`_recv_ack`, `_fmt`).

```
DobotApiDashboard                   DobotApiMove
  ├── _SystemMixin                    ├── _BasicMotionMixin
  ├── _IOMixin                        ├── _RelativeMotionMixin
  ├── _ConfigMixin                    ├── _ServoJogMixin
  ├── _QueryMixin                     ├── _TrajectoryMixin
  └── DobotApi (TCP base)             └── DobotApi (TCP base)
```

## Why typed response dataclasses?

Raw string responses from the controller (e.g., `"0,{5},robot_mode;"`) are
fragile to work with — parsing logic leaks into application code, and typos in
field access go undetected until runtime.

The `responses` module provides frozen dataclasses (`AckResponse`,
`IntResponse`, `PoseResponse`, `ErrorIdResponse`) that parse the controller
string once and expose fields with proper Python types. This enables IDE
autocomplete, static type checking via `mypy`, and `isinstance`-based dispatch.

## Why `FeedbackData` alongside `FeedbackDtype`?

The 1440-byte binary packet is most efficiently decoded as a NumPy structured
array (`FeedbackDtype`). However, NumPy scalars behave surprisingly in some
contexts (e.g., `numpy.uint64` is not `int`), and field access via string keys
(`raw["robot_mode"]`) provides no IDE assistance.

`FeedbackData` is a plain Python frozen dataclass built from the NumPy array
via `FeedbackData.from_numpy()`. It converts NumPy scalars to native Python
types and multi-element fields to tuples, giving downstream code full type
safety and autocompletion with minimal overhead.

## Why `snake_case` only?

Earlier versions of the API mirrored the protocol's PascalCase command names
(e.g., `EnableRobot()`, `MovJ()`). This conflicted with PEP 8 and created
ambiguity between class names and method calls. Starting with v3, all protocol
command methods use `snake_case` exclusively. The mapping from protocol names
to Python names is defined in `.github/copilot-instructions.md` and enforced
by linting.
