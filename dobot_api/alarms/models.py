"""Data models for alarm information."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class AlarmLevel(IntEnum):
    """Alarm severity levels."""

    CRITICAL = 0  # Critical error - requires immediate attention
    SEVERE = 1  # Severe error
    WARNING = 5  # Warning - robot may continue with caution


@dataclass(frozen=True)
class LocalizedText:
    """Localized text with description, cause, and solution."""

    description: str
    cause: str = ""
    solution: str = ""


@dataclass(frozen=True)
class AlarmInfo:
    """Alarm information with bilingual support.

    Attributes:
        id: Unique alarm identifier
        level: Alarm severity level (0=critical, 5=warning)
        en: English description, cause, and solution
        zh_CN: Chinese description, cause, and solution

    """

    id: int
    level: AlarmLevel
    en: LocalizedText
    zh_CN: LocalizedText

    @classmethod
    def create(
        cls,
        id: int,
        level: int,
        en_description: str,
        en_cause: str = "",
        en_solution: str = "",
        zh_description: str = "",
        zh_cause: str = "",
        zh_solution: str = "",
    ) -> AlarmInfo:
        """Factory method to create AlarmInfo from flat parameters."""
        return cls(
            id=id,
            level=AlarmLevel(level),
            en=LocalizedText(
                description=en_description,
                cause=en_cause,
                solution=en_solution,
            ),
            zh_CN=LocalizedText(
                description=zh_description or en_description,
                cause=zh_cause or en_cause,
                solution=zh_solution or en_solution,
            ),
        )

    def get_description(self, lang: str = "en") -> str:
        """Get description in specified language."""
        if lang == "zh_CN" or lang == "zh":
            return self.zh_CN.description
        return self.en.description

    def get_solution(self, lang: str = "en") -> str:
        """Get solution in specified language."""
        if lang == "zh_CN" or lang == "zh":
            return self.zh_CN.solution
        return self.en.solution

    def get_cause(self, lang: str = "en") -> str:
        """Get cause in specified language."""
        if lang == "zh_CN" or lang == "zh":
            return self.zh_CN.cause
        return self.en.cause

    def __str__(self) -> str:
        return f"Alarm {self.id} (Level {self.level}): {self.en.description}"

    def to_dict(self) -> dict:
        """Convert to dictionary (compatible with original JSON format)."""
        return {
            "id": self.id,
            "level": int(self.level),
            "en": {
                "description": self.en.description,
                "cause": self.en.cause,
                "solution": self.en.solution,
            },
            "zh_CN": {
                "description": self.zh_CN.description,
                "cause": self.zh_CN.cause,
                "solution": self.zh_CN.solution,
            },
        }
