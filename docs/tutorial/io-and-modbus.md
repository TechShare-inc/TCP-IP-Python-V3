# I/O and Modbus

<!-- Diátaxis type: Tutorial -->

In this tutorial, we will control digital and analog I/O pins and set up a
Modbus TCP session through the dashboard subsystem. By the end you will know
how to read inputs, set outputs, and communicate with Modbus slave devices.

## Prerequisites

- Completed the [Basic Motion](./basic-motion.md) tutorial.
- Robot is connected and enabled.

## Step 1 — Set digital outputs

I/O commands are forwarded directly to `DobotRobot`, so you can call them
without going through `robot.dashboard`:

```python
from dobot_api_v3 import DobotRobot

with DobotRobot("192.168.5.1") as robot:
    robot.startup(speed=40)

    # Set digital output port 1 to HIGH
    print(robot.do_execute(1, 1))

    # Set tool digital output port 1 to HIGH
    print(robot.tool_do_execute(1, 1))
```

**Expected output:**

> ```
> DO,1,1
> ToolDO,1,1
> ```
>
> The exact response format depends on the controller firmware.

## Step 2 — Read digital inputs

```python
    # Read digital input port 1
    print(robot.di(1))

    # Read tool digital input port 1
    print(robot.tool_di(1))
```

**Expected output:**

> ```
> DI,1,{0 or 1}
> ToolDI,1,{0 or 1}
> ```

## Step 3 — Set analog output

```python
    # Set analog output port 1 to 5.0 V
    print(robot.ao_execute(1, 5.0))
```

**Expected output:**

> ```
> AO,1,5.0
> ```

## Step 4 — Modbus TCP session

We create a Modbus TCP connection to an external slave device, read and write
a holding register, then close the session:

```python
    # Create a Modbus TCP connection (slave at 192.168.1.100:502, ID 1, non-RTU)
    print(robot.modbus_create("192.168.1.100", 502, 1, 0))

    # Read one holding register at address 3095 as U16
    print(robot.get_hold_regs(0, 3095, 1, "U16"))

    # Write value 1 to holding register at address 3095
    print(robot.set_hold_regs(0, 3095, 1, "{1}", "U16"))

    # Close the Modbus connection
    print(robot.modbus_close(0))
```

**Expected output:**

> ```
> ModbusCreate,0,...
> GetHoldRegs,0,{value}
> SetHoldRegs,0,...
> ModbusClose,0,...
> ```

## Step 5 — Shut down

```python
    robot.shutdown()
```

::: tip
I/O and Modbus commands are defined in the `_IOMixin` class
(`dobot_api_v3/commands/_io_mixin.py`). See the
[API Reference](../reference/) for the full parameter list.
:::

## Next steps

- [Alarm I18n](./i18n.md) — format alarm messages in multiple languages.
- [Command Patterns](../reference/command-patterns.md) — reference for all
  argument patterns.
