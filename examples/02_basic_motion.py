"""Basic motion example using dashboard + move ports.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-2-optional-dynamic-parameters-dyn_params
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

import time
from dobot_api_v3 import DobotApiDashboard, DobotApiMove


def main() -> None:
    """Run a minimal motion sequence and wait for completion."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)
    move = DobotApiMove(ip, 30003)

    try:
        print(dashboard.clear_error())
        print(dashboard.power_on())
        time.sleep(10)  # Wait for the robot to power on
        print(dashboard.disable_robot())
        print(dashboard.enable_robot())
        print(dashboard.speed_factor(40))
        print(dashboard.acc_j(40))
        print(dashboard.speed_j(40))

        # Move to home pose using joint angles
        print(move.joint_mov_j(-11.530027, 4.636217, 87.164818, -2.841284, -77.713211, 0.010011))
        print(move.sync())

        # Small relative movement from home pose
        print(move.rel_joint_mov_j(15, 0, 0, 0, 0, 0))
        print(move.sync())

        print(dashboard.disable_robot())

    except KeyboardInterrupt:
        print("Motion interrupted by user.")

    finally:
        move.close()
        dashboard.close()


if __name__ == "__main__":
    main()
