"""Basic robot connection and motion example.

This example demonstrates:
- Connecting to a Dobot robot
- Enabling the robot
- Real-time feedback monitoring
- Error handling
- Basic point-to-point motion
"""

import re
import threading
from time import sleep

from dobot_api import (
    DobotApiDashboard,
    DobotApiFeedback,
    DobotApiMove,
)

# Global state variables
current_actual = [-1]
algorithm_queue = -1
enable_status_robot = -1
robot_error_state = False
robot_mode = 0
global_lock_value = threading.Lock()


def connect_robot(ip: str = "192.168.5.1"):
    """Establish connection to Dobot robot.

    Args:
        ip: Robot IP address

    Returns:
        Tuple of (dashboard, move, feedback) API instances

    """
    try:
        print("Connecting to robot...")
        dashboard = DobotApiDashboard(ip, 29999)
        move = DobotApiMove(ip, 30003)
        feedback = DobotApiFeedback(ip, 30004)
        print("Connection successful!")
        return dashboard, move, feedback
    except Exception as e:
        print("Connection failed!")
        raise e


def run_point(move: DobotApiMove, point_list: list):
    """Move robot to specified point using linear motion."""
    move.mov_l(
        point_list[0],
        point_list[1],
        point_list[2],
        point_list[3],
        point_list[4],
        point_list[5],
    )


def get_feedback(feedback: DobotApiFeedback):
    """Continuously read robot feedback data.

    Updates global state variables with current robot status.
    """
    global current_actual, algorithm_queue, enable_status_robot
    global robot_error_state, robot_mode

    while True:
        with global_lock_value:
            feed_info = feedback.feedback_data()
            if feed_info is not None:
                # Verify data integrity
                if hex(feed_info["test_value"][0]) == "0x123456789abcdef":
                    robot_mode = feed_info["robot_mode"][0]
                    current_actual = feed_info["tool_vector_actual"][0]
                    algorithm_queue = feed_info["run_queued_cmd"][0]
                    enable_status_robot = feed_info["enable_status"][0]
                    robot_error_state = feed_info["error_status"][0]
        sleep(0.001)


def wait_arrive(point_list: list, tolerance: float = 1.0):
    """Wait for robot to arrive at specified point.

    Args:
        point_list: Target position [x, y, z, rx, ry, rz]
        tolerance: Position tolerance in mm/degrees

    """
    while True:
        is_arrive = True
        global_lock_value.acquire()
        if current_actual is not None:
            for index in range(4):
                if abs(current_actual[index] - point_list[index]) > tolerance:
                    is_arrive = False
            if is_arrive:
                global_lock_value.release()
                return
        global_lock_value.release()
        sleep(0.001)


def clear_robot_error(dashboard: DobotApiDashboard):
    """Monitor and clear robot errors.

    Continuously monitors for robot errors and provides
    user prompt to clear errors and continue operation.
    """
    global robot_error_state

    while True:
        global_lock_value.acquire()
        if robot_error_state:
            numbers = re.findall(r"-?\d+", dashboard.get_error_id())
            numbers = [int(num) for num in numbers]

            if numbers[0] == 0 and len(numbers) > 1:
                for error_id in numbers[1:]:
                    if error_id == -2:
                        print(f"Robot alarm: Collision detected (ID: {error_id})")

                # Prompt user to clear error
                choose = input("Enter 1 to clear error and continue: ")
                if int(choose) == 1:
                    dashboard.clear_error()
                    sleep(0.01)
                    dashboard.resume()
        else:
            if int(enable_status_robot) == 1 and int(algorithm_queue) == 0:
                dashboard.resume()

        global_lock_value.release()
        sleep(5)


def main():
    """Main entry point for basic connection example."""
    # Connect to robot
    dashboard, move, feedback = connect_robot()

    # Start feedback thread
    feed_thread = threading.Thread(target=get_feedback, args=(feedback,))
    feed_thread.daemon = True
    feed_thread.start()

    # Start error monitoring thread
    error_thread = threading.Thread(target=clear_robot_error, args=(dashboard,))
    error_thread.daemon = True
    error_thread.start()

    # Enable robot
    print("Enabling robot...")
    dashboard.enable_robot()
    print("Robot enabled!")

    # Define waypoints
    point_a = [148.021667, -325.570190, 1461.586304, -87.462433, 23.257524, -114.395256]
    point_b = [46.395420, -345.765656, 1463.996338, -87.583336, 22.516230, -133.578445]

    # Main loop - move between points
    print("Starting motion loop...")
    while True:
        run_point(move, point_a)
        wait_arrive(point_a)
        run_point(move, point_b)
        wait_arrive(point_b)


if __name__ == "__main__":
    main()
