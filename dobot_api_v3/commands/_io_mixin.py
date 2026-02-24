"""Digital/analog I/O and Modbus command mixin for DobotApiDashboard."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _IOMixin(_SerializationMixin):
    """Digital output, analog output, digital input, and Modbus commands."""

    def do_output(self, index: int, status: int) -> str:
        """Set digital signal output (queued).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DO({:d},{:d})".format(index, status))

    def do_execute(self, index: int, status: int) -> str:
        """Set digital signal output (immediate).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DOExecute({:d},{:d})".format(index, status))

    def tool_do(self, index: int, status: int) -> str:
        """Set terminal signal output (queued).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDO({:d},{:d})".format(index, status))

    def tool_do_execute(self, index: int, status: int) -> str:
        """Set terminal signal output (immediate).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDOExecute({:d},{:d})".format(index, status))

    def ao(self, index: int, val: float) -> str:
        """Set analog signal output (queued).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AO({:d},{:f})".format(index, val))

    def ao_execute(self, index: int, val: float) -> str:
        """Set analog signal output (immediate).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AOExecute({:d},{:f})".format(index, val))

    def di(self, offset1: int) -> str:
        """Read a digital input port.

        Args:
            offset1: Digital input index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DI({:d})".format(offset1))

    def tool_di(self, offset1: int) -> str:
        """Read a terminal digital input port.

        Args:
            offset1: Terminal digital input index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDI({:d})".format(offset1))

    def do_group(self, *dyn_params: DynParam) -> str:
        """Set multiple digital outputs in one command.

        Args:
            *dyn_params: Repeating output pairs such as ``(index, status)``.

        Returns:
            Robot response string.
        """
        string = "DOGroup("
        for params in dyn_params:
            string = string + str(params) + ","
        string = string + ")"
        logger.debug(f"DOGroup command: {string}")
        return self.send_recv_msg(string)

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int) -> str:
        """Create a Modbus connection.

        Args:
            ip: Modbus device IP address.
            port: Modbus device port.
            slave_id: Slave device identifier.
            is_rtu: Connection mode flag (0 for TCP, 1 for RTU).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "ModbusCreate({:s},{:d},{:d},{:d})".format(ip, port, slave_id, is_rtu)
        )

    def modbus_close(self, offset1: int) -> str:
        """Close a Modbus connection."""
        return self.send_recv_msg("ModbusClose({:d})".format(offset1))

    def get_hold_regs(self, id: int, addr: int, count: int, type_: str) -> str:
        """Read hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to read (1-16).
            type_: Data type, such as ``"U16"``, ``"U32"``, ``"F32"``, or
                ``"F64"``.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, type_)
        )

    def set_hold_regs(
        self, id: int, addr: int, count: int, table: str, type_: str | None = None
    ) -> str:
        """Write hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to write (1-16).
            table: Register data payload string.
            type_: Optional data type, such as ``"U16"``, ``"U32"``,
                ``"F32"``, or ``"F64"``.

        Returns:
            Robot response string.
        """
        if type_ is not None:
            string = "SetHoldRegs({:d},{:d},{:d},{:s},{:s})".format(
                id, addr, count, table, type_
            )
        else:
            string = "SetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, table)
        return self.send_recv_msg(string)

    def get_coils(self, offset1: int, offset2: int, offset3: int) -> str:
        """Read coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetCoils({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def set_coils(self, offset1: int, offset2: int, offset3: int, offset4: int) -> str:
        """Write coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.
            offset4: Packed coil value.

        Returns:
            Robot response string.
        """
        string = (
            "SetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3)
            + ","
            + repr(offset4)
            + ")"
        )
        logger.debug(f"SetCoils offset4 value: {offset4}")
        return self.send_recv_msg(string)

    def get_in_bits(self, offset1: int, offset2: int, offset3: int) -> str:
        """Read digital input bits.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Number of bits.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetInBits({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def get_in_regs(
        self, offset1: int, offset2: int, offset3: int, *dyn_params: DynParam
    ) -> str:
        """Read input registers.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Register count.
            *dyn_params: Optional data type and mode parameters.

        Returns:
            Robot response string.
        """
        string = "GetInRegs({:d},{:d},{:d}".format(offset1, offset2, offset3)
        for params in dyn_params:
            logger.debug(f"GetInRegs params: type={type(params)}, value={params}")
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)
