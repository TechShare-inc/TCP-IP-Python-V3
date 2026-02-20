"""Digital/analog I/O and Modbus example.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

import time
from dobot_api_v3 import DobotApiDashboard


def main() -> None:
    """Run basic I/O commands and a simple Modbus session."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)

    try:
        print(dashboard.clear_error())
        print(dashboard.power_on())
        time.sleep(10)  # Wait for the robot to power on
        print(dashboard.disable_robot())
        print(dashboard.enable_robot())

        print("Setting digital outputs...")
        print(dashboard.do_execute(1, 1))
        print(dashboard.tool_do_execute(1, 1))

        print("Reading digital inputs...")
        print(dashboard.di(1))
        print(dashboard.tool_di(1))

        print("Setting analog output...")
        print(dashboard.ao_execute(1, 5.0))

        print("Creating Modbus TCP connection...")
        print(dashboard.modbus_create("192.168.1.100", 502, 1, 0))

        print("Reading holding register...")
        print(dashboard.get_hold_regs(0, 3095, 1, "U16"))

        print("Writing holding register...")
        print(dashboard.set_hold_regs(0, 3095, 1, "{1}", "U16"))

        print("Closing Modbus connection...")
        print(dashboard.modbus_close(0))

        print(dashboard.disable_robot())
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
