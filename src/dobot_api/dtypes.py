"""Shared public data types for the unified Dobot API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True, slots=True)
class Pose:
    """Six-axis pose or joint vector."""

    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    @classmethod
    def from_sequence(cls, values: Any) -> "Pose":
        vals = list(values)
        if len(vals) != 6:
            raise ValueError(f"Pose requires 6 values, got {len(vals)}")
        return cls(*(float(v) for v in vals))


@dataclass(frozen=True, slots=True)
class FeedbackData:
    """Protocol-neutral subset of a Dobot 1440-byte feedback packet."""

    test_value: int
    q_actual: tuple[float, ...]
    qd_actual: tuple[float, ...]
    i_actual: tuple[float, ...]
    tool_vector_actual: tuple[float, ...]
    tcp_speed_actual: tuple[float, ...]
    tcp_force: tuple[float, ...]
    robot_mode: int
    enable_status: int
    error_status: int
    drag_status: int
    brake_status: int
    digital_inputs: int
    digital_outputs: int
    motor_temperatures: tuple[float, ...]
    speed_scaling: float
    load: float
    current_command_id: int

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "FeedbackData":
        row = arr[0]

        def field(name: str, default: Any = 0) -> Any:
            if arr.dtype.names and name in arr.dtype.names:
                return row[name]
            return default

        def tuple_field(name: str) -> tuple[float, ...]:
            value = field(name, np.zeros(6))
            return tuple(float(x) for x in np.asarray(value).tolist())

        return cls(
            test_value=int(field("test_value")),
            q_actual=tuple_field("q_actual"),
            qd_actual=tuple_field("qd_actual"),
            i_actual=tuple_field("i_actual"),
            tool_vector_actual=tuple_field("tool_vector_actual"),
            tcp_speed_actual=tuple_field("tcp_speed_actual"),
            tcp_force=tuple_field("tcp_force"),
            robot_mode=int(field("robot_mode")),
            enable_status=int(field("enable_status")),
            error_status=int(field("error_status")),
            drag_status=int(field("drag_status")),
            brake_status=int(field("brake_status")),
            digital_inputs=int(field("digital_inputs", field("digital_input_bits"))),
            digital_outputs=int(field("digital_outputs", field("digital_output_bits"))),
            motor_temperatures=tuple_field("motor_temperatures"),
            speed_scaling=float(field("speed_scaling")),
            load=float(field("load")),
            current_command_id=int(field("current_command_id")),
        )
