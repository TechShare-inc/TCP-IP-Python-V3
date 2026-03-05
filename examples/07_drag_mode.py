"""Drag mode example.

This script demonstrates how to enable drag mode, allowing the user to manually
move the robot arm for a specified duration before disabling it.
"""

import time

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Run a drag mode sequence."""
    ip = "192.168.5.1"

    with DobotRobot(ip) as robot:
        robot.startup(speed=40)

        print("Starting drag mode. You can now move the robot manually.")
        print(robot.start_drag())

        # Allow the user to drag the robot for 10 seconds
        drag_duration = 5
        for i in range(drag_duration, 0, -1):
            print(f"Drag mode active for {i} more seconds...")
            time.sleep(1)

        print("Stopping drag mode.")
        print(robot.stop_drag())
        time.sleep(0.5)  # Short delay to ensure stop_drag command is processed
        robot.sync()  # Wait for any remaining drag mode actions to complete

        robot.shutdown()


if __name__ == "__main__":
    main()
