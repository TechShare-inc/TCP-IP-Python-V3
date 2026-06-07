"""Alarm internationalisation manager.

Loads locale YAML files from the unified package's ``locales/`` directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import i18n
from loguru import logger


class AlarmI18n:
    """Alarm internationalisation manager.

    Resolves alarm metadata from locale YAML files and provides
    language switching, structured alarm dictionaries, and formatted strings.

    Locale files are loaded from the ``locales/`` directory adjacent to this
    module.
    """

    SUPPORTED_LANGUAGES = ["en", "zh_CN"]
    LANGUAGE_ALIASES: Dict[str, str] = {"zh_cn": "zh_CN"}
    SERVO_ID_MIN = 8000

    _initialized: bool = False

    def __init__(self, default_language: str = "en") -> None:
        self._setup_i18n()
        self.set_language(default_language)

    # ------------------------------------------------------------------
    # i18n backend setup
    # ------------------------------------------------------------------

    @classmethod
    def _setup_i18n(cls) -> None:
        if cls._initialized:
            return
        locale_path = Path(__file__).parent / "locales"
        if not locale_path.exists():
            logger.warning(f"Locales directory not found: {locale_path}")
            return
        locale_path_str = str(locale_path)
        if locale_path_str not in i18n.load_path:
            i18n.load_path.append(locale_path_str)
        i18n.set("file_format", "yml")
        i18n.set("fallback", "en")
        i18n.set("error_on_missing_translation", False)
        i18n.set("skip_locale_root_data", True)
        cls._initialized = True

    # ------------------------------------------------------------------
    # Language management
    # ------------------------------------------------------------------

    def set_language(self, language: str) -> None:
        """Set the active language for alarm translation.

        Args:
            language: Language code to activate (``"en"`` or ``"zh_CN"``).

        Raises:
            ValueError: If the language is not supported.
        """
        normalized = self.LANGUAGE_ALIASES.get(language.lower(), language)
        if normalized not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language {language!r}; "
                f"must be one of {self.SUPPORTED_LANGUAGES}"
            )
        i18n.set("locale", normalized)

    def get_current_language(self) -> str:
        """Return the currently active language code."""
        return str(i18n.get("locale"))

    def translate(self, key: str, **kwargs: Any) -> str:
        """Translate an alarm key.

        Args:
            key: The translation key (e.g. ``"controller.16.description"``).
            **kwargs: Additional format arguments.

        Returns:
            The translated string, or ``key`` if not found.
        """
        return i18n.t(key, **kwargs)

    # ------------------------------------------------------------------
    # Alarm helpers
    # ------------------------------------------------------------------

    def get_alarm(self, alarm_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve structured alarm metadata.

        Args:
            alarm_id: The numeric alarm ID.

        Returns:
            A dict with keys ``description``, ``cause``, ``solution``,
            ``level``, or ``None`` if the alarm ID is unknown.
        """
        section = "servo" if alarm_id >= self.SERVO_ID_MIN else "controller"
        try:
            return {
                "description": self.translate(f"{section}.{alarm_id}.description"),
                "cause": self.translate(f"{section}.{alarm_id}.cause") or "",
                "solution": self.translate(f"{section}.{alarm_id}.solution") or "",
                "level": int(self.translate(f"{section}.{alarm_id}.level") or 0),
            }
        except Exception:
            return None

    def get_alarm_description(self, alarm_id: int) -> str:
        """Return a one-line alarm description."""
        section = "servo" if alarm_id >= self.SERVO_ID_MIN else "controller"
        return self.translate(f"{section}.{alarm_id}.description")

    def format_alarm(self, alarm_id: int) -> str:
        """Format an alarm as a human-readable multi-line string."""
        info = self.get_alarm(alarm_id)
        if info is None:
            return f"Alarm {alarm_id}: Unknown"
        return (
            f"Alarm {alarm_id} (level {info['level']}): {info['description']}\n"
            f"  Cause   : {info['cause'] or 'N/A'}\n"
            f"  Solution: {info['solution'] or 'N/A'}"
        )

    def get_all_alarm_ids(self, section: str = "controller") -> List[int]:
        """Return all known alarm IDs for a section."""
        try:
            data = i18n.t(f"{section}")
            if isinstance(data, dict):
                return sorted(int(k) for k in data.keys() if k.isdigit())
        except Exception:
            pass
        return []


__all__ = ["AlarmI18n"]
