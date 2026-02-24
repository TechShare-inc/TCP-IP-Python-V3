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
    ) -> str:
        """Enable the robot with optional payload parameters.

        Args:
            load: Payload weight.
            center_x: Payload center offset on X axis.
            center_y: Payload center offset on Y axis.
            center_z: Payload center offset on Z axis.

        Returns:
            Robot response string.

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
        return self.send_recv_msg(string)

    def disable_robot(self) -> str:
        """Disable the robot arm."""
        return self.send_recv_msg("DisableRobot()")

    def clear_error(self) -> str:
        """Clear controller alarm information.

        Returns:
            Robot response string.

        Example:
            >>> dashboard.clear_error()
        """
        return self.send_recv_msg("ClearError()")

    def reset_robot(self) -> str:
        """Stop the robot."""
        return self.send_recv_msg("ResetRobot()")

    def power_on(self) -> str:
        """Power on the robot.

        Note: Takes ~10 s before the robot is enabled after power-on.
        """
        return self.send_recv_msg("PowerOn()")

    def emergency_stop(self) -> str:
        """Trigger emergency stop."""
        return self.send_recv_msg("EmergencyStop()")

    def speed_factor(self, speed: int) -> str:
        """Set global speed factor.

        Args:
            speed: Rate value in range 1-100.

        Returns:
            Robot response string.

        Example:
            >>> dashboard.speed_factor(40)
        """
        return self.send_recv_msg("SpeedFactor({:d})".format(speed))

    def robot_mode(self) -> str:
        """View the robot status."""
        return self.send_recv_msg("RobotMode()")

    def run_script(self, project_name: str) -> str:
        """Run a script file.

        Args:
            project_name: Script file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("RunScript({:s})".format(project_name))

    def stop_script(self) -> str:
        """Stop scripts."""
        return self.send_recv_msg("StopScript()")

    def pause_script(self) -> str:
        """Pause the script."""
        return self.send_recv_msg("PauseScript()")

    def continue_script(self) -> str:
        """Continue running the script."""
        return self.send_recv_msg("ContinueScript()")

    def wait(self, t: float) -> str:
        """Wait for specified time (queued command).

        Args:
            t: Wait duration in milliseconds.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("wait({:d})".format(t))

    def pause(self) -> str:
        """Pause queued motion execution."""
        return self.send_recv_msg("pause()")

    def resume(self) -> str:
        """Resume paused motion execution.

        Note: maps to the ``continue()`` protocol command; ``continue`` is a
        Python keyword so the method is named ``resume``.
        """
        return self.send_recv_msg("continue()")
