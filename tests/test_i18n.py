from dobot_api.i18n_manager import AlarmI18n


def test_i18n_lookup_en_and_zh_cn():
    mgr = AlarmI18n(default_language="en")
    en_alarm = mgr.get_controller_alarm(16)
    assert "description" in en_alarm
    mgr.set_language("zh_CN")
    zh_alarm = mgr.get_controller_alarm(16)
    assert "description" in zh_alarm


def test_i18n_fallback_unknown_alarm():
    mgr = AlarmI18n(default_language="en")
    alarm = mgr.get_controller_alarm(999999)
    assert alarm["description"] in ("Unknown error", "")
