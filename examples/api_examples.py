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

from dobot_api import DobotApiDashboard, DobotApiFeedBack, DobotApiMove


def connect_robot(ip: str = "192.168.5.1"):
    """Establish connection to Dobot robot."""
    try:
        print("Connecting to robot...")
        dashboard = DobotApiDashboard(ip, 29999)
        move = DobotApiMove(ip, 30003)
        feed = DobotApiFeedBack(ip, 30004)
        print("Connection successful!")
        return dashboard, move, feed
    except Exception as e:
        print("Connection failed!")
        raise e


def example_enable_disable(dashboard: DobotApiDashboard):
    """Example: Enable and disable robot."""
    # Enable without parameters
    dashboard.EnableRobot()

    # Enable with load parameter
    load = 0.1
    dashboard.EnableRobot(load)

    # Enable with full load parameters
    load = 0.1
    centerX = 0.1
    centerY = 0.1
    centerZ = 0.1
    dashboard.EnableRobot(load, centerX, centerY, centerZ)

    # Disable robot
    dashboard.DisableRobot()


def example_digital_io(dashboard: DobotApiDashboard):
    """Example: Digital I/O control."""
    # Set digital output (queued)
    index = 1
    status = 1
    dashboard.DO(index, status)

    # Set digital output (immediate)
    dashboard.DOExecute(index, status)

    # Set multiple digital outputs
    dashboard.DOGroup(1, 0, 2, 1, 3, 0)


def example_speed_acceleration(dashboard: DobotApiDashboard):
    """Example: Speed and acceleration settings."""
    # Set joint acceleration ratio
    dashboard.AccJ(50)

    # Set cartesian acceleration ratio
    dashboard.AccL(50)

    # Set joint speed ratio
    dashboard.SpeedJ(50)

    # Set cartesian speed ratio
    dashboard.SpeedL(50)

    # Set global speed factor
    dashboard.SpeedFactor(50)


def example_arm_orientation(dashboard: DobotApiDashboard):
    """Example: Set arm orientation."""
    # Single parameter
    LorR = 1  # 1: forward, -1: backward
    dashboard.SetArmOrientation(LorR)

    # Full parameters
    LorR = 1  # forward/backward
    UorD = 1  # up elbow/down elbow
    ForN = 1  # wrist flip
    Config = 1  # sixth axis angle
    dashboard.SetArmOrientation(LorR, UorD, ForN, Config)


def example_scripts(dashboard: DobotApiDashboard):
    """Example: Script control."""
    # Run a Lua script
    dashboard.RunScript("luaname")

    # Stop script
    dashboard.StopScript()

    # Pause script
    dashboard.PauseScript()

    # Continue script
    dashboard.ContinueScript()


def example_kinematics(dashboard: DobotApiDashboard):
    """Example: Forward and inverse kinematics."""
    # Forward kinematics (joint to cartesian)
    J1, J2, J3, J4, J5, J6 = 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
    user = 0
    tool = 0
    result = dashboard.PositiveSolution(J1, J2, J3, J4, J5, J6, user, tool)
    print(f"Forward kinematics result: {result}")

    # Inverse kinematics (cartesian to joint)
    x, y, z, rx, ry, rz = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0
    result = dashboard.InverseSolution(x, y, z, rx, ry, rz, user, tool)
    print(f"Inverse kinematics result: {result}")


def example_modbus(dashboard: DobotApiDashboard):
    """Example: Modbus communication."""
    # Create Modbus connection
    ip = "192.168.1.100"
    port = 502
    slave_id = 1
    isRTU = 0  # TCP mode
    dashboard.ModbusCreate(ip, port, slave_id, isRTU)

    # Read holding registers
    id = 0  # Device ID
    addr = 3095  # Starting address
    count = 1  # Number of registers
    type = "U16"  # Data type
    result = dashboard.GetHoldRegs(id, addr, count, type)
    print(f"Modbus read result: {result}")

    # Close Modbus connection
    dashboard.ModbusClose(0)


def example_terminal_485(dashboard: DobotApiDashboard):
    """Example: Terminal RS485 configuration."""
    # Set terminal RS485 parameters
    baud = 115200
    data_bits = 8
    parity = "N"  # None
    stop_bits = 1
    dashboard.SetTerminal485(baud, data_bits, parity, stop_bits)

    # Get terminal RS485 configuration
    result = dashboard.GetTerminal485()
    print(f"Terminal 485 config: {result}")


def example_linear_motion(move: DobotApiMove):
    """Example: Linear motion commands."""
    # Basic linear motion
    x, y, z = 300.0, 0.0, 200.0
    rx, ry, rz = 0.0, 0.0, 0.0
    move.MovL(x, y, z, rx, ry, rz)

    # Linear motion with parameters
    move.MovL(x, y, z, rx, ry, rz, "User=0", "Tool=0", "SpeedL=50", "AccL=50")


