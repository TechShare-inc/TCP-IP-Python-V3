"""Base classes and data types for Dobot API."""

from __future__ import annotations

import dataclasses
import socket
import threading
import warnings
from typing import Optional

import numpy as np
from loguru import logger

# ---------------------------------------------------------------------------
# Feedback packet dtype.
# All field names use snake_case.  The original Dobot protocol documentation
# names are available via PROTOCOL_FIELD_MAP below.
# ---------------------------------------------------------------------------

FeedbackDtype = np.dtype(
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
        ("actual_tcp_force", np.float64, (6,)),
        ("tool_vector_actual", np.float64, (6,)),
        ("tcp_speed_actual", np.float64, (6,)),
        ("tcp_force", np.float64, (6,)),
        ("tool_vector_target", np.float64, (6,)),
        ("tcp_speed_target", np.float64, (6,)),
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
        ("user_coords", np.float64, (6,)),
        ("tool_coords", np.float64, (6,)),
        ("trace_index", np.float64),
        ("six_force_value", np.float64, (6,)),
        ("target_quaternion", np.float64, (4,)),
        ("actual_quaternion", np.float64, (4,)),
        ("reserve3", np.byte, (24,)),
    ]
)

# ---------------------------------------------------------------------------
# Protocol field name mapping — maps snake_case field names used in
# FeedbackDtype to the original names from the Dobot protocol documentation.
# ---------------------------------------------------------------------------
PROTOCOL_FIELD_MAP: dict[str, str] = {
    "actual_tcp_force": "actual_TCP_force",
    "tcp_speed_actual": "TCP_speed_actual",
    "tcp_force": "TCP_force",
    "tool_vector_target": "Tool_vector_target",
    "tcp_speed_target": "TCP_speed_target",
    "user_coords": "user[6]",
    "tool_coords": "tool[6]",
}


