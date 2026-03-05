"""Unit tests for DobotApiFeedback — binary packet reading and parsing."""

from __future__ import annotations

import numpy as np
import pytest

from dobot_api_v3.dtypes import FeedbackData, FeedbackDtype
from dobot_api_v3.feedback import DobotApiFeedback

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_buffer(**kwargs: object) -> bytes:
    """Build a 1440-byte buffer with given FeedbackDtype field overrides."""
    arr = np.zeros(1, dtype=FeedbackDtype)
    for field, value in kwargs.items():
        arr[0][field] = value  # type: ignore[index]
    return bytes(arr.tobytes()[:1440])


assert (
    FeedbackDtype.itemsize == 1440
), f"FeedbackDtype size changed: expected 1440, got {FeedbackDtype.itemsize}"


# ---------------------------------------------------------------------------
# Happy path — exactly 1440 bytes
# ---------------------------------------------------------------------------


class TestFeedbackDataHappyPath:
    def test_returns_feedback_data_for_exact_1440_bytes(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        mock_feedback.socket_dobot.recv.return_value = _valid_buffer()  # type: ignore[union-attr]
        result = mock_feedback.feedback_data()
        assert isinstance(result, FeedbackData)

    def test_raw_returns_numpy_array_for_exact_1440_bytes(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        mock_feedback.socket_dobot.recv.return_value = _valid_buffer()  # type: ignore[union-attr]
        result = mock_feedback.raw_feedback_data()
        assert isinstance(result, np.ndarray)

    def test_raw_array_has_feedback_dtype(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        mock_feedback.socket_dobot.recv.return_value = _valid_buffer()  # type: ignore[union-attr]
        result = mock_feedback.raw_feedback_data()
        assert result is not None
        assert result.dtype == FeedbackDtype

    def test_field_values_round_trip(self, mock_feedback: DobotApiFeedback) -> None:
        """Values written into the buffer should be readable from the parsed FeedbackData."""
        buf = _valid_buffer(robot_mode=5, load=2.5, speed_scaling=0.75)
        mock_feedback.socket_dobot.recv.return_value = buf  # type: ignore[union-attr]
        result = mock_feedback.feedback_data()
        assert result is not None
        assert result.robot_mode == 5
        assert result.load == pytest.approx(2.5)
        assert result.speed_scaling == pytest.approx(0.75)

    def test_updates_last_recv_time(self, mock_feedback: DobotApiFeedback) -> None:
        before = mock_feedback.last_recv_time
        mock_feedback.socket_dobot.recv.return_value = _valid_buffer()  # type: ignore[union-attr]
        mock_feedback.feedback_data()
        assert mock_feedback.last_recv_time >= before


# ---------------------------------------------------------------------------
# Oversized packet (> 1440 bytes) — code reads again and then slices
# ---------------------------------------------------------------------------


class TestFeedbackDataOversizedPacket:
    def test_re_reads_on_oversized_first_packet(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        """If first recv > 1440 bytes, feedback_data re-reads once, then slices."""
        big_buf = _valid_buffer(robot_mode=7) + bytes(100)  # 1540 bytes
        exact_buf = _valid_buffer(robot_mode=7)  # 1440 bytes after re-read

        mock_feedback.socket_dobot.recv.side_effect = [big_buf, exact_buf]  # type: ignore[union-attr]
        result = mock_feedback.feedback_data()
        assert result is not None
        # Two recv calls: first oversized → re-read
        assert mock_feedback.socket_dobot.recv.call_count == 2  # type: ignore[union-attr]

    def test_second_oversized_still_returns_sliced_result(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        """If both recvs return oversized, len < 1440 is False → slices first 1440."""
        big_buf = _valid_buffer(robot_mode=3) + bytes(200)

        mock_feedback.socket_dobot.recv.side_effect = [big_buf, big_buf]  # type: ignore[union-attr]
        result = mock_feedback.feedback_data()
        assert result is not None
        assert result.robot_mode == 3


# ---------------------------------------------------------------------------
# Partial packet — retry logic
# ---------------------------------------------------------------------------


class TestFeedbackDataPartialPacket:
    def test_retries_up_to_5_times_on_short_packet(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        """If every recv returns a short packet, exactly 6 calls are made (1 initial + 5 retries)."""
        short = bytes(100)

        mock_feedback.socket_dobot.recv.return_value = short  # type: ignore[union-attr]
        with pytest.raises(RuntimeError, match="Missing data packets"):
            mock_feedback.feedback_data()

        # 1 initial recv + 5 retries = 6 total
        assert mock_feedback.socket_dobot.recv.call_count == 6  # type: ignore[union-attr]

    def test_succeeds_if_retry_returns_1440_bytes(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        """Returns successfully when a retry delivers > 1440 bytes."""
        short = bytes(100)
        good_buf = _valid_buffer(robot_mode=9) + bytes(200)  # >1440 triggers break

        mock_feedback.socket_dobot.recv.side_effect = [short, short, good_buf]  # type: ignore[union-attr]
        result = mock_feedback.feedback_data()
        assert result is not None
        assert result.robot_mode == 9


# ---------------------------------------------------------------------------
# Socket not connected
# ---------------------------------------------------------------------------


class TestFeedbackDataNoSocket:
    def test_raises_runtime_error_when_socket_is_none(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        mock_feedback.socket_dobot = None
        with pytest.raises(RuntimeError, match="Socket connection is not established"):
            mock_feedback.feedback_data()

    def test_raw_raises_runtime_error_when_socket_is_none(
        self, mock_feedback: DobotApiFeedback
    ) -> None:
        mock_feedback.socket_dobot = None
        with pytest.raises(RuntimeError, match="Socket connection is not established"):
            mock_feedback.raw_feedback_data()


# ---------------------------------------------------------------------------
# FeedbackDtype field completeness
# ---------------------------------------------------------------------------


class TestFeedbackDtype:
    def test_itemsize_is_1440(self) -> None:
        assert FeedbackDtype.itemsize == 1440

    def test_all_fields_accessible(self) -> None:
        arr = np.zeros(1, dtype=FeedbackDtype)
        for field_name in FeedbackDtype.names:  # type: ignore[union-attr]
            _ = arr[0][field_name]  # type: ignore[index]

    def test_joint_array_fields_have_6_elements(self) -> None:
        arr = np.zeros(1, dtype=FeedbackDtype)
        joint_fields = [
            "q_target",
            "qd_target",
            "qdd_target",
            "i_target",
            "m_target",
            "q_actual",
            "qd_actual",
            "i_actual",
            "actual_tcp_force",
            "tool_vector_actual",
            "tcp_speed_actual",
            "tcp_force",
            "tool_vector_target",
            "tcp_speed_target",
            "motor_temperatures",
            "joint_modes",
            "v_actual",
        ]
        for field in joint_fields:
            assert len(arr[0][field]) == 6, f"field {field!r} should have 6 elements"


# ---------------------------------------------------------------------------
# FeedbackData typed dataclass
# ---------------------------------------------------------------------------


class TestFeedbackDataClass:
    """Tests for FeedbackData.from_numpy() and immutability."""

    def _make_data(self, **kwargs: object) -> FeedbackData:
        buf = _valid_buffer(**kwargs)
        arr = np.frombuffer(buf, dtype=FeedbackDtype)
        return FeedbackData.from_numpy(arr)

    def test_scalar_fields_are_python_int_or_float(self) -> None:
        data = self._make_data(robot_mode=3)
        assert isinstance(data.robot_mode, int)
        assert isinstance(data.load, float)
        assert isinstance(data.speed_scaling, float)

    def test_array_fields_are_tuples(self) -> None:
        data = self._make_data()
        assert isinstance(data.q_actual, tuple)
        assert isinstance(data.tool_vector_actual, tuple)
        assert isinstance(data.hand_type, tuple)

    def test_six_element_tuple_lengths(self) -> None:
        data = self._make_data()
        six_fields = [
            "q_target",
            "qd_target",
            "qdd_target",
            "i_target",
            "m_target",
            "q_actual",
            "qd_actual",
            "i_actual",
            "actual_tcp_force",
            "tool_vector_actual",
            "tcp_speed_actual",
            "tcp_force",
            "tool_vector_target",
            "tcp_speed_target",
            "motor_temperatures",
            "joint_modes",
            "v_actual",
            "m_actual",
            "user_coords",
            "tool_coords",
            "six_force_value",
        ]
        for field in six_fields:
            value = getattr(data, field)
            assert len(value) == 6, f"field {field!r} should have 6 elements"

    def test_three_element_tuple_lengths(self) -> None:
        data = self._make_data()
        for field in ("tool_accelerometer_values", "elbow_position", "elbow_velocity"):
            assert len(getattr(data, field)) == 3, f"{field!r} should have 3 elements"

    def test_quaternion_fields_have_four_elements(self) -> None:
        data = self._make_data()
        assert len(data.target_quaternion) == 4
        assert len(data.actual_quaternion) == 4

    def test_round_trip_scalar_values(self) -> None:
        data = self._make_data(robot_mode=7, load=1.5, speed_scaling=0.5)
        assert data.robot_mode == 7
        assert data.load == pytest.approx(1.5)
        assert data.speed_scaling == pytest.approx(0.5)

    def test_is_frozen(self) -> None:
        import dataclasses

        data = self._make_data()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            data.robot_mode = 99  # type: ignore[misc]
