"""Alarm internationalization example.

See also:
- docs/reference/command-patterns.md#tips
"""

from dobot_api_v3 import AlarmI18n


def main() -> None:
    """Lookup and format alarms in English and Chinese."""
    i18n = AlarmI18n(default_language="en")

    print("Supported languages:", i18n.get_supported_languages())

    controller_alarm = i18n.get_controller_alarm(16)
    servo_alarm = i18n.get_servo_alarm(8000)
    print("Controller alarm (en):", controller_alarm)
    print("Servo alarm (en):", servo_alarm)

    print("Formatted controller alarm (en):")
    print(i18n.format_alarm(16, alarm_type="controller"))

    i18n.set_language("zh_CN")
    print("Formatted controller alarm (zh_CN):")
    print(i18n.format_alarm(16, alarm_type="controller"))

    enriched_alarm = i18n.enrich_alarm_data({"id": 16, "type": "controller"})
    print("Enriched alarm:", enriched_alarm)


if __name__ == "__main__":
    main()
