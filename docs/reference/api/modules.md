# dobot_api_v3

Dobot API (modular V4-style architecture for V3 protocol semantics).

### *class* dobot_api_v3.DobotApi(ip, port)

Bases: `object`

Base TCP communication class for Dobot TCP API ports.

This class provides connection lifecycle management, message send/receive
helpers, and thread-safe request/response behavior for the dashboard,
movement, and feedback sockets.

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### \_\_init_\_(ip, port)

Initialize and connect a Dobot TCP socket.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **port** (*int*) – Robot TCP port. Supported ports are 29999, 30003, 30004,
    30005, and 30006.
* **Raises:**
  * **ValueError** – If `port` is not a supported Dobot TCP port.
  * **ConnectionError** – If the socket connection fails.
* **Return type:**
  None

#### reconnect()

Reconnect the socket to the original endpoint.

* **Raises:**
  * **ValueError** – If `self.port` is invalid.
  * **ConnectionError** – If reconnection fails.
* **Return type:**
  None

#### log(text)

Write a log message using the project logger.

* **Parameters:**
  **text** (*str*) – Message to emit.
* **Return type:**
  None

#### send_data(string)

Send a UTF-8 command string to the robot.

* **Parameters:**
  **string** (*str*) – Command string to send.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  None

#### wait_reply()

Receive and decode one robot reply frame.

* **Returns:**
  UTF-8 decoded response string, or an empty string if the socket
  returns zero bytes.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  str

#### send_recv_msg(string)

Send one command and wait for one reply atomically.

* **Parameters:**
  **string** (*str*) – Command string to send.
* **Returns:**
  Decoded robot response string.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  str

#### close()

Close the socket if connected.

* **Return type:**
  None

### *class* dobot_api_v3.DobotApiDashboard(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Dashboard command client for Dobot control APIs.

This class sends robot lifecycle, I/O, configuration, and status commands
over the dashboard TCP port (usually `29999`).

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### enable_robot(load=0.0, center_x=0.0, center_y=0.0, center_z=0.0)

Enable the robot with optional payload parameters.

* **Parameters:**
  * **load** (*float*) – Payload weight.
  * **center_x** (*float*) – Payload center offset on X axis.
  * **center_y** (*float*) – Payload center offset on Y axis.
  * **center_z** (*float*) – Payload center offset on Z axis.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.enable_robot()
>>> dashboard.enable_robot(load=0.5, center_x=0.0, center_y=0.0, center_z=0.05)
```

#### disable_robot()

Disable the robot.

* **Return type:**
  str

#### clear_error()

Clear controller alarm information.

* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.clear_error()
```

#### reset_robot()

Stop the robot.

* **Return type:**
  str

#### speed_factor(speed)

Set global speed factor.

* **Parameters:**
  **speed** (*int*) – Rate value in range 1-100.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.speed_factor(40)
