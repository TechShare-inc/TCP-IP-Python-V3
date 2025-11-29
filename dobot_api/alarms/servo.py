"""ServoAlarms alarm definitions."""

from __future__ import annotations

from dobot_api.alarms.models import AlarmInfo, AlarmLevel, LocalizedText


class ServoAlarms:
    """Servo alarm database.

    Contains 88 alarm definitions.
    """

    _alarms: dict[int, AlarmInfo] = {}

    @classmethod
    def get(cls, alarm_id: int) -> AlarmInfo | None:
        """Get alarm by ID."""
        return cls._alarms.get(alarm_id)

    @classmethod
    def all(cls) -> dict[int, AlarmInfo]:
        """Get all alarms."""
        return cls._alarms.copy()


# Alarm definitions
ServoAlarms._alarms = {
    2: AlarmInfo(
        id=2,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="SoftMotion axis is wrong",
            cause="",
            solution="Check whether the communication of joints is working properly, then clear the alarm， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴错误",
            cause="",
            solution="检查关节通信是否正常，再清除告警，或联系技术支持工程师",
        ),
    ),
    3: AlarmInfo(
        id=3,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Bus synchoronic mode is abnormal",
            cause="",
            solution="Check whether the communication of joints is working properly, clear the alarm， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="总线同步模式失效",
            cause="",
            solution="检查关节通信是否正常，再清除告警，或联系技术支持工程师",
        ),
    ),
    10: AlarmInfo(
        id=10,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The current position is out of Software limit",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="当前位置已超出软限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    11: AlarmInfo(
        id=11,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The current position is out of Hardware limit",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="当前位置已达硬限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    12: AlarmInfo(
        id=12,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameters of SoftMotion command are out of range",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion指令的输入参数超出范围",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    13: AlarmInfo(
        id=13,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The servo does not support emergency stop or fast stop",
            cause="",
            solution="Please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="该伺服不支持急停/快停",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    14: AlarmInfo(
        id=14,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The servo dose not power on",
            cause="",
            solution="Check  whether the hardware is working properly, and power on again， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服未上电",
            cause="",
            solution="检查硬件是否正常，再重新上电，或联系技术支持工程师",
        ),
    ),
    16: AlarmInfo(
        id=16,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Difference between the set position and current position exceeds the range",
            cause="",
            solution="Check whether the motor and circuit are working properly, and adjust the servo parameters",
        ),
        zh_CN=LocalizedText(
            description="位置预设值与当前位置出现超差",
            cause="",
            solution="检测电机和线路是否正常，并调整伺服参数",
        ),
    ),
    17: AlarmInfo(
        id=17,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Homing error",
            cause="",
            solution="Please operate homing procedure  again",
        ),
        zh_CN=LocalizedText(
            description="回零错误",
            cause="",
            solution="重新回零",
        ),
    ),
    18: AlarmInfo(
        id=18,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The license is lost",
            cause="",
            solution="Re-acquire license",
        ),
        zh_CN=LocalizedText(
            description="许可证缺失",
            cause="",
            solution="重新获取许可证",
        ),
    ),
    20: AlarmInfo(
        id=20,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The sevo is disabled",
            cause="",
            solution="Enable the servo",
        ),
        zh_CN=LocalizedText(
            description="运动前尚未使能伺服",
            cause="",
            solution="使能伺服",
        ),
    ),
    21: AlarmInfo(
        id=21,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Control mode of SoftMotion axis is wrong",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴控制模式错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    25: AlarmInfo(
        id=25,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Invalid action at logical axis",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="当前SoftMotion轴为逻辑轴，不支持该操作",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    30: AlarmInfo(
        id=30,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Interpolation module is not called again before the motion is over",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="运动过程结束前，插补模块未被再次调用",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    31: AlarmInfo(
        id=31,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="AXIS_REF variable has been replaced when the SoftMotion module was called",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion模块输入并非AXIS_REF类型",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    32: AlarmInfo(
        id=32,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="AXIS_REF variable has been replaced when the SoftMotion module was called",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion模块调用中AXIS_REF变量被替换",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    33: AlarmInfo(
        id=33,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The SoftMotion axis is disabled when it is running",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴运行中，被下使能",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    34: AlarmInfo(
        id=34,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="CAN NOT execute motion commands when the SoftMotion axis is in the current state",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴当前状态不能执行运动命令",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    35: AlarmInfo(
        id=35,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The servo drive is abnormal when the SoftMotion is running",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion运行中，伺服驱动器报错",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    40: AlarmInfo(
        id=40,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Working speed is higher than the expected speed",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="运行速度超过SoftMotion轴限制",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    41: AlarmInfo(
        id=41,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Working acceleration is higher than the expected acceleration",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="运行加速度超过SoftMotion轴限制",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    42: AlarmInfo(
        id=42,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Working deceleration is higher than the expected deceleration",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="运行减速度超过SoftMotion轴限制",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    50: AlarmInfo(
        id=50,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Invalid velocity or acceleration values",
            cause="",
            solution="Reset speed or acceleration",
        ),
        zh_CN=LocalizedText(
            description="速度或加速度不合适",
            cause="",
            solution="重新设置速度或加速度",
        ),
    ),
    51: AlarmInfo(
        id=51,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="In this mode, the hardware limit is required, please set it",
            cause="",
            solution="Please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="为安全考虑，本模式需使用硬限位，请在SoftMotion轴中进行配置",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    60: AlarmInfo(
        id=60,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to open CNC file",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="无法打开CNC文件",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    70: AlarmInfo(
        id=70,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Invalid control mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="不支持当前的控制模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    71: AlarmInfo(
        id=71,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="In current mode, controller mode CAN NOT be modified",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="当前模式下，控制器模式不可改变",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    72: AlarmInfo(
        id=72,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="SMC_SetControllerMode has been interrupted by MC_Stop or errorstop",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="SMC_SetControllerMode的执行被MC_Stop或errorstop状态打断",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    80: AlarmInfo(
        id=80,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="SoftMotion axes Initialization is wrong",
            cause="",
            solution="Power on again",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴组初始化错误",
            cause="",
            solution="重新上电",
        ),
    ),
    81: AlarmInfo(
        id=81,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The SoftMotion axis is not in the required state",
            cause="",
            solution="The SoftMotion axis switches to the corresponding state",
        ),
        zh_CN=LocalizedText(
            description="SoftMotion轴尚未切换到对应状态",
            cause="",
            solution="SoftMotion轴切换到对应状态",
        ),
    ),
    85: AlarmInfo(
        id=85,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The function does not support virtual or logical mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="调用的功能块不支持虚拟或者逻辑模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    86: AlarmInfo(
        id=86,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The bit width is invalid",
            cause="",
            solution="Reset the bit width, volue ranges from 8 to 32",
        ),
        zh_CN=LocalizedText(
            description="绝对位宽不合适",
            cause="",
            solution="重新设置绝对位宽，取值范围[8，32]",
        ),
    ),
    91: AlarmInfo(
        id=91,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Reduction ratio parameters does not be modified when the servo is working",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="在控制伺服过程中，减速比参数不可改变",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    92: AlarmInfo(
        id=92,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Invalid module period",
            cause="",
            solution="Reset module period, it is lower than 0 or greater than half of the bandwidth, or please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="无效的模数周期",
            cause="",
            solution="重新配置模数周期，模数周期小于等于零或大于带宽的一半，或联系技术支持工程师",
        ),
    ),
    93: AlarmInfo(
        id=93,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The pulse value of module period is not an integer",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="模数配置换算到脉冲值，并非整型",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    110: AlarmInfo(
        id=110,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The fTaskCycle is set to 0",
            cause="",
            solution="Reset the fTaskCycle ",
        ),
        zh_CN=LocalizedText(
            description="fTaskCycle被设置为0",
            cause="",
            solution="正确设置fTaskCycle",
        ),
    ),
    121: AlarmInfo(
        id=121,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Servo has no response to the reset command",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服对复位命令无响应",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    122: AlarmInfo(
        id=122,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Unable to reset",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="无法复位",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    123: AlarmInfo(
        id=123,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The servo communication is abnormal",
            cause="",
            solution="Check the EtheCAT node connection, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服通讯未工作",
            cause="",
            solution="检查EtheCAT节点连接是否正常，或联系技术支持工程师",
        ),
    ),
    170: AlarmInfo(
        id=170,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis is not enabled",
            cause="",
            solution="Enable axis",
        ),
        zh_CN=LocalizedText(
            description="轴尚未在使能状态",
            cause="",
            solution="使能轴",
        ),
    ),
    171: AlarmInfo(
        id=171,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Homing operation is wrong. The SofotMotion axis is not operated homing procedure",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="回零操作出错，SoftMotion轴未开始回零",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    172: AlarmInfo(
        id=172,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Homing operation is wrong. The SofotMotion has no response to the Homing operation",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="回零操作出错，SoftMotion轴未响应",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    173: AlarmInfo(
        id=173,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Homing operation is wrong. The deceleration is not set",
            cause="",
            solution="Set deceleration",
        ),
        zh_CN=LocalizedText(
            description="回零操作出错，回零停止错误，减速度未配置",
            cause="",
            solution="配置减加速度",
        ),
    ),
    174: AlarmInfo(
        id=174,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Homing operation is wrong. The servo is in the error status",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="回零操作出错，伺服在错误状态，无法回零",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    1000: AlarmInfo(
        id=1000,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="CNC license is lost",
            cause="",
            solution="Add CNC license",
        ),
        zh_CN=LocalizedText(
            description="CNC许可证缺失",
            cause="",
            solution="添加CNC许可证",
        ),
    ),
    5000: AlarmInfo(
        id=5000,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Denominator of reduction ratio is 0",
            cause="",
            solution="Reset the denominator of reduction ratio",
        ),
        zh_CN=LocalizedText(
            description="减速比分母为零",
            cause="",
            solution="重新设置减速比分母",
        ),
    ),
    60929: AlarmInfo(
        id=60929,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Communication error",
            cause="",
            solution="Check whether the hardware is working properly, restart controller, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="通讯错误",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    8752: AlarmInfo(
        id=8752,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="IPM abnormality",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="IPM异常保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    8992: AlarmInfo(
        id=8992,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Software over-current",
            cause="",
            solution="Power off and restart controller, or please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="软件过流保护",
            cause="",
            solution="断电重新启动，或联系技术支持工程师",
        ),
    ),
    9088: AlarmInfo(
        id=9088,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The current offset of homing point is too high",
            cause="",
            solution="Reset the Zero point current offset",
        ),
        zh_CN=LocalizedText(
            description="零点电流偏置过大保护",
            cause="",
            solution="重新设置零点电流偏置",
        ),
    ),
    30080: AlarmInfo(
        id=30080,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="EtherCAT communication is abnormal",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="EtherCAT通讯异常保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    33920: AlarmInfo(
        id=33920,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Output speed is higher than the expected speed",
            cause="",
            solution="Reduce the output speed",
        ),
        zh_CN=LocalizedText(
            description="超过最大转速保护",
            cause="",
            solution="减小输出转速",
        ),
    ),
    33921: AlarmInfo(
        id=33921,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Difference between the set speed and current speed exceeds the range",
            cause="",
            solution="Check whether the hardware is working properly, restart the controller, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="速度偏差过大保护",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    33922: AlarmInfo(
        id=33922,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Motor is stalled ",
            cause="",
            solution="Check whether the motor is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="电机失速保护",
            cause="",
            solution="检查电机是否正常，或联系技术支持工程师",
        ),
    ),
    29568: AlarmInfo(
        id=29568,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Encoder communication is abnormal",
            cause="",
            solution="Check whether the communication of encoder is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="编码器通信断线异常保护",
            cause="",
            solution="检查编码器通信线路是否正常，或联系技术支持工程师",
        ),
    ),
    29569: AlarmInfo(
        id=29569,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Encoder is abnormal",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="编码器异常故障",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    29570: AlarmInfo(
        id=29570,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Encoder battery is abnormal",
            cause="",
            solution="Please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="编码器电池异常保护",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    29571: AlarmInfo(
        id=29571,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Encoder internal error",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="主编码器内部错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    29572: AlarmInfo(
        id=29572,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Encoder CRC check error",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="主编码器CRC校验错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    29573: AlarmInfo(
        id=29573,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Auxiliary Encoder is disconnected",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="辅助编码器断线错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    29574: AlarmInfo(
        id=29574,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Auxiliary Encoder internal error",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="辅助编码器内部错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    29575: AlarmInfo(
        id=29575,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Auxiliary Encoder CRC check error",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="辅助编码器CRC校验错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    34321: AlarmInfo(
        id=34321,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Difference between the set positon and current position exceeds the range",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="位置偏差过大保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    34322: AlarmInfo(
        id=34322,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Postion is out of range",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="位置给定超限保护",
            cause="",
            solution="请输入正确参数",
        ),
    ),
    12832: AlarmInfo(
        id=12832,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Voltage between PN is too low",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="PN间电压不足保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12816: AlarmInfo(
        id=12816,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Voltage between PN is too high",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="PN间过电压保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    17168: AlarmInfo(
        id=17168,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Driver temperature is too high",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="驱动器过热保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    9040: AlarmInfo(
        id=9040,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Module in overload status",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="模块过载保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    13184: AlarmInfo(
        id=13184,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Driver output phase is wrong",
            cause="",
            solution="Wire as the correct phase sequence",
        ),
        zh_CN=LocalizedText(
            description="驱动器输出相序错误保护",
            cause="",
            solution="按正确相序接线",
        ),
    ),
    13185: AlarmInfo(
        id=13185,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Driver output phase is lost",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="驱动器输出缺相保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    12592: AlarmInfo(
        id=12592,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Driver input phase is lost",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="驱动器输入缺相保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    21569: AlarmInfo(
        id=21569,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Dirver connection is abnormal",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="驱动板连接异常保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    21008: AlarmInfo(
        id=21008,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Driver recognition is abnormal",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="驱动板辨识异常保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    21120: AlarmInfo(
        id=21120,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="FPGA configuration is wrong",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="FPGA配置错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    21121: AlarmInfo(
        id=21121,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="System error",
            cause="",
            solution="Please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="内部错误",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    21122: AlarmInfo(
        id=21122,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="STO safety wiring is fault",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="STO安全接线故障保护",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    28961: AlarmInfo(
        id=28961,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Motor is in Locked-Rotor status",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="电机堵转保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    29056: AlarmInfo(
        id=29056,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Motor is in overload status",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="电机过载保护",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    16912: AlarmInfo(
        id=16912,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Motor temperature is too high",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="电机温度过高",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    29057: AlarmInfo(
        id=29057,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Brake malfunction",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="抱闸故障",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    29058: AlarmInfo(
        id=29058,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="External brake resistor is in overload status",
            cause="",
            solution="Check the cable connection, and set an appropriate resistance value, reduce the load",
        ),
        zh_CN=LocalizedText(
            description="外接制动电阻过载保护",
            cause="",
            solution="检查线路连接，设合适阻值，减低负载",
        ),
    ),
    29059: AlarmInfo(
        id=29059,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to enable",
            cause="",
            solution="Check the cable connection, and enable again",
        ),
        zh_CN=LocalizedText(
            description="上使能失败",
            cause="",
            solution="检查线路连接，重新上使能",
        ),
    ),
    60944: AlarmInfo(
        id=60944,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Not in OP state, in boot state, the system will try to switch from station to Op.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP模式，在BOOT状态，系统将尝试切换从站到OP",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60945: AlarmInfo(
        id=60945,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Not in OP state, in Init state, the system will try to switch from station to Op.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP状态，在Init状态，系统将尝试切换从站到OP",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60946: AlarmInfo(
        id=60946,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Not in OP state, in PREOP state, the system will try to switch from station to Op.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP状态，在PREOP状态，系统将尝试切换从站到OP",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60948: AlarmInfo(
        id=60948,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Not in OP state, in SAFEOP state, the system will try to switch from station to Op.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP状态，在SAFEOP状态，系统将尝试切换从站到OP",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60949: AlarmInfo(
        id=60949,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Not in OP state, but may be offline.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP状态,可能在离线状态",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    29584: AlarmInfo(
        id=29584,
        level=AlarmLevel(1),
        en=LocalizedText(
            description="Large deviation of joint position",
            cause="",
            solution="1. Check production parameters; 2. Check encoder installation; 3. Check transmission structure",
        ),
        zh_CN=LocalizedText(
            description="关节位置偏差大",
            cause="",
            solution="1.检查生产参数 2.检查编码器安装 3.检查传动结构",
        ),
    ),
}
