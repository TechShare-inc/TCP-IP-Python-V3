"""Unit tests for protocol-aware error monitor."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from dobot_api.error_monitor import RobotErrorMonitor


class TestRobotErrorMonitor:
    @staticmethod
    def _make_mock_dashboard() -> MagicMock:
        dashboard = MagicMock()
        dashboard.ip = "192.168.1.6"
        dashboard.clear_error = MagicMock(return_value=None)
        return dashboard

    @pytest.mark.parametrize("protocol", ["v3", "v4"])
    def test_constructor_accepts_both_protocols(
        self, protocol: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify RobotErrorMonitor can be constructed for both protocols."""
        if protocol == "v3":
            import dobot_api.v3 as v3_mod

            mock_backend = SimpleNamespace(
                check_errors=lambda language="en": False,
                clear_robot_error=lambda language="en": True,
                get_error_info=lambda language="en": {},
                monitor_errors=lambda interval=5, language="en": None,
                save_error_log=lambda filename=None, language="en": None,
            )
            monkeypatch.setattr(v3_mod, "RobotErrorMonitor", lambda dashboard: mock_backend)
        else:
            import dobot_api.v4 as v4_mod

            mock_backend = SimpleNamespace(
                check_errors=lambda language="en": False,
                clear_robot_error=lambda language="en": True,
                get_error_info=lambda language="en": {},
                monitor_errors=lambda interval=5, language="en": None,
                save_error_log=lambda filename=None, language="en": None,
            )
            monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        monitor = RobotErrorMonitor(self._make_mock_dashboard(), protocol=protocol)
        assert monitor.protocol == protocol

    def test_v3_check_errors_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v3 as v3_mod

        mock_backend = MagicMock()
        mock_backend.check_errors.return_value = True
        monkeypatch.setattr(v3_mod, "RobotErrorMonitor", lambda dashboard: mock_backend)

        monitor = RobotErrorMonitor(self._make_mock_dashboard(), protocol="v3")
        result = monitor.check_errors(language="en")
        assert result is True
        mock_backend.check_errors.assert_called_once_with(language="en")

    def test_v4_check_errors_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v4 as v4_mod

        mock_backend = MagicMock()
        mock_backend.check_errors.return_value = False
        monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        monitor = RobotErrorMonitor(self._make_mock_dashboard(), protocol="v4")
        result = monitor.check_errors(language="en")
        assert result is False

    def test_v3_clear_robot_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v3 as v3_mod

        mock_backend = MagicMock()
        mock_backend.clear_robot_error.return_value = True
        monkeypatch.setattr(v3_mod, "RobotErrorMonitor", lambda dashboard: mock_backend)

        monitor = RobotErrorMonitor(self._make_mock_dashboard(), protocol="v3")
        assert monitor.clear_robot_error(language="en") is True

    def test_v4_clear_robot_error_uses_dashboard(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v4 as v4_mod

        # V4 backend has clear_robot_error; it takes the first branch
        mock_backend = MagicMock()
        mock_backend.clear_robot_error.return_value = True
        monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        dashboard = self._make_mock_dashboard()
        monitor = RobotErrorMonitor(dashboard, protocol="v4")
        result = monitor.clear_robot_error(language="en")
        # V4 backend has clear_robot_error, so the first branch is taken
        assert result is True
        mock_backend.clear_robot_error.assert_called_once_with(language="en")
        dashboard.clear_error.assert_not_called()

    def test_unknown_protocol_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown protocol"):
            RobotErrorMonitor(self._make_mock_dashboard(), protocol="v5")  # type: ignore[arg-type]

    def test_get_error_info(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v4 as v4_mod

        expected = {"16": "shoulder singularity"}
        mock_backend = MagicMock()
        mock_backend.get_error_info.return_value = expected
        monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        monitor = RobotErrorMonitor("192.168.1.6", protocol="v4")
        assert monitor.get_error_info(language="en") == expected

    def test_monitor_errors(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v4 as v4_mod

        mock_backend = MagicMock()
        monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        monitor = RobotErrorMonitor("192.168.1.6", protocol="v4")
        monitor.monitor_errors(interval=10, language="en")
        mock_backend.monitor_errors.assert_called_once_with(interval=10, language="en")

    def test_save_error_log(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import dobot_api.v4 as v4_mod

        mock_backend = MagicMock()
        monkeypatch.setattr(v4_mod, "RobotErrorMonitor", lambda ip: mock_backend)

        monitor = RobotErrorMonitor("192.168.1.6", protocol="v4")
        monitor.save_error_log(filename="test.log", language="en")
        mock_backend.save_error_log.assert_called_once_with(
            filename="test.log", language="en"
        )
