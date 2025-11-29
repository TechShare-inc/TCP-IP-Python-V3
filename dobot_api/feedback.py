"""Feedback API for real-time robot state data."""

from __future__ import annotations

import time

import numpy as np
from loguru import logger

from dobot_api.base import DobotApi

# NumPy structured dtype for parsing 1440-byte feedback packets
FeedbackType = np.dtype(
    [
        ("len", np.int64),
        ("digital_input_bits", np.uint64),
        ("digital_output_bits", np.uint64),
        ("robot_mode", np.uint64),
        ("time_stamp", np.uint64),
        ("time_stamp_reserve_bit", np.uint64),
        ("test_value", np.uint64),
        ("test_value_keep_bit", np.float64),
        ("speed_scaling", np.float64),
        ("linear_momentum_norm", np.float64),
        ("v_main", np.float64),
        ("v_robot", np.float64),
        ("i_robot", np.float64),
        ("i_robot_keep_bit1", np.float64),
        ("i_robot_keep_bit2", np.float64),
        ("tool_accelerometer_values", np.float64, (3,)),
        ("elbow_position", np.float64, (3,)),
        ("elbow_velocity", np.float64, (3,)),
        ("q_target", np.float64, (6,)),
        ("qd_target", np.float64, (6,)),
        ("qdd_target", np.float64, (6,)),
        ("i_target", np.float64, (6,)),
        ("m_target", np.float64, (6,)),
        ("q_actual", np.float64, (6,)),
        ("qd_actual", np.float64, (6,)),
        ("i_actual", np.float64, (6,)),
        ("actual_TCP_force", np.float64, (6,)),
        ("tool_vector_actual", np.float64, (6,)),
        ("TCP_speed_actual", np.float64, (6,)),
        ("TCP_force", np.float64, (6,)),
        ("Tool_vector_target", np.float64, (6,)),
        ("TCP_speed_target", np.float64, (6,)),
        ("motor_temperatures", np.float64, (6,)),
        ("joint_modes", np.float64, (6,)),
        ("v_actual", np.float64, (6,)),
        ("hand_type", np.byte, (4,)),
        ("user", np.byte),
        ("tool", np.byte),
        ("run_queued_cmd", np.byte),
        ("pause_cmd_flag", np.byte),
        ("velocity_ratio", np.byte),
        ("acceleration_ratio", np.byte),
        ("jerk_ratio", np.byte),
        ("xyz_velocity_ratio", np.byte),
        ("r_velocity_ratio", np.byte),
        ("xyz_acceleration_ratio", np.byte),
        ("r_acceleration_ratio", np.byte),
        ("xyz_jerk_ratio", np.byte),
        ("r_jerk_ratio", np.byte),
        ("brake_status", np.byte),
        ("enable_status", np.byte),
        ("drag_status", np.byte),
        ("running_status", np.byte),
        ("error_status", np.byte),
        ("jog_status", np.byte),
        ("robot_type", np.byte),
        ("drag_button_signal", np.byte),
        ("enable_button_signal", np.byte),
        ("record_button_signal", np.byte),
        ("reappear_button_signal", np.byte),
        ("jaw_button_signal", np.byte),
        ("six_force_online", np.byte),
        ("reserve2", np.byte, (82,)),
        ("m_actual", np.float64, (6,)),
        ("load", np.float64),
        ("center_x", np.float64),
        ("center_y", np.float64),
        ("center_z", np.float64),
        ("user[6]", np.float64, (6,)),
        ("tool[6]", np.float64, (6,)),
        ("trace_index", np.float64),
        ("six_force_value", np.float64, (6,)),
        ("target_quaternion", np.float64, (4,)),
        ("actual_quaternion", np.float64, (4,)),
        ("reserve3", np.byte, (24,)),
    ]
)

# Packet size for feedback data
FEEDBACK_PACKET_SIZE = 1440


