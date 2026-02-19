"""Unit tests for AlarmI18n — locale loading, alarm lookups, language switching."""

from __future__ import annotations

import pytest
import i18n

from dobot_api_v3.i18n_manager import AlarmI18n

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixture: reset i18n global locale after each test to prevent leakage.
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_i18n_locale() -> None:
    """Save and restore the i18n locale after each test."""
    saved = i18n.get("locale")
    yield
    i18n.set("locale", saved)


@pytest.fixture
def alarm_en() -> AlarmI18n:
    return AlarmI18n(default_language="en")


@pytest.fixture
def alarm_zh() -> AlarmI18n:
    return AlarmI18n(default_language="zh_CN")


# ---------------------------------------------------------------------------
# Instantiation & language support
# ---------------------------------------------------------------------------


class TestInstantiation:
    def test_default_language_is_en(self, alarm_en: AlarmI18n) -> None:
        assert alarm_en.get_current_language() == "en"

    def test_default_language_zh_cn(self, alarm_zh: AlarmI18n) -> None:
        assert alarm_zh.get_current_language() == "zh_CN"

    def test_supported_languages_contains_en_and_zh(self) -> None:
        langs = AlarmI18n.get_supported_languages()
        assert "en" in langs
        assert "zh_CN" in langs

    def test_get_supported_languages_returns_copy(self) -> None:
        langs1 = AlarmI18n.get_supported_languages()
        langs1.append("fake")
        langs2 = AlarmI18n.get_supported_languages()
        assert "fake" not in langs2


# ---------------------------------------------------------------------------
# set_language
# ---------------------------------------------------------------------------


class TestSetLanguage:
    def test_set_language_en(self, alarm_en: AlarmI18n) -> None:
        alarm_en.set_language("en")
        assert alarm_en.get_current_language() == "en"

    def test_set_language_zh_cn(self, alarm_en: AlarmI18n) -> None:
        alarm_en.set_language("zh_CN")
        assert alarm_en.get_current_language() == "zh_CN"

    def test_alias_zh_cn_lowercase_accepted(self, alarm_en: AlarmI18n) -> None:
        """'zh_cn' is an alias that must not raise."""
        alarm_en.set_language("zh_cn")
        assert alarm_en.get_current_language() == "zh_CN"

    def test_unsupported_language_raises_value_error(self, alarm_en: AlarmI18n) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            alarm_en.set_language("fr")


# ---------------------------------------------------------------------------
# normalize_language_code
# ---------------------------------------------------------------------------


class TestNormalizeLanguageCode:
    def test_zh_cn_lowercase_normalised(self) -> None:
        assert AlarmI18n.normalize_language_code("zh_cn") == "zh_CN"

    def test_en_unchanged(self) -> None:
        assert AlarmI18n.normalize_language_code("en") == "en"

    def test_unknown_code_returned_as_is(self) -> None:
        assert AlarmI18n.normalize_language_code("de") == "de"


# ---------------------------------------------------------------------------
# get_alarm — structure
# ---------------------------------------------------------------------------


class TestGetAlarm:
    def test_returns_dict_with_required_keys(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(1001)
        for key in ("id", "type", "description", "cause", "solution", "level"):
            assert key in result, f"Missing key: {key}"

    def test_id_matches_input(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(1001)
        assert result["id"] == 1001

    def test_servo_alarm_type_for_high_id(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(AlarmI18n.SERVO_ID_MIN + 1)
        assert result["type"] == "servo"

    def test_controller_alarm_type_for_low_id(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(100)
        assert result["type"] == "controller"

    def test_explicit_alarm_type_overrides_auto(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(100, alarm_type="servo")
        assert result["type"] == "servo"

    def test_field_filter_returns_only_that_field(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(1001, field="description")
        assert list(result.keys()) == ["description"]

    def test_level_is_int(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(1001)
        assert isinstance(result["level"], int)

    def test_unknown_alarm_id_returns_defaults(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_alarm(99999)
        assert result["description"] == "Unknown error"
        assert result["level"] == 0


# ---------------------------------------------------------------------------
# get_controller_alarm / get_servo_alarm
# ---------------------------------------------------------------------------


class TestSpecialisedAlarmGetters:
    def test_get_controller_alarm_sets_type(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_controller_alarm(100)
        assert result["type"] == "controller"

    def test_get_servo_alarm_sets_type(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.get_servo_alarm(8001)
        assert result["type"] == "servo"


# ---------------------------------------------------------------------------
# format_alarm
# ---------------------------------------------------------------------------


class TestFormatAlarm:
    def test_returns_string(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.format_alarm(1001)
        assert isinstance(result, str)

    def test_contains_id_and_level(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.format_alarm(1001)
        assert "1001" in result

    def test_include_cause_false_omits_cause(self, alarm_en: AlarmI18n) -> None:
        result = alarm_en.format_alarm(1001, include_cause=False)
        assert "Cause:" not in result


# ---------------------------------------------------------------------------
# enrich_alarm_data
# ---------------------------------------------------------------------------


class TestEnrichAlarmData:
    def test_adds_translation_fields(self, alarm_en: AlarmI18n) -> None:
        data: dict = {"id": 1001}
        result = alarm_en.enrich_alarm_data(data)
        assert "description" in result

    def test_returns_unchanged_when_no_id(self, alarm_en: AlarmI18n) -> None:
        data: dict = {"some": "thing"}
        result = alarm_en.enrich_alarm_data(data)
        assert result == data
