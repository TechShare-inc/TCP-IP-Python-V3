"""Digital/analog I/O and Modbus example.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Run basic I/O commands and a simple Modbus session."""
    ip = "192.168.5.1"

    with DobotRobot(ip) as robot:
        robot.startup(speed=40)

        # IO commands not forwarded at the top level — access via robot.dashboard
        print("Setting digital outputs...")
        print(robot.dashboard.do_execute(1, 1))
        print(robot.dashboard.tool_do_execute(1, 1))

        print("Reading digital inputs...")
        print(robot.dashboard.di(1))
        print(robot.dashboard.tool_di(1))

        print("Setting analog output...")
        print(robot.dashboard.ao_execute(1, 5.0))

        print("Creating Modbus TCP connection...")
        print(robot.dashboard.modbus_create("192.168.1.100", 502, 1, 0))

        print("Reading holding register...")
        print(robot.dashboard.get_hold_regs(0, 3095, 1, "U16"))

        print("Writing holding register...")
        print(robot.dashboard.set_hold_regs(0, 3095, 1, "{1}", "U16"))

        print("Closing Modbus connection...")
        print(robot.dashboard.modbus_close(0))

        robot.shutdown()


if __name__ == "__main__":
    main()
