"""Unit tests for protocol-aware feedback reader."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import numpy as np
import pytest

from dobot_api.feedback import DobotApiFeedback


class TestDobotApiFeedback:
    @staticmethod
    def _make_raw_array() -> np.ndarray:
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
        arr["robot_mode"] = 5
        return arr

    @pytest.mark.parametrize("protocol", ["v3", "v4"])
    def test_constructor_accepts_both_protocols(
        self, protocol: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_backend = MagicMock()
        mock_backend.port = 30004
        mock_backend.socket_dobot = SimpleNamespace()
        if protocol == "v3":
            monkeypatch.setattr(
                "dobot_api.v3.DobotApiFeedback", lambda ip, port: mock_backend
            )
        else:
            monkeypatch.setattr(
                "dobot_api.v4.DobotApiFeedback", lambda ip, port: mock_backend
            )

        fb = DobotApiFeedback("192.168.1.6", 30004, protocol=protocol)
        assert fb.protocol == protocol
        assert fb.port == 30004

    def test_unknown_protocol_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown protocol"):
            DobotApiFeedback("192.168.1.6", 30004, protocol="v5")  # type: ignore[arg-type]

    def test_feedback_data_returns_normalized_type(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        raw = self._make_raw_array()
        mock_backend = MagicMock()
        mock_backend.raw_feedback_data.return_value = raw
        monkeypatch.setattr(
            "dobot_api.v4.DobotApiFeedback", lambda ip, port: mock_backend
        )

        fb = DobotApiFeedback("192.168.1.6", 30004, protocol="v4")
        result = fb.feedback_data()
        from dobot_api.dtypes import FeedbackData

        assert isinstance(result, FeedbackData)
        assert result.test_value == 42
        assert result.robot_mode == 5

    def test_feedback_data_returns_none_when_raw_is_none(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_backend = MagicMock()
        mock_backend.raw_feedback_data.return_value = None
        monkeypatch.setattr(
            "dobot_api.v3.DobotApiFeedback", lambda ip, port: mock_backend
        )

        fb = DobotApiFeedback("192.168.1.6", 30004, protocol="v3")
        assert fb.feedback_data() is None

    def test_raw_feedback_data_delegates(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        raw = self._make_raw_array()
        mock_backend = MagicMock()
        mock_backend.raw_feedback_data.return_value = raw
        monkeypatch.setattr(
            "dobot_api.v3.DobotApiFeedback", lambda ip, port: mock_backend
        )

        fb = DobotApiFeedback("192.168.1.6", 30004, protocol="v3")
        result = fb.raw_feedback_data()
        assert result is raw

    def test_close_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_backend = MagicMock()
        monkeypatch.setattr(
            "dobot_api.v4.DobotApiFeedback", lambda ip, port: mock_backend
        )

        fb = DobotApiFeedback("192.168.1.6", 30004, protocol="v4")
        fb.close()
        mock_backend.close.assert_called_once()