# ---------------------------------------------------------------------------
# Typed Python representation of a decoded feedback packet.
# Prefer this over the raw NumPy structured array for type hints and IDE
# autocompletion.  The raw decode step still uses FeedbackDtype internally.
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class FeedbackData:
    """Immutable snapshot of one decoded feedback packet (1440 bytes).

    All scalar fields are plain Python ``int`` or ``float``.  Multi-element
    fields (joint arrays, vectors, quaternions, …) are ``tuple[float, ...]``
    or ``tuple[int, ...]``.  Because the dataclass is frozen, field values
    cannot be mutated after construction — treat each instance as a read-only
    timestamped snapshot.

    Use :meth:`from_numpy` to construct a ``FeedbackData`` from the raw
    ``np.ndarray`` produced by ``np.frombuffer(buf, dtype=FeedbackDtype)``.
    For direct NumPy access call ``raw_feedback_data()`` instead of
    ``feedback_data()``.

    Attributes:
        len: Total packet length in bytes.
        digital_input_bits: Digital input bitmask.
        digital_output_bits: Digital output bitmask.
        robot_mode: Current robot mode code.
        time_stamp: Controller timestamp.
        time_stamp_reserve_bit: Reserved timestamp bits.
        test_value: Internal test value.
        test_value_keep_bit: Internal test keep bit.
        speed_scaling: Global speed scaling factor (0–1).
        linear_momentum_norm: Linear momentum magnitude.
        v_main: Main voltage (V).
        v_robot: Robot voltage (V).
        i_robot: Robot current (A).
        i_robot_keep_bit1: Reserved current field 1.
        i_robot_keep_bit2: Reserved current field 2.
        tool_accelerometer_values: Tool accelerometer XYZ (3 values).
        elbow_position: Elbow Cartesian position XYZ (3 values).
        elbow_velocity: Elbow Cartesian velocity XYZ (3 values).
        q_target: Target joint angles, radians (6 joints).
        qd_target: Target joint velocities, rad/s (6 joints).
        qdd_target: Target joint accelerations, rad/s² (6 joints).
        i_target: Target joint currents (6 joints).
        m_target: Target joint torques, N·m (6 joints).
        q_actual: Actual joint angles, radians (6 joints).
        qd_actual: Actual joint velocities, rad/s (6 joints).
        i_actual: Actual joint currents (6 joints).
        actual_tcp_force: Actual TCP force/torque (6 values).
        tool_vector_actual: Actual TCP pose [x, y, z, rx, ry, rz] (6 values).
        tcp_speed_actual: Actual TCP speed vector (6 values).
        tcp_force: TCP force/torque sensor reading (6 values).
        tool_vector_target: Target TCP pose (6 values).
        tcp_speed_target: Target TCP speed vector (6 values).
        motor_temperatures: Joint motor temperatures, °C (6 joints).
        joint_modes: Joint mode codes (6 joints).
        v_actual: Actual joint voltages (6 joints).
        hand_type: Hand type flags (4 bytes).
        user: Active user coordinate index.
        tool: Active tool coordinate index.
        run_queued_cmd: Whether queued command is running (1 = yes).
        pause_cmd_flag: Pause command flag.
        velocity_ratio: Joint velocity ratio (%).
        acceleration_ratio: Joint acceleration ratio (%).
        jerk_ratio: Joint jerk ratio (%).
        xyz_velocity_ratio: Cartesian velocity ratio (%).
        r_velocity_ratio: Rotational velocity ratio (%).
        xyz_acceleration_ratio: Cartesian acceleration ratio (%).
        r_acceleration_ratio: Rotational acceleration ratio (%).
        xyz_jerk_ratio: Cartesian jerk ratio (%).
        r_jerk_ratio: Rotational jerk ratio (%).
        brake_status: Brake status bitmask.
        enable_status: Robot enable status (1 = enabled).
        drag_status: Drag mode status.
        running_status: Motion running flag.
        error_status: Error flag (non-zero = fault present).
        jog_status: Jog mode status.
        robot_type: Robot model type code.
        drag_button_signal: Physical drag button signal.
        enable_button_signal: Physical enable button signal.
        record_button_signal: Physical record button signal.
        reappear_button_signal: Physical reappear button signal.
        jaw_button_signal: Jaw button signal.
        six_force_online: Six-axis force sensor online flag.
        reserve2: Reserved bytes (82 bytes).
        m_actual: Actual joint torques, N·m (6 joints).
        load: Payload mass, kg.
        center_x: Payload centre-of-mass X offset, mm.
        center_y: Payload centre-of-mass Y offset, mm.
        center_z: Payload centre-of-mass Z offset, mm.
        user_coords: Active user coordinate frame [x, y, z, rx, ry, rz].
        tool_coords: Active tool coordinate frame [x, y, z, rx, ry, rz].
        trace_index: Current trace index.
        six_force_value: Six-axis force sensor readings (6 values).
        target_quaternion: Target TCP orientation quaternion [w, x, y, z].
        actual_quaternion: Actual TCP orientation quaternion [w, x, y, z].
        reserve3: Reserved bytes (24 bytes).

    Example:
        >>> data = robot.feedback_data()
        >>> if data is not None:
        ...     print(data.robot_mode)
        ...     print(data.tool_vector_actual)
        ...     print(data.enable_status)
    """

    # --- Header ---
    len: int
    # --- I/O bitmasks ---
    digital_input_bits: int
    digital_output_bits: int
    # --- Mode and timing ---
    robot_mode: int
    time_stamp: int
    time_stamp_reserve_bit: int
    test_value: int
    test_value_keep_bit: float
    # --- Dynamics scalars ---
    speed_scaling: float
    linear_momentum_norm: float
    v_main: float
    v_robot: float
    i_robot: float
    i_robot_keep_bit1: float
    i_robot_keep_bit2: float
    # --- Tool and elbow vectors (3-element) ---
    tool_accelerometer_values: tuple[float, ...]
    elbow_position: tuple[float, ...]
    elbow_velocity: tuple[float, ...]
    # --- Joint target state (6 joints each) ---
    q_target: tuple[float, ...]
    qd_target: tuple[float, ...]
    qdd_target: tuple[float, ...]
    i_target: tuple[float, ...]
    m_target: tuple[float, ...]
    # --- Joint actual state (6 joints each) ---
    q_actual: tuple[float, ...]
    qd_actual: tuple[float, ...]
    i_actual: tuple[float, ...]
    # --- TCP force / pose / speed (6-element each) ---
    actual_tcp_force: tuple[float, ...]
    tool_vector_actual: tuple[float, ...]
    tcp_speed_actual: tuple[float, ...]
    tcp_force: tuple[float, ...]
    tool_vector_target: tuple[float, ...]
    tcp_speed_target: tuple[float, ...]
    # --- Thermal and mode per joint (6 joints each) ---
    motor_temperatures: tuple[float, ...]
    joint_modes: tuple[float, ...]
    v_actual: tuple[float, ...]
    # --- Hand type flags (4 bytes) ---
    hand_type: tuple[int, ...]
    # --- Coordinate / command byte flags ---
    user: int
    tool: int
    run_queued_cmd: int
    pause_cmd_flag: int
    # --- Ratio flags ---
    velocity_ratio: int
    acceleration_ratio: int
    jerk_ratio: int
    xyz_velocity_ratio: int
    r_velocity_ratio: int
    xyz_acceleration_ratio: int
    r_acceleration_ratio: int
    xyz_jerk_ratio: int
    r_jerk_ratio: int
    # --- Status flags ---
    brake_status: int
    enable_status: int
    drag_status: int
    running_status: int
    error_status: int
    jog_status: int
    robot_type: int
    drag_button_signal: int
    enable_button_signal: int
    record_button_signal: int
    reappear_button_signal: int
    jaw_button_signal: int
    six_force_online: int
    # --- Reserved ---
    reserve2: tuple[int, ...]
    # --- Actual torques and payload ---
    m_actual: tuple[float, ...]
    load: float
    center_x: float
    center_y: float
    center_z: float
    # --- Active coordinate frames ---
    user_coords: tuple[float, ...]
    tool_coords: tuple[float, ...]
    # --- Tracing and six-force ---
    trace_index: float
    six_force_value: tuple[float, ...]
    # --- Quaternions (4-element each) ---
    target_quaternion: tuple[float, ...]
    actual_quaternion: tuple[float, ...]
    # --- Reserved ---
    reserve3: tuple[int, ...]

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> FeedbackData:
        """Construct a :class:`FeedbackData` from a raw structured NumPy array.

        Args:
            arr: A 1-element NumPy structured array decoded with
                :data:`FeedbackDtype`, as returned by
                ``np.frombuffer(buf, dtype=FeedbackDtype)``.

        Returns:
            Immutable :class:`FeedbackData` snapshot with all fields converted
            to plain Python scalars or tuples.

        Example:
            >>> raw = np.frombuffer(buf, dtype=FeedbackDtype)
            >>> data = FeedbackData.from_numpy(raw)
            >>> data.robot_mode
        """
        row = arr[0]
        return cls(
            len=int(row["len"]),
            digital_input_bits=int(row["digital_input_bits"]),
            digital_output_bits=int(row["digital_output_bits"]),
            robot_mode=int(row["robot_mode"]),
            time_stamp=int(row["time_stamp"]),
            time_stamp_reserve_bit=int(row["time_stamp_reserve_bit"]),
            test_value=int(row["test_value"]),
            test_value_keep_bit=float(row["test_value_keep_bit"]),
            speed_scaling=float(row["speed_scaling"]),
            linear_momentum_norm=float(row["linear_momentum_norm"]),
            v_main=float(row["v_main"]),
            v_robot=float(row["v_robot"]),
            i_robot=float(row["i_robot"]),
            i_robot_keep_bit1=float(row["i_robot_keep_bit1"]),
            i_robot_keep_bit2=float(row["i_robot_keep_bit2"]),
            tool_accelerometer_values=tuple(row["tool_accelerometer_values"].tolist()),
            elbow_position=tuple(row["elbow_position"].tolist()),
            elbow_velocity=tuple(row["elbow_velocity"].tolist()),
            q_target=tuple(row["q_target"].tolist()),
            qd_target=tuple(row["qd_target"].tolist()),
            qdd_target=tuple(row["qdd_target"].tolist()),
            i_target=tuple(row["i_target"].tolist()),
            m_target=tuple(row["m_target"].tolist()),
            q_actual=tuple(row["q_actual"].tolist()),
            qd_actual=tuple(row["qd_actual"].tolist()),
            i_actual=tuple(row["i_actual"].tolist()),
            actual_tcp_force=tuple(row["actual_tcp_force"].tolist()),
            tool_vector_actual=tuple(row["tool_vector_actual"].tolist()),
            tcp_speed_actual=tuple(row["tcp_speed_actual"].tolist()),
            tcp_force=tuple(row["tcp_force"].tolist()),
            tool_vector_target=tuple(row["tool_vector_target"].tolist()),
            tcp_speed_target=tuple(row["tcp_speed_target"].tolist()),
            motor_temperatures=tuple(row["motor_temperatures"].tolist()),
            joint_modes=tuple(row["joint_modes"].tolist()),
            v_actual=tuple(row["v_actual"].tolist()),
            hand_type=tuple(int(b) for b in row["hand_type"].tolist()),
            user=int(row["user"]),
            tool=int(row["tool"]),
            run_queued_cmd=int(row["run_queued_cmd"]),
            pause_cmd_flag=int(row["pause_cmd_flag"]),
            velocity_ratio=int(row["velocity_ratio"]),
            acceleration_ratio=int(row["acceleration_ratio"]),
            jerk_ratio=int(row["jerk_ratio"]),
            xyz_velocity_ratio=int(row["xyz_velocity_ratio"]),
            r_velocity_ratio=int(row["r_velocity_ratio"]),
            xyz_acceleration_ratio=int(row["xyz_acceleration_ratio"]),
            r_acceleration_ratio=int(row["r_acceleration_ratio"]),
            xyz_jerk_ratio=int(row["xyz_jerk_ratio"]),
            r_jerk_ratio=int(row["r_jerk_ratio"]),
            brake_status=int(row["brake_status"]),
            enable_status=int(row["enable_status"]),
            drag_status=int(row["drag_status"]),
            running_status=int(row["running_status"]),
            error_status=int(row["error_status"]),
            jog_status=int(row["jog_status"]),
            robot_type=int(row["robot_type"]),
            drag_button_signal=int(row["drag_button_signal"]),
            enable_button_signal=int(row["enable_button_signal"]),
            record_button_signal=int(row["record_button_signal"]),
            reappear_button_signal=int(row["reappear_button_signal"]),
            jaw_button_signal=int(row["jaw_button_signal"]),
            six_force_online=int(row["six_force_online"]),
            reserve2=tuple(int(b) for b in row["reserve2"].tolist()),
            m_actual=tuple(row["m_actual"].tolist()),
            load=float(row["load"]),
            center_x=float(row["center_x"]),
            center_y=float(row["center_y"]),
            center_z=float(row["center_z"]),
            user_coords=tuple(row["user_coords"].tolist()),
            tool_coords=tuple(row["tool_coords"].tolist()),
            trace_index=float(row["trace_index"]),
            six_force_value=tuple(row["six_force_value"].tolist()),
            target_quaternion=tuple(row["target_quaternion"].tolist()),
            actual_quaternion=tuple(row["actual_quaternion"].tolist()),
            reserve3=tuple(int(b) for b in row["reserve3"].tolist()),
        )