```

#### set_user(index)

Select the calibrated user coordinate system.

* **Parameters:**
  **index** (*int*) – Calibrated user coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_tool(index)

Select the calibrated tool coordinate system.

* **Parameters:**
  **index** (*int*) – Calibrated tool coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### robot_mode()

View the robot status.

* **Return type:**
  str

#### payload(weight, inertia)

Set robot load.

* **Parameters:**
  * **weight** (*float*) – Payload weight.
  * **inertia** (*float*) – Payload moment of inertia.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_output(index, status)

Set digital signal output (queued).

* **Parameters:**
  * **index** (*int*) – Digital output index (1-24).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_execute(index, status)

Set digital signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Digital output index (1-24).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_do(index, status)

Set terminal signal output (queued).

* **Parameters:**
  * **index** (*int*) – Terminal output index (1-2).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_do_execute(index, status)

Set terminal signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Terminal output index (1-2).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### ao(index, val)

Set analog signal output (queued).

* **Parameters:**
  * **index** (*int*) – Analog output index (1-2).
  * **val** (*float*) – Output voltage (0-10).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### ao_execute(index, val)

Set analog signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Analog output index (1-2).
  * **val** (*float*) – Output voltage (0-10).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### acc_j(speed)

Set joint acceleration ratio (MovJ / MovJIO / MovJR / JointMovJ).

* **Parameters:**
  **speed** (*int*) – Joint acceleration ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### acc_l(speed)

Set Cartesian acceleration ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

* **Parameters:**
  **speed** (*int*) – Cartesian acceleration ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### speed_j(speed)

Set joint speed ratio (MovJ / MovJIO / MovJR / JointMovJ).

* **Parameters:**
  **speed** (*int*) – Joint speed ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### speed_l(speed)

Set Cartesian speed ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

* **Parameters:**
  **speed** (*int*) – Cartesian speed ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### vel_j(speed)

Alias for `speed_j()` (V4-style name).

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### vel_l(speed)

Alias for `speed_l()` (V4-style name).

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### arch(index)

Set Jump gate parameter index (start lift height, max lift, end drop).

* **Parameters:**
  **index** (*int*) – Jump parameter index (0-9).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### cp(ratio)

Set smooth transition ratio.

* **Parameters:**
  **ratio** (*int*) – Smooth transition ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### lim_z(value)

Set maximum lifting height for door-type parameters.

* **Parameters:**
  **value** (*int*) – Maximum lifting height.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_arm_orientation(r, d, n, cfg)

Set the hand command.

* **Parameters:**
  * **r** (*int*) – Forward/backward selector (1 for forward, -1 for backward).
  * **d** (*int*) – Elbow orientation (1 for up, -1 for down).
  * **n** (*int*) – Wrist flip selector (1 for no flip, -1 for flip).
  * **cfg** (*int*) – Sixth-axis angle configuration identifier.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### power_on()

Power on the robot.

Note: Takes ~10 s before the robot is enabled after power-on.

* **Return type:**
  str

#### run_script(project_name)

Run a script file.

* **Parameters:**
  **project_name** (*str*) – Script file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### stop_script()

Stop scripts.

* **Return type:**
  str

#### pause_script()

Pause the script.

* **Return type:**
  str

#### continue_script()

Continue running the script.

* **Return type:**
  str

#### get_hold_regs(id, addr, count, type_)

Read hold register.

* **Parameters:**
  * **id** (*int*) – Secondary device number (0-4, where 0 is controller slave).
  * **addr** (*int*) – Starting hold-register address (3095-4095).
  * **count** (*int*) – Number of items to read (1-16).
  * **type** – Data type, such as `"U16"`, `"U32"`, `"F32"`, or
    `"F64"`.
  * **type_** (*str*)
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_hold_regs(id, addr, count, table, type_=None)

Write hold register.

* **Parameters:**
  * **id** (*int*) – Secondary device number (0-4, where 0 is controller slave).
  * **addr** (*int*) – Starting hold-register address (3095-4095).
  * **count** (*int*) – Number of items to write (1-16).
  * **table** (*str*) – Register data payload string.
  * **type** – Optional data type, such as `"U16"`, `"U32"`,
    `"F32"`, or `"F64"`.
  * **type_** (*str* *|* *None*)
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_error_id()

Get robot error code.

* **Return type:**
  str

#### set_payload(offset1, \*dyn_params)

Set payload parameters.

* **Parameters:**
  * **offset1** (*float*) – Base payload value.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Additional payload arguments.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### positive_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool)

Run forward kinematics from joint angles to Cartesian pose.

* **Parameters:**
  * **offset1** (*float*) – Joint 1 angle.
  * **offset2** (*float*) – Joint 2 angle.
  * **offset3** (*float*) – Joint 3 angle.
  * **offset4** (*float*) – Joint 4 angle.
  * **offset5** (*float*) – Joint 5 angle.
  * **offset6** (*float*) – Joint 6 angle.
  * **user** (*int*) – User coordinate index.
  * **tool** (*int*) – Tool coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### inverse_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool, \*dyn_params)

Run inverse kinematics from Cartesian pose to joint angles.

* **Parameters:**
  * **offset1** (*float*) – X position.
  * **offset2** (*float*) – Y position.
  * **offset3** (*float*) – Z position.
  * **offset4** (*float*) – RX rotation.
  * **offset5** (*float*) – RY rotation.
  * **offset6** (*float*) – RZ rotation.
  * **user** (*int*) – User coordinate index.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional solver parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_collision_level(offset1)

Set collision detection level.

* **Parameters:**
  **offset1** (*int*) – Collision level value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_angle()

Get current joint angles.

* **Return type:**
  str

#### get_pose()

Get current Cartesian pose.

* **Return type:**
  str

#### emergency_stop()

Trigger emergency stop.

* **Return type:**
  str

#### modbus_create(ip, port, slave_id, is_rtu)

Create a Modbus connection.

* **Parameters:**
  * **ip** (*str*) – Modbus device IP address.
  * **port** (*int*) – Modbus device port.
  * **slave_id** (*int*) – Slave device identifier.
  * **is_rtu** (*int*) – Connection mode flag (0 for TCP, 1 for RTU).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### modbus_close(offset1)

Close a Modbus connection.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### set_safe_skin(offset1)

Configure safe-skin feature.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### set_obstacle_avoid(offset1)

Configure obstacle avoidance feature.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### get_trace_start_pose(offset1)

Get starting pose of a Cartesian trajectory file.

* **Parameters:**
  **offset1** (*str*) – Trajectory file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_path_start_pose(offset1)

Get starting pose of a joint path file.

* **Parameters:**
  **offset1** (*str*) – Path file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### handle_traj_points(offset1)

Process a trajectory points file.

* **Parameters:**
  **offset1** (*str*) – Trajectory file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_six_force_data()

Read six-axis force sensor data.

* **Return type:**
  str

#### set_collide_drag(offset1)

Configure collision drag mode.

* **Parameters:**
  **offset1** (*int*) – Drag mode flag.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_terminal_keys(offset1)

Configure terminal key behavior.

* **Parameters:**
  **offset1** (*int*) – Key mode value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_terminal_485(offset1, offset2, offset3, offset4)

Set terminal RS-485 parameters.

* **Parameters:**
  * **offset1** (*int*) – Baud rate.
  * **offset2** (*int*) – Data bits.
  * **offset3** (*str*) – Parity setting.
  * **offset4** (*int*) – Stop bits.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_terminal_485()

Get terminal RS-485 configuration.

* **Return type:**
  str

#### tcp_speed(offset1)

Set TCP speed.

* **Parameters:**
  **offset1** (*int*) – TCP speed value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tcp_speed_end()

End TCP speed mode.

* **Return type:**
  str

#### get_in_bits(offset1, offset2, offset3)

Read digital input bits.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Number of bits.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_in_regs(offset1, offset2, offset3, \*dyn_params)

Read input registers.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Register count.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional data type and mode parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_coils(offset1, offset2, offset3)

Read coil values.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Coil count.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_coils(offset1, offset2, offset3, offset4)

Write coil values.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Coil count.
  * **offset4** (*int*) – Packed coil value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### di(offset1)

Read a digital input port.

* **Parameters:**
  **offset1** (*int*) – Digital input index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_di(offset1)

Read a terminal digital input port.

* **Parameters:**
  **offset1** (*int*) – Terminal digital input index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_group(\*dyn_params)

Set multiple digital outputs in one command.

* **Parameters:**
  **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Repeating output pairs such as `(index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### brake_control(offset1, offset2)

Control joint brakes.

* **Parameters:**
  * **offset1** (*int*) – Joint index.
  * **offset2** (*int*) – Brake control value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_drag()

Enable drag mode.

* **Return type:**
  str

#### stop_drag()

Disable drag mode.

* **Return type:**
  str

#### load_switch(offset1)

Switch load configuration.

* **Parameters:**
  **offset1** (*int*) – Load profile index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### wait(t)

Wait for specified time (queued command).

* **Parameters:**
  **t** (*float*) – Wait duration in milliseconds.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### pause()

Pause queued motion execution.

* **Return type:**
  str

#### resume()

Resume paused motion execution.

Note: maps to the `continue()` protocol command; `continue` is a
Python keyword so the method is named `resume`.

* **Return type:**
  str

#### EnableRobot(\*args, \*\*kwargs)

* **Return type:**
  str

#### DisableRobot()

* **Return type:**
  str

#### ClearError()

* **Return type:**
  str

#### ResetRobot()

* **Return type:**
  str

#### SpeedFactor(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### User(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### Tool(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### RobotMode()

* **Return type:**
  str

#### PayLoad(weight, inertia)

* **Parameters:**
  * **weight** (*float*)
  * **inertia** (*float*)
* **Return type:**
  str

#### DO(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### DOExecute(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### ToolDO(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### ToolDOExecute(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### AO(index, val)

* **Parameters:**
  * **index** (*int*)
  * **val** (*float*)
* **Return type:**
  str

#### AOExecute(index, val)

* **Parameters:**
  * **index** (*int*)
  * **val** (*float*)
* **Return type:**
  str

#### AccJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### AccL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### SpeedJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### SpeedL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### VelJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### VelL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### Arch(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### CP(ratio)

* **Parameters:**
  **ratio** (*int*)
* **Return type:**
  str

#### LimZ(value)

* **Parameters:**
  **value** (*int*)
* **Return type:**
  str

#### SetArmOrientation(r, d, n, cfg)

* **Parameters:**
  * **r** (*int*)
  * **d** (*int*)
  * **n** (*int*)
  * **cfg** (*int*)
* **Return type:**
  str

#### PowerOn()

* **Return type:**
  str

#### RunScript(project_name)

* **Parameters:**
  **project_name** (*str*)
* **Return type:**
  str

#### StopScript()

* **Return type:**
  str

#### PauseScript()

* **Return type:**
  str

#### ContinueScript()

* **Return type:**
  str

#### GetHoldRegs(id, addr, count, type_)

* **Parameters:**
  * **id** (*int*)
  * **addr** (*int*)
  * **count** (*int*)
  * **type_** (*str*)
* **Return type:**
  str

#### SetHoldRegs(id, addr, count, table, type_=None)

* **Parameters:**
  * **id** (*int*)
  * **addr** (*int*)
  * **count** (*int*)
  * **table** (*str*)
  * **type_** (*str* *|* *None*)
* **Return type:**
  str

#### GetErrorID()

* **Return type:**
  str

#### SetPayload(offset1, \*dyn_params)

* **Parameters:**
  * **offset1** (*float*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### PositiveSolution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool)

* **Parameters:**
  * **offset1** (*float*)
  * **offset2** (*float*)
  * **offset3** (*float*)
  * **offset4** (*float*)
  * **offset5** (*float*)
  * **offset6** (*float*)
  * **user** (*int*)
  * **tool** (*int*)
* **Return type:**
  str

#### InverseSolution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool, \*dyn_params)

* **Parameters:**
  * **offset1** (*float*)
  * **offset2** (*float*)
  * **offset3** (*float*)
  * **offset4** (*float*)
  * **offset5** (*float*)
  * **offset6** (*float*)
  * **user** (*int*)
  * **tool** (*int*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### SetCollisionLevel(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### GetAngle()

* **Return type:**
  str

#### GetPose()

* **Return type:**
  str

#### EmergencyStop()

* **Return type:**
  str

#### ModbusCreate(ip, port, slave_id, isRTU)

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)
  * **slave_id** (*int*)
  * **isRTU** (*int*)
* **Return type:**
  str

#### ModbusClose(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetSafeSkin(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetObstacleAvoid(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### GetTraceStartPose(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### GetPathStartPose(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### HandleTrajPoints(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### GetSixForceData()

* **Return type:**
  str

#### SetCollideDrag(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetTerminalKeys(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetTerminal485(offset1, offset2, offset3, offset4)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*str*)
  * **offset4** (*int*)
* **Return type:**
  str

#### GetTerminal485()

* **Return type:**
  str

#### TCPSpeed(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### TCPSpeedEnd()

* **Return type:**
  str

#### GetInBits(offset1, offset2, offset3)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
* **Return type:**
  str

#### GetInRegs(offset1, offset2, offset3, \*dyn_params)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### GetCoils(offset1, offset2, offset3)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
* **Return type:**
  str

#### SetCoils(offset1, offset2, offset3, offset4)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
  * **offset4** (*int*)
* **Return type:**
  str

#### DI(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### ToolDI(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### DOGroup(\*dyn_params)

* **Parameters:**
  **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### BrakeControl(offset1, offset2)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
* **Return type:**
  str

#### StartDrag()

* **Return type:**
  str

#### StopDrag()

* **Return type:**
  str

#### LoadSwitch(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### Continue()

* **Return type:**
  str

#### Pause()

* **Return type:**
  str

#### Stop()

* **Return type:**
  str

### *class* dobot_api_v3.DobotApiMove(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Movement command client for Dobot motion APIs.

This class sends trajectory and servo commands to the move TCP port
(usually `30003`).

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### mov_j(x, y, z, rx, ry, rz, \*dyn_params)

Joint motion interface (point-to-point motion mode).

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_j(200, 0, 200, 0, 0, 0)
>>> move.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
```

#### mov_l(x, y, z, rx, ry, rz, \*dyn_params)

Linear motion interface.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_l(250, 0, 180, 0, 0, 0)
>>> move.mov_l(250, 30, 180, 0, 0, 0, "SpeedL=30", "AccL=30")
```

#### joint_mov_j(j1, j2, j3, j4, j5, j6, \*dyn_params)

Joint motion interface (joint target).

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### jump()

Placeholder for Jump command.

This method is intentionally not implemented in the current version.

* **Return type:**
  None

#### rel_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, \*dyn_params)

Relative joint offset motion (point-to-point mode).

* **Parameters:**
  * **offset1** (*float*) – Joint 1 offset.
  * **offset2** (*float*) – Joint 2 offset.
  * **offset3** (*float*) – Joint 3 offset.
  * **offset4** (*float*) – Joint 4 offset.
  * **offset5** (*float*) – Joint 5 offset.
  * **offset6** (*float*) – Joint 6 offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l(offset_x, offset_y, offset_z, \*dyn_params)

Relative Cartesian offset motion (linear mode).

* **Parameters:**
  * **offset_x** (*float*) – X-axis offset.
  * **offset_y** (*float*) – Y-axis offset.
  * **offset_z** (*float*) – Z-axis offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### mov_l_io(x, y, z, a, b, c, \*dyn_params)

Linear motion with parallel digital output control.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Parallel I/O tuples `(mode, distance, index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### mov_j_io(x, y, z, a, b, c, \*dyn_params)

Point-to-point motion with parallel digital output control.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Parallel I/O tuples `(mode, distance, index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, \*dyn_params)

Circular motion through an intermediate point.

* **Parameters:**
  * **x1** (*float*) – Intermediate point X.
  * **y1** (*float*) – Intermediate point Y.
  * **z1** (*float*) – Intermediate point Z.
  * **a1** (*float*) – Intermediate point A.
  * **b1** (*float*) – Intermediate point B.
  * **c1** (*float*) – Intermediate point C.
  * **x2** (*float*) – End point X.
  * **y2** (*float*) – End point Y.
  * **z2** (*float*) – End point Z.
  * **a2** (*float*) – End point A.
  * **b2** (*float*) – End point B.
  * **c2** (*float*) – End point C.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count, \*dyn_params)

Full-circle motion command.

* **Parameters:**
  * **x1** (*float*) – Intermediate point X.
  * **y1** (*float*) – Intermediate point Y.
  * **z1** (*float*) – Intermediate point Z.
  * **a1** (*float*) – Intermediate point A.
  * **b1** (*float*) – Intermediate point B.
  * **c1** (*float*) – Intermediate point C.
  * **x2** (*float*) – End point X.
  * **y2** (*float*) – End point Y.
  * **z2** (*float*) – End point Z.
  * **a2** (*float*) – End point A.
  * **b2** (*float*) – End point B.
  * **c2** (*float*) – End point C.
  * **count** (*int*) – Number of full rotations.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_j(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50.0, gain=500.0)

Dynamic following in joint space.

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
  * **t** (*float*) – Point run time in seconds.
  * **lookahead_time** (*float*) – Feed-forward smoothing parameter.
  * **gain** (*float*) – Servo gain parameter.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_js(j1, j2, j3, j4, j5, j6)

Dynamic following in joint space (simplified form).

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_p(x, y, z, a, b, c)

Dynamic following in Cartesian space.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### move_jog(axis_id, \*dyn_params)

Jog motion along a single axis.

* **Parameters:**
  * **axis_id** (*str*) – Axis command such as `"J1+"` or `"X-"`.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional jog parameters `(coord_type, user, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.move_jog("J1+")
>>> move.move_jog("")
```

#### start_trace(trace_name)

Execute a trajectory file (Cartesian points).

* **Parameters:**
  **trace_name** (*str*) – Trajectory file name including suffix.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_path(trace_name, const, cart)

Replay a trajectory file (joint points).

* **Parameters:**
  * **trace_name** (*str*) – Trajectory file name including suffix.
  * **const** (*int*) – Constant-speed mode flag.
  * **cart** (*int*) – Cartesian/joint path flag.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_fc_trace(trace_name)

Execute a trajectory file with force control (Cartesian points).

* **Parameters:**
  **trace_name** (*str*) – Trajectory file name including suffix.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### sync()

Block until all queued commands have been executed.

* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_j(200, 0, 200, 0, 0, 0)
>>> move.mov_l(220, 20, 180, 0, 0, 0)
>>> move.sync()
```

#### rel_mov_j_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, \*dyn_params)

Relative joint motion along the tool coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in tool frame.
  * **offset_y** (*float*) – Y offset in tool frame.
  * **offset_z** (*float*) – Z offset in tool frame.
  * **offset_rx** (*float*) – RX offset in tool frame.
  * **offset_ry** (*float*) – RY offset in tool frame.
  * **offset_rz** (*float*) – RZ offset in tool frame.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*tuple* *[**int* *,* *int* *,* *int* *]*) – Optional tuples `(speed_j, acc_j, user)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, \*dyn_params)

