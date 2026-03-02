"""Digital/analog I/O and Modbus command mixin for DobotApiDashboard."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _IOMixin(_SerializationMixin):
    """Digital output, analog output, digital input, and Modbus commands."""

    def do_output(self, index: int, status: int) -> int:
        """Set digital signal output (queued).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("DO({:d},{:d})".format(index, status))

    def do_execute(self, index: int, status: int) -> int:
        """Set digital signal output (immediate).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("DOExecute({:d},{:d})".format(index, status))

    def tool_do(self, index: int, status: int) -> int:
        """Set terminal signal output (queued).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("ToolDO({:d},{:d})".format(index, status))

    def tool_do_execute(self, index: int, status: int) -> int:
        """Set terminal signal output (immediate).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("ToolDOExecute({:d},{:d})".format(index, status))

    def ao(self, index: int, val: float) -> int:
        """Set analog signal output (queued).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("AO({:d},{:f})".format(index, val))

    def ao_execute(self, index: int, val: float) -> int:
        """Set analog signal output (immediate).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("AOExecute({:d},{:f})".format(index, val))

    def di(self, offset1: int) -> int:
        """Read a digital input port.

        Args:
            offset1: Digital input index.

        Returns:
            Digital input state (0 or 1).
        """
        return self._recv_int("DI({:d})".format(offset1))

    def tool_di(self, offset1: int) -> int:
        """Read a terminal digital input port.

        Args:
            offset1: Terminal digital input index.

        Returns:
            Digital input state (0 or 1).
        """
        return self._recv_int("ToolDI({:d})".format(offset1))

    def do_group(self, *dyn_params: DynParam) -> int:
        """Set multiple digital outputs in one command.

        Args:
            *dyn_params: Repeating output pairs such as ``(index, status)``.

        Returns:
            Command queue ID.
        """
        string = "DOGroup("
        for params in dyn_params:
            string = string + str(params) + ","
        string = string + ")"
        logger.debug(f"DOGroup command: {string}")
        return self._recv_ack(string)

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int) -> int:
        """Create a Modbus connection.

        Args:
            ip: Modbus device IP address.
            port: Modbus device port.
            slave_id: Slave device identifier.
            is_rtu: Connection mode flag (0 for TCP, 1 for RTU).

        Returns:
            Created Modbus connection index.
        """
        return self._recv_int(
            "ModbusCreate({:s},{:d},{:d},{:d})".format(ip, port, slave_id, is_rtu)
        )

    def modbus_close(self, offset1: int) -> int:
        """Close a Modbus connection.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("ModbusClose({:d})".format(offset1))

    def get_hold_regs(
        self, id: int, addr: int, count: int, type_: str
    ) -> tuple[float, ...]:
        """Read hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to read (1-16).
            type_: Data type, such as ``"U16"``, ``"U32"``, ``"F32"``, or
                ``"F64"``.

        Returns:
            Tuple of register values as floats.
        """
        return self._recv_float_list(
            "GetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, type_)
        )

    def set_hold_regs(
        self, id: int, addr: int, count: int, table: str, type_: str | None = None
    ) -> int:
        """Write hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to write (1-16).
            table: Register data payload string.
            type_: Optional data type, such as ``"U16"``, ``"U32"``,
                ``"F32"``, or ``"F64"``.

        Returns:
            Command queue ID.
        """
        if type_ is not None:
            string = "SetHoldRegs({:d},{:d},{:d},{:s},{:s})".format(
                id, addr, count, table, type_
            )
        else:
            string = "SetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, table)
        return self._recv_ack(string)

    def get_coils(self, offset1: int, offset2: int, offset3: int) -> tuple[int, ...]:
        """Read coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.

        Returns:
            Tuple of coil values as integers.
        """
        return self._recv_int_list(
            "GetCoils({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def set_coils(self, offset1: int, offset2: int, offset3: int, offset4: int) -> int:
        """Write coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.
            offset4: Packed coil value.

        Returns:
            Command queue ID.
        """
        string = (
            "SetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3)
            + ","
            + repr(offset4)
            + ")"
        )
        logger.debug(f"SetCoils offset4 value: {offset4}")
        return self._recv_ack(string)

    def get_in_bits(self, offset1: int, offset2: int, offset3: int) -> tuple[int, ...]:
        """Read digital input bits.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Number of bits.

        Returns:
            Tuple of bit values as integers.
        """
        return self._recv_int_list(
            "GetInBits({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def get_in_regs(
        self, offset1: int, offset2: int, offset3: int, *dyn_params: DynParam
    ) -> tuple[float, ...]:
        """Read input registers.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Register count.
            *dyn_params: Optional data type and mode parameters.

        Returns:
            Tuple of register values as floats.
        """
        string = "GetInRegs({:d},{:d},{:d}".format(offset1, offset2, offset3)
        for params in dyn_params:
            logger.debug(f"GetInRegs params: type={type(params)}, value={params}")
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_float_list(string)
