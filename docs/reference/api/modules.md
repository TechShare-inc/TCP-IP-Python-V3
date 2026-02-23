# dobot_api_v3

Dobot API (modular V4-style architecture for V3 protocol semantics).

### *class* dobot_api_v3.DobotRobot(ip, \*, language='en')

Bases: `object`

Unified high-level interface for Dobot V3 robots.

This class manages the dashboard (port 29999) and move (port 30003)
connections immediately on construction.  Feedback connections on ports
30004, 30005, and 30006 are created lazily on first access through the
corresponding properties.

The individual component objects remain accessible as public attributes
(`robot.dashboard`, `robot.move`, etc.) so that the full API surface
of each subsystem is always reachable.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **language** (*str*) – Default language for alarm messages (`"en"` or
    `"zh_CN"`).

### Example

```
>>> with DobotRobot("192.168.5.1") as robot:
...     robot.startup(speed=40)
...     robot.mov_j(200, 0, 200, 0, 0, 0)
...     robot.sync()
...     robot.shutdown()
```

#### \_\_init_\_(ip, \*, language='en')

Initialize dashboard and move connections.

* **Parameters:**
  * **ip** (*str*) – Robot controller IP address.
  * **language** (*str*) – Default alarm language for the error monitor.
* **Raises:**
  **ConnectionError** – If any eager socket connection fails.
* **Return type:**
  None

#### *property* feedback *: [DobotApiFeedback](#dobot_api_v3.feedback.DobotApiFeedback)*

Primary feedback connection (port 30004), created on first access.

* **Returns:**
  A connected `DobotApiFeedback` instance.

#### *property* feedback_30005 *: [DobotApiFeedback](#dobot_api_v3.feedback.DobotApiFeedback)*

Secondary feedback connection (port 30005), created on first access.

Port 30005 provides feedback at a different query frequency than the
primary port 30004.

* **Returns:**
  A connected `DobotApiFeedback` instance.

#### *property* feedback_30006 *: [DobotApiFeedback](#dobot_api_v3.feedback.DobotApiFeedback)*

Tertiary feedback connection (port 30006), created on first access.

Port 30006 provides feedback at a different query frequency than the
primary port 30004.

* **Returns:**
  A connected `DobotApiFeedback` instance.

#### startup(speed=40, load=0.0, center_x=0.0, center_y=0.0, center_z=0.0, \*, power_on_wait=15.0)

Perform the standard robot startup sequence.

First checks for controller errors.  If errors are present the
sequence is `clear_error → power_on → wait → disable_robot →
enable_robot → speed_factor`.  If no errors are detected,
`clear_error` and `power_on` (and the associated wait) are
skipped and the sequence continues directly with
`disable_robot → enable_robot → speed_factor`.

* **Parameters:**
  * **speed** (*int*) – Global speed factor (1-100) applied after enable.
  * **load** (*float*) – Payload weight forwarded to `enable_robot()`.
  * **center_x** (*float*) – Payload center X offset forwarded to
    `enable_robot()`.
  * **center_y** (*float*) – Payload center Y offset forwarded to
    `enable_robot()`.
  * **center_z** (*float*) – Payload center Z offset forwarded to
    `enable_robot()`.
  * **power_on_wait** (*float*) – Seconds to sleep after `power_on()` before
    continuing (default `15`).  Only used when errors are
    detected and `power_on` is called.
* **Return type:**
  None

### Example

```python
>>> robot.startup(speed=50, load=1.0, center_z=0.05)
```

#### shutdown()

Disable the robot arm (graceful stop).

Does **not** close TCP connections — call `close()` separately
when finished, or rely on `__exit__` when using as a context manager.

### Example

```python
>>> robot.shutdown()
```

* **Return type:**
  None

#### close()

Close all open TCP connections.

It is safe to call this method more than once.  Connections that have
not been opened (e.g. unrequested feedback ports) are silently skipped.

### Example

```python
>>> robot.close()
```

* **Return type:**
  None

#### reconnect()

Reconnect all currently-open TCP sockets.

Opens new sockets for dashboard and move (always), and for whichever
feedback ports were previously opened.

* **Raises:**
  **ConnectionError** – If any reconnection attempt fails.
* **Return type:**
  None

### Example

```python
>>> robot.reconnect()
```

#### check_errors(language='en')

Query and log all current alarms.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  `True` if alarms are present, otherwise `False`.
* **Return type:**
  bool

### Example

```python
>>> has_errors = robot.check_errors(language="en")
```

#### clear_and_recover(language='en')

Display current alarm details then send a clear command.

* **Parameters:**
  **language** (*str*) – Alarm translation language.
* **Returns:**
  `True` if errors were found and a clear command was sent,
  otherwise `False`.
* **Return type:**
  bool

### Example

```python
>>> robot.clear_and_recover(language="en")
```

#### feedback_data()

Read one feedback frame from the primary feedback port (30004).

Opens the feedback connection lazily on the first call.  Returns a
typed `FeedbackData` for full IDE autocompletion.
For zero-copy NumPy access use `raw_feedback_data()` instead.

* **Returns:**
  A `FeedbackData` instance when a valid
  1440-byte frame is parsed, otherwise `None`.
