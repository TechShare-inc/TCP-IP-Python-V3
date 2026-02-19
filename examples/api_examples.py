"""API usage examples for dobot-api package.

This file contains examples for various API commands including:
- EnableRobot / DisableRobot
- Digital I/O control
- Motion commands (MovL, MovJ, Arc, Circle)
- Modbus communication
- Kinematics (forward/inverse)
- Trajectory execution
"""

from time import sleep

from dobot_api import DobotApiDashboard, DobotApiFeedback, DobotApiMove


def connect_robot(ip: str = "192.168.5.1"):
    """Establish connection to Dobot robot."""
    try:
        print("Connecting to robot...")
        dashboard = DobotApiDashboard(ip, 29999)
        move = DobotApiMove(ip, 30003)
        feed = DobotApiFeedback(ip, 30004)
        print("Connection successful!")
        return dashboard, move, feed
    except Exception as e:
        print("Connection failed!")
        raise e


def example_enable_disable(dashboard: DobotApiDashboard):
    """Example: Enable and disable robot."""
    # Enable without parameters
    dashboard.enable_robot()

    # Enable with load parameter
    load = 0.1
    dashboard.enable_robot(load)

    # Enable with full load parameters
    load = 0.1
    center_x = 0.1
    center_y = 0.1
    center_z = 0.1
    dashboard.enable_robot(load, center_x, center_y, center_z)

    # Disable robot
    dashboard.disable_robot()


def example_digital_io(dashboard: DobotApiDashboard):
    """Example: Digital I/O control."""
    # Set digital output (queued)
    index = 1
    status = 1
    dashboard.do_output(index, status)

    # Set digital output (immediate)
    dashboard.do_execute(index, status)

    # Set multiple digital outputs
    dashboard.do_group(1, 0, 2, 1, 3, 0)


def example_speed_acceleration(dashboard: DobotApiDashboard):
    """Example: Speed and acceleration settings."""
    # Set joint acceleration ratio
    dashboard.acc_j(50)

    # Set cartesian acceleration ratio
    dashboard.acc_l(50)

    # Set joint speed ratio
    dashboard.speed_j(50)

    # Set cartesian speed ratio
    dashboard.speed_l(50)

    # Set global speed factor
    dashboard.speed_factor(50)


def example_arm_orientation(dashboard: DobotApiDashboard):
    """Example: Set arm orientation."""
    # Single parameter
    l_or_r = 1  # 1: forward, -1: backward
    dashboard.set_arm_orientation(l_or_r)

    # Full parameters
    l_or_r = 1  # forward/backward
    u_or_d = 1  # up elbow/down elbow
    f_or_n = 1  # wrist flip
    config = 1  # sixth axis angle
    dashboard.set_arm_orientation(l_or_r, u_or_d, f_or_n, config)


def example_scripts(dashboard: DobotApiDashboard):
    """Example: Script control."""
    # Run a Lua script
    dashboard.run_script("luaname")

    # Stop script
    dashboard.stop_script()

    # Pause script
    dashboard.pause_script()

    # Continue script
    dashboard.continue_script()


def example_kinematics(dashboard: DobotApiDashboard):
    """Example: Forward and inverse kinematics."""
    # Forward kinematics (joint to cartesian)
    J1, J2, J3, J4, J5, J6 = 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
    user = 0
    tool = 0
    result = dashboard.positive_solution(J1, J2, J3, J4, J5, J6, user, tool)
    print(f"Forward kinematics result: {result}")

    # Inverse kinematics (cartesian to joint)
    x, y, z, rx, ry, rz = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0
    result = dashboard.inverse_solution(x, y, z, rx, ry, rz, user, tool)
    print(f"Inverse kinematics result: {result}")


def example_modbus(dashboard: DobotApiDashboard):
    """Example: Modbus communication."""
    # Create Modbus connection
    ip = "192.168.1.100"
    port = 502
    slave_id = 1
    is_rtu = 0  # TCP mode
    dashboard.modbus_create(ip, port, slave_id, is_rtu)

    # Read holding registers
    id = 0  # Device ID
    addr = 3095  # Starting address
    count = 1  # Number of registers
    type = "U16"  # Data type
    result = dashboard.get_hold_regs(id, addr, count, type)
    print(f"Modbus read result: {result}")

    # Close Modbus connection
    dashboard.modbus_close(0)


def example_terminal_485(dashboard: DobotApiDashboard):
    """Example: Terminal RS485 configuration."""
    # Set terminal RS485 parameters
    baud = 115200
    data_bits = 8
    parity = "N"  # None
    stop_bits = 1
    dashboard.set_terminal_485(baud, data_bits, parity, stop_bits)

    # Get terminal RS485 configuration
    result = dashboard.get_terminal_485()
    print(f"Terminal 485 config: {result}")


