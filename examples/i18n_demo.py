"""Alarm i18n usage demo."""

from dobot_api_v3 import AlarmI18n


def main() -> None:
    i18n = AlarmI18n(default_language="en")
    print(i18n.format_alarm(16))

    i18n.set_language("zh_CN")
    alarm = i18n.get_controller_alarm(16)
    print(alarm["description"])


if __name__ == "__main__":
    main()
