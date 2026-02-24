"""Dashboard-based alarm monitor for Dobot V3 robots."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from loguru import logger

from .dashboard import DobotApiDashboard
from .i18n_manager import AlarmI18n
from .responses import ErrorIdResponse, parse_response


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
        """Initialize the error monitor.

        Args:
            dashboard: Shared dashboard client used for alarm queries and clear.
            language: Default alarm translation language.
        """
        self.dashboard = dashboard
        self.i18n = AlarmI18n(default_language=language)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def get_error_info(self, language: str = "zh_CN") -> Optional[Dict[str, Any]]:
        """Get current robot alarm information.

        Args:
            language: Alarm translation language.

        Returns:
            Dictionary in the format ``{"errMsg": [...]}``, or ``None`` when
            an unexpected exception occurs.
        """
        try:
            self.i18n.set_language(language)

            # Get error ID string from dashboard
            error_response = self.dashboard.get_error_id()
            if not error_response:
                return {"errMsg": []}

            # Parse error codes with the typed response parser
            parsed = parse_response(error_response, ErrorIdResponse)
            error_codes = list(parsed.error_ids)

            # Build error message list with enriched alarm data
            error_list: List[Dict[str, Any]] = []
            for error_id in error_codes:
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
        """Query and log all current alarms.

        Args:
            language: Alarm translation language.

        Returns:
            ``True`` if alarms are present, otherwise ``False``.
        """
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
        """Continuously poll and log robot alarms.

        Args:
            interval: Polling interval in seconds.
            language: Alarm translation language.
        """
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
        """Persist current alarm payload to a JSON file.

        Args:
            filename: Output file path. If omitted, a timestamped filename is
                generated.
            language: Alarm translation language.
        """
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
            ``True`` if errors were found and a clear command was sent,
            otherwise ``False``.
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
