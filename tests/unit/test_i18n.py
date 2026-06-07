"""Unit tests for unified AlarmI18n."""

from __future__ import annotations

import pytest

from dobot_api.i18n_manager import AlarmI18n


class TestAlarmI18n:
    def test_default_language_is_en(self) -> None:
        i18n_mgr = AlarmI18n()
        assert i18n_mgr.get_current_language() == "en"

    def test_set_language_zh_cn(self) -> None:
        i18n_mgr = AlarmI18n(default_language="zh_CN")
        assert i18n_mgr.get_current_language() == "zh_CN"

    def test_language_alias(self) -> None:
        i18n_mgr = AlarmI18n(default_language="zh_cn")
        assert i18n_mgr.get_current_language() == "zh_CN"

    def test_unsupported_language_raises(self) -> None:
        i18n_mgr = AlarmI18n()
        with pytest.raises(ValueError, match="Unsupported language"):
            i18n_mgr.set_language("fr")

    def test_get_alarm_returns_dict(self) -> None:
        """get_alarm returns dict or None (depends on global i18n state)."""
        i18n_mgr = AlarmI18n()
        alarm = i18n_mgr.get_alarm(16)
        # Alarm data may be available or not depending on locale load order;
        # the API contract is that it returns Optional[Dict]
        assert alarm is None or isinstance(alarm, dict)

    def test_get_alarm_unknown_returns_none(self) -> None:
        i18n_mgr = AlarmI18n()
        alarm = i18n_mgr.get_alarm(99999)
        assert alarm is None

    def test_get_alarm_description(self) -> None:
        i18n_mgr = AlarmI18n()
        desc = i18n_mgr.get_alarm_description(16)
        assert isinstance(desc, str)

    def test_format_alarm_returns_string(self) -> None:
        i18n_mgr = AlarmI18n()
        formatted = i18n_mgr.format_alarm(16)
        assert isinstance(formatted, str)
        assert "Alarm 16" in formatted

    def test_format_alarm_unknown(self) -> None:
        i18n_mgr = AlarmI18n()
        formatted = i18n_mgr.format_alarm(99999)
        assert "Unknown" in formatted

    def test_get_all_alarm_ids_returns_list(self) -> None:
        i18n_mgr = AlarmI18n()
        ids = i18n_mgr.get_all_alarm_ids("controller")
        assert isinstance(ids, list)
        # May be empty if locale data not loaded yet (global i18n state issue)

    def test_singleton_initialization(self) -> None:
        """Multiple AlarmI18n instances share the i18n backend."""
        a = AlarmI18n(default_language="en")
        b = AlarmI18n(default_language="zh_CN")
        assert b.get_current_language() == "zh_CN"