def example_joint_motion(move: DobotApiMove):
    """Example: Joint motion commands."""
    # Point-to-point motion (cartesian target)
    x, y, z = 300.0, 0.0, 200.0
    rx, ry, rz = 0.0, 0.0, 0.0
    move.MovJ(x, y, z, rx, ry, rz)

    # Joint motion (joint target)
    j1, j2, j3, j4, j5, j6 = 0.0, 0.0, 90.0, 0.0, 90.0, 0.0
    move.JointMovJ(j1, j2, j3, j4, j5, j6)


def example_motion_with_io(move: DobotApiMove):
    """Example: Motion with parallel I/O control."""
    x, y, z, a, b, c = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0

    # Linear motion with I/O
    # Set DO1 high at 50% of motion
    move.MovLIO(x, y, z, a, b, c, (0, 50, 1, 1))

    # Point-to-point motion with I/O
    # Set DO1 high at 50%, DO2 low at 1mm from target
    move.MovJIO(x, y, z, a, b, c, (0, 50, 1, 1), (1, -1, 2, 0))


def example_arc_circle(move: DobotApiMove):
    """Example: Arc and circle motion."""
    # Arc motion through intermediate point
    # Current -> P1 (intermediate) -> P2 (end)
    x1, y1, z1 = 350.0, 50.0, 200.0
    a1, b1, c1 = 0.0, 0.0, 0.0
    x2, y2, z2 = 300.0, 100.0, 200.0
    a2, b2, c2 = 0.0, 0.0, 0.0
    move.Arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2)

    # Full circle motion (3 laps)
    count = 3
    move.Circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count)


def example_relative_motion(move: DobotApiMove):
    """Example: Relative motion commands."""
    # Relative linear motion
    offsetX, offsetY, offsetZ = 10.0, 0.0, 0.0
    move.RelMovL(offsetX, offsetY, offsetZ)

    # Relative joint motion
    dx, dy, dz = 10.0, 0.0, 0.0
    drx, dry, drz = 0.0, 0.0, 0.0
    move.RelMovJ(dx, dy, dz, drx, dry, drz)

    # Relative motion in tool coordinate
    tool = 0
    move.RelMovJTool(10.0, 0.0, 0.0, 0.0, 0.0, 0.0, tool)

    # Relative motion in user coordinate
    user = 0
    move.RelMovJUser(10.0, 0.0, 0.0, 0.0, 0.0, 0.0, user)


def example_servo_control(move: DobotApiMove):
    """Example: Servo control for dynamic following."""
    # Servo control in joint space
    j1, j2, j3, j4, j5, j6 = 0.0, 0.0, 90.0, 0.0, 90.0, 0.0
    move.ServoJ(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50, gain=500)

    # Servo control in Cartesian space
    x, y, z, a, b, c = 300.0, 0.0, 200.0, 0.0, 0.0, 0.0
    move.ServoP(x, y, z, a, b, c)


def example_jog(move: DobotApiMove):
    """Example: Jog motion control."""
    # Jog joint 1 positive
    move.MoveJog("J1+")
    sleep(0.5)
    move.MoveJog("")  # Stop jog

    # Jog X axis negative
    move.MoveJog("X-")
    sleep(0.5)
    move.MoveJog("")  # Stop jog

    # Jog with coordinate settings
    coord_type = 1  # User coordinate
    user_index = 0
    tool_index = 0
    move.MoveJog("Z+", coord_type, user_index, tool_index)


def example_trajectory(move: DobotApiMove, dashboard: DobotApiDashboard):
    """Example: Trajectory execution."""
    trace_name = "trajectory.json"

    # Get trajectory start pose first
    start_pose = dashboard.GetTraceStartPose(trace_name)
    print(f"Trajectory start pose: {start_pose}")

    # Execute trajectory (Cartesian points)
    move.StartTrace(trace_name)

    # Execute trajectory (joint points)
    const = 1  # Constant speed
    cart = 1  # Cartesian path
    move.StartPath(trace_name, const, cart)


def example_sync(move: DobotApiMove):
    """Example: Synchronization."""
    # Queue multiple motions
    move.MovL(300, 0, 200, 0, 0, 0)
    move.MovL(350, 50, 200, 0, 0, 0)
    move.MovL(300, 100, 200, 0, 0, 0)

    # Wait for all motions to complete
    move.Sync()
    print("All motions completed!")


def main():
    """Main entry point demonstrating API usage."""
    dashboard, move, feed = connect_robot()

    print("\n=== Enable Robot Example ===")
    dashboard.EnableRobot()
    sleep(1)

    print("\n=== Motion Examples ===")
    example_linear_motion(move)
    move.Sync()

    print("\n=== Disable Robot ===")
    dashboard.DisableRobot()


if __name__ == "__main__":
    main()