* **Return type:**
  [*FeedbackData*](#dobot_api_v3.base.FeedbackData) | None

### Example

```python
>>> data = robot.feedback_data()
>>> if data is not None:
...     print(data.tool_vector_actual)
...     print(data.robot_mode)
```

#### raw_feedback_data()

Read one feedback frame and return the raw NumPy structured array.

Opens the feedback connection lazily on the first call.  Use this
method for NumPy-native numeric pipelines; for typed access prefer
`feedback_data()`.

* **Returns:**
  A NumPy structured array of length 1 (`dtype=FeedbackDtype`)
  when a valid 1440-byte frame is parsed, otherwise `None`.
* **Return type:**
  *ndarray* | None

### Example

```python
>>> raw = robot.raw_feedback_data()
>>> if raw is not None:
...     print(raw[0]["tool_vector_actual"])
```

#### enable_robot(load=0.0, center_x=0.0, center_y=0.0, center_z=0.0)

Enable the robot with optional payload parameters.

Delegates to `enable_robot()`.

* **Parameters:**
  * **load** (*float*) – Payload weight.
  * **center_x** (*float*) – Payload center offset on X axis.
  * **center_y** (*float*) – Payload center offset on Y axis.
  * **center_z** (*float*) – Payload center offset on Z axis.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### disable_robot()

Disable the robot arm.

Delegates to `disable_robot()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### clear_error()

Clear controller alarm information.

Delegates to `clear_error()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### reset_robot()

Stop the robot.

Delegates to `reset_robot()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### power_on()

Power on the controller.

Delegates to `power_on()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### emergency_stop()

Trigger an emergency stop.

Delegates to `emergency_stop()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### speed_factor(speed)

Set global speed factor.

Delegates to `speed_factor()`.

* **Parameters:**
  **speed** (*int*) – Rate value in range 1-100.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### robot_mode()

Query the robot operating mode.

Delegates to `robot_mode()`.

* **Returns:**
  `IntResponse` with `value` set to the
  current mode code (e.g. 5 = idle, 7 = running).
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *IntResponse*

#### get_pose()

Get current Cartesian pose.

Delegates to `get_pose()`.

* **Returns:**
  `PoseResponse` with `x`, `y`, `z`,
  `rx`, `ry`, `rz` fields populated in mm / degrees.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *PoseResponse*

#### get_angle()

Get current joint angles.

Delegates to `get_angle()`.

* **Returns:**
  `PoseResponse` with `x`-`rz` fields
  mapping to joint angles J1-J6 in degrees.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *PoseResponse*

#### get_error_id()

Get current error IDs from the controller.

Delegates to `get_error_id()`.

* **Returns:**
  `ErrorIdResponse` with `error_ids` tuple
  of active non-zero alarm codes.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *ErrorIdResponse*

#### start_drag()

Enable drag (teach) mode.

Delegates to `start_drag()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### stop_drag()

Disable drag (teach) mode.

Delegates to `stop_drag()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### set_user(index)

Select the calibrated user coordinate system.

Delegates to `set_user()`.

* **Parameters:**
  **index** (*int*) – Calibrated user coordinate index.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### set_tool(index)

Select the calibrated tool coordinate system.

Delegates to `set_tool()`.

* **Parameters:**
  **index** (*int*) – Calibrated tool coordinate index.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### mov_j(x, y, z, rx, ry, rz, \*dyn_params)

Joint motion interface (point-to-point motion mode).

Delegates to `mov_j()`.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.mov_j(200, 0, 200, 0, 0, 0)
>>> robot.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
```

#### mov_l(x, y, z, rx, ry, rz, \*dyn_params)

Linear motion interface.

Delegates to `mov_l()`.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **rx** (*float*) – Target RX rotation.
  * **ry** (*float*) – Target RY rotation.
  * **rz** (*float*) – Target RZ rotation.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.mov_l(250, 0, 180, 0, 0, 0)
```

#### joint_mov_j(j1, j2, j3, j4, j5, j6, \*dyn_params)

Joint motion interface (joint target).

Delegates to `joint_mov_j()`.

* **Parameters:**
  * **j1** (*float*) – Target joint 1 angle.
  * **j2** (*float*) – Target joint 2 angle.
  * **j3** (*float*) – Target joint 3 angle.
  * **j4** (*float*) – Target joint 4 angle.
  * **j5** (*float*) – Target joint 5 angle.
  * **j6** (*float*) – Target joint 6 angle.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.joint_mov_j(-11.53, 4.64, 87.16, -2.84, -77.71, 0.01)
```

#### rel_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, \*dyn_params)

Relative joint offset motion (point-to-point mode).

Delegates to `rel_mov_j()`.

* **Parameters:**
  * **offset1** (*float*) – Joint 1 offset.
  * **offset2** (*float*) – Joint 2 offset.
  * **offset3** (*float*) – Joint 3 offset.
  * **offset4** (*float*) – Joint 4 offset.
  * **offset5** (*float*) – Joint 5 offset.
  * **offset6** (*float*) – Joint 6 offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.rel_mov_j(15, 0, 0, 0, 0, 0)
```

#### rel_mov_l(offset_x, offset_y, offset_z, \*dyn_params)

Relative Cartesian offset motion (linear mode).

Delegates to `rel_mov_l()`.

* **Parameters:**
  * **offset_x** (*float*) – X-axis offset.
  * **offset_y** (*float*) – Y-axis offset.
  * **offset_z** (*float*) – Z-axis offset.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional motion parameters.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, \*dyn_params)

Circular motion through an intermediate point.

Delegates to `arc()`.

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
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### servo_j(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50.0, gain=500.0)

Dynamic following in joint space.

Delegates to `servo_j()`.

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
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### servo_p(x, y, z, a, b, c)

Dynamic following in Cartesian space.

Delegates to `servo_p()`.

* **Parameters:**
  * **x** (*float*) – Target X coordinate.
  * **y** (*float*) – Target Y coordinate.
  * **z** (*float*) – Target Z coordinate.
  * **a** (*float*) – Target A rotation.
  * **b** (*float*) – Target B rotation.
  * **c** (*float*) – Target C rotation.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

#### move_jog(axis_id, \*dyn_params)

Jog motion along a single axis.

Delegates to `move_jog()`.

* **Parameters:**
  * **axis_id** (*str*) – Axis command such as `"J1+"` or `"X-"`.
  * **\*dyn_params** (*int* *|* *float* *|* *str* *|* *tuple*) – Optional jog parameters `(coord_type, user, tool)`.
* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.move_jog("J1+")
>>> robot.move_jog("")  # stop jog
```

#### sync()

Block until all queued motion commands complete.

Delegates to `sync()`.

* **Returns:**
  `AckResponse` on success.
* **Raises:**
  **DobotApiError** – If the controller returns a non-zero error code.
* **Return type:**
  *AckResponse*

### Example

```python
>>> robot.mov_j(200, 0, 200, 0, 0, 0)
>>> robot.sync()
```

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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

#### raw_feedback_data()

Read one feedback frame and return the raw NumPy structured array.

Use this method when you need zero-copy NumPy access to the packet
fields (e.g., for numeric pipelines or direct array slicing).  For
typed, IDE-friendly access prefer `feedback_data()` instead.

* **Returns:**
  A NumPy structured array of length 1 (`dtype=FeedbackDtype`)
  when a valid 1440-byte frame is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  *ndarray* | None

#### feedback_data()

Read one feedback frame and return a typed `FeedbackData`.

Internally calls `raw_feedback_data()` and converts the result to
an immutable `FeedbackData` dataclass for full
IDE autocompletion and type-checker support.

For zero-copy NumPy access (e.g., numeric pipelines) use
`raw_feedback_data()` directly.

* **Returns:**
  A `FeedbackData` instance when a valid
  1440-byte frame is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  [*FeedbackData*](#dobot_api_v3.base.FeedbackData) | None

### Example

```python
>>> data = feedback.feedback_data()
>>> if data is not None:
...     print(data.robot_mode)
...     print(data.tool_vector_actual)
```

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

### *class* dobot_api_v3.FeedbackData(len, digital_input_bits, digital_output_bits, robot_mode, time_stamp, time_stamp_reserve_bit, test_value, test_value_keep_bit, speed_scaling, linear_momentum_norm, v_main, v_robot, i_robot, i_robot_keep_bit1, i_robot_keep_bit2, tool_accelerometer_values, elbow_position, elbow_velocity, q_target, qd_target, qdd_target, i_target, m_target, q_actual, qd_actual, i_actual, actual_tcp_force, tool_vector_actual, tcp_speed_actual, tcp_force, tool_vector_target, tcp_speed_target, motor_temperatures, joint_modes, v_actual, hand_type, user, tool, run_queued_cmd, pause_cmd_flag, velocity_ratio, acceleration_ratio, jerk_ratio, xyz_velocity_ratio, r_velocity_ratio, xyz_acceleration_ratio, r_acceleration_ratio, xyz_jerk_ratio, r_jerk_ratio, brake_status, enable_status, drag_status, running_status, error_status, jog_status, robot_type, drag_button_signal, enable_button_signal, record_button_signal, reappear_button_signal, jaw_button_signal, six_force_online, reserve2, m_actual, load, center_x, center_y, center_z, user_coords, tool_coords, trace_index, six_force_value, target_quaternion, actual_quaternion, reserve3)

Bases: `object`

Immutable snapshot of one decoded feedback packet (1440 bytes).

All scalar fields are plain Python `int` or `float`.  Multi-element
fields (joint arrays, vectors, quaternions, …) are `tuple[float, ...]`
or `tuple[int, ...]`.  Because the dataclass is frozen, field values
cannot be mutated after construction — treat each instance as a read-only
timestamped snapshot.

Use `from_numpy()` to construct a `FeedbackData` from the raw
`np.ndarray` produced by `np.frombuffer(buf, dtype=FeedbackDtype)`.
For direct NumPy access call `raw_feedback_data()` instead of
`feedback_data()`.

* **Parameters:**
  * **len** (*int*)
  * **digital_input_bits** (*int*)
  * **digital_output_bits** (*int*)
  * **robot_mode** (*int*)
  * **time_stamp** (*int*)
  * **time_stamp_reserve_bit** (*int*)
  * **test_value** (*int*)
  * **test_value_keep_bit** (*float*)
  * **speed_scaling** (*float*)
  * **linear_momentum_norm** (*float*)
  * **v_main** (*float*)
  * **v_robot** (*float*)
  * **i_robot** (*float*)
  * **i_robot_keep_bit1** (*float*)
  * **i_robot_keep_bit2** (*float*)
  * **tool_accelerometer_values** (*tuple* *[**float* *,*  *...* *]*)
  * **elbow_position** (*tuple* *[**float* *,*  *...* *]*)
  * **elbow_velocity** (*tuple* *[**float* *,*  *...* *]*)
  * **q_target** (*tuple* *[**float* *,*  *...* *]*)
  * **qd_target** (*tuple* *[**float* *,*  *...* *]*)
  * **qdd_target** (*tuple* *[**float* *,*  *...* *]*)
  * **i_target** (*tuple* *[**float* *,*  *...* *]*)
  * **m_target** (*tuple* *[**float* *,*  *...* *]*)
  * **q_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **qd_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **i_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **actual_tcp_force** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_vector_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_speed_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_force** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_vector_target** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_speed_target** (*tuple* *[**float* *,*  *...* *]*)
  * **motor_temperatures** (*tuple* *[**float* *,*  *...* *]*)
  * **joint_modes** (*tuple* *[**float* *,*  *...* *]*)
  * **v_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **hand_type** (*tuple* *[**int* *,*  *...* *]*)
  * **user** (*int*)
  * **tool** (*int*)
  * **run_queued_cmd** (*int*)
  * **pause_cmd_flag** (*int*)
  * **velocity_ratio** (*int*)
  * **acceleration_ratio** (*int*)
  * **jerk_ratio** (*int*)
  * **xyz_velocity_ratio** (*int*)
  * **r_velocity_ratio** (*int*)
  * **xyz_acceleration_ratio** (*int*)
  * **r_acceleration_ratio** (*int*)
  * **xyz_jerk_ratio** (*int*)
  * **r_jerk_ratio** (*int*)
  * **brake_status** (*int*)
  * **enable_status** (*int*)
  * **drag_status** (*int*)
  * **running_status** (*int*)
  * **error_status** (*int*)
  * **jog_status** (*int*)
  * **robot_type** (*int*)
  * **drag_button_signal** (*int*)
  * **enable_button_signal** (*int*)
  * **record_button_signal** (*int*)
  * **reappear_button_signal** (*int*)
  * **jaw_button_signal** (*int*)
  * **six_force_online** (*int*)
  * **reserve2** (*tuple* *[**int* *,*  *...* *]*)
  * **m_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **load** (*float*)
  * **center_x** (*float*)
  * **center_y** (*float*)
  * **center_z** (*float*)
  * **user_coords** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_coords** (*tuple* *[**float* *,*  *...* *]*)
  * **trace_index** (*float*)
  * **six_force_value** (*tuple* *[**float* *,*  *...* *]*)
  * **target_quaternion** (*tuple* *[**float* *,*  *...* *]*)
  * **actual_quaternion** (*tuple* *[**float* *,*  *...* *]*)
  * **reserve3** (*tuple* *[**int* *,*  *...* *]*)

#### len

Total packet length in bytes.

* **Type:**
  int

#### digital_input_bits

Digital input bitmask.

* **Type:**
  int

#### digital_output_bits

Digital output bitmask.

* **Type:**
  int

#### robot_mode

Current robot mode code.

* **Type:**
  int

#### time_stamp

Controller timestamp.

* **Type:**
  int

#### time_stamp_reserve_bit

Reserved timestamp bits.

* **Type:**
  int

#### test_value

Internal test value.

* **Type:**
  int

#### test_value_keep_bit

Internal test keep bit.

* **Type:**
  float

#### speed_scaling

Global speed scaling factor (0-1).

* **Type:**
  float

#### linear_momentum_norm

Linear momentum magnitude.

* **Type:**
  float

#### v_main

Main voltage (V).

* **Type:**
  float

#### v_robot

Robot voltage (V).

* **Type:**
  float

#### i_robot

Robot current (A).

* **Type:**
  float

#### i_robot_keep_bit1

Reserved current field 1.

* **Type:**
  float

#### i_robot_keep_bit2

Reserved current field 2.

* **Type:**
  float

#### tool_accelerometer_values

Tool accelerometer XYZ (3 values).

* **Type:**
  tuple[float, …]

#### elbow_position

Elbow Cartesian position XYZ (3 values).

* **Type:**
  tuple[float, …]

#### elbow_velocity

Elbow Cartesian velocity XYZ (3 values).

* **Type:**
  tuple[float, …]

#### q_target

Target joint angles, radians (6 joints).

* **Type:**
  tuple[float, …]

#### qd_target

Target joint velocities, rad/s (6 joints).

* **Type:**
  tuple[float, …]

#### qdd_target

Target joint accelerations, rad/s² (6 joints).

* **Type:**
  tuple[float, …]

#### i_target

Target joint currents (6 joints).

* **Type:**
  tuple[float, …]

#### m_target

Target joint torques, N·m (6 joints).

* **Type:**
  tuple[float, …]

#### q_actual

Actual joint angles, radians (6 joints).

* **Type:**
  tuple[float, …]

#### qd_actual

Actual joint velocities, rad/s (6 joints).

* **Type:**
  tuple[float, …]

#### i_actual

Actual joint currents (6 joints).

* **Type:**
  tuple[float, …]

#### actual_tcp_force

Actual TCP force/torque (6 values).

* **Type:**
  tuple[float, …]

#### tool_vector_actual

Actual TCP pose [x, y, z, rx, ry, rz] (6 values).

* **Type:**
  tuple[float, …]

#### tcp_speed_actual

Actual TCP speed vector (6 values).

* **Type:**
  tuple[float, …]

#### tcp_force

TCP force/torque sensor reading (6 values).

* **Type:**
  tuple[float, …]

#### tool_vector_target

Target TCP pose (6 values).

* **Type:**
  tuple[float, …]

#### tcp_speed_target

Target TCP speed vector (6 values).

* **Type:**
  tuple[float, …]

#### motor_temperatures

Joint motor temperatures, °C (6 joints).

* **Type:**
  tuple[float, …]

#### joint_modes

Joint mode codes (6 joints).

* **Type:**
  tuple[float, …]

#### v_actual

Actual joint voltages (6 joints).

* **Type:**
  tuple[float, …]

#### hand_type

Hand type flags (4 bytes).

* **Type:**
  tuple[int, …]

#### user

Active user coordinate index.

* **Type:**
  int

#### tool

Active tool coordinate index.

* **Type:**
  int

#### run_queued_cmd

Whether queued command is running (1 = yes).

* **Type:**
  int

#### pause_cmd_flag

Pause command flag.

* **Type:**
  int

#### velocity_ratio

Joint velocity ratio (%).

* **Type:**
  int

#### acceleration_ratio

Joint acceleration ratio (%).

* **Type:**
  int

#### jerk_ratio

Joint jerk ratio (%).

* **Type:**
  int

#### xyz_velocity_ratio

Cartesian velocity ratio (%).

* **Type:**
  int

#### r_velocity_ratio

Rotational velocity ratio (%).

* **Type:**
  int

#### xyz_acceleration_ratio

Cartesian acceleration ratio (%).

* **Type:**
  int

#### r_acceleration_ratio

Rotational acceleration ratio (%).

* **Type:**
  int

#### xyz_jerk_ratio

Cartesian jerk ratio (%).

* **Type:**
  int

#### r_jerk_ratio

Rotational jerk ratio (%).

* **Type:**
  int

#### brake_status

Brake status bitmask.

* **Type:**
  int

#### enable_status

Robot enable status (1 = enabled).

* **Type:**
  int

#### drag_status

Drag mode status.

* **Type:**
  int

#### running_status

Motion running flag.

* **Type:**
  int

#### error_status

Error flag (non-zero = fault present).

* **Type:**
  int

#### jog_status

Jog mode status.

* **Type:**
  int

#### robot_type

Robot model type code.

* **Type:**
  int

#### drag_button_signal

Physical drag button signal.

* **Type:**
  int

#### enable_button_signal

Physical enable button signal.

* **Type:**
  int

#### record_button_signal

Physical record button signal.

* **Type:**
  int

#### reappear_button_signal

Physical reappear button signal.

* **Type:**
  int

#### jaw_button_signal

Jaw button signal.

* **Type:**
  int

#### six_force_online

Six-axis force sensor online flag.

* **Type:**
  int

#### reserve2

Reserved bytes (82 bytes).

* **Type:**
  tuple[int, …]

#### m_actual

Actual joint torques, N·m (6 joints).

* **Type:**
  tuple[float, …]

#### load

Payload mass, kg.

* **Type:**
  float

#### center_x

Payload centre-of-mass X offset, mm.

* **Type:**
  float

#### center_y

Payload centre-of-mass Y offset, mm.

* **Type:**
  float

#### center_z

Payload centre-of-mass Z offset, mm.

* **Type:**
  float

#### user_coords

Active user coordinate frame [x, y, z, rx, ry, rz].

* **Type:**
  tuple[float, …]

#### tool_coords

Active tool coordinate frame [x, y, z, rx, ry, rz].

* **Type:**
  tuple[float, …]

#### trace_index

Current trace index.

* **Type:**
  float

#### six_force_value

Six-axis force sensor readings (6 values).

* **Type:**
  tuple[float, …]

#### target_quaternion

Target TCP orientation quaternion [w, x, y, z].

* **Type:**
  tuple[float, …]

#### actual_quaternion

Actual TCP orientation quaternion [w, x, y, z].

* **Type:**
  tuple[float, …]

#### reserve3

Reserved bytes (24 bytes).

* **Type:**
  tuple[int, …]

### Example

```python
>>> data = robot.feedback_data()
>>> if data is not None:
...     print(data.robot_mode)
...     print(data.tool_vector_actual)
...     print(data.enable_status)
```

#### len *: int*

#### digital_input_bits *: int*

#### digital_output_bits *: int*

#### robot_mode *: int*

#### time_stamp *: int*

#### time_stamp_reserve_bit *: int*

#### test_value *: int*

#### test_value_keep_bit *: float*

#### speed_scaling *: float*

#### linear_momentum_norm *: float*

#### v_main *: float*

#### v_robot *: float*

#### i_robot *: float*

#### i_robot_keep_bit1 *: float*

#### i_robot_keep_bit2 *: float*

#### tool_accelerometer_values *: tuple[float, ...]*

#### elbow_position *: tuple[float, ...]*

#### elbow_velocity *: tuple[float, ...]*

#### q_target *: tuple[float, ...]*

#### qd_target *: tuple[float, ...]*

#### qdd_target *: tuple[float, ...]*

#### i_target *: tuple[float, ...]*

#### m_target *: tuple[float, ...]*

#### q_actual *: tuple[float, ...]*

#### qd_actual *: tuple[float, ...]*

#### i_actual *: tuple[float, ...]*

#### actual_tcp_force *: tuple[float, ...]*

#### tool_vector_actual *: tuple[float, ...]*

#### tcp_speed_actual *: tuple[float, ...]*

#### tcp_force *: tuple[float, ...]*

#### tool_vector_target *: tuple[float, ...]*

#### tcp_speed_target *: tuple[float, ...]*

#### motor_temperatures *: tuple[float, ...]*

#### joint_modes *: tuple[float, ...]*

#### v_actual *: tuple[float, ...]*

#### hand_type *: tuple[int, ...]*

#### user *: int*

#### tool *: int*

#### run_queued_cmd *: int*

#### pause_cmd_flag *: int*

#### velocity_ratio *: int*

#### acceleration_ratio *: int*

#### jerk_ratio *: int*

#### xyz_velocity_ratio *: int*

#### r_velocity_ratio *: int*

#### xyz_acceleration_ratio *: int*

#### r_acceleration_ratio *: int*

#### xyz_jerk_ratio *: int*

#### r_jerk_ratio *: int*

#### brake_status *: int*

#### enable_status *: int*

#### drag_status *: int*

#### running_status *: int*

#### error_status *: int*

#### jog_status *: int*

#### robot_type *: int*

#### drag_button_signal *: int*

#### enable_button_signal *: int*

#### record_button_signal *: int*

#### reappear_button_signal *: int*

#### jaw_button_signal *: int*

#### six_force_online *: int*

#### reserve2 *: tuple[int, ...]*

#### m_actual *: tuple[float, ...]*

#### load *: float*

#### center_x *: float*

#### center_y *: float*

#### center_z *: float*

#### user_coords *: tuple[float, ...]*

#### tool_coords *: tuple[float, ...]*

#### trace_index *: float*

#### six_force_value *: tuple[float, ...]*

#### target_quaternion *: tuple[float, ...]*

#### actual_quaternion *: tuple[float, ...]*

#### reserve3 *: tuple[int, ...]*

#### *classmethod* from_numpy(arr)

Construct a `FeedbackData` from a raw structured NumPy array.

* **Parameters:**
  **arr** (*ndarray*) – A 1-element NumPy structured array decoded with
  `FeedbackDtype`, as returned by
  `np.frombuffer(buf, dtype=FeedbackDtype)`.
* **Returns:**
  Immutable `FeedbackData` snapshot with all fields converted
  to plain Python scalars or tuples.
* **Return type:**
  [*FeedbackData*](#dobot_api_v3.base.FeedbackData)

### Example

```python
>>> raw = np.frombuffer(buf, dtype=FeedbackDtype)
>>> data = FeedbackData.from_numpy(raw)
>>> data.robot_mode
```

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

### *exception* dobot_api_v3.DobotApiError(error_code, command_id, message, raw)

Bases: `Exception`

Raised when the Dobot controller returns a non-zero error code
or when the response string cannot be parsed.

* **Parameters:**
  * **error_code** (*int*)
  * **command_id** (*int*)
  * **message** (*str*)
  * **raw** (*str*)
* **Return type:**
  None

#### error_code

The integer error code from the response (negative for
parse failures).

#### command_id

The command queue ID from the response (0 when absent).

#### message

Human-readable detail extracted from the payload.

#### raw

The original response string received from the robot.

### *class* dobot_api_v3.AckResponse(command_id)

Bases: `object`

Simple acknowledgment response with no data payload.

Returned by lifecycle commands (`enable_robot`, `disable_robot`, …)
and all motion commands (`mov_j`, `sync`, …).

* **Parameters:**
  **command_id** (*int*)

#### command_id

Motion-queue command ID from the controller (often 0).

* **Type:**
  int

#### command_id *: int*

### *class* dobot_api_v3.IntResponse(command_id, value)

Bases: `object`

Single integer value response.

Returned by status-query commands such as `robot_mode`.

* **Parameters:**
  * **command_id** (*int*)
  * **value** (*int*)

#### command_id

Motion-queue command ID from the controller.

* **Type:**
  int

#### value

The integer value returned by the controller.

* **Type:**
  int

#### command_id *: int*

#### value *: int*

### *class* dobot_api_v3.PoseResponse(command_id, x, y, z, rx, ry, rz)

Bases: `object`

Six-degree-of-freedom pose or joint-angle response.

Returned by `get_pose` (Cartesian) and `get_angle` (joint).

* **Parameters:**
  * **command_id** (*int*)
  * **x** (*float*)
  * **y** (*float*)
  * **z** (*float*)
  * **rx** (*float*)
  * **ry** (*float*)
  * **rz** (*float*)

#### command_id

Motion-queue command ID from the controller.

* **Type:**
  int

#### x

X coordinate or joint-1 angle.

* **Type:**
  float

#### y

Y coordinate or joint-2 angle.

* **Type:**
  float

#### z

Z coordinate or joint-3 angle.

* **Type:**
  float

#### rx

RX rotation or joint-4 angle.

* **Type:**
  float

#### ry

RY rotation or joint-5 angle.

* **Type:**
  float

#### rz

RZ rotation or joint-6 angle.

* **Type:**
  float

#### command_id *: int*

#### x *: float*

#### y *: float*

#### z *: float*

#### rx *: float*

#### ry *: float*

#### rz *: float*

### *class* dobot_api_v3.ErrorIdResponse(command_id, error_ids)

Bases: `object`

Alarm / error-ID list response.

Returned by `get_error_id`.  Zero sentinel values from the controller
are filtered out, matching the behaviour of
`RobotErrorMonitor`.

* **Parameters:**
  * **command_id** (*int*)
  * **error_ids** (*Tuple* *[**int* *,*  *...* *]*)

#### command_id

Motion-queue command ID from the controller.

* **Type:**
  int

#### error_ids

Tuple of non-zero alarm codes active on the controller.

* **Type:**
  Tuple[int, …]

#### command_id *: int*

#### error_ids *: Tuple[int, ...]*

### dobot_api_v3.parse_response(raw, response_type)

Parse a raw Dobot TCP response string into a typed dataclass.

Accepts both Dobot response formats:

* `"error_code,command_id,payload;"` — 3-field plain
* `"error_code,{brace_payload};"` — 2-field brace

* **Parameters:**
  * **raw** (*str*) – The raw response string received from the robot controller.
  * **response_type** (*Type* *[* *\_ResponseT* *]*) – The dataclass type to parse into.  Must be one of
    `AckResponse`, `IntResponse`,
    `PoseResponse`, or `ErrorIdResponse`.
* **Returns:**
  A populated, frozen response dataclass instance.
* **Raises:**
  **DobotApiError** – If the controller reports a non-zero error code, or
      if the response string is malformed / missing expected values.
* **Return type:**
   *\_ResponseT*

### Example

```python
>>> raw = dashboard.robot_mode()
>>> resp = parse_response(raw, IntResponse)
>>> print(resp.value)
5
```

<a id="module-dobot_api_v3.base"></a>

Base classes and data types for Dobot API.

### *class* dobot_api_v3.base.FeedbackData(len, digital_input_bits, digital_output_bits, robot_mode, time_stamp, time_stamp_reserve_bit, test_value, test_value_keep_bit, speed_scaling, linear_momentum_norm, v_main, v_robot, i_robot, i_robot_keep_bit1, i_robot_keep_bit2, tool_accelerometer_values, elbow_position, elbow_velocity, q_target, qd_target, qdd_target, i_target, m_target, q_actual, qd_actual, i_actual, actual_tcp_force, tool_vector_actual, tcp_speed_actual, tcp_force, tool_vector_target, tcp_speed_target, motor_temperatures, joint_modes, v_actual, hand_type, user, tool, run_queued_cmd, pause_cmd_flag, velocity_ratio, acceleration_ratio, jerk_ratio, xyz_velocity_ratio, r_velocity_ratio, xyz_acceleration_ratio, r_acceleration_ratio, xyz_jerk_ratio, r_jerk_ratio, brake_status, enable_status, drag_status, running_status, error_status, jog_status, robot_type, drag_button_signal, enable_button_signal, record_button_signal, reappear_button_signal, jaw_button_signal, six_force_online, reserve2, m_actual, load, center_x, center_y, center_z, user_coords, tool_coords, trace_index, six_force_value, target_quaternion, actual_quaternion, reserve3)

Bases: `object`

Immutable snapshot of one decoded feedback packet (1440 bytes).

All scalar fields are plain Python `int` or `float`.  Multi-element
fields (joint arrays, vectors, quaternions, …) are `tuple[float, ...]`
or `tuple[int, ...]`.  Because the dataclass is frozen, field values
cannot be mutated after construction — treat each instance as a read-only
timestamped snapshot.

Use [`from_numpy()`](#dobot_api_v3.base.FeedbackData.from_numpy) to construct a `FeedbackData` from the raw
`np.ndarray` produced by `np.frombuffer(buf, dtype=FeedbackDtype)`.
For direct NumPy access call `raw_feedback_data()` instead of
`feedback_data()`.

* **Parameters:**
  * **len** (*int*)
  * **digital_input_bits** (*int*)
  * **digital_output_bits** (*int*)
  * **robot_mode** (*int*)
  * **time_stamp** (*int*)
  * **time_stamp_reserve_bit** (*int*)
  * **test_value** (*int*)
  * **test_value_keep_bit** (*float*)
  * **speed_scaling** (*float*)
  * **linear_momentum_norm** (*float*)
  * **v_main** (*float*)
  * **v_robot** (*float*)
  * **i_robot** (*float*)
  * **i_robot_keep_bit1** (*float*)
  * **i_robot_keep_bit2** (*float*)
  * **tool_accelerometer_values** (*tuple* *[**float* *,*  *...* *]*)
  * **elbow_position** (*tuple* *[**float* *,*  *...* *]*)
  * **elbow_velocity** (*tuple* *[**float* *,*  *...* *]*)
  * **q_target** (*tuple* *[**float* *,*  *...* *]*)
  * **qd_target** (*tuple* *[**float* *,*  *...* *]*)
  * **qdd_target** (*tuple* *[**float* *,*  *...* *]*)
  * **i_target** (*tuple* *[**float* *,*  *...* *]*)
  * **m_target** (*tuple* *[**float* *,*  *...* *]*)
  * **q_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **qd_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **i_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **actual_tcp_force** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_vector_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_speed_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_force** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_vector_target** (*tuple* *[**float* *,*  *...* *]*)
  * **tcp_speed_target** (*tuple* *[**float* *,*  *...* *]*)
  * **motor_temperatures** (*tuple* *[**float* *,*  *...* *]*)
  * **joint_modes** (*tuple* *[**float* *,*  *...* *]*)
  * **v_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **hand_type** (*tuple* *[**int* *,*  *...* *]*)
  * **user** (*int*)
  * **tool** (*int*)
  * **run_queued_cmd** (*int*)
  * **pause_cmd_flag** (*int*)
  * **velocity_ratio** (*int*)
  * **acceleration_ratio** (*int*)
  * **jerk_ratio** (*int*)
  * **xyz_velocity_ratio** (*int*)
  * **r_velocity_ratio** (*int*)
  * **xyz_acceleration_ratio** (*int*)
  * **r_acceleration_ratio** (*int*)
  * **xyz_jerk_ratio** (*int*)
  * **r_jerk_ratio** (*int*)
  * **brake_status** (*int*)
  * **enable_status** (*int*)
  * **drag_status** (*int*)
  * **running_status** (*int*)
  * **error_status** (*int*)
  * **jog_status** (*int*)
  * **robot_type** (*int*)
  * **drag_button_signal** (*int*)
  * **enable_button_signal** (*int*)
  * **record_button_signal** (*int*)
  * **reappear_button_signal** (*int*)
  * **jaw_button_signal** (*int*)
  * **six_force_online** (*int*)
  * **reserve2** (*tuple* *[**int* *,*  *...* *]*)
  * **m_actual** (*tuple* *[**float* *,*  *...* *]*)
  * **load** (*float*)
  * **center_x** (*float*)
  * **center_y** (*float*)
  * **center_z** (*float*)
  * **user_coords** (*tuple* *[**float* *,*  *...* *]*)
  * **tool_coords** (*tuple* *[**float* *,*  *...* *]*)
  * **trace_index** (*float*)
  * **six_force_value** (*tuple* *[**float* *,*  *...* *]*)
  * **target_quaternion** (*tuple* *[**float* *,*  *...* *]*)
  * **actual_quaternion** (*tuple* *[**float* *,*  *...* *]*)
  * **reserve3** (*tuple* *[**int* *,*  *...* *]*)

#### len

Total packet length in bytes.

* **Type:**
  int

#### digital_input_bits

Digital input bitmask.

* **Type:**
  int

#### digital_output_bits

Digital output bitmask.

* **Type:**
  int

#### robot_mode

Current robot mode code.

* **Type:**
  int

#### time_stamp

Controller timestamp.

* **Type:**
  int

#### time_stamp_reserve_bit

Reserved timestamp bits.

* **Type:**
  int

#### test_value

Internal test value.

* **Type:**
  int

#### test_value_keep_bit

Internal test keep bit.

* **Type:**
  float

#### speed_scaling

Global speed scaling factor (0-1).

* **Type:**
  float

#### linear_momentum_norm

Linear momentum magnitude.

* **Type:**
  float

#### v_main

Main voltage (V).

* **Type:**
  float

#### v_robot

Robot voltage (V).

* **Type:**
  float

#### i_robot

Robot current (A).

* **Type:**
  float

#### i_robot_keep_bit1

Reserved current field 1.

* **Type:**
  float

#### i_robot_keep_bit2

Reserved current field 2.

* **Type:**
  float

#### tool_accelerometer_values

Tool accelerometer XYZ (3 values).

* **Type:**
  tuple[float, …]

#### elbow_position

Elbow Cartesian position XYZ (3 values).

* **Type:**
  tuple[float, …]

#### elbow_velocity

Elbow Cartesian velocity XYZ (3 values).

* **Type:**
  tuple[float, …]

#### q_target

Target joint angles, radians (6 joints).

* **Type:**
  tuple[float, …]

#### qd_target

Target joint velocities, rad/s (6 joints).

* **Type:**
  tuple[float, …]

#### qdd_target

Target joint accelerations, rad/s² (6 joints).

* **Type:**
  tuple[float, …]

#### i_target

Target joint currents (6 joints).

* **Type:**
  tuple[float, …]

#### m_target

Target joint torques, N·m (6 joints).

* **Type:**
  tuple[float, …]

#### q_actual

Actual joint angles, radians (6 joints).

* **Type:**
  tuple[float, …]

#### qd_actual

Actual joint velocities, rad/s (6 joints).

* **Type:**
  tuple[float, …]

#### i_actual

Actual joint currents (6 joints).

* **Type:**
  tuple[float, …]

#### actual_tcp_force

Actual TCP force/torque (6 values).

* **Type:**
  tuple[float, …]

#### tool_vector_actual

Actual TCP pose [x, y, z, rx, ry, rz] (6 values).

* **Type:**
  tuple[float, …]

#### tcp_speed_actual

Actual TCP speed vector (6 values).

* **Type:**
  tuple[float, …]

#### tcp_force

TCP force/torque sensor reading (6 values).

* **Type:**
  tuple[float, …]

#### tool_vector_target

Target TCP pose (6 values).

* **Type:**
  tuple[float, …]

#### tcp_speed_target

Target TCP speed vector (6 values).

* **Type:**
  tuple[float, …]

#### motor_temperatures

Joint motor temperatures, °C (6 joints).

* **Type:**
  tuple[float, …]

#### joint_modes

Joint mode codes (6 joints).

* **Type:**
  tuple[float, …]

#### v_actual

Actual joint voltages (6 joints).

* **Type:**
  tuple[float, …]

#### hand_type

Hand type flags (4 bytes).

* **Type:**
  tuple[int, …]

#### user

Active user coordinate index.

* **Type:**
  int

#### tool

Active tool coordinate index.

* **Type:**
  int

#### run_queued_cmd

Whether queued command is running (1 = yes).

* **Type:**
  int

#### pause_cmd_flag

Pause command flag.

* **Type:**
  int

#### velocity_ratio

Joint velocity ratio (%).

* **Type:**
  int

#### acceleration_ratio

Joint acceleration ratio (%).

* **Type:**
  int

#### jerk_ratio

Joint jerk ratio (%).

* **Type:**
  int

#### xyz_velocity_ratio

Cartesian velocity ratio (%).

* **Type:**
  int

#### r_velocity_ratio

Rotational velocity ratio (%).

* **Type:**
  int

#### xyz_acceleration_ratio

Cartesian acceleration ratio (%).

* **Type:**
  int

#### r_acceleration_ratio

Rotational acceleration ratio (%).

* **Type:**
  int

#### xyz_jerk_ratio

Cartesian jerk ratio (%).

* **Type:**
  int

#### r_jerk_ratio

Rotational jerk ratio (%).

* **Type:**
  int

#### brake_status

Brake status bitmask.

* **Type:**
  int

#### enable_status

Robot enable status (1 = enabled).

* **Type:**
  int

#### drag_status

Drag mode status.

* **Type:**
  int

#### running_status

Motion running flag.

* **Type:**
  int

#### error_status

Error flag (non-zero = fault present).

* **Type:**
  int

#### jog_status

Jog mode status.

* **Type:**
  int

#### robot_type

Robot model type code.

* **Type:**
  int

#### drag_button_signal

Physical drag button signal.

* **Type:**
  int

#### enable_button_signal

Physical enable button signal.

* **Type:**
  int

#### record_button_signal

Physical record button signal.

* **Type:**
  int

#### reappear_button_signal

Physical reappear button signal.

* **Type:**
  int

#### jaw_button_signal

Jaw button signal.

* **Type:**
  int

#### six_force_online

Six-axis force sensor online flag.

* **Type:**
  int

#### reserve2

Reserved bytes (82 bytes).

* **Type:**
  tuple[int, …]

#### m_actual

Actual joint torques, N·m (6 joints).

* **Type:**
  tuple[float, …]

#### load

Payload mass, kg.

* **Type:**
  float

#### center_x

Payload centre-of-mass X offset, mm.

* **Type:**
  float

#### center_y

Payload centre-of-mass Y offset, mm.

* **Type:**
  float

#### center_z

Payload centre-of-mass Z offset, mm.

* **Type:**
  float

#### user_coords

Active user coordinate frame [x, y, z, rx, ry, rz].

* **Type:**
  tuple[float, …]

#### tool_coords

Active tool coordinate frame [x, y, z, rx, ry, rz].

* **Type:**
  tuple[float, …]

#### trace_index

Current trace index.

* **Type:**
  float

#### six_force_value

Six-axis force sensor readings (6 values).

* **Type:**
  tuple[float, …]

#### target_quaternion

Target TCP orientation quaternion [w, x, y, z].

* **Type:**
  tuple[float, …]

#### actual_quaternion

Actual TCP orientation quaternion [w, x, y, z].

* **Type:**
  tuple[float, …]

#### reserve3

Reserved bytes (24 bytes).

* **Type:**
  tuple[int, …]

### Example

```python
>>> data = robot.feedback_data()
>>> if data is not None:
...     print(data.robot_mode)
...     print(data.tool_vector_actual)
...     print(data.enable_status)
```

#### len *: int*

#### digital_input_bits *: int*

#### digital_output_bits *: int*

#### robot_mode *: int*

#### time_stamp *: int*

#### time_stamp_reserve_bit *: int*

#### test_value *: int*

#### test_value_keep_bit *: float*

#### speed_scaling *: float*

#### linear_momentum_norm *: float*

#### v_main *: float*

#### v_robot *: float*

#### i_robot *: float*

#### i_robot_keep_bit1 *: float*

#### i_robot_keep_bit2 *: float*

#### tool_accelerometer_values *: tuple[float, ...]*

#### elbow_position *: tuple[float, ...]*

#### elbow_velocity *: tuple[float, ...]*

#### q_target *: tuple[float, ...]*

#### qd_target *: tuple[float, ...]*

#### qdd_target *: tuple[float, ...]*

#### i_target *: tuple[float, ...]*

#### m_target *: tuple[float, ...]*

#### q_actual *: tuple[float, ...]*

#### qd_actual *: tuple[float, ...]*

#### i_actual *: tuple[float, ...]*

#### actual_tcp_force *: tuple[float, ...]*

#### tool_vector_actual *: tuple[float, ...]*

#### tcp_speed_actual *: tuple[float, ...]*

#### tcp_force *: tuple[float, ...]*

#### tool_vector_target *: tuple[float, ...]*

#### tcp_speed_target *: tuple[float, ...]*

#### motor_temperatures *: tuple[float, ...]*

#### joint_modes *: tuple[float, ...]*

#### v_actual *: tuple[float, ...]*

#### hand_type *: tuple[int, ...]*

#### user *: int*

#### tool *: int*

#### run_queued_cmd *: int*

#### pause_cmd_flag *: int*

#### velocity_ratio *: int*

#### acceleration_ratio *: int*

#### jerk_ratio *: int*

#### xyz_velocity_ratio *: int*

#### r_velocity_ratio *: int*

#### xyz_acceleration_ratio *: int*

#### r_acceleration_ratio *: int*

#### xyz_jerk_ratio *: int*

#### r_jerk_ratio *: int*

#### brake_status *: int*

#### enable_status *: int*

#### drag_status *: int*

#### running_status *: int*

#### error_status *: int*

#### jog_status *: int*

#### robot_type *: int*

#### drag_button_signal *: int*

#### enable_button_signal *: int*

#### record_button_signal *: int*

#### reappear_button_signal *: int*

#### jaw_button_signal *: int*

#### six_force_online *: int*

#### reserve2 *: tuple[int, ...]*

#### m_actual *: tuple[float, ...]*

#### load *: float*

#### center_x *: float*

#### center_y *: float*

#### center_z *: float*

#### user_coords *: tuple[float, ...]*

#### tool_coords *: tuple[float, ...]*

#### trace_index *: float*

#### six_force_value *: tuple[float, ...]*

#### target_quaternion *: tuple[float, ...]*

#### actual_quaternion *: tuple[float, ...]*

#### reserve3 *: tuple[int, ...]*

#### *classmethod* from_numpy(arr)

Construct a [`FeedbackData`](#dobot_api_v3.base.FeedbackData) from a raw structured NumPy array.

* **Parameters:**
  **arr** (*ndarray*) – A 1-element NumPy structured array decoded with
  `FeedbackDtype`, as returned by
  `np.frombuffer(buf, dtype=FeedbackDtype)`.
* **Returns:**
  Immutable [`FeedbackData`](#dobot_api_v3.base.FeedbackData) snapshot with all fields converted
  to plain Python scalars or tuples.
* **Return type:**
  [*FeedbackData*](#dobot_api_v3.base.FeedbackData)

### Example

```python
>>> raw = np.frombuffer(buf, dtype=FeedbackDtype)
>>> data = FeedbackData.from_numpy(raw)
>>> data.robot_mode
```

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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

#### raw_feedback_data()

Read one feedback frame and return the raw NumPy structured array.

Use this method when you need zero-copy NumPy access to the packet
fields (e.g., for numeric pipelines or direct array slicing).  For
typed, IDE-friendly access prefer [`feedback_data()`](#dobot_api_v3.feedback.DobotApiFeedback.feedback_data) instead.

* **Returns:**
  A NumPy structured array of length 1 (`dtype=FeedbackDtype`)
  when a valid 1440-byte frame is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  *ndarray* | None

#### feedback_data()

Read one feedback frame and return a typed `FeedbackData`.

Internally calls [`raw_feedback_data()`](#dobot_api_v3.feedback.DobotApiFeedback.raw_feedback_data) and converts the result to
an immutable `FeedbackData` dataclass for full
IDE autocompletion and type-checker support.

For zero-copy NumPy access (e.g., numeric pipelines) use
[`raw_feedback_data()`](#dobot_api_v3.feedback.DobotApiFeedback.raw_feedback_data) directly.

* **Returns:**
  A `FeedbackData` instance when a valid
  1440-byte frame is parsed, otherwise `None`.
* **Raises:**
  * **RuntimeError** – If the socket is not connected.
  * **RuntimeError** – If repeated short reads indicate packet loss.
* **Return type:**
  [*FeedbackData*](#dobot_api_v3.base.FeedbackData) | None

### Example

```python
>>> data = feedback.feedback_data()
>>> if data is not None:
...     print(data.robot_mode)
...     print(data.tool_vector_actual)
```

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