Relative linear motion along the tool coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in tool frame.
  * **offset_y** (*float*) – Y offset in tool frame.
  * **offset_z** (*float*) – Z offset in tool frame.
  * **offset_rx** (*float*) – RX offset in tool frame.
  * **offset_ry** (*float*) – RY offset in tool frame.
  * **offset_rz** (*float*) – RZ offset in tool frame.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*tuple* *[**int* *,* *int* *,* *int* *]*) – Optional tuples `(speed_l, acc_l, user)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_j_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, \*dyn_params)

Relative joint motion along the user coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in user frame.
  * **offset_y** (*float*) – Y offset in user frame.
  * **offset_z** (*float*) – Z offset in user frame.
  * **offset_rx** (*float*) – RX offset in user frame.
  * **offset_ry** (*float*) – RY offset in user frame.
  * **offset_rz** (*float*) – RZ offset in user frame.
  * **user** (*int*) – User coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples `(speed_j, acc_j, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, \*dyn_params)

Relative linear motion along the user coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in user frame.
  * **offset_y** (*float*) – Y offset in user frame.
  * **offset_z** (*float*) – Z offset in user frame.
  * **offset_rx** (*float*) – RX offset in user frame.
  * **offset_ry** (*float*) – RY offset in user frame.
  * **offset_rz** (*float*) – RZ offset in user frame.
  * **user** (*int*) – User coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples `(speed_l, acc_l, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_joint_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, \*dyn_params)

Relative motion along each joint axis (joint motion mode).

* **Parameters:**
  * **offset1** (*float*) – Joint 1 offset.
  * **offset2** (*float*) – Joint 2 offset.
  * **offset3** (*float*) – Joint 3 offset.
  * **offset4** (*float*) – Joint 4 offset.
  * **offset5** (*float*) – Joint 5 offset.
  * **offset6** (*float*) – Joint 6 offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples such as `(speed_j, acc_j)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### MovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### MovL(\*args, \*\*kwargs)

* **Return type:**
  str

#### JointMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### Jump()

* **Return type:**
  None

#### RelMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovL(offsetX, offsetY, offsetZ, \*dyn_params)

