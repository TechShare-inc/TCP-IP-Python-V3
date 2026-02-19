"""Basic motion example using dashboard + move ports.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-2-optional-dynamic-parameters-dyn_params
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotApiDashboard, DobotApiMove


def main() -> None:
    """Run a minimal motion sequence and wait for completion."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)
    move = DobotApiMove(ip, 30003)

    try:
        print(dashboard.clear_error())
        print(dashboard.enable_robot())
        print(dashboard.speed_factor(40))
        print(dashboard.acc_j(40))
        print(dashboard.speed_j(40))

        print(move.mov_j(200, 0, 200, 0, 0, 0))
        print(move.mov_l(230, 30, 180, 0, 0, 0))
        print(move.joint_mov_j(0, 0, 60, 0, 60, 0))
        print(move.sync())

        print(dashboard.disable_robot())
    finally:
        move.close()
        dashboard.close()


if __name__ == "__main__":
    main()
