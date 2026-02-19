"""Internationalization manager for robot alarms."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import i18n
from loguru import logger


class AlarmI18n:
    SUPPORTED_LANGUAGES = ["en", "zh_CN"]
    LANGUAGE_ALIASES = {"zh_cn": "zh_CN"}
    SERVO_ID_MIN = 8000

    def __init__(self, default_language: str = "en") -> None:
        self._initialized = False
        self._setup_i18n()
        self.set_language(default_language)

    def _setup_i18n(self) -> None:
        if self._initialized:
            return
        locale_path = Path(__file__).parent / "locales"
        if not locale_path.exists():
            logger.warning(f"Locales directory not found: {locale_path}")
            return
        i18n.load_path.append(str(locale_path))
        i18n.set("file_format", "yml")
        i18n.set("fallback", "en")
        i18n.set("error_on_missing_translation", False)
        i18n.set("skip_locale_root_data", True)
        self._initialized = True

    def set_language(self, language: str) -> None:
        normalized = self.LANGUAGE_ALIASES.get(language.lower(), language)
        if normalized not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        i18n.set("locale", normalized)

    def get_current_language(self) -> str:
        return i18n.get("locale")

    def get_alarm(
        self,
        alarm_id: int,
        alarm_type: Optional[str] = None,
        field: Optional[str] = None,
    ) -> Dict[str, Any]:
        if alarm_type is None:
            alarm_type = "servo" if alarm_id >= self.SERVO_ID_MIN else "controller"
        base_key = f"{alarm_type}.{alarm_id}"

        if field:
            return {field: i18n.t(f"{base_key}.{field}", default="")}

        description = i18n.t(f"{base_key}.description", default="Unknown error")
        cause = i18n.t(f"{base_key}.cause", default="")
        solution = i18n.t(f"{base_key}.solution", default="")
        level_raw = i18n.t(f"{base_key}.level", default=0)
        try:
            level = int(level_raw)
        except (TypeError, ValueError):
            level = 0
        return {
            "id": alarm_id,
            "type": alarm_type,
            "description": description,
            "cause": cause,
            "solution": solution,
            "level": level,
        }

    def get_controller_alarm(self, alarm_id: int) -> Dict[str, Any]:
        return self.get_alarm(alarm_id, alarm_type="controller")

    def get_servo_alarm(self, alarm_id: int) -> Dict[str, Any]:
        return self.get_alarm(alarm_id, alarm_type="servo")

    def format_alarm(
        self,
        alarm_id: int,
        alarm_type: Optional[str] = None,
        include_cause: bool = True,
    ) -> str:
        alarm = self.get_alarm(alarm_id, alarm_type)
        lines = [f"ID {alarm['id']} [Level {alarm['level']}]: {alarm['description']}"]
        if include_cause and alarm["cause"]:
            lines.append(f"  Cause: {alarm['cause']}")
        if alarm["solution"]:
            lines.append(f"  Solution: {alarm['solution']}")
        return "\n".join(lines)

    def enrich_alarm_data(self, alarm_data: Dict[str, Any]) -> Dict[str, Any]:
        alarm_id = alarm_data.get("id")
        if alarm_id is None:
            return alarm_data
        translation = self.get_alarm(int(alarm_id))
        return {**alarm_data, **translation}

    @classmethod
    def get_supported_languages(cls) -> List[str]:
        return cls.SUPPORTED_LANGUAGES.copy()

    @classmethod
    def normalize_language_code(cls, language: str) -> str:
        normalized = cls.LANGUAGE_ALIASES.get(language.lower(), language)
        if normalized not in cls.SUPPORTED_LANGUAGES:
            logger.warning(f"Unsupported language: {language}")
        return normalized
