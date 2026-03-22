"""System lifecycle and motion-control command mixin for DobotApiDashboard."""

from __future__ import annotations

from ._serialization import _SerializationMixin


class _SystemMixin(_SerializationMixin):
    """Robot lifecycle, script, and motion-flow commands.

    Groups: enable/disable, power, emergency stop, speed factor, robot mode,
    script control, and queued-motion flow (wait / pause / resume).
    """

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> int:
        """Enable the robot with optional payload parameters.

        Args:
            load: Payload weight.
            center_x: Payload center offset on X axis.
            center_y: Payload center offset on Y axis.
            center_z: Payload center offset on Z axis.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.enable_robot()
            >>> dashboard.enable_robot(load=0.5, center_x=0.0, center_y=0.0, center_z=0.05)
        """
        string = "EnableRobot("
        if load != 0:
            string = string + "{:f}".format(load)
            if center_x != 0 or center_y != 0 or center_z != 0:
                string = string + ",{:f},{:f},{:f}".format(center_x, center_y, center_z)
        string = string + ")"
        return self._recv_ack(string)

    def disable_robot(self) -> int:
        """Disable the robot arm.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("DisableRobot()")

    def clear_error(self) -> int:
        """Clear controller alarm information.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.clear_error()
        """
        return self._recv_ack("ClearError()")

    def reset_robot(self) -> int:
        """Stop the robot.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("ResetRobot()")

    def power_on(self) -> int:
        """Power on the robot.

        Note: Takes ~10 s before the robot is enabled after power-on.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("PowerOn()")

    def emergency_stop(self) -> int:
        """Trigger emergency stop.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("EmergencyStop()")

    def speed_factor(self, speed: int) -> int:
        """Set global speed factor.

        Args:
            speed: Rate value in range 1-100.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.speed_factor(40)
        """
        return self._recv_ack("SpeedFactor({:d})".format(speed))

    def robot_mode(self) -> int:
        """View the robot status.

        Returns:
            Robot mode value as integer.
        """
        return self._recv_int("RobotMode()")

    def run_script(self, project_name: str) -> int:
        """Run a script file.

        Args:
            project_name: Script file name.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("RunScript({:s})".format(project_name))

    def stop_script(self) -> int:
        """Stop scripts.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("StopScript()")

    def pause_script(self) -> int:
        """Pause the script.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("PauseScript()")

    def continue_script(self) -> int:
        """Continue running the script.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("ContinueScript()")

    def wait(self, t: float) -> int:
        """Wait for specified time (queued command).

        Args:
            t: Wait duration in milliseconds.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("wait({:d})".format(t))

    def pause(self) -> int:
        """Pause queued motion execution.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("pause()")

    def resume(self) -> int:
        """Resume paused motion execution.

        Note: maps to the ``continue()`` protocol command; ``continue`` is a
        Python keyword so the method is named ``resume``.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("continue()")
