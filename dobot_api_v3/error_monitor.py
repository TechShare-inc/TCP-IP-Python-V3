"""Dashboard-based alarm monitor for Dobot V3 robots."""

from __future__ import annotations

import json
import re
import time
import warnings
from typing import Any, Dict, List, Optional

from loguru import logger

from .dashboard import DobotApiDashboard
from .i18n_manager import AlarmI18n


class RobotErrorMonitor:
    """Alarm monitor backed by an externally-supplied :class:`DobotApiDashboard`.

    The caller is responsible for the dashboard's lifecycle (opening and
    closing the connection).  ``RobotErrorMonitor`` never closes the dashboard
    it receives.

    Example::

        dashboard = DobotApiDashboard("192.168.5.1", 29999)
        monitor = RobotErrorMonitor(dashboard)
        monitor.check_errors(language="en")
        dashboard.close()
    """

    def __init__(self, dashboard: DobotApiDashboard, *, language: str = "en") -> None:
        self.dashboard = dashboard
        self.i18n = AlarmI18n(default_language=language)

    # ------------------------------------------------------------------
    # Deprecated factory — kept for backward compatibility
    # ------------------------------------------------------------------

    @classmethod
    def from_connection(
        cls,
        robot_ip: str = "192.168.200.1",
        dashboard_port: int = 29999,
    ) -> "RobotErrorMonitor":
        """Create a monitor by opening a new dashboard connection.

        .. deprecated::
            Prefer creating a :class:`~dobot_api_v3.DobotApiDashboard`
            yourself and passing it to :class:`RobotErrorMonitor` directly
            so that the same connection can be shared with other API objects.
        """
        warnings.warn(
            "RobotErrorMonitor.from_connection() is deprecated. "
            "Create a DobotApiDashboard instance and pass it to "
            "RobotErrorMonitor(dashboard) instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        dashboard = DobotApiDashboard(robot_ip, dashboard_port)
        return cls(dashboard)

    # ------------------------------------------------------------------
    # Deprecated lifecycle helpers — kept for backward compatibility
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        """No-op kept for backward compatibility.

        .. deprecated::
            Lifecycle is now the caller's responsibility.  Manage the
            :class:`DobotApiDashboard` connection yourself.
        """
        warnings.warn(
            "RobotErrorMonitor.connect() is deprecated and is now a no-op. "
            "Manage the DobotApiDashboard connection yourself.",
            DeprecationWarning,
            stacklevel=2,
        )
        return True

    def disconnect(self) -> None:
        """No-op kept for backward compatibility.

        .. deprecated::
            Lifecycle is now the caller's responsibility.  Close the
            :class:`DobotApiDashboard` yourself when done.
        """
        warnings.warn(
            "RobotErrorMonitor.disconnect() is deprecated and is now a no-op. "
            "Close the DobotApiDashboard yourself when done.",
            DeprecationWarning,
            stacklevel=2,
        )

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def get_error_info(self, language: str = "zh_CN") -> Optional[Dict[str, Any]]:
        """Get error information using dashboard.get_error_id()."""
        try:
            self.i18n.set_language(language)

            # Get error ID string from dashboard
            error_response = self.dashboard.get_error_id()
            if not error_response:
                return {"errMsg": []}

            # Parse error codes from the response using regex
            error_codes = re.findall(r"-?\d+", str(error_response))

            # Build error message list with enriched alarm data
            error_list: List[Dict[str, Any]] = []
            for error_code in error_codes:
                error_id = int(error_code)
                # Skip error code 0 (no error)
                if error_id == 0:
                    continue

                # Get alarm information from i18n system
                alarm_info = self.i18n.get_alarm(error_id)
                error_list.append(alarm_info)

            return {"errMsg": error_list}

        except Exception as exc:
            logger.error(f"Error getting error info: {exc}")
            return None

    def check_errors(self, language: str = "zh_cn") -> bool:
        info = self.get_error_info(language)
        if not info or "errMsg" not in info:
            logger.warning("Failed to fetch error information")
            return False
        errors = info["errMsg"]
        if not errors:
            logger.info("No error information")
            return False
        for idx, error in enumerate(errors, start=1):
            logger.error(
                f"Error {idx}: ID={error.get('id')} Level={error.get('level')} "
                f"Description={error.get('description')} Solution={error.get('solution')}"
            )
        return True

    def monitor_errors(self, interval: int = 5, language: str = "zh_cn") -> None:
        logger.info(f"Monitoring errors every {interval}s")
        try:
            while True:
                self.check_errors(language)
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped")

    def save_error_log(
        self, filename: Optional[str] = None, language: str = "zh_cn"
    ) -> None:
        if filename is None:
            filename = f"robot_errors_{time.strftime('%Y%m%d_%H%M%S')}.json"
        info = self.get_error_info(language)
        if not info:
            logger.warning("Unable to fetch error information")
            return
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(info, file, ensure_ascii=False, indent=2)
        logger.info(f"Saved error information to {filename}")

    def clear_robot_error(self, language: str = "zh_CN") -> bool:
        """Clear robot errors after displaying them with details.

        Args:
            language: Language for error messages (default: "zh_CN")

        Returns:
            bool: True if errors were found and cleared, False otherwise
        """
        try:
            # Get current error information
            info = self.get_error_info(language)
            if not info or "errMsg" not in info:
                logger.info("No error information to clear")
                return False

            errors = info["errMsg"]
            if not errors:
                logger.info("No errors to clear")
                return False

            # Log all errors with details
            for error in errors:
                error_id = error.get("id")
                error_type = error.get("type", "unknown")
                level = error.get("level", 0)
                description = error.get("description", "Unknown error")

                logger.warning(
                    f"Robot alarm [{error_type}] ID: {error_id}, "
                    f"Level: {level}, Description: {description}"
                )

            # Clear the errors
            clear_result = self.dashboard.clear_error()
            logger.info(f"Clear error command sent: {clear_result}")
            return True

        except Exception as exc:
            logger.error(f"Failed to clear robot error: {exc}")
            return False
