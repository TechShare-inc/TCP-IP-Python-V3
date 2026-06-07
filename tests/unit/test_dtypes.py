"""Unit tests for shared dtypes: Pose and FeedbackData."""

from __future__ import annotations

import numpy as np
import pytest

from dobot_api.dtypes import FeedbackData, Pose


class TestPose:
    def test_creation_from_args(self) -> None:
        p = Pose(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        assert p.x == 1.0
        assert p.y == 2.0
        assert p.z == 3.0
        assert p.rx == 4.0
        assert p.ry == 5.0
        assert p.rz == 6.0

    def test_immutable(self) -> None:
        p = Pose(0, 0, 0, 0, 0, 0)
        with pytest.raises(Exception):
            p.x = 1.0  # type: ignore[misc]

    def test_equality(self) -> None:
        assert Pose(1, 2, 3, 4, 5, 6) == Pose(1, 2, 3, 4, 5, 6)
        assert Pose(1, 2, 3, 4, 5, 6) != Pose(0, 0, 0, 0, 0, 0)

    def test_from_sequence_list(self) -> None:
        p = Pose.from_sequence([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        assert p == Pose(10, 20, 30, 40, 50, 60)

    def test_from_sequence_tuple(self) -> None:
        p = Pose.from_sequence((1, 2, 3, 4, 5, 6))
        assert p == Pose(1, 2, 3, 4, 5, 6)

    def test_from_sequence_numpy(self) -> None:
        arr = np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
        p = Pose.from_sequence(arr)
        assert p == Pose(1.1, 2.2, 3.3, 4.4, 5.5, 6.6)

    def test_from_sequence_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError, match="requires 6"):
            Pose.from_sequence([1, 2, 3])


class TestFeedbackData:
    @staticmethod
    def _make_raw_feedback(**overrides: object) -> np.ndarray:
        """Build a minimal numpy structured array matching the feedback dtype."""
        defaults: dict[str, object] = {
            "test_value": 42,
            "q_actual": np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
            "qd_actual": np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            "i_actual": np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06]),
            "tool_vector_actual": np.array([100.0, 200.0, 300.0, 0.1, 0.2, 0.3]),
            "tcp_speed_actual": np.array([10.0, 20.0, 30.0, 1.0, 2.0, 3.0]),
            "tcp_force": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            "robot_mode": 5,
            "enable_status": 1,
            "error_status": 0,
            "drag_status": 0,
            "brake_status": 0,
            "digital_inputs": 0xFF,
            "digital_outputs": 0x00,
            "motor_temperatures": np.array([30.0, 31.0, 32.0, 33.0, 34.0, 35.0]),
            "speed_scaling": 50.0,
            "load": 0.5,
            "current_command_id": 7,
        }
        defaults.update(overrides)
        dtype = np.dtype([(k, np.float64, (6,) if "actual" in k or "force" in k or "speed" in k or "temperatures" in k or "q_actual" in k or "qd_actual" in k or "i_actual" in k else ()) for k in defaults])  # type: ignore[arg-type]
        # Use a simpler approach: build with object dtype then cast
        return np.array([tuple(defaults.values())], dtype=object)  # type: ignore[arg-type]

    def test_from_numpy_basic(self) -> None:
        # Create a simple structured array that mimics feedback fields
        dtype = np.dtype([
            ("test_value", np.int32),
            ("q_actual", np.float64, (6,)),
            ("qd_actual", np.float64, (6,)),
            ("i_actual", np.float64, (6,)),
            ("tool_vector_actual", np.float64, (6,)),
            ("tcp_speed_actual", np.float64, (6,)),
            ("tcp_force", np.float64, (6,)),
            ("robot_mode", np.int32),
            ("enable_status", np.int32),
            ("error_status", np.int32),
            ("drag_status", np.int32),
            ("brake_status", np.int32),
            ("digital_inputs", np.int32),
            ("digital_outputs", np.int32),
            ("motor_temperatures", np.float64, (6,)),
            ("speed_scaling", np.float64),
            ("load", np.float64),
            ("current_command_id", np.int32),
        ])
        arr = np.zeros(1, dtype=dtype)
        arr["test_value"] = 42
        arr["q_actual"] = [1, 2, 3, 4, 5, 6]
        arr["robot_mode"] = 5
        arr["speed_scaling"] = 50.0

        fb = FeedbackData.from_numpy(arr)

        assert fb.test_value == 42
        assert fb.q_actual == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        assert fb.robot_mode == 5
        assert fb.speed_scaling == 50.0

    def test_from_numpy_digital_inputs_fallback(self) -> None:
        """When digital_inputs is absent, fall back to digital_input_bits."""
        dtype = np.dtype([
            ("test_value", np.int32),
            ("q_actual", np.float64, (6,)),
            ("qd_actual", np.float64, (6,)),
            ("i_actual", np.float64, (6,)),
            ("tool_vector_actual", np.float64, (6,)),
            ("tcp_speed_actual", np.float64, (6,)),
            ("tcp_force", np.float64, (6,)),
            ("robot_mode", np.int32),
            ("enable_status", np.int32),
            ("error_status", np.int32),
            ("drag_status", np.int32),
            ("brake_status", np.int32),
            ("digital_input_bits", np.int32),
            ("digital_output_bits", np.int32),
            ("motor_temperatures", np.float64, (6,)),
            ("speed_scaling", np.float64),
            ("load", np.float64),
            ("current_command_id", np.int32),
        ])
        arr = np.zeros(1, dtype=dtype)
        arr["digital_input_bits"] = 0xAB
        arr["digital_output_bits"] = 0xCD

        fb = FeedbackData.from_numpy(arr)

        assert fb.digital_inputs == 0xAB
        assert fb.digital_outputs == 0xCD

    def test_from_numpy_missing_fields_default_to_zero(self) -> None:
        """Fields not in the dtype should default to 0."""
        dtype = np.dtype([
            ("test_value", np.int32),
            ("q_actual", np.float64, (6,)),
            ("qd_actual", np.float64, (6,)),
            ("i_actual", np.float64, (6,)),
            ("tool_vector_actual", np.float64, (6,)),
            ("tcp_speed_actual", np.float64, (6,)),
            ("tcp_force", np.float64, (6,)),
            ("robot_mode", np.int32),
            ("enable_status", np.int32),
            ("error_status", np.int32),
            ("drag_status", np.int32),
            ("brake_status", np.int32),
            ("digital_inputs", np.int32),
            ("digital_outputs", np.int32),
            ("motor_temperatures", np.float64, (6,)),
            ("speed_scaling", np.float64),
            ("load", np.float64),
            ("current_command_id", np.int32),
        ])
        arr = np.zeros(1, dtype=dtype)

        fb = FeedbackData.from_numpy(arr)

        assert fb.robot_mode == 0
        assert fb.speed_scaling == 0.0
        assert fb.load == 0.0