class DobotApiFeedBack(DobotApi):
    """Feedback API for receiving real-time robot state.

    This class connects to port 30004 and receives 1440-byte packets
    containing comprehensive robot state information including:
    - Joint positions, velocities, currents, and temperatures
    - TCP position, velocity, and forces
    - Digital I/O states
    - Robot mode and status flags
    - Six-axis force sensor data

    Example:
        feedback = DobotApiFeedBack("192.168.1.6", 30004)
        while True:
            data = feedback.feedBackData()
            if data is not None:
                print(f"Joint positions: {data['q_actual']}")
                print(f"TCP position: {data['tool_vector_actual']}")

    """

    def __init__(self, ip: str, port: int, *args) -> None:
        super().__init__(ip, port, *args)
        self._last_data: np.ndarray | None = None
        self._last_recv_time = time.perf_counter()

    def feedBackData(self) -> np.ndarray | None:
        """Receive and parse robot feedback data.

        Returns:
            NumPy structured array with robot state, or None if reception failed.
            Access fields like: data['q_actual'], data['tool_vector_actual'], etc.

        Raises:
            Exception: If packet data is incomplete after retries.

        Note:
            The feedback packet is 1440 bytes. This method handles buffering
            and ensures complete packets are received.

        """
        if not self.socket_dobot:
            return None

        self.socket_dobot.setblocking(True)

        # Receive data with buffer clearing
        temp = self.socket_dobot.recv(144000)

        # If we got more than one packet, clear the buffer and try again
        if len(temp) > FEEDBACK_PACKET_SIZE:
            temp = self.socket_dobot.recv(144000)

        # Retry logic for incomplete packets
        retry_count = 0
        max_retries = 5

        while len(temp) < FEEDBACK_PACKET_SIZE and retry_count < max_retries:
            logger.debug(
                f"Incomplete packet ({len(temp)} bytes), retry {retry_count + 1}/{max_retries}"
            )
            temp = self.socket_dobot.recv(144000)
            if len(temp) >= FEEDBACK_PACKET_SIZE:
                break
            retry_count += 1

        if retry_count >= max_retries:
            logger.error(
                f"Feedback packet incomplete after {max_retries} retries - received {len(temp)} bytes"
            )
            raise Exception("Feedback packet incomplete - please check network connection")

        # Extract exactly 1440 bytes
        data = temp[:FEEDBACK_PACKET_SIZE]

        # Parse the data
        self._last_data = None
        if len(data) == FEEDBACK_PACKET_SIZE:
            self._last_data = np.frombuffer(data, dtype=FeedbackType)

        return self._last_data

    @property
    def last_data(self) -> np.ndarray | None:
        """Get the last received feedback data."""
        return self._last_data

    def get_joint_positions(self) -> np.ndarray | None:
        """Get current joint positions (convenience method).

        Returns:
            Array of 6 joint angles in degrees, or None if no data.

        """
        if self._last_data is not None:
            return self._last_data["q_actual"][0]
        return None

    def get_tcp_pose(self) -> np.ndarray | None:
        """Get current TCP pose (convenience method).

        Returns:
            Array of [x, y, z, rx, ry, rz], or None if no data.

        """
        if self._last_data is not None:
            return self._last_data["tool_vector_actual"][0]
        return None

    def get_joint_velocities(self) -> np.ndarray | None:
        """Get current joint velocities (convenience method).

        Returns:
            Array of 6 joint velocities, or None if no data.

        """
        if self._last_data is not None:
            return self._last_data["qd_actual"][0]
        return None

    def get_tcp_force(self) -> np.ndarray | None:
        """Get current TCP force (convenience method).

        Returns:
            Array of 6 force/torque values, or None if no data.

        """
        if self._last_data is not None:
            return self._last_data["TCP_force"][0]
        return None

    def is_enabled(self) -> bool | None:
        """Check if robot is enabled.

        Returns:
            True if enabled, False if not, None if no data.

        """
        if self._last_data is not None:
            return bool(self._last_data["enable_status"][0])
        return None

    def is_running(self) -> bool | None:
        """Check if robot is running a motion.

        Returns:
            True if running, False if not, None if no data.

        """
        if self._last_data is not None:
            return bool(self._last_data["running_status"][0])
        return None

    def has_error(self) -> bool | None:
        """Check if robot has an error.

        Returns:
            True if error, False if not, None if no data.

        """
        if self._last_data is not None:
            return bool(self._last_data["error_status"][0])
        return None


# Legacy alias for backward compatibility
MyType = FeedbackType