# ---------------------------------------------------------------------------
# Deprecated alias — kept for backward compatibility.
# PEP 562: module __getattr__ emits DeprecationWarning on access.
# ---------------------------------------------------------------------------
_DEPRECATED_NAMES: dict[str, object] = {
    "MyType": FeedbackDtype,
}


def __getattr__(name: str) -> object:
    """Emit DeprecationWarning for legacy module-level names."""
    if name in _DEPRECATED_NAMES:
        warnings.warn(
            f"{name} is deprecated, use FeedbackDtype instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _DEPRECATED_NAMES[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


class DobotApi:
    """Base TCP communication class for Dobot TCP API ports.

    This class provides connection lifecycle management, message send/receive
    helpers, and thread-safe request/response behavior for the dashboard,
    movement, and feedback sockets.
    """

    def __init__(self, ip: str, port: int) -> None:
        """Initialize and connect a Dobot TCP socket.

        Args:
            ip: Robot controller IP address.
            port: Robot TCP port. Supported ports are 29999, 30003, 30004,
                30005, and 30006.

        Raises:
            ValueError: If ``port`` is not a supported Dobot TCP port.
            ConnectionError: If the socket connection fails.
        """
        self.ip = ip
        self.port = port
        self.socket_dobot: Optional[socket.socket] = None
        self._global_lock = threading.Lock()
        self._connect()

    def _connect(self) -> None:
        """Open a socket connection to the configured endpoint.

        Raises:
            ValueError: If ``self.port`` is not a supported Dobot TCP port.
            ConnectionError: If the socket connection cannot be established.
        """
        if self.port not in (29999, 30003, 30004, 30005, 30006):
            raise ValueError(f"Unsupported Dobot TCP port: {self.port}")
        try:
            self.socket_dobot = socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
        except OSError as exc:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}"
            ) from exc

    def reconnect(self) -> None:
        """Reconnect the socket to the original endpoint.

        Raises:
            ValueError: If ``self.port`` is invalid.
            ConnectionError: If reconnection fails.
        """
        self.close()
        self._connect()

    def log(self, text: str) -> None:
        """Write a log message using the project logger.

        Args:
            text: Message to emit.
        """
        logger.info(text)

    def send_data(self, string: str) -> None:
        """Send a UTF-8 command string to the robot.

        Args:
            string: Command string to send.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        self.log(f"Send to {self.ip}:{self.port}: {string}")
        self.socket_dobot.send(string.encode("utf-8"))

    def wait_reply(self) -> str:
        """Receive and decode one robot reply frame.

        Returns:
            UTF-8 decoded response string, or an empty string if the socket
            returns zero bytes.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        data = self.socket_dobot.recv(1024)
        data_str = "" if len(data) == 0 else data.decode("utf-8")
        self.log(f"Receive from {self.ip}:{self.port}: {data_str}")
        return data_str

    def send_recv_msg(self, string: str) -> str:
        """Send one command and wait for one reply atomically.

        Args:
            string: Command string to send.

        Returns:
            Decoded robot response string.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        with self._global_lock:
            self.send_data(string)
            return self.wait_reply()

    def close(self) -> None:
        """Close the socket if connected."""
        if self.socket_dobot is not None:
            self.socket_dobot.close()
            self.socket_dobot = None

    def __del__(self) -> None:
        self.close()