def example_linear_motion(move: DobotApiMove):
    """Example: Linear motion commands."""
    # Basic linear motion
    x, y, z = 300.0, 0.0, 200.0
    rx, ry, rz = 0.0, 0.0, 0.0
    move.mov_l(x, y, z, rx, ry, rz)

    # Linear motion with parameters
    move.mov_l(x, y, z, rx, ry, rz, "User=0", "Tool=0", "SpeedL=50", "AccL=50")


def example_joint_motion(move: DobotApiMove):
    """Example: Joint motion commands."""
    # Point-to-point motion (cartesian target)
    x, y, z = 300.0, 0.0, 200.0
    rx, ry, rz = 0.0, 0.0, 0.0
    move.mov_j(x, y, z, rx, ry, rz)

    # Joint motion (joint target)
    j1, j2, j3, j4, j5, j6 = 0.0, 0.0, 90.0, 0.0, 90.0, 0.0
    move.joint_mov_j(j1, j2, j3, j4, j5, j6)


def example_motion_with_io(move: DobotApiMove):
    """Example: Motion with parallel I/O control."""
    x, y, z, a, b, c = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0

    # Linear motion with I/O
    # Set DO1 high at 50% of motion
    move.mov_l_io(x, y, z, a, b, c, (0, 50, 1, 1))

    # Point-to-point motion with I/O
    # Set DO1 high at 50%, DO2 low at 1mm from target
    move.mov_j_io(x, y, z, a, b, c, (0, 50, 1, 1), (1, -1, 2, 0))


def example_arc_circle(move: DobotApiMove):
    """Example: Arc and circle motion."""
    # Arc motion through intermediate point
    # Current -> P1 (intermediate) -> P2 (end)
    x1, y1, z1 = 350.0, 50.0, 200.0
    a1, b1, c1 = 0.0, 0.0, 0.0
    x2, y2, z2 = 300.0, 100.0, 200.0
    a2, b2, c2 = 0.0, 0.0, 0.0
    move.arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2)

    # Full circle motion (3 laps)
    count = 3
    move.circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count)


def example_relative_motion(move: DobotApiMove):
    """Example: Relative motion commands."""
    # Relative linear motion
    offset_x, offset_y, offset_z = 10.0, 0.0, 0.0
    move.rel_mov_l(offset_x, offset_y, offset_z)

    # Relative joint motion
    dx, dy, dz = 10.0, 0.0, 0.0
    drx, dry, drz = 0.0, 0.0, 0.0
    move.rel_mov_j(dx, dy, dz, drx, dry, drz)

    # Relative motion in tool coordinate
    tool = 0
    move.rel_mov_j_tool(10.0, 0.0, 0.0, 0.0, 0.0, 0.0, tool)

    # Relative motion in user coordinate
    user = 0
    move.rel_mov_j_user(10.0, 0.0, 0.0, 0.0, 0.0, 0.0, user)


def example_servo_control(move: DobotApiMove):
    """Example: Servo control for dynamic following."""
    # Servo control in joint space
    j1, j2, j3, j4, j5, j6 = 0.0, 0.0, 90.0, 0.0, 90.0, 0.0
    move.servo_j(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50, gain=500)

    # Servo control in Cartesian space
    x, y, z, a, b, c = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0
    move.servo_p(x, y, z, a, b, c)


def example_jog(move: DobotApiMove):
    """Example: Jog motion control."""
    # Jog joint 1 positive
    move.move_jog("J1+")
    sleep(0.5)
    move.move_jog("")  # Stop jog

    # Jog X axis negative
    move.move_jog("X-")
    sleep(0.5)
    move.move_jog("")  # Stop jog

    # Jog with coordinate settings
    coord_type = 1  # User coordinate
    user_index = 0
    tool_index = 0
    move.move_jog("Z+", coord_type, user_index, tool_index)


def example_trajectory(move: DobotApiMove, dashboard: DobotApiDashboard):
    """Example: Trajectory execution."""
    trace_name = "trajectory.json"

    # Get trajectory start pose first
    start_pose = dashboard.get_trace_start_pose(trace_name)
    print(f"Trajectory start pose: {start_pose}")

    # Execute trajectory (Cartesian points)
    move.start_trace(trace_name)

    # Execute trajectory (joint points)
    const = 1  # Constant speed
    cart = 1  # Cartesian path
    move.start_path(trace_name, const, cart)


def example_sync(move: DobotApiMove):
    """Example: Synchronization."""
    # Queue multiple motions
    move.mov_l(300, 0, 200, 0, 0, 0)
    move.mov_l(350, 50, 200, 0, 0, 0)
    move.mov_l(300, 100, 200, 0, 0, 0)

    # Wait for all motions to complete
    move.sync()
    print("All motions completed!")


def main():
    """Main entry point demonstrating API usage."""
    dashboard, move, feed = connect_robot()

    print("\n=== Enable Robot Example ===")
    dashboard.enable_robot()
    sleep(1)

    print("\n=== Motion Examples ===")
    example_linear_motion(move)
    move.sync()

    print("\n=== Disable Robot ===")
    dashboard.disable_robot()


if __name__ == "__main__":
    main()