* **Parameters:**
  * **offsetX** (*float*)
  * **offsetY** (*float*)
  * **offsetZ** (*float*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### MovLIO(\*args, \*\*kwargs)

* **Return type:**
  str

#### MovJIO(\*args, \*\*kwargs)

* **Return type:**
  str

#### Arc(\*args, \*\*kwargs)

* **Return type:**
  str

#### Circle3(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoJS(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoP(\*args, \*\*kwargs)

* **Return type:**
  str

#### MoveJog(\*args, \*\*kwargs)

* **Return type:**
  str

#### StartTrace(trace_name)

* **Parameters:**
  **trace_name** (*str*)
* **Return type:**
  str

#### StartPath(trace_name, const, cart)

* **Parameters:**
  * **trace_name** (*str*)
  * **const** (*int*)
  * **cart** (*int*)
* **Return type:**
  str

#### StartFCTrace(trace_name)

* **Parameters:**
  **trace_name** (*str*)
* **Return type:**
  str

#### Sync()

* **Return type:**
  str

#### RelMovJTool(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovLTool(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovJUser(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovLUser(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelJointMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

### *class* dobot_api_v3.DobotApiFeedback(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Feedback interface for reading 1440-byte robot status packets.

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### \_\_init_\_(ip, port)

Initialize the feedback socket client.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **port** (*int*) – Feedback TCP port, usually `30004`.
* **Raises:**
  * **ValueError** – If `port` is unsupported.
  * **ConnectionError** – If the socket connection fails.
* **Return type:**
  None

#### feedback_data()

Read one feedback frame and parse it with `FeedbackDtype`.

* **Returns:**
  A NumPy structured array of length 1 when a valid 1440-byte frame
  is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  *ndarray* | None

#### feedBackData()

Deprecated alias for `feedback_data()`.

* **Returns:**
  Same value as `feedback_data()`.
* **Return type:**
  *ndarray* | None

### *class* dobot_api_v3.RobotErrorMonitor(dashboard, \*, language='en')

Bases: `object`

Alarm monitor backed by an externally-supplied `DobotApiDashboard`.

The caller is responsible for the dashboard’s lifecycle (opening and
closing the connection).  `RobotErrorMonitor` never closes the dashboard
it receives.

Example:

```default
dashboard = DobotApiDashboard("192.168.5.1", 29999)
monitor = RobotErrorMonitor(dashboard)
monitor.check_errors(language="en")
dashboard.close()
```

* **Parameters:**
  * **dashboard** ([*DobotApiDashboard*](#dobot_api_v3.dashboard.DobotApiDashboard))
  * **language** (*str*)

#### \_\_init_\_(dashboard, \*, language='en')

Initialize the error monitor.

* **Parameters:**
  * **dashboard** ([*DobotApiDashboard*](#dobot_api_v3.dashboard.DobotApiDashboard)) – Shared dashboard client used for alarm queries and clear.
  * **language** (*str*) – Default alarm translation language.
* **Return type:**
  None

#### *classmethod* from_connection(robot_ip='192.168.200.1', dashboard_port=29999)

Create a monitor by opening a new dashboard connection.

* **Parameters:**
  * **robot_ip** (*str*) – Robot controller IP address.
  * **dashboard_port** (*int*) – Dashboard TCP port.
* **Returns:**
  New monitor instance bound to a newly created dashboard client.
* **Return type:**
  [*RobotErrorMonitor*](#dobot_api_v3.error_monitor.RobotErrorMonitor)

#### Deprecated
Deprecated since version Prefer: creating a `DobotApiDashboard`
yourself and passing it to `RobotErrorMonitor` directly
so that the same connection can be shared with other API objects.

#### connect()

No-op kept for backward compatibility.

* **Returns:**
  Always `True`.
* **Return type:**
  bool

#### Deprecated
Deprecated since version Lifecycle: is now the caller’s responsibility.  Manage the
`DobotApiDashboard` connection yourself.

#### disconnect()

No-op kept for backward compatibility.

#### Deprecated
Deprecated since version Lifecycle: is now the caller’s responsibility.  Close the
`DobotApiDashboard` yourself when done.

* **Return type:**
  None

#### get_error_info(language='zh_CN')

Get current robot alarm information.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  Dictionary in the format `{"errMsg": [...]}`, or `None` when
  an unexpected exception occurs.
* **Return type:**
  *Dict*[str, *Any*] | None

#### check_errors(language='zh_cn')

Query and log all current alarms.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  `True` if alarms are present, otherwise `False`.
* **Return type:**
  bool

#### monitor_errors(interval=5, language='zh_cn')

Continuously poll and log robot alarms.

* **Parameters:**
  * **interval** (*int*) – Polling interval in seconds.
  * **language** (*str*) – Alarm translation language.
* **Return type:**
  None

#### save_error_log(filename=None, language='zh_cn')

Persist current alarm payload to a JSON file.

* **Parameters:**
  * **filename** (*str* *|* *None*) – Output file path. If omitted, a timestamped filename is
    generated.
  * **language** (*str*) – Alarm translation language.
* **Return type:**
  None

#### clear_robot_error(language='zh_CN')

Clear robot errors after displaying them with details.

* **Parameters:**
  **language** (*str*) – Language for error messages (default: “zh_CN”)
* **Returns:**
  `True` if errors were found and a clear command was sent,
  otherwise `False`.
* **Return type:**
  bool

### *class* dobot_api_v3.AlarmI18n(default_language='en')

Bases: `object`

Alarm internationalization manager.

This helper resolves alarm metadata from locale YAML files and provides
language switching, structured alarm dictionaries, and formatted strings.

* **Parameters:**
  **default_language** (*str*)

#### SUPPORTED_LANGUAGES *= ['en', 'zh_CN']*

#### LANGUAGE_ALIASES *= {'zh_cn': 'zh_CN'}*

#### SERVO_ID_MIN *= 8000*

#### \_\_init_\_(default_language='en')

Initialize the i18n backend and set the active language.

* **Parameters:**
  **default_language** (*str*) – Initial language code, such as `"en"` or
  `"zh_CN"`.
* **Raises:**
  **ValueError** – If `default_language` is not supported.
* **Return type:**
  None

#### set_language(language)

Set the active language for alarm translation.

* **Parameters:**
  **language** (*str*) – Language code to activate.
* **Raises:**
  **ValueError** – If `language` is not in supported languages.
* **Return type:**
  None

#### get_current_language()

Get the current active language code.

* **Returns:**
  Active language code stored in the i18n backend.
* **Return type:**
  str

#### get_alarm(alarm_id, alarm_type=None, field=None)

Get localized alarm data.

* **Parameters:**
  * **alarm_id** (*int*) – Alarm identifier.
  * **alarm_type** (*str* *|* *None*) – Alarm category. If omitted, it is inferred from
    `alarm_id` using `SERVO_ID_MIN`.
  * **field** (*str* *|* *None*) – Optional single field name to return.
* **Returns:**
  Alarm dictionary containing translated fields. When `field` is
  provided, returns `{field: value}`.
* **Return type:**
  *Dict*[str, *Any*]

#### get_controller_alarm(alarm_id)

Get localized controller alarm data.

* **Parameters:**
  **alarm_id** (*int*) – Controller alarm identifier.
* **Returns:**
  Localized alarm dictionary.
* **Return type:**
  *Dict*[str, *Any*]

#### get_servo_alarm(alarm_id)

Get localized servo alarm data.

* **Parameters:**
  **alarm_id** (*int*) – Servo alarm identifier.
* **Returns:**
  Localized alarm dictionary.
* **Return type:**
  *Dict*[str, *Any*]

#### format_alarm(alarm_id, alarm_type=None, include_cause=True)

Format one alarm into a human-readable multi-line string.

* **Parameters:**
  * **alarm_id** (*int*) – Alarm identifier.
  * **alarm_type** (*str* *|* *None*) – Optional explicit alarm category.
  * **include_cause** (*bool*) – Whether to include the translated cause line.
* **Returns:**
  Formatted alarm text.
* **Return type:**
  str

#### enrich_alarm_data(alarm_data)

Merge translated alarm metadata into an existing alarm payload.

* **Parameters:**
  **alarm_data** (*Dict* *[**str* *,* *Any* *]*) – Alarm payload that may contain at least `id`.
* **Returns:**
  A merged dictionary with translated alarm fields when `id` is
  present; otherwise the original `alarm_data`.
* **Return type:**
  *Dict*[str, *Any*]

#### *classmethod* get_supported_languages()

Get supported language codes.

* **Returns:**
  Copy of supported language list.
* **Return type:**
  *List*[str]

#### *classmethod* normalize_language_code(language)

Normalize a language code using alias mapping.

* **Parameters:**
  **language** (*str*) – Raw language code.
* **Returns:**
  Normalized language code. Unsupported codes are returned unchanged
  and logged as warnings.
* **Return type:**
  str

### dobot_api_v3.DobotApiFeedBack

alias of [`DobotApiFeedback`](#dobot_api_v3.feedback.DobotApiFeedback)

<a id="module-dobot_api_v3.base"></a>

Base classes and data types for Dobot API.

### *class* dobot_api_v3.base.DobotApi(ip, port)

Bases: `object`

Base TCP communication class for Dobot TCP API ports.

This class provides connection lifecycle management, message send/receive
helpers, and thread-safe request/response behavior for the dashboard,
movement, and feedback sockets.

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### \_\_init_\_(ip, port)

Initialize and connect a Dobot TCP socket.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **port** (*int*) – Robot TCP port. Supported ports are 29999, 30003, 30004,
    30005, and 30006.
* **Raises:**
  * **ValueError** – If `port` is not a supported Dobot TCP port.
  * **ConnectionError** – If the socket connection fails.
* **Return type:**
  None

#### reconnect()

Reconnect the socket to the original endpoint.

* **Raises:**
  * **ValueError** – If `self.port` is invalid.
  * **ConnectionError** – If reconnection fails.
* **Return type:**
  None

#### log(text)

Write a log message using the project logger.

* **Parameters:**
  **text** (*str*) – Message to emit.
* **Return type:**
  None

#### send_data(string)

Send a UTF-8 command string to the robot.

* **Parameters:**
  **string** (*str*) – Command string to send.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  None

#### wait_reply()

Receive and decode one robot reply frame.

* **Returns:**
  UTF-8 decoded response string, or an empty string if the socket
  returns zero bytes.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  str

#### send_recv_msg(string)

Send one command and wait for one reply atomically.

* **Parameters:**
  **string** (*str*) – Command string to send.
* **Returns:**
  Decoded robot response string.
* **Raises:**
  **RuntimeError** – If the socket is not connected.
* **Return type:**
  str

#### close()

Close the socket if connected.

* **Return type:**
  None

<a id="module-dobot_api_v3.dashboard"></a>

Dashboard/control commands for Dobot API.

### *class* dobot_api_v3.dashboard.DobotApiDashboard(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Dashboard command client for Dobot control APIs.

This class sends robot lifecycle, I/O, configuration, and status commands
over the dashboard TCP port (usually `29999`).

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### enable_robot(load=0.0, center_x=0.0, center_y=0.0, center_z=0.0)

Enable the robot with optional payload parameters.

* **Parameters:**
  * **load** (*float*) – Payload weight.
  * **center_x** (*float*) – Payload center offset on X axis.
  * **center_y** (*float*) – Payload center offset on Y axis.
  * **center_z** (*float*) – Payload center offset on Z axis.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.enable_robot()
>>> dashboard.enable_robot(load=0.5, center_x=0.0, center_y=0.0, center_z=0.05)
```

#### disable_robot()

Disable the robot.

* **Return type:**
  str

#### clear_error()

Clear controller alarm information.

* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.clear_error()
```

#### reset_robot()

Stop the robot.

* **Return type:**
  str

#### speed_factor(speed)

Set global speed factor.

* **Parameters:**
  **speed** (*int*) – Rate value in range 1-100.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> dashboard.speed_factor(40)
```

#### set_user(index)

Select the calibrated user coordinate system.

* **Parameters:**
  **index** (*int*) – Calibrated user coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_tool(index)

Select the calibrated tool coordinate system.

* **Parameters:**
  **index** (*int*) – Calibrated tool coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### robot_mode()

View the robot status.

* **Return type:**
  str

#### payload(weight, inertia)

Set robot load.

* **Parameters:**
  * **weight** (*float*) – Payload weight.
  * **inertia** (*float*) – Payload moment of inertia.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_output(index, status)

Set digital signal output (queued).

* **Parameters:**
  * **index** (*int*) – Digital output index (1-24).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_execute(index, status)

Set digital signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Digital output index (1-24).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_do(index, status)

Set terminal signal output (queued).

* **Parameters:**
  * **index** (*int*) – Terminal output index (1-2).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_do_execute(index, status)

Set terminal signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Terminal output index (1-2).
  * **status** (*int*) – Output state (0 for low, 1 for high).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### ao(index, val)

Set analog signal output (queued).

* **Parameters:**
  * **index** (*int*) – Analog output index (1-2).
  * **val** (*float*) – Output voltage (0-10).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### ao_execute(index, val)

Set analog signal output (immediate).

* **Parameters:**
  * **index** (*int*) – Analog output index (1-2).
  * **val** (*float*) – Output voltage (0-10).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### acc_j(speed)

Set joint acceleration ratio (MovJ / MovJIO / MovJR / JointMovJ).

* **Parameters:**
  **speed** (*int*) – Joint acceleration ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### acc_l(speed)

Set Cartesian acceleration ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

* **Parameters:**
  **speed** (*int*) – Cartesian acceleration ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### speed_j(speed)

Set joint speed ratio (MovJ / MovJIO / MovJR / JointMovJ).

* **Parameters:**
  **speed** (*int*) – Joint speed ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### speed_l(speed)

Set Cartesian speed ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

* **Parameters:**
  **speed** (*int*) – Cartesian speed ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### vel_j(speed)

Alias for [`speed_j()`](#dobot_api_v3.dashboard.DobotApiDashboard.speed_j) (V4-style name).

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### vel_l(speed)

Alias for [`speed_l()`](#dobot_api_v3.dashboard.DobotApiDashboard.speed_l) (V4-style name).

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### arch(index)

Set Jump gate parameter index (start lift height, max lift, end drop).

* **Parameters:**
  **index** (*int*) – Jump parameter index (0-9).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### cp(ratio)

Set smooth transition ratio.

* **Parameters:**
  **ratio** (*int*) – Smooth transition ratio (1-100).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### lim_z(value)

Set maximum lifting height for door-type parameters.

* **Parameters:**
  **value** (*int*) – Maximum lifting height.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_arm_orientation(r, d, n, cfg)

Set the hand command.

* **Parameters:**
  * **r** (*int*) – Forward/backward selector (1 for forward, -1 for backward).
  * **d** (*int*) – Elbow orientation (1 for up, -1 for down).
  * **n** (*int*) – Wrist flip selector (1 for no flip, -1 for flip).
  * **cfg** (*int*) – Sixth-axis angle configuration identifier.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### power_on()

Power on the robot.

Note: Takes ~10 s before the robot is enabled after power-on.

* **Return type:**
  str

#### run_script(project_name)

Run a script file.

* **Parameters:**
  **project_name** (*str*) – Script file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### stop_script()

Stop scripts.

* **Return type:**
  str

#### pause_script()

Pause the script.

* **Return type:**
  str

#### continue_script()

Continue running the script.

* **Return type:**
  str

#### get_hold_regs(id, addr, count, type_)

Read hold register.

* **Parameters:**
  * **id** (*int*) – Secondary device number (0-4, where 0 is controller slave).
  * **addr** (*int*) – Starting hold-register address (3095-4095).
  * **count** (*int*) – Number of items to read (1-16).
  * **type** – Data type, such as `"U16"`, `"U32"`, `"F32"`, or
    `"F64"`.
  * **type_** (*str*)
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_hold_regs(id, addr, count, table, type_=None)

Write hold register.

* **Parameters:**
  * **id** (*int*) – Secondary device number (0-4, where 0 is controller slave).
  * **addr** (*int*) – Starting hold-register address (3095-4095).
  * **count** (*int*) – Number of items to write (1-16).
  * **table** (*str*) – Register data payload string.
  * **type** – Optional data type, such as `"U16"`, `"U32"`,
    `"F32"`, or `"F64"`.
  * **type_** (*str* *|* *None*)
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_error_id()

Get robot error code.

* **Return type:**
  str

#### set_payload(offset1, \*dyn_params)

Set payload parameters.

* **Parameters:**
  * **offset1** (*float*) – Base payload value.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Additional payload arguments.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### positive_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool)

Run forward kinematics from joint angles to Cartesian pose.

* **Parameters:**
  * **offset1** (*float*) – Joint 1 angle.
  * **offset2** (*float*) – Joint 2 angle.
  * **offset3** (*float*) – Joint 3 angle.
  * **offset4** (*float*) – Joint 4 angle.
  * **offset5** (*float*) – Joint 5 angle.
  * **offset6** (*float*) – Joint 6 angle.
  * **user** (*int*) – User coordinate index.
  * **tool** (*int*) – Tool coordinate index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### inverse_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool, \*dyn_params)

Run inverse kinematics from Cartesian pose to joint angles.

* **Parameters:**
  * **offset1** (*float*) – X position.
  * **offset2** (*float*) – Y position.
  * **offset3** (*float*) – Z position.
  * **offset4** (*float*) – RX rotation.
  * **offset5** (*float*) – RY rotation.
  * **offset6** (*float*) – RZ rotation.
  * **user** (*int*) – User coordinate index.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional solver parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_collision_level(offset1)

Set collision detection level.

* **Parameters:**
  **offset1** (*int*) – Collision level value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_angle()

Get current joint angles.

* **Return type:**
  str

#### get_pose()

Get current Cartesian pose.

* **Return type:**
  str

#### emergency_stop()

Trigger emergency stop.

* **Return type:**
  str

#### modbus_create(ip, port, slave_id, is_rtu)

Create a Modbus connection.

* **Parameters:**
  * **ip** (*str*) – Modbus device IP address.
  * **port** (*int*) – Modbus device port.
  * **slave_id** (*int*) – Slave device identifier.
  * **is_rtu** (*int*) – Connection mode flag (0 for TCP, 1 for RTU).
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### modbus_close(offset1)

Close a Modbus connection.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### set_safe_skin(offset1)

Configure safe-skin feature.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### set_obstacle_avoid(offset1)

Configure obstacle avoidance feature.

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### get_trace_start_pose(offset1)

Get starting pose of a Cartesian trajectory file.

* **Parameters:**
  **offset1** (*str*) – Trajectory file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_path_start_pose(offset1)

Get starting pose of a joint path file.

* **Parameters:**
  **offset1** (*str*) – Path file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### handle_traj_points(offset1)

Process a trajectory points file.

* **Parameters:**
  **offset1** (*str*) – Trajectory file name.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_six_force_data()

Read six-axis force sensor data.

* **Return type:**
  str

#### set_collide_drag(offset1)

Configure collision drag mode.

* **Parameters:**
  **offset1** (*int*) – Drag mode flag.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_terminal_keys(offset1)

Configure terminal key behavior.

* **Parameters:**
  **offset1** (*int*) – Key mode value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_terminal_485(offset1, offset2, offset3, offset4)

Set terminal RS-485 parameters.

* **Parameters:**
  * **offset1** (*int*) – Baud rate.
  * **offset2** (*int*) – Data bits.
  * **offset3** (*str*) – Parity setting.
  * **offset4** (*int*) – Stop bits.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_terminal_485()

Get terminal RS-485 configuration.

* **Return type:**
  str

#### tcp_speed(offset1)

Set TCP speed.

* **Parameters:**
  **offset1** (*int*) – TCP speed value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tcp_speed_end()

End TCP speed mode.

* **Return type:**
  str

#### get_in_bits(offset1, offset2, offset3)

Read digital input bits.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Number of bits.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_in_regs(offset1, offset2, offset3, \*dyn_params)

Read input registers.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Register count.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional data type and mode parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### get_coils(offset1, offset2, offset3)

Read coil values.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Coil count.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### set_coils(offset1, offset2, offset3, offset4)

Write coil values.

* **Parameters:**
  * **offset1** (*int*) – Device identifier.
  * **offset2** (*int*) – Start address.
  * **offset3** (*int*) – Coil count.
  * **offset4** (*int*) – Packed coil value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### di(offset1)

Read a digital input port.

* **Parameters:**
  **offset1** (*int*) – Digital input index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### tool_di(offset1)

Read a terminal digital input port.

* **Parameters:**
  **offset1** (*int*) – Terminal digital input index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### do_group(\*dyn_params)

Set multiple digital outputs in one command.

* **Parameters:**
  **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Repeating output pairs such as `(index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### brake_control(offset1, offset2)

Control joint brakes.

* **Parameters:**
  * **offset1** (*int*) – Joint index.
  * **offset2** (*int*) – Brake control value.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_drag()

Enable drag mode.

* **Return type:**
  str

#### stop_drag()

Disable drag mode.

* **Return type:**
  str

#### load_switch(offset1)

Switch load configuration.

* **Parameters:**
  **offset1** (*int*) – Load profile index.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### wait(t)

Wait for specified time (queued command).

* **Parameters:**
  **t** (*float*) – Wait duration in milliseconds.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### pause()

Pause queued motion execution.

* **Return type:**
  str

#### resume()

Resume paused motion execution.

Note: maps to the `continue()` protocol command; `continue` is a
Python keyword so the method is named `resume`.

* **Return type:**
  str

#### EnableRobot(\*args, \*\*kwargs)

* **Return type:**
  str

#### DisableRobot()

* **Return type:**
  str

#### ClearError()

* **Return type:**
  str

#### ResetRobot()

* **Return type:**
  str

#### SpeedFactor(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### User(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### Tool(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### RobotMode()

* **Return type:**
  str

#### PayLoad(weight, inertia)

* **Parameters:**
  * **weight** (*float*)
  * **inertia** (*float*)
* **Return type:**
  str

#### DO(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### DOExecute(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### ToolDO(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### ToolDOExecute(index, status)

* **Parameters:**
  * **index** (*int*)
  * **status** (*int*)
* **Return type:**
  str

#### AO(index, val)

* **Parameters:**
  * **index** (*int*)
  * **val** (*float*)
* **Return type:**
  str

#### AOExecute(index, val)

* **Parameters:**
  * **index** (*int*)
  * **val** (*float*)
* **Return type:**
  str

#### AccJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### AccL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### SpeedJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### SpeedL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### VelJ(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### VelL(speed)

* **Parameters:**
  **speed** (*int*)
* **Return type:**
  str

#### Arch(index)

* **Parameters:**
  **index** (*int*)
* **Return type:**
  str

#### CP(ratio)

* **Parameters:**
  **ratio** (*int*)
* **Return type:**
  str

#### LimZ(value)

* **Parameters:**
  **value** (*int*)
* **Return type:**
  str

#### SetArmOrientation(r, d, n, cfg)

* **Parameters:**
  * **r** (*int*)
  * **d** (*int*)
  * **n** (*int*)
  * **cfg** (*int*)
* **Return type:**
  str

#### PowerOn()

* **Return type:**
  str

#### RunScript(project_name)

* **Parameters:**
  **project_name** (*str*)
* **Return type:**
  str

#### StopScript()

* **Return type:**
  str

#### PauseScript()

* **Return type:**
  str

#### ContinueScript()

* **Return type:**
  str

#### GetHoldRegs(id, addr, count, type_)

* **Parameters:**
  * **id** (*int*)
  * **addr** (*int*)
  * **count** (*int*)
  * **type_** (*str*)
* **Return type:**
  str

#### SetHoldRegs(id, addr, count, table, type_=None)

* **Parameters:**
  * **id** (*int*)
  * **addr** (*int*)
  * **count** (*int*)
  * **table** (*str*)
  * **type_** (*str* *|* *None*)
* **Return type:**
  str

#### GetErrorID()

* **Return type:**
  str

#### SetPayload(offset1, \*dyn_params)

* **Parameters:**
  * **offset1** (*float*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### PositiveSolution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool)

* **Parameters:**
  * **offset1** (*float*)
  * **offset2** (*float*)
  * **offset3** (*float*)
  * **offset4** (*float*)
  * **offset5** (*float*)
  * **offset6** (*float*)
  * **user** (*int*)
  * **tool** (*int*)
* **Return type:**
  str

#### InverseSolution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool, \*dyn_params)

* **Parameters:**
  * **offset1** (*float*)
  * **offset2** (*float*)
  * **offset3** (*float*)
  * **offset4** (*float*)
  * **offset5** (*float*)
  * **offset6** (*float*)
  * **user** (*int*)
  * **tool** (*int*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### SetCollisionLevel(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### GetAngle()

* **Return type:**
  str

#### GetPose()

* **Return type:**
  str

#### EmergencyStop()

* **Return type:**
  str

#### ModbusCreate(ip, port, slave_id, isRTU)

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)
  * **slave_id** (*int*)
  * **isRTU** (*int*)
* **Return type:**
  str

#### ModbusClose(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetSafeSkin(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetObstacleAvoid(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### GetTraceStartPose(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### GetPathStartPose(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### HandleTrajPoints(offset1)

* **Parameters:**
  **offset1** (*str*)
* **Return type:**
  str

#### GetSixForceData()

* **Return type:**
  str

#### SetCollideDrag(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetTerminalKeys(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### SetTerminal485(offset1, offset2, offset3, offset4)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*str*)
  * **offset4** (*int*)
* **Return type:**
  str

#### GetTerminal485()

* **Return type:**
  str

#### TCPSpeed(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### TCPSpeedEnd()

* **Return type:**
  str

#### GetInBits(offset1, offset2, offset3)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
* **Return type:**
  str

#### GetInRegs(offset1, offset2, offset3, \*dyn_params)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### GetCoils(offset1, offset2, offset3)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
* **Return type:**
  str

#### SetCoils(offset1, offset2, offset3, offset4)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
  * **offset3** (*int*)
  * **offset4** (*int*)
* **Return type:**
  str

#### DI(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### ToolDI(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### DOGroup(\*dyn_params)

* **Parameters:**
  **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### BrakeControl(offset1, offset2)

* **Parameters:**
  * **offset1** (*int*)
  * **offset2** (*int*)
* **Return type:**
  str

#### StartDrag()

* **Return type:**
  str

#### StopDrag()

* **Return type:**
  str

#### LoadSwitch(offset1)

* **Parameters:**
  **offset1** (*int*)
* **Return type:**
  str

#### Continue()

* **Return type:**
  str

#### Pause()

* **Return type:**
  str

#### Stop()

* **Return type:**
  str

<a id="module-dobot_api_v3.move"></a>

Movement commands for Dobot API (DobotApiMove class).

### *class* dobot_api_v3.move.DobotApiMove(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Movement command client for Dobot motion APIs.

This class sends trajectory and servo commands to the move TCP port
(usually `30003`).

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### mov_j(x, y, z, rx, ry, rz, \*dyn_params)

Joint motion interface (point-to-point motion mode).

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_j(200, 0, 200, 0, 0, 0)
>>> move.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
```

#### mov_l(x, y, z, rx, ry, rz, \*dyn_params)

Linear motion interface.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_l(250, 0, 180, 0, 0, 0)
>>> move.mov_l(250, 30, 180, 0, 0, 0, "SpeedL=30", "AccL=30")
```

#### joint_mov_j(j1, j2, j3, j4, j5, j6, \*dyn_params)

Joint motion interface (joint target).

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### jump()

Placeholder for Jump command.

This method is intentionally not implemented in the current version.

* **Return type:**
  None

#### rel_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, \*dyn_params)

Relative joint offset motion (point-to-point mode).

* **Parameters:**
  * **offset1** (*float*) – Joint 1 offset.
  * **offset2** (*float*) – Joint 2 offset.
  * **offset3** (*float*) – Joint 3 offset.
  * **offset4** (*float*) – Joint 4 offset.
  * **offset5** (*float*) – Joint 5 offset.
  * **offset6** (*float*) – Joint 6 offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l(offset_x, offset_y, offset_z, \*dyn_params)

Relative Cartesian offset motion (linear mode).

* **Parameters:**
  * **offset_x** (*float*) – X-axis offset.
  * **offset_y** (*float*) – Y-axis offset.
  * **offset_z** (*float*) – Z-axis offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### mov_l_io(x, y, z, a, b, c, \*dyn_params)

Linear motion with parallel digital output control.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Parallel I/O tuples `(mode, distance, index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### mov_j_io(x, y, z, a, b, c, \*dyn_params)

Point-to-point motion with parallel digital output control.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Parallel I/O tuples `(mode, distance, index, status)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, \*dyn_params)

Circular motion through an intermediate point.

* **Parameters:**
  * **x1** (*float*) – Intermediate point X.
  * **y1** (*float*) – Intermediate point Y.
  * **z1** (*float*) – Intermediate point Z.
  * **a1** (*float*) – Intermediate point A.
  * **b1** (*float*) – Intermediate point B.
  * **c1** (*float*) – Intermediate point C.
  * **x2** (*float*) – End point X.
  * **y2** (*float*) – End point Y.
  * **z2** (*float*) – End point Z.
  * **a2** (*float*) – End point A.
  * **b2** (*float*) – End point B.
  * **c2** (*float*) – End point C.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count, \*dyn_params)

Full-circle motion command.

* **Parameters:**
  * **x1** (*float*) – Intermediate point X.
  * **y1** (*float*) – Intermediate point Y.
  * **z1** (*float*) – Intermediate point Z.
  * **a1** (*float*) – Intermediate point A.
  * **b1** (*float*) – Intermediate point B.
  * **c1** (*float*) – Intermediate point C.
  * **x2** (*float*) – End point X.
  * **y2** (*float*) – End point Y.
  * **z2** (*float*) – End point Z.
  * **a2** (*float*) – End point A.
  * **b2** (*float*) – End point B.
  * **c2** (*float*) – End point C.
  * **count** (*int*) – Number of full rotations.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_j(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50.0, gain=500.0)

Dynamic following in joint space.

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
  * **t** (*float*) – Point run time in seconds.
  * **lookahead_time** (*float*) – Feed-forward smoothing parameter.
  * **gain** (*float*) – Servo gain parameter.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_js(j1, j2, j3, j4, j5, j6)

Dynamic following in joint space (simplified form).

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### servo_p(x, y, z, a, b, c)

Dynamic following in Cartesian space.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### move_jog(axis_id, \*dyn_params)

Jog motion along a single axis.

* **Parameters:**
  * **axis_id** (*str*) – Axis command such as `"J1+"` or `"X-"`.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional jog parameters `(coord_type, user, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.move_jog("J1+")
>>> move.move_jog("")
```

#### start_trace(trace_name)

Execute a trajectory file (Cartesian points).

* **Parameters:**
  **trace_name** (*str*) – Trajectory file name including suffix.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_path(trace_name, const, cart)

Replay a trajectory file (joint points).

* **Parameters:**
  * **trace_name** (*str*) – Trajectory file name including suffix.
  * **const** (*int*) – Constant-speed mode flag.
  * **cart** (*int*) – Cartesian/joint path flag.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### start_fc_trace(trace_name)

Execute a trajectory file with force control (Cartesian points).

* **Parameters:**
  **trace_name** (*str*) – Trajectory file name including suffix.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### sync()

Block until all queued commands have been executed.

* **Returns:**
  Robot response string.
* **Return type:**
  str

### Example

```pycon
>>> move.mov_j(200, 0, 200, 0, 0, 0)
>>> move.mov_l(220, 20, 180, 0, 0, 0)
>>> move.sync()
```

#### rel_mov_j_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, \*dyn_params)

Relative joint motion along the tool coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in tool frame.
  * **offset_y** (*float*) – Y offset in tool frame.
  * **offset_z** (*float*) – Z offset in tool frame.
  * **offset_rx** (*float*) – RX offset in tool frame.
  * **offset_ry** (*float*) – RY offset in tool frame.
  * **offset_rz** (*float*) – RZ offset in tool frame.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*tuple* *[**int* *,* *int* *,* *int* *]*) – Optional tuples `(speed_j, acc_j, user)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, \*dyn_params)

Relative linear motion along the tool coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in tool frame.
  * **offset_y** (*float*) – Y offset in tool frame.
  * **offset_z** (*float*) – Z offset in tool frame.
  * **offset_rx** (*float*) – RX offset in tool frame.
  * **offset_ry** (*float*) – RY offset in tool frame.
  * **offset_rz** (*float*) – RZ offset in tool frame.
  * **tool** (*int*) – Tool coordinate index.
  * **\*dyn_params** (*tuple* *[**int* *,* *int* *,* *int* *]*) – Optional tuples `(speed_l, acc_l, user)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_j_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, \*dyn_params)

Relative joint motion along the user coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in user frame.
  * **offset_y** (*float*) – Y offset in user frame.
  * **offset_z** (*float*) – Z offset in user frame.
  * **offset_rx** (*float*) – RX offset in user frame.
  * **offset_ry** (*float*) – RY offset in user frame.
  * **offset_rz** (*float*) – RZ offset in user frame.
  * **user** (*int*) – User coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples `(speed_j, acc_j, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_mov_l_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, \*dyn_params)

Relative linear motion along the user coordinate system.

* **Parameters:**
  * **offset_x** (*float*) – X offset in user frame.
  * **offset_y** (*float*) – Y offset in user frame.
  * **offset_z** (*float*) – Z offset in user frame.
  * **offset_rx** (*float*) – RX offset in user frame.
  * **offset_ry** (*float*) – RY offset in user frame.
  * **offset_rz** (*float*) – RZ offset in user frame.
  * **user** (*int*) – User coordinate index.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples `(speed_l, acc_l, tool)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### rel_joint_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, \*dyn_params)

Relative motion along each joint axis (joint motion mode).

* **Parameters:**
  * **offset1** (*float*) – Joint 1 offset.
  * **offset2** (*float*) – Joint 2 offset.
  * **offset3** (*float*) – Joint 3 offset.
  * **offset4** (*float*) – Joint 4 offset.
  * **offset5** (*float*) – Joint 5 offset.
  * **offset6** (*float*) – Joint 6 offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional tuples such as `(speed_j, acc_j)`.
* **Returns:**
  Robot response string.
* **Return type:**
  str

#### MovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### MovL(\*args, \*\*kwargs)

* **Return type:**
  str

#### JointMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### Jump()

* **Return type:**
  None

#### RelMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovL(offsetX, offsetY, offsetZ, \*dyn_params)

* **Parameters:**
  * **offsetX** (*float*)
  * **offsetY** (*float*)
  * **offsetZ** (*float*)
  * **dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*)
* **Return type:**
  str

#### MovLIO(\*args, \*\*kwargs)

* **Return type:**
  str

#### MovJIO(\*args, \*\*kwargs)

* **Return type:**
  str

#### Arc(\*args, \*\*kwargs)

* **Return type:**
  str

#### Circle3(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoJ(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoJS(\*args, \*\*kwargs)

* **Return type:**
  str

#### ServoP(\*args, \*\*kwargs)

* **Return type:**
  str

#### MoveJog(\*args, \*\*kwargs)

* **Return type:**
  str

#### StartTrace(trace_name)

* **Parameters:**
  **trace_name** (*str*)
* **Return type:**
  str

#### StartPath(trace_name, const, cart)

* **Parameters:**
  * **trace_name** (*str*)
  * **const** (*int*)
  * **cart** (*int*)
* **Return type:**
  str

#### StartFCTrace(trace_name)

* **Parameters:**
  **trace_name** (*str*)
* **Return type:**
  str

#### Sync()

* **Return type:**
  str

#### RelMovJTool(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovLTool(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovJUser(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelMovLUser(\*args, \*\*kwargs)

* **Return type:**
  str

#### RelJointMovJ(\*args, \*\*kwargs)

* **Return type:**
  str

<a id="module-dobot_api_v3.feedback"></a>

Feedback interface for Dobot API.

### *class* dobot_api_v3.feedback.DobotApiFeedback(ip, port)

Bases: [`DobotApi`](#dobot_api_v3.base.DobotApi)

Feedback interface for reading 1440-byte robot status packets.

* **Parameters:**
  * **ip** (*str*)
  * **port** (*int*)

#### \_\_init_\_(ip, port)

Initialize the feedback socket client.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **port** (*int*) – Feedback TCP port, usually `30004`.
* **Raises:**
  * **ValueError** – If `port` is unsupported.
  * **ConnectionError** – If the socket connection fails.
* **Return type:**
  None

#### feedback_data()

Read one feedback frame and parse it with `FeedbackDtype`.

* **Returns:**
  A NumPy structured array of length 1 when a valid 1440-byte frame
  is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  *ndarray* | None

#### feedBackData()

Deprecated alias for [`feedback_data()`](#dobot_api_v3.feedback.DobotApiFeedback.feedback_data).

* **Returns:**
  Same value as [`feedback_data()`](#dobot_api_v3.feedback.DobotApiFeedback.feedback_data).
* **Return type:**
  *ndarray* | None

### dobot_api_v3.feedback.DobotApiFeedBack

alias of [`DobotApiFeedback`](#dobot_api_v3.feedback.DobotApiFeedback)

<a id="module-dobot_api_v3.error_monitor"></a>

Dashboard-based alarm monitor for Dobot V3 robots.

### *class* dobot_api_v3.error_monitor.RobotErrorMonitor(dashboard, \*, language='en')

Bases: `object`

Alarm monitor backed by an externally-supplied `DobotApiDashboard`.

The caller is responsible for the dashboard’s lifecycle (opening and
closing the connection).  `RobotErrorMonitor` never closes the dashboard
it receives.

Example:

```default
dashboard = DobotApiDashboard("192.168.5.1", 29999)
monitor = RobotErrorMonitor(dashboard)
monitor.check_errors(language="en")
dashboard.close()
```

* **Parameters:**
  * **dashboard** ([*DobotApiDashboard*](#dobot_api_v3.dashboard.DobotApiDashboard))
  * **language** (*str*)

#### \_\_init_\_(dashboard, \*, language='en')

Initialize the error monitor.

* **Parameters:**
  * **dashboard** ([*DobotApiDashboard*](#dobot_api_v3.dashboard.DobotApiDashboard)) – Shared dashboard client used for alarm queries and clear.
  * **language** (*str*) – Default alarm translation language.
* **Return type:**
  None

#### *classmethod* from_connection(robot_ip='192.168.200.1', dashboard_port=29999)

Create a monitor by opening a new dashboard connection.

* **Parameters:**
  * **robot_ip** (*str*) – Robot controller IP address.
  * **dashboard_port** (*int*) – Dashboard TCP port.
* **Returns:**
  New monitor instance bound to a newly created dashboard client.
* **Return type:**
  [*RobotErrorMonitor*](#dobot_api_v3.error_monitor.RobotErrorMonitor)

#### Deprecated
Deprecated since version Prefer: creating a `DobotApiDashboard`
yourself and passing it to [`RobotErrorMonitor`](#dobot_api_v3.error_monitor.RobotErrorMonitor) directly
so that the same connection can be shared with other API objects.

#### connect()

No-op kept for backward compatibility.

* **Returns:**
  Always `True`.
* **Return type:**
  bool

#### Deprecated
Deprecated since version Lifecycle: is now the caller’s responsibility.  Manage the
`DobotApiDashboard` connection yourself.

#### disconnect()

No-op kept for backward compatibility.

#### Deprecated
Deprecated since version Lifecycle: is now the caller’s responsibility.  Close the
`DobotApiDashboard` yourself when done.

* **Return type:**
  None

#### get_error_info(language='zh_CN')

Get current robot alarm information.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  Dictionary in the format `{"errMsg": [...]}`, or `None` when
  an unexpected exception occurs.
* **Return type:**
  *Dict*[str, *Any*] | None

#### check_errors(language='zh_cn')

Query and log all current alarms.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  `True` if alarms are present, otherwise `False`.
* **Return type:**
  bool

#### monitor_errors(interval=5, language='zh_cn')

Continuously poll and log robot alarms.

* **Parameters:**
  * **interval** (*int*) – Polling interval in seconds.
  * **language** (*str*) – Alarm translation language.
* **Return type:**
  None

#### save_error_log(filename=None, language='zh_cn')

Persist current alarm payload to a JSON file.

* **Parameters:**
  * **filename** (*str* *|* *None*) – Output file path. If omitted, a timestamped filename is
    generated.
  * **language** (*str*) – Alarm translation language.
* **Return type:**
  None

#### clear_robot_error(language='zh_CN')

Clear robot errors after displaying them with details.

* **Parameters:**
  **language** (*str*) – Language for error messages (default: “zh_CN”)
* **Returns:**
  `True` if errors were found and a clear command was sent,
  otherwise `False`.
* **Return type:**
  bool

<a id="module-dobot_api_v3.i18n_manager"></a>

Internationalization manager for robot alarms.

### *class* dobot_api_v3.i18n_manager.AlarmI18n(default_language='en')

Bases: `object`

Alarm internationalization manager.

This helper resolves alarm metadata from locale YAML files and provides
language switching, structured alarm dictionaries, and formatted strings.

* **Parameters:**
  **default_language** (*str*)

#### SUPPORTED_LANGUAGES *= ['en', 'zh_CN']*

#### LANGUAGE_ALIASES *= {'zh_cn': 'zh_CN'}*

#### SERVO_ID_MIN *= 8000*

#### \_\_init_\_(default_language='en')

Initialize the i18n backend and set the active language.

* **Parameters:**
  **default_language** (*str*) – Initial language code, such as `"en"` or
  `"zh_CN"`.
* **Raises:**
  **ValueError** – If `default_language` is not supported.
* **Return type:**
  None

#### set_language(language)

Set the active language for alarm translation.

* **Parameters:**
  **language** (*str*) – Language code to activate.
* **Raises:**
  **ValueError** – If `language` is not in supported languages.
* **Return type:**
  None

#### get_current_language()

Get the current active language code.

* **Returns:**
  Active language code stored in the i18n backend.
* **Return type:**
  str

#### get_alarm(alarm_id, alarm_type=None, field=None)

Get localized alarm data.

* **Parameters:**
  * **alarm_id** (*int*) – Alarm identifier.
  * **alarm_type** (*str* *|* *None*) – Alarm category. If omitted, it is inferred from
    `alarm_id` using `SERVO_ID_MIN`.
  * **field** (*str* *|* *None*) – Optional single field name to return.
* **Returns:**
  Alarm dictionary containing translated fields. When `field` is
  provided, returns `{field: value}`.
* **Return type:**
  *Dict*[str, *Any*]

#### get_controller_alarm(alarm_id)

Get localized controller alarm data.

* **Parameters:**
  **alarm_id** (*int*) – Controller alarm identifier.
* **Returns:**
  Localized alarm dictionary.
* **Return type:**
  *Dict*[str, *Any*]

#### get_servo_alarm(alarm_id)

Get localized servo alarm data.

* **Parameters:**
  **alarm_id** (*int*) – Servo alarm identifier.
* **Returns:**
  Localized alarm dictionary.
* **Return type:**
  *Dict*[str, *Any*]

#### format_alarm(alarm_id, alarm_type=None, include_cause=True)

Format one alarm into a human-readable multi-line string.

* **Parameters:**
  * **alarm_id** (*int*) – Alarm identifier.
  * **alarm_type** (*str* *|* *None*) – Optional explicit alarm category.
  * **include_cause** (*bool*) – Whether to include the translated cause line.
* **Returns:**
  Formatted alarm text.
* **Return type:**
  str

#### enrich_alarm_data(alarm_data)

Merge translated alarm metadata into an existing alarm payload.

* **Parameters:**
  **alarm_data** (*Dict* *[**str* *,* *Any* *]*) – Alarm payload that may contain at least `id`.
* **Returns:**
  A merged dictionary with translated alarm fields when `id` is
  present; otherwise the original `alarm_data`.
* **Return type:**
  *Dict*[str, *Any*]

#### *classmethod* get_supported_languages()

Get supported language codes.

* **Returns:**
  Copy of supported language list.
* **Return type:**
  *List*[str]

#### *classmethod* normalize_language_code(language)

Normalize a language code using alias mapping.

* **Parameters:**
  **language** (*str*) – Raw language code.
* **Returns:**
  Normalized language code. Unsupported codes are returned unchanged
  and logged as warnings.
* **Return type:**
  str

<a id="module-dobot_api_v3.utils"></a>

Utility helpers for Dobot API.

### dobot_api_v3.utils.deprecated_alias(new_name)

Decorator that marks a method as a deprecated alias for *new_name*.

Usage (inside a class body):

```default
@deprecated_alias("enable_robot")
def EnableRobot(self, *args, **kwargs):
    return self.enable_robot(*args, **kwargs)
```

At call time the decorator emits a `DeprecationWarning` pointing at the
caller’s frame and then delegates to the wrapped function body.

* **Parameters:**
  **new_name** (*str*)
* **Return type:**
  *Callable*[[*Callable*[[…], *Any*]], *Callable*[[…], *Any*]]
