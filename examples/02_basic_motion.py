"""Basic motion example.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-2-optional-dynamic-parameters-dyn_params
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Run a minimal motion sequence and wait for completion."""
    ip = "192.168.5.1"

    try:
        with DobotRobot(ip) as robot:
            robot.startup(speed=40)
            print(robot.acc_j(40))
            print(robot.speed_j(40))

            # Move to home pose using joint angles
            print(
                robot.joint_mov_j(
                    -11.530027, 4.636217, 87.164818, -2.841284, -77.713211, 0.010011
                )
            )
            robot.sync()

            # Small relative movement from home pose
            print(robot.rel_joint_mov_j(15, 0, 0, 0, 0, 0))
            robot.sync()

            robot.shutdown()

    except KeyboardInterrupt:
        print("Motion interrupted by user.")


if __name__ == "__main__":
    main()
