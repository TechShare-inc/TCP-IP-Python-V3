"""Base classes and data types for Dobot API."""

from __future__ import annotations

import socket
import threading
from datetime import datetime
from tkinter import END, Text
from typing import Optional

import numpy as np
from loguru import logger


MyType = np.dtype(
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


class DobotApi:
    """Base TCP communication class for Dobot dashboard/move/feedback ports."""

    def __init__(self, ip: str, port: int, *args: Text) -> None:
        self.ip = ip
        self.port = port
        self.socket_dobot: Optional[socket.socket] = None
        self._global_lock = threading.Lock()
        self.text_log: Optional[Text] = args[0] if args else None
        self._connect()

    def _connect(self) -> None:
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
        """Reconnect the socket on the original endpoint."""
        self.close()
        self._connect()

    def log(self, text: str) -> None:
        if self.text_log is not None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            self.text_log.insert(END, date + text + "\n")
        else:
            logger.info(text)

    def send_data(self, string: str) -> None:
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        self.log(f"Send to {self.ip}:{self.port}: {string}")
        self.socket_dobot.send(string.encode("utf-8"))

    def wait_reply(self) -> str:
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        data = self.socket_dobot.recv(1024)
        data_str = "" if len(data) == 0 else data.decode("utf-8")
        self.log(f"Receive from {self.ip}:{self.port}: {data_str}")
        return data_str

    def send_recv_msg(self, string: str) -> str:
        with self._global_lock:
            self.send_data(string)
            return self.wait_reply()

    def close(self) -> None:
        if self.socket_dobot is not None:
            self.socket_dobot.close()
            self.socket_dobot = None

    def __del__(self) -> None:
        self.close()
