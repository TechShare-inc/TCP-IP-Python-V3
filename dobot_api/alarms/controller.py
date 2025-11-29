"""ControllerAlarms alarm definitions."""

from __future__ import annotations

from dobot_api.alarms.models import AlarmInfo, AlarmLevel, LocalizedText


class ControllerAlarms:
    """Controller alarm database.

    Contains 572 alarm definitions.
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
ControllerAlarms._alarms = {
    0: AlarmInfo(
        id=0,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="No error",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="无错误",
            cause="",
            solution="",
        ),
    ),
    16: AlarmInfo(
        id=16,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is closed to the shoulder singularity point",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="规划位置接近肩奇异点",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    17: AlarmInfo(
        id=17,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics error with no solution",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="逆解算无解",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    18: AlarmInfo(
        id=18,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics error with result out of working area",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="逆解结果限位",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    19: AlarmInfo(
        id=19,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The starting point and the end point are the same when the JUMP command, ARC command or Circle command is running",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="JUMP或ARC或Circles指令点位重复",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    20: AlarmInfo(
        id=20,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The points of arc are wrong",
            cause="",
            solution="Enter the correct points",
        ),
        zh_CN=LocalizedText(
            description="圆弧点位错误",
            cause="",
            solution="请重新输入合适的点位",
        ),
    ),
    21: AlarmInfo(
        id=21,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters of JUMP command are wrong,The starting height or end height is negative or the zLimit value is lower than the starting point or the end point",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="抬升高度、下降高度为负或者zLimit低于起始点或结束点的高度",
            cause="",
            solution="输入正确参数",
        ),
    ),
    22: AlarmInfo(
        id=22,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Arm orientation error",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="手势切换错误",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    23: AlarmInfo(
        id=23,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is out of range of the workspace in MOVL mode",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="直线运动过程中规划点超出工作空间",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    24: AlarmInfo(
        id=24,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is out of range of the workspace in ARC mode",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="圆弧运动过程中规划点超出工作空间",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    25: AlarmInfo(
        id=25,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is out of range of the workspace in JUMP mode",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="JUMP过程中规划点超出工作空间",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    26: AlarmInfo(
        id=26,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is closed to the wrist singularity point",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="规划位置接近腕奇异点",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    27: AlarmInfo(
        id=27,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The planned point is closed to the elbow singularity point",
            cause="Reselect the movement points",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="规划位置接近肘奇异点",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    28: AlarmInfo(
        id=28,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The motion command is wrong",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="运动指令模式错误",
            cause="",
            solution="内部软件错误，重启或联系厂商",
        ),
    ),
    29: AlarmInfo(
        id=29,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Speed parameter is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="速度输入参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32: AlarmInfo(
        id=32,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics error with shoulder singularity when robot moving ",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程逆解算肩部奇异",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    33: AlarmInfo(
        id=33,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics error with no solution when robot moving",
            cause="",
            solution="Reselect movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程逆解算无解",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    34: AlarmInfo(
        id=34,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics error with result out of working area when robot moving",
            cause="",
            solution="Reselect movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程逆解算限位",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    35: AlarmInfo(
        id=35,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics with wrist singularity when robot moving",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程逆解算腕奇异",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    36: AlarmInfo(
        id=36,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Inverse kinematics with elbow singularity when robot moving",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程逆解算肘奇异",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    37: AlarmInfo(
        id=37,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The Joint angle is changed over 180 degree",
            cause="",
            solution="Reselect the movement points",
        ),
        zh_CN=LocalizedText(
            description="运动过程关节目标位置变化大于180度",
            cause="",
            solution="重新选取运动点位",
        ),
    ),
    41: AlarmInfo(
        id=41,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="First axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第一轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    42: AlarmInfo(
        id=42,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Second axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第二轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    43: AlarmInfo(
        id=43,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Third axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第三轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    44: AlarmInfo(
        id=44,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Fourth axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第四轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    45: AlarmInfo(
        id=45,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Fifth axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第五轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    46: AlarmInfo(
        id=46,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Sixth axis collision back ",
            cause="",
            solution="Contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="第六轴碰撞回退",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    48: AlarmInfo(
        id=48,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint1 is overspeed",
            cause="",
            solution="Reset the speed or reselect the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节1超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    49: AlarmInfo(
        id=49,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint2 overspeed",
            cause="",
            solution="Reset the speed or re-select the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节2超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    50: AlarmInfo(
        id=50,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint3 overspeed",
            cause="",
            solution="Reset the speed or re-select the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节3超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    51: AlarmInfo(
        id=51,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint4 overspeed",
            cause="",
            solution="Reset the speed or re-select the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节4超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    52: AlarmInfo(
        id=52,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint5 overspeed",
            cause="",
            solution="Reset the speed or re-select the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节5超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    53: AlarmInfo(
        id=53,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint6 overspeed",
            cause="",
            solution="Reset the speed or re-select the movement point away from the singularity",
        ),
        zh_CN=LocalizedText(
            description="关节6超速",
            cause="",
            solution="重新设置速度或重新选取运动点位远离奇异点",
        ),
    ),
    54: AlarmInfo(
        id=54,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint1 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节1位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    55: AlarmInfo(
        id=55,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint2 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节2位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    56: AlarmInfo(
        id=56,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint3 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节3位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    57: AlarmInfo(
        id=57,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint4 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节4位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    58: AlarmInfo(
        id=58,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint5 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节5位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    59: AlarmInfo(
        id=59,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Joint6 position lag error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节6位置超差",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    64: AlarmInfo(
        id=64,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint1",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节1正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    65: AlarmInfo(
        id=65,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint1",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节1负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    66: AlarmInfo(
        id=66,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint2",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节2正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    67: AlarmInfo(
        id=67,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint2",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节2负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    68: AlarmInfo(
        id=68,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint3",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节3正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    69: AlarmInfo(
        id=69,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint3",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节3负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    70: AlarmInfo(
        id=70,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint4",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节4正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    71: AlarmInfo(
        id=71,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint4",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节4负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    72: AlarmInfo(
        id=72,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint5",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节5正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    73: AlarmInfo(
        id=73,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint5",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节5负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    74: AlarmInfo(
        id=74,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Positive limit alarm of Joint6",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节6正向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    75: AlarmInfo(
        id=75,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Negative limit alarm of Joint6",
            cause="",
            solution="Jog the right joints towards the opposite direction",
        ),
        zh_CN=LocalizedText(
            description="关节6负向限位",
            cause="",
            solution="反向点动脱离限位",
        ),
    ),
    76: AlarmInfo(
        id=76,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Posture joint self-interference: type1",
            cause="",
            solution="Leave the wrong position and reselect the movement point",
        ),
        zh_CN=LocalizedText(
            description="姿态关节自干涉",
            cause="",
            solution="离开错误位置，重新选取运动点位",
        ),
    ),
    77: AlarmInfo(
        id=77,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Posture joint self-interference: type2",
            cause="",
            solution="Leave the wrong position and reselect the movement point",
        ),
        zh_CN=LocalizedText(
            description="姿态关节自干涉",
            cause="",
            solution="离开错误位置，重新选取运动点位",
        ),
    ),
    78: AlarmInfo(
        id=78,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Posture joint self-interference: type3",
            cause="",
            solution="Leave the wrong position and reselect the movement point",
        ),
        zh_CN=LocalizedText(
            description="姿态关节自干涉",
            cause="",
            solution="离开错误位置，重新选取运动点位",
        ),
    ),
    80: AlarmInfo(
        id=80,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint1 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节1丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    81: AlarmInfo(
        id=81,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint2 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节2丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    82: AlarmInfo(
        id=82,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint3 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节3丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    83: AlarmInfo(
        id=83,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint4 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节4丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    84: AlarmInfo(
        id=84,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint5 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节5丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    85: AlarmInfo(
        id=85,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint6 lose step",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节6丢步",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    96: AlarmInfo(
        id=96,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint1 status is wrong ",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节1轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    97: AlarmInfo(
        id=97,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint1 Drive State Disable",
            cause="",
            solution="Re-enable joint 1",
        ),
        zh_CN=LocalizedText(
            description="关节1轴状态下使能",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    99: AlarmInfo(
        id=99,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint2 status is wrong",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节2轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    100: AlarmInfo(
        id=100,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint2 is disabled ",
            cause="",
            solution="Enable all joints",
        ),
        zh_CN=LocalizedText(
            description="关节2轴状态下使能",
            cause="",
            solution="重新使能所有关节",
        ),
    ),
    102: AlarmInfo(
        id=102,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint3 status is wrong ",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节3轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    103: AlarmInfo(
        id=103,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint3 is disabled",
            cause="",
            solution="Enable all joints, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节3轴状态下未使能",
            cause="",
            solution="重新使能所有关节或联系技术支持工程师",
        ),
    ),
    105: AlarmInfo(
        id=105,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint4 status is wrong ",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节4轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    106: AlarmInfo(
        id=106,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint4 is disabled",
            cause="",
            solution="Enable all joints, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节4轴状态下未使能",
            cause="",
            solution="重新使能所有关节或联系技术支持工程师",
        ),
    ),
    108: AlarmInfo(
        id=108,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint5 status is wrong ",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节5轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    109: AlarmInfo(
        id=109,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint5 Drive State Disable",
            cause="",
            solution="Enable all joints, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节5轴状态下使能",
            cause="",
            solution="重新使能所有关节或联系技术支持工程师",
        ),
    ),
    111: AlarmInfo(
        id=111,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint6 status is wrong ",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="关节6轴状态错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    112: AlarmInfo(
        id=112,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Enable all joints, or contact technical support engineer",
            cause="",
            solution="Re-enable joint 6",
        ),
        zh_CN=LocalizedText(
            description="关节6轴状态下使能",
            cause="",
            solution="重新使能所有关节或联系技术支持工程师",
        ),
    ),
    114: AlarmInfo(
        id=114,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Homing error",
            cause="",
            solution="Please operate homing procedure  again",
        ),
        zh_CN=LocalizedText(
            description="机器人回零失败",
            cause="",
            solution="重新回零",
        ),
    ),
    115: AlarmInfo(
        id=115,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Fail to enable controller",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="机器人使能失败",
            cause="",
            solution="检查硬件是否正常，重新使能",
        ),
    ),
    116: AlarmInfo(
        id=116,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The emergency stop button is pressed",
            cause="",
            solution="release emergency stop button，Clear the alarm and power on again",
        ),
        zh_CN=LocalizedText(
            description="急停按钮按下",
            cause="",
            solution="松开急停按钮，清除告警，重新上电",
        ),
    ),
    117: AlarmInfo(
        id=117,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Collision detection",
            cause="",
            solution="Keep away from the obstruction,  clear the alarm and continue to run robot",
        ),
        zh_CN=LocalizedText(
            description="碰撞检测",
            cause="",
            solution="避开障碍物，清除警报并继续运行",
        ),
    ),
    118: AlarmInfo(
        id=118,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Security I/O is disconnected",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="安全IO掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系厂商",
        ),
    ),
    119: AlarmInfo(
        id=119,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Electronic skin collision detection",
            cause="",
            solution="Keep away from the obstruction,  clear the alarm and continue to run robot",
        ),
        zh_CN=LocalizedText(
            description="电子皮肤碰撞检测",
            cause="",
            solution="避开障碍物，清除警报，继续运行",
        ),
    ),
    120: AlarmInfo(
        id=120,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Six dimension force is not enabled",
            cause="",
            solution="Enable six dimensions",
        ),
        zh_CN=LocalizedText(
            description="六维力未使能",
            cause="",
            solution="使能六维力",
        ),
    ),
    121: AlarmInfo(
        id=121,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Fail to initialize the controller",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="初始化失败",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    122: AlarmInfo(
        id=122,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Contactor is open",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="接触器未闭合",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    123: AlarmInfo(
        id=123,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The feedback board did not feedback the power on signal",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板未反馈上电信号，上电失败",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    124: AlarmInfo(
        id=124,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="AC detection board status is wrong",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="AC检测板状态错误",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    125: AlarmInfo(
        id=125,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The feedback board data is not updated",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板数据未更新",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    126: AlarmInfo(
        id=126,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The switch on the controller board is pressed",
            cause="",
            solution="Power on again， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="控制柜面板开关被按下",
            cause="",
            solution="重新上电，或联系技术支持工程师",
        ),
    ),
    127: AlarmInfo(
        id=127,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="CAN NOT connect to modbus of the feedback board",
            cause="",
            solution="Power on again， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板modbus无法连接",
            cause="",
            solution="重新上电，或联系技术支持工程师",
        ),
    ),
    128: AlarmInfo(
        id=128,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Internal error - time overflow",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="内部错误-超时",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    130: AlarmInfo(
        id=130,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Universal IO board offline",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="通用IO板掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系厂商",
        ),
    ),
    131: AlarmInfo(
        id=131,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Terminal IO board offline",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="末端IO板掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系厂商",
        ),
    ),
    132: AlarmInfo(
        id=132,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal charging detection of 24V super capacitor",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="24V超级电容充电检测异常",
            cause="",
            solution="检查硬件是否正常，或联系厂商",
        ),
    ),
    133: AlarmInfo(
        id=133,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal charging detection of 48V super capacitor",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="48V超级电容充电检测异常",
            cause="",
            solution="检查硬件是否正常，或联系厂商",
        ),
    ),
    134: AlarmInfo(
        id=134,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Position deviation of  joint is too large when enabled",
            cause="",
            solution="Check that the load parameters and mounting Angle are correct",
        ),
        zh_CN=LocalizedText(
            description="上使能关节位置偏差过大",
            cause="",
            solution="检查负载参数和安装角度是否正确",
        ),
    ),
    144: AlarmInfo(
        id=144,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The selected points are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="选择点位不合适",
            cause="",
            solution="输入正确参数",
        ),
    ),
    146: AlarmInfo(
        id=146,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The target point is out range of workspace when inching robot",
            cause="",
            solution="Check whether the target point is in the workspace of the robot",
        ),
        zh_CN=LocalizedText(
            description="寸动参数错误",
            cause="",
            solution="确认目标点位是否限位",
        ),
    ),
    160: AlarmInfo(
        id=160,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The current motion instruction does not support pause",
            cause="",
            solution="The current motion instruction does not support pause",
        ),
        zh_CN=LocalizedText(
            description="当前运动指令不支持暂停",
            cause="",
            solution="当前运动指令不支持暂停",
        ),
    ),
    161: AlarmInfo(
        id=161,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control mode switching error",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="控制模式切换错误",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    162: AlarmInfo(
        id=162,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="MCU undervoltage",
            cause="",
            solution="Check if the voltage is normal, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="mcu欠压",
            cause="",
            solution="检查电压是否正常，或联系技术支持工程师",
        ),
    ),
    163: AlarmInfo(
        id=163,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="MCU overvoltage",
            cause="",
            solution="Check if the hardware is functioning properly, or contact a technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="mcu过压",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    164: AlarmInfo(
        id=164,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal energy feedback circuit",
            cause="",
            solution="Check if the hardware is functioning properly, or contact a technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能电路异常",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    165: AlarmInfo(
        id=165,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Soft or hard emergency stop triggered",
            cause="",
            solution="Release the emergency stop, power on again, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="软急停或者硬急停被触发",
            cause="",
            solution="松开急停，重新上电，或联系技术支持工程师",
        ),
    ),
    166: AlarmInfo(
        id=166,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal hard emergency stop line",
            cause="",
            solution="Check if the hardware is functioning properly, or contact a technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="硬急停线异常",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    167: AlarmInfo(
        id=167,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal short circuit of body power supply",
            cause="",
            solution="Check if the hardware is functioning properly, or contact a technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="本体供电短路异常",
            cause="",
            solution="检查硬件是否正常，或联系技术支持工程师",
        ),
    ),
    168: AlarmInfo(
        id=168,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Error in setting the minimum value of feedback voltage",
            cause="",
            solution="Reset or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能电压最小值设置错误",
            cause="",
            solution="重新设置，或联系技术支持工程师",
        ),
    ),
    169: AlarmInfo(
        id=169,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Error in setting the maximum value of the feedback voltage",
            cause="",
            solution="Reset or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能电压最大值设置错误",
            cause="",
            solution="重新设置，或联系技术支持工程师",
        ),
    ),
    170: AlarmInfo(
        id=170,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MCU temperature too high",
            cause="",
            solution="Please connect an external power supply resistor. If an external power supply resistor is already connected, please contact the after-sales FAE",
        ),
        zh_CN=LocalizedText(
            description="mcu温度过高",
            cause="",
            solution="请外接馈能电阻,如已外接馈能电阻,请联系售后FAE",
        ),
    ),
    171: AlarmInfo(
        id=171,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MCU universal IO failed to set PNP",
            cause="",
            solution="Please reset or contact after-sales FAE",
        ),
        zh_CN=LocalizedText(
            description="mcu通用io设置pnp失败",
            cause="",
            solution="请重新设置,或者联系售后FAE",
        ),
    ),
    172: AlarmInfo(
        id=172,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MCU universal io setting npn failed",
            cause="",
            solution="Please reset or contact after-sales FAE",
        ),
        zh_CN=LocalizedText(
            description="mcu通用io设置npn失败",
            cause="",
            solution="请重新设置,或者联系售后FAE",
        ),
    ),
    173: AlarmInfo(
        id=173,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Abnormal shutdown",
            cause="",
            solution="Please check if the RMT port is short circuited, or contact the after-sales FAE",
        ),
        zh_CN=LocalizedText(
            description="关机异常",
            cause="",
            solution="请检查rmt端口是否短接,或者联系售后FAE",
        ),
    ),
    174: AlarmInfo(
        id=174,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Abnormal energy feedback time detection",
            cause="",
            solution="Check if the input power supply and load are standardized, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能时间检测异常",
            cause="",
            solution="检查输入电源和负载是否规范，或联系技术支持工程师",
        ),
    ),
    176: AlarmInfo(
        id=176,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Force Control Command timeout",
            cause="",
            solution="Please contact fae",
        ),
        zh_CN=LocalizedText(
            description="力控指令超时",
            cause="",
            solution="请联系fae",
        ),
    ),
    177: AlarmInfo(
        id=177,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Error FC Pause",
            cause="",
            solution="Force control state does not support pause, restart after stopping",
        ),
        zh_CN=LocalizedText(
            description="力控暂停错误",
            cause="",
            solution="力控状态不支持暂停，停止后重新运行",
        ),
    ),
    178: AlarmInfo(
        id=178,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Force Control sensor data overrange",
            cause="",
            solution="check Force Control sensor",
        ),
        zh_CN=LocalizedText(
            description="力控传感器数据异常",
            cause="",
            solution="检查力控传感器",
        ),
    ),
    179: AlarmInfo(
        id=179,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Force Control sensor disabled",
            cause="",
            solution="enable Force Control sensor",
        ),
        zh_CN=LocalizedText(
            description="力控传感器未启用",
            cause="",
            solution="启用力控传感器",
        ),
    ),
    180: AlarmInfo(
        id=180,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Terminal DO1 output overcurrent alarm",
            cause="",
            solution="Check whether the hardware is normal and restart, or contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="末端DO1输出过流报警",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    181: AlarmInfo(
        id=181,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Terminal DO2 output overcurrent alarm",
            cause="",
            solution="Check whether the hardware is normal and restart, or contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="末端DO2输出过流报警",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    182: AlarmInfo(
        id=182,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Terminal 24V output overcurrent alarm",
            cause="",
            solution="Check whether the hardware is normal and restart, or contact technical support engineers",
        ),
        zh_CN=LocalizedText(
            description="末端24V输出过流报警",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    192: AlarmInfo(
        id=192,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="CAN NOT pause in tracking process",
            cause="",
            solution="Rerun the script",
        ),
        zh_CN=LocalizedText(
            description="不支持跟踪过程中暂停",
            cause="",
            solution="重新运行脚本",
        ),
    ),
    193: AlarmInfo(
        id=193,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="CAN NOT run joint interpolated motion commands in tracking  process",
            cause="",
            solution="Select the correct motion command",
        ),
        zh_CN=LocalizedText(
            description="不支持跟踪过程中使用使用关节类型的运动指令",
            cause="",
            solution="选择合适的运动指令",
        ),
    ),
    194: AlarmInfo(
        id=194,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Tracking limit",
            cause="",
            solution="Increase tracking range or speed up",
        ),
        zh_CN=LocalizedText(
            description="跟踪超限",
            cause="",
            solution="增加跟踪范围或者提速",
        ),
    ),
    208: AlarmInfo(
        id=208,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The fitting point is not enough",
            cause="",
            solution="The trajectory needs 4 points at least",
        ),
        zh_CN=LocalizedText(
            description="轨迹拟合点数太少",
            cause="",
            solution="轨迹拟合需要至少四个点",
        ),
    ),
    209: AlarmInfo(
        id=209,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Playback preprocessing is failed",
            cause="",
            solution="Record a new trajectory",
        ),
        zh_CN=LocalizedText(
            description="StartPath预处理失败",
            cause="",
            solution="录制新的轨迹或设置合适的参数。",
        ),
    ),
    210: AlarmInfo(
        id=210,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="直线摆焊参数错误",
            cause="",
            solution="请输入正确的参数",
        ),
    ),
    211: AlarmInfo(
        id=211,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="圆弧摆焊参数错误",
            cause="",
            solution="请输入正确的参数",
        ),
    ),
    212: AlarmInfo(
        id=212,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="ServoP或ServoJ规划失败",
            cause="",
            solution="请输入正确的参数",
        ),
    ),
    224: AlarmInfo(
        id=224,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="End TCP / elbow crossing safety wall alarm",
            cause="",
            solution="The inching robot returns to the safety wall.",
        ),
        zh_CN=LocalizedText(
            description="末端TCP/肘部越过安全墙报警",
            cause="",
            solution="点动机器人回到安全墙内。",
        ),
    ),
    225: AlarmInfo(
        id=225,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 1 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第一轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    226: AlarmInfo(
        id=226,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 2 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第二轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    227: AlarmInfo(
        id=227,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 3 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第三轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    228: AlarmInfo(
        id=228,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 4 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第四轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    229: AlarmInfo(
        id=229,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 5 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第五轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    230: AlarmInfo(
        id=230,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tracking difference of Joint 6 is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第六轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    231: AlarmInfo(
        id=231,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="圆弧半径超限",
            cause="",
            solution="请重新选择点位",
        ),
    ),
    232: AlarmInfo(
        id=232,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="摆焊速度超限",
            cause="",
            solution="请输入正确的速度参数",
        ),
    ),
    233: AlarmInfo(
        id=233,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="摆弧频率超限",
            cause="",
            solution="请输入正确的摆弧频率",
        ),
    ),
    240: AlarmInfo(
        id=240,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="机器人末端超过压力阈值",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    241: AlarmInfo(
        id=241,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="机器人末端下探距离超限",
            cause="",
            solution="请联系技术支持工程师",
        ),
    ),
    242: AlarmInfo(
        id=242,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the first axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第一轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    243: AlarmInfo(
        id=243,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the second axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第二轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    244: AlarmInfo(
        id=244,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the third axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第三轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    245: AlarmInfo(
        id=245,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the fourth axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第四轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    246: AlarmInfo(
        id=246,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the fifth axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第五轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    247: AlarmInfo(
        id=247,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The following error of the sixth axis is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第六轴跟随误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    248: AlarmInfo(
        id=248,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The first axis steady state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第一轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    249: AlarmInfo(
        id=249,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The second axis steady state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第二轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    250: AlarmInfo(
        id=250,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The third axis steady state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第三轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    251: AlarmInfo(
        id=251,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The fourth axis steady-state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第四轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    252: AlarmInfo(
        id=252,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The fifth axis steady-state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第五轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    253: AlarmInfo(
        id=253,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The sixth axis steady-state error is too large",
            cause="",
            solution="System error, restart controller or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="第六轴稳态误差过大",
            cause="",
            solution="系统错误，重新启动或联系技术支持工程师",
        ),
    ),
    254: AlarmInfo(
        id=254,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The current command does not support resuming operation after collision",
            cause="",
            solution="Please adjust the instructions to avoid obstacles",
        ),
        zh_CN=LocalizedText(
            description="当前指令不支持碰撞后恢复运行",
            cause="",
            solution="请调整指令，避开障碍物",
        ),
    ),
    1000: AlarmInfo(
        id=1000,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="disable exit drag failed",
            cause="",
            solution="Check whether the hardware is working properly, and restart the the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="下使能退出拖拽失败",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    1001: AlarmInfo(
        id=1001,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The first parameter of tcpread is incorrect",
            cause="",
            solution="Please check input",
        ),
        zh_CN=LocalizedText(
            description="tcpread第1个参数错误",
            cause="",
            solution="请检查输入",
        ),
    ),
    1002: AlarmInfo(
        id=1002,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The second parameter of tcpread is incorrect",
            cause="",
            solution="Please check input",
        ),
        zh_CN=LocalizedText(
            description="tcpread第2个参数错误",
            cause="",
            solution="请检查输入",
        ),
    ),
    1003: AlarmInfo(
        id=1003,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The third parameter of tcpread is incorrect",
            cause="",
            solution="Please check input",
        ),
        zh_CN=LocalizedText(
            description="tcpread第3个参数错误",
            cause="",
            solution="请检查输入",
        ),
    ),
    1004: AlarmInfo(
        id=1004,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to exit the drag",
            cause="",
            solution="contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="退出拖拽失败",
            cause="",
            solution="联系技术支持工程师",
        ),
    ),
    1005: AlarmInfo(
        id=1005,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to exit the drag",
            cause="",
            solution="contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="远程modbus配置异常",
            cause="",
            solution="modbus配置异常,使能coils:100,下使能coils:101",
        ),
    ),
    1006: AlarmInfo(
        id=1006,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="attempt to compare number with nil.",
            cause="",
            solution="Please check if there are null variables in the Lua code.",
        ),
        zh_CN=LocalizedText(
            description="尝试将数字与零进行比较.",
            cause="",
            solution="请检查lua代码是否有空值变量.",
        ),
    ),
    1007: AlarmInfo(
        id=1007,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Power-on failure, internal controller error.",
            cause="",
            solution="Please reboot the device or contact FAE.",
        ),
        zh_CN=LocalizedText(
            description="上电失败，控制器内部异常.",
            cause="",
            solution="请重启设备，或联系FAE.",
        ),
    ),
    1008: AlarmInfo(
        id=1008,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Power-on failure, emergency stop triggered during power-up.",
            cause="",
            solution="Please check if the software and hardware emergency stop buttons have been pressed, and after inspection, power on again.",
        ),
        zh_CN=LocalizedText(
            description="上电失败，上电过程中触发急停.",
            cause="",
            solution="请检查软硬件急停是否被拍下，检查完毕后重新上电.",
        ),
    ),
    1009: AlarmInfo(
        id=1009,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Power-on failure, communication exception occurred during the power-on process.",
            cause="",
            solution="Please check if the hardware is functioning properly, or contact FAE for assistance.",
        ),
        zh_CN=LocalizedText(
            description="上电失败，上电过程中发生通讯异常.",
            cause="",
            solution="请检查硬件是否正常，或者联系FAE.",
        ),
    ),
    1772: AlarmInfo(
        id=1772,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Contactor is open",
            cause="",
            solution="Check whether the hardware is working properly, and restart the the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="接触器未闭合",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    1773: AlarmInfo(
        id=1773,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The feedback board fails to supply the power-on signal.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板未反馈上电信号，上电失败",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    1775: AlarmInfo(
        id=1775,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The AC detection board status is error",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="AC检测板状态错误",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    1776: AlarmInfo(
        id=1776,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Data of the feedback board is not updated",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板数据未更新",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    4096: AlarmInfo(
        id=4096,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Failed to open the mechanical parameters file",
            cause="",
            solution="Check the file path and restart the controller",
        ),
        zh_CN=LocalizedText(
            description="打开机械参数文件失败",
            cause="",
            solution="检查文件位置是否正确并重新启动",
        ),
    ),
    4118: AlarmInfo(
        id=4118,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Security I/O is disconnected",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="mcu掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系厂商",
        ),
    ),
    8192: AlarmInfo(
        id=8192,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Failed to open the project file",
            cause="",
            solution="Check the file path and restart the controller",
        ),
        zh_CN=LocalizedText(
            description="打开工程文件失败",
            cause="",
            solution="检查文件位置是否正确并重新启动",
        ),
    ),
    8193: AlarmInfo(
        id=8193,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Failed to open the program file",
            cause="",
            solution="Check the file path and restart the controller",
        ),
        zh_CN=LocalizedText(
            description="打开程序文件失败",
            cause="",
            solution="检查文件位置是否正确并重新启动",
        ),
    ),
    8194: AlarmInfo(
        id=8194,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Failed to open the global variable file",
            cause="",
            solution="Check the file path and restart the controller",
        ),
        zh_CN=LocalizedText(
            description="打开全局参数文件失败",
            cause="",
            solution="检查文件位置是否正确并重新启动",
        ),
    ),
    8195: AlarmInfo(
        id=8195,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Failed to open the teaching  point file",
            cause="",
            solution="Check the file path and restart the controller",
        ),
        zh_CN=LocalizedText(
            description="打开示教点文件失败",
            cause="",
            solution="检查文件位置是否正确并重新启动",
        ),
    ),
    8196: AlarmInfo(
        id=8196,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to run debugger",
            cause="",
            solution="Rerun debugger",
        ),
        zh_CN=LocalizedText(
            description="启动调试进程失败",
            cause="",
            solution="重新运行调试进程",
        ),
    ),
    8197: AlarmInfo(
        id=8197,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to parse project file",
            cause="",
            solution="Rerun debugger",
        ),
        zh_CN=LocalizedText(
            description="解析工程文件失败",
            cause="",
            solution="重新运行调试进程",
        ),
    ),
    8198: AlarmInfo(
        id=8198,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Project file content is empty",
            cause="",
            solution="Rerun debugger",
        ),
        zh_CN=LocalizedText(
            description="工程文件内容为空",
            cause="",
            solution="重新运行调试进程",
        ),
    ),
    8199: AlarmInfo(
        id=8199,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The project file does not exist",
            cause="",
            solution="Rerun debugger",
        ),
        zh_CN=LocalizedText(
            description="工程文件不存在",
            cause="",
            solution="重新运行调试进程",
        ),
    ),
    8200: AlarmInfo(
        id=8200,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to parse CPUs",
            cause="",
            solution="Rerun debugger",
        ),
        zh_CN=LocalizedText(
            description="解析CPUS失败",
            cause="",
            solution="重新运行调试进程",
        ),
    ),
    8201: AlarmInfo(
        id=8201,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Internal communication error",
            cause="",
            solution="Rerun the script",
        ),
        zh_CN=LocalizedText(
            description="内部通讯错误",
            cause="",
            solution="重新运行脚本",
        ),
    ),
    8448: AlarmInfo(
        id=8448,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Failed to get robot type",
            cause="",
            solution="Confirm robot type file",
        ),
        zh_CN=LocalizedText(
            description="获取机器人类型失败",
            cause="",
            solution="确认机器类型文件",
        ),
    ),
    12288: AlarmInfo(
        id=12288,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Press the emergency stop button",
            cause="",
            solution="Clear the alarm and power on again",
        ),
        zh_CN=LocalizedText(
            description="紧急停止按键按下",
            cause="",
            solution="清除告警并重新上电",
        ),
    ),
    12289: AlarmInfo(
        id=12289,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Detecte external emergency-stopped status",
            cause="",
            solution="Clear the alarm and power on again ",
        ),
        zh_CN=LocalizedText(
            description="检测到外部急停状态",
            cause="",
            solution="清除告警并重新上电",
        ),
    ),
    12290: AlarmInfo(
        id=12290,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis1 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴1不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12291: AlarmInfo(
        id=12291,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis2 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴2不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12292: AlarmInfo(
        id=12292,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis3 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴3不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12293: AlarmInfo(
        id=12293,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis4 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴4不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12294: AlarmInfo(
        id=12294,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis5 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴5不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12295: AlarmInfo(
        id=12295,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Axis6 not in Bus Mode",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="轴6不在总线模式",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12296: AlarmInfo(
        id=12296,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The robot is powered off",
            cause="",
            solution="Clear the alarm and power on again， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="本体下电",
            cause="",
            solution="清除告警，并重新上电，或联系技术支持工程师",
        ),
    ),
    12297: AlarmInfo(
        id=12297,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="CPU温度高于告警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12298: AlarmInfo(
        id=12298,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服一MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12299: AlarmInfo(
        id=12299,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服二MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12300: AlarmInfo(
        id=12300,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服三MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12301: AlarmInfo(
        id=12301,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服四MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12302: AlarmInfo(
        id=12302,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服五MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    12303: AlarmInfo(
        id=12303,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The CPU temperature is higher than the alarm threshold of 65 degrees",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="伺服六MCU温度超过报警阈值",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    16384: AlarmInfo(
        id=16384,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Detecte obstacles in the operateion area",
            cause="",
            solution="Clear obstacles and continue to operate the robot",
        ),
        zh_CN=LocalizedText(
            description="检测到该区域有障碍物",
            cause="",
            solution="清理障碍物，继续运行",
        ),
    ),
    16386: AlarmInfo(
        id=16386,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The inverse kinematics solution is failed，the planned target points are wrong",
            cause="",
            solution="Clear the alarm and re-teach point ",
        ),
        zh_CN=LocalizedText(
            description="逆解算失败，点位错误",
            cause="",
            solution="清除告警，并重新示教点位",
        ),
    ),
    20480: AlarmInfo(
        id=20480,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Modbus of feedback board  is disconnected ",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板Modbus掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20481: AlarmInfo(
        id=20481,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Before power supply, the voltage is higher than 49.5V",
            cause="",
            solution="The voltage is too high，please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="供电前，电压高于49.5V",
            cause="",
            solution="本体供电电压过高,请联系技术支持工程师",
        ),
    ),
    20482: AlarmInfo(
        id=20482,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Before power supply, the voltage is lower than 42V",
            cause="",
            solution="The voltage is too low，please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="供电前，电压低于42V",
            cause="",
            solution="本体供电电压过低,请联系技术支持工程师",
        ),
    ),
    20483: AlarmInfo(
        id=20483,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The hardware circuit related to the current-limiting chip is abnormal",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="限流芯片相关硬件电路异常",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20484: AlarmInfo(
        id=20484,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="After power supply, the voltage is higher than 56V",
            cause="",
            solution="The voltage is too high，please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="供电后，电压高于56V",
            cause="",
            solution="本体供电电压过高,请联系技术支持工程师",
        ),
    ),
    20485: AlarmInfo(
        id=20485,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="After power supply, the voltage is lower than 24V",
            cause="",
            solution="The voltage is too low，please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="供电后，电压低于24V",
            cause="",
            solution="本体供电电压过低,请联系技术支持工程师",
        ),
    ),
    20486: AlarmInfo(
        id=20486,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Internal first stabilized voltage is abnormal",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="内部第一路稳压值异常",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    20487: AlarmInfo(
        id=20487,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Internal second stabilized voltage is abnormal",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="内部第二路稳压值异常",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    20488: AlarmInfo(
        id=20488,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Output voltage alarms before the robot slow-start powering",
            cause="",
            solution="System error, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="本体上电缓启动前输出电压异常报警",
            cause="",
            solution="系统错误，请联系技术支持工程师",
        ),
    ),
    20489: AlarmInfo(
        id=20489,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The feedback current is higher than 17A",
            cause="",
            solution="The feedback current is too high, please contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="检测馈电电流大于17A",
            cause="",
            solution="馈电电流过大，请联系技术支持工程师",
        ),
    ),
    20490: AlarmInfo(
        id=20490,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Overpower protection of cement resistance",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="水泥电阻的功率保护",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20491: AlarmInfo(
        id=20491,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="DC bus current is higher  than 26A",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="母线电流大于26A",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20492: AlarmInfo(
        id=20492,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="the Feedback board alarms when the robot is slow-starting",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="本体上电缓启动时发生馈能报警",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20493: AlarmInfo(
        id=20493,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The fan circuit of the feedback board is short-circuited",
            cause="",
            solution="Check whether the hardware is working properly,  and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板电扇电路短路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    20494: AlarmInfo(
        id=20494,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="the robot slow-start failed",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="本体上电缓启动失败报警",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24576: AlarmInfo(
        id=24576,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Modbus of I/O board is  disconnected ",
            cause="",
            solution="Check whether the hardware is working properly, and restart the collaborative robot， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="安全IO板Modbus掉线",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24578: AlarmInfo(
        id=24578,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The contactor did not close as required",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="接触器连续1s没有按要求闭合",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24579: AlarmInfo(
        id=24579,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The feedback board does not return an electrified signal during 2s",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="控制上电的状态下，馈能板2s没有返回上电信号",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24581: AlarmInfo(
        id=24581,
        level=AlarmLevel(0),
        en=LocalizedText(
            description=" AC status is abnormal",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="AC状态检测错误",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24582: AlarmInfo(
        id=24582,
        level=AlarmLevel(0),
        en=LocalizedText(
            description=" After 5 minutes of powering on, the feeback board data did not update for 1 min",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="上电5分钟后，馈能板数据数据持续1分钟没更新",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24583: AlarmInfo(
        id=24583,
        level=AlarmLevel(0),
        en=LocalizedText(
            description=" The switch on the controller is pressed",
            cause="",
            solution="Clear the alarm and power on again",
        ),
        zh_CN=LocalizedText(
            description="面板开关被按下",
            cause="",
            solution="清除告警，并重新上电",
        ),
    ),
    24584: AlarmInfo(
        id=24584,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="The communication of feedback board modbus is interrupted",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="馈能板Modbus通信中断",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    24588: AlarmInfo(
        id=24588,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal charging detection of 24V super capacitor(modbus)",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="24V超级电容充电检测异常（modbus）",
            cause="",
            solution="检查硬件是否正常，或联系厂商",
        ),
    ),
    24589: AlarmInfo(
        id=24589,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Abnormal charging detection of 48V super capacitor(modbus)",
            cause="",
            solution="Check whether the hardware is working properly, or contact technical support engineer",
        ),
        zh_CN=LocalizedText(
            description="48V超级电容充电检测异常（modbus）",
            cause="",
            solution="检查硬件是否正常，或联系厂商",
        ),
    ),
    32768: AlarmInfo(
        id=32768,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SpeedFactor command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedFactor指令无输入参数",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32769: AlarmInfo(
        id=32769,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters of SpeedFactor command are  out of range",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedFactor指令参数超出范围",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32770: AlarmInfo(
        id=32770,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters of DO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="DO 参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32771: AlarmInfo(
        id=32771,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters of DI command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="DI 参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32772: AlarmInfo(
        id=32772,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DIGroup params number err",
            cause="",
            solution="params is too much",
        ),
        zh_CN=LocalizedText(
            description="DIGroup 参数数量错误",
            cause="",
            solution="点位过多，最好不要一次输入超过100个点",
        ),
    ),
    32773: AlarmInfo(
        id=32773,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DIGroup have some params's index out of range",
            cause="",
            solution="input correct params",
        ),
        zh_CN=LocalizedText(
            description="DIGroup 参数中存在的点位索引 超出边界",
            cause="",
            solution="请核对点位范围",
        ),
    ),
    32774: AlarmInfo(
        id=32774,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DIGroup have some params's index type error",
            cause="",
            solution="input correct params",
        ),
        zh_CN=LocalizedText(
            description="DIGroup 参数中存在的点位索引的类型错误",
            cause="",
            solution="只能输入数字",
        ),
    ),
    32775: AlarmInfo(
        id=32775,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DIGroup err internal ",
            cause="",
            solution="internal error has happend,try again.",
        ),
        zh_CN=LocalizedText(
            description="DIGroup 发生内部错误",
            cause="",
            solution="再次尝试，如果一直存在错误，请联系技术支持",
        ),
    ),
    32776: AlarmInfo(
        id=32776,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup params number err",
            cause="",
            solution="params is too much",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 参数数量错误",
            cause="",
            solution="点位过多，最好不要一次输入超过100个点",
        ),
    ),
    32777: AlarmInfo(
        id=32777,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup have some params's index out of range",
            cause="",
            solution="input correct params",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 参数中存在的点位索引 超出边界",
            cause="",
            solution="请核对点位范围",
        ),
    ),
    32778: AlarmInfo(
        id=32778,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup have some params's index type error",
            cause="",
            solution="input correct params",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 参数中存在的点位索引的类型错误",
            cause="",
            solution="只能输入数字",
        ),
    ),
    32779: AlarmInfo(
        id=32779,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup have some params's value type error",
            cause="",
            solution="input correct params,number type and boolean is needed eg.(0/1) || (true/false) || (ON/OFF)",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 参数中存在的点位输出值的类型错误",
            cause="",
            solution="请输入数字(0/1)或bool(true/false)或内置的 ON/OFF",
        ),
    ),
    32780: AlarmInfo(
        id=32780,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup have some params's isqueue type error",
            cause="",
            solution="eg.(0/1) || (true/false) || (ON/OFF) . true means queue command(default),false:Immediate command",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 参数中存在的可选参数 指令类型的类型错误",
            cause="",
            solution="请输入数字(0/1)或bool(true/false)或内置的 ON/OFF 真 : 队列指令(默认) 假: 立即指令",
        ),
    ),
    32781: AlarmInfo(
        id=32781,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DOGroup err internal ",
            cause="",
            solution="internal error has happend,try again.",
        ),
        zh_CN=LocalizedText(
            description="DOGroup 发生内部错误",
            cause="",
            solution="再次尝试，如果一直存在错误，请联系技术支持",
        ),
    ),
    32785: AlarmInfo(
        id=32785,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters of AI command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AI 参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32801: AlarmInfo(
        id=32801,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameters number of AO command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AO 参数个数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    32802: AlarmInfo(
        id=32802,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Index parameter of AO command is wrong",
            cause="",
            solution="Enter the correct parameters, the index parameter can only be set to 1 or 2",
        ),
        zh_CN=LocalizedText(
            description="AO指令索引参数错误",
            cause="",
            solution="输入正确参数，参数只能为1 或者2 ",
        ),
    ),
    32803: AlarmInfo(
        id=32803,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Voltage parameter of AO command is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 0.0 to 10.0",
        ),
        zh_CN=LocalizedText(
            description="AO电压值参数错误，超过边界",
            cause="",
            solution="输入正确参数,取值范围[0，10.0]",
        ),
    ),
    32804: AlarmInfo(
        id=32804,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="index parameter of AO command is out of range",
            cause="",
            solution="Enter the correct parameters, value is 0 or 1",
        ),
        zh_CN=LocalizedText(
            description="AO索引值错误",
            cause="",
            solution="输入正确参数,取值范围是 0  或 1 ",
        ),
    ),
    32849: AlarmInfo(
        id=32849,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="AO mode err",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AO 模式错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    33024: AlarmInfo(
        id=33024,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="CP command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="CP指令无输入参数",
            cause="",
            solution="输入正确参数",
        ),
    ),
    33025: AlarmInfo(
        id=33025,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of CP command is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 0 to 100",
        ),
        zh_CN=LocalizedText(
            description="CP指令参数超出范围",
            cause="",
            solution="输入正确参数,取值范围[0，100]",
        ),
    ),
    33280: AlarmInfo(
        id=33280,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Arch command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch指令无输入参数",
            cause="",
            solution="请输入正确参数",
        ),
    ),
    33281: AlarmInfo(
        id=33281,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Index parameter of Arch command is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 0 to 9",
        ),
        zh_CN=LocalizedText(
            description="Arch指令索引超出范围",
            cause="",
            solution="输入正确参数，取值范围[0，9]",
        ),
    ),
    33282: AlarmInfo(
        id=33282,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameters coorespongding to index parameter of Arch command are not configured",
            cause="",
            solution="Please set index parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch指令索引对应参数尚未设置",
            cause="",
            solution="请设置索引参数",
        ),
    ),
    33536: AlarmInfo(
        id=33536,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="LimZ command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="LimZ指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    33537: AlarmInfo(
        id=33537,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of LimZ instruction out of range",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="LimZ指令参数超出范围",
            cause="",
            solution="输入正确参数",
        ),
    ),
    33792: AlarmInfo(
        id=33792,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Speed command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Speed指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    33793: AlarmInfo(
        id=33793,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of Speed command is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="Speed指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    34048: AlarmInfo(
        id=34048,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Accel command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Accel指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    34049: AlarmInfo(
        id=34049,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of Accel command is out of range ",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="Accel指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    34304: AlarmInfo(
        id=34304,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jerk command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jerk指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    34305: AlarmInfo(
        id=34305,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of Jerk command is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="Jerk指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    34560: AlarmInfo(
        id=34560,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SpeedS command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedS指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    34561: AlarmInfo(
        id=34561,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of SpeedS command is out of range ",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="SpeedS指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    34816: AlarmInfo(
        id=34816,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SpeedR command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedR指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    34817: AlarmInfo(
        id=34817,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of SpeedR commandis is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="SpeedR指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    35072: AlarmInfo(
        id=35072,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="AccelS command has no input parameters",
            cause="",
            solution="Enter the correct parameters, value ranges from 1 to 100",
        ),
        zh_CN=LocalizedText(
            description="AccelS指令无输入参数",
            cause="",
            solution="请输入正确参数，取值范围[1, 100]",
        ),
    ),
    35073: AlarmInfo(
        id=35073,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of AccelS command is out of range",
            cause="",
            solution="Enter the correct parameters, volue ranges from 0 to 100",
        ),
        zh_CN=LocalizedText(
            description="AccelS指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    35328: AlarmInfo(
        id=35328,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="AccelR command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AccelR指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    35329: AlarmInfo(
        id=35329,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of AccelR command is out of range",
            cause="",
            solution="Enter the correct parameters, volue ranges from 0 to 100",
        ),
        zh_CN=LocalizedText(
            description="AccelR指令比例参数超出范围[1, 100]",
            cause="",
            solution="输入正确参数",
        ),
    ),
    35584: AlarmInfo(
        id=35584,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="JerkS command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="JerkS指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    35585: AlarmInfo(
        id=35585,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of JerkS instruction is out of range",
            cause="",
            solution="Enter the correct parameters, value ranges from 0 to 100",
        ),
        zh_CN=LocalizedText(
            description="JerkS指令比例参数超出范围[1, 100]",
            cause="",
            solution="输入正确参数",
        ),
    ),
    35840: AlarmInfo(
        id=35840,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="JerkR command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="JerkR指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    35841: AlarmInfo(
        id=35841,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter of JerkR command is out of range",
            cause="",
            solution="Enter the correct parameters,value ranges from 0 to 100",
        ),
        zh_CN=LocalizedText(
            description="JerkR指令比例参数超出范围",
            cause="",
            solution="输入正确参数，取值范围[1, 100]",
        ),
    ),
    36096: AlarmInfo(
        id=36096,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Go command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Go指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36097: AlarmInfo(
        id=36097,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Go command has no point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Go指令缺少坐标点参数",
            cause="",
            solution="请输入正确参数",
        ),
    ),
    36098: AlarmInfo(
        id=36098,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of Go command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Go指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36099: AlarmInfo(
        id=36099,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control parameter of Go command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Go指令控制参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36100: AlarmInfo(
        id=36100,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJ command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJ指令无输入参数",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36101: AlarmInfo(
        id=36101,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJ command has no point parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJ指令缺少坐标点参数",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36102: AlarmInfo(
        id=36102,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJ command has no point parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJ指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36103: AlarmInfo(
        id=36103,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of RP command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="RP指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36104: AlarmInfo(
        id=36104,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Offset parameters of RP command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="RP指令偏移量参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36105: AlarmInfo(
        id=36105,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of RJ command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="RJ指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36106: AlarmInfo(
        id=36106,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Offset parameters of RJ command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="RJ指令偏移值点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36107: AlarmInfo(
        id=36107,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GoR command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoR指令无输入参数",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36108: AlarmInfo(
        id=36108,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of GoR command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoR指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36109: AlarmInfo(
        id=36109,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJR instruction has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJR指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36110: AlarmInfo(
        id=36110,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of MoveJR command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJR指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36111: AlarmInfo(
        id=36111,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GoIO command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoIO指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36112: AlarmInfo(
        id=36112,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of GoIO command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoIO指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36113: AlarmInfo(
        id=36113,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="I/O parameters of GoIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoIO指令I/O参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36114: AlarmInfo(
        id=36114,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveIO command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveIO指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36115: AlarmInfo(
        id=36115,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of MoveIO command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveIO指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36116: AlarmInfo(
        id=36116,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="I/O parameters of MoveIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveIO指令I/O参数错误",
            cause="",
            solution="请输入正确参数",
        ),
    ),
    36117: AlarmInfo(
        id=36117,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJIO command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJIO指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36118: AlarmInfo(
        id=36118,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of MoveJIO command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJIO指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36119: AlarmInfo(
        id=36119,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="I/O parameters of MoveJIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJIO指令I/O参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36120: AlarmInfo(
        id=36120,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveJ command has no point parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJ指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36121: AlarmInfo(
        id=36121,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveR command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveR指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36122: AlarmInfo(
        id=36122,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of MoveR command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveR指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    36352: AlarmInfo(
        id=36352,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Move command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Move指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36353: AlarmInfo(
        id=36353,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Move command has no point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Move指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36354: AlarmInfo(
        id=36354,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of Move command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Move指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36355: AlarmInfo(
        id=36355,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control parameter of Move command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Move指令控制参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36608: AlarmInfo(
        id=36608,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Arch3 command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch3指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36609: AlarmInfo(
        id=36609,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Arch3 command has no point parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch3指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36610: AlarmInfo(
        id=36610,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of Arch3 command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch3指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36611: AlarmInfo(
        id=36611,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control parameter of Arch3 command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch3指令控制参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36612: AlarmInfo(
        id=36612,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetRunningData command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetRunningData指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36613: AlarmInfo(
        id=36613,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wait input parameter type is an integer",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Wait指令输入参数类型为整型",
            cause="",
            solution="请输入参数",
        ),
    ),
    36614: AlarmInfo(
        id=36614,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Sleep input parameter type is an integer",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Sleep指令输入参数类型为整型",
            cause="",
            solution="请输入参数",
        ),
    ),
    36864: AlarmInfo(
        id=36864,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jump command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jump指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36865: AlarmInfo(
        id=36865,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jump command has no point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jump指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    36866: AlarmInfo(
        id=36866,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameter of Jump command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jump指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    36867: AlarmInfo(
        id=36867,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control parameter of Jump command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jump指令控制参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    40960: AlarmInfo(
        id=40960,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Circle3 command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Circle3指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    40961: AlarmInfo(
        id=40961,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Circle3 command has no point parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Circle3指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    40962: AlarmInfo(
        id=40962,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Point parameters of Circle3 command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Circle3指令坐标点参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    40963: AlarmInfo(
        id=40963,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Control parameter of Circle3 command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Circle3指令控制参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    41216: AlarmInfo(
        id=41216,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The Spiral command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    41217: AlarmInfo(
        id=41217,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The Spiral command lacks a coordinate point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    41218: AlarmInfo(
        id=41218,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Spiral command coordinate point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41220: AlarmInfo(
        id=41220,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Spiral command control parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令控制参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41221: AlarmInfo(
        id=41221,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Spiral command threshold parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令阈值参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41222: AlarmInfo(
        id=41222,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Spiral command radius parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Spiral指令半径参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41472: AlarmInfo(
        id=41472,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The Rotation command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    41473: AlarmInfo(
        id=41473,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The Rotation command lacks a coordinate point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令缺少坐标点参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    41474: AlarmInfo(
        id=41474,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Rotation command coordinate point parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令坐标点参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41475: AlarmInfo(
        id=41475,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Rotation command control parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令控制参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41476: AlarmInfo(
        id=41476,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Rotation command speed parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令速度参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41477: AlarmInfo(
        id=41477,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong Rotation command max Torque parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Rotation指令最大力矩参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41728: AlarmInfo(
        id=41728,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command Liner has no parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="liner 指令无输入参数",
            cause="",
            solution="请输入参数",
        ),
    ),
    41732: AlarmInfo(
        id=41732,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command Liner optional parameters err",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="liner 指令可选参数错误",
            cause="",
            solution="请输入参数",
        ),
    ),
    41984: AlarmInfo(
        id=41984,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jack direction parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="插孔方向参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    41985: AlarmInfo(
        id=41985,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jack speed parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="插孔速度参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    41986: AlarmInfo(
        id=41986,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jack force parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="插孔力参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    41987: AlarmInfo(
        id=41987,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jack max speed parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="插孔最大速度参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    41988: AlarmInfo(
        id=41988,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Jack mode parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="插孔模式参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42240: AlarmInfo(
        id=42240,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="6 d force return to zero parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="六维力回零参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42241: AlarmInfo(
        id=42241,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Six dimensions are not turned on",
            cause="",
            solution="Turn on six dimensions",
        ),
        zh_CN=LocalizedText(
            description="六维力没有开启",
            cause="",
            solution="开启六维力",
        ),
    ),
    42242: AlarmInfo(
        id=42242,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Six dimensions parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="六维力参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42243: AlarmInfo(
        id=42243,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Six force sensor has no data over 1 second",
            cause="",
            solution="check the connect of the sensor",
        ),
        zh_CN=LocalizedText(
            description="六维力数据异常，超过1s没有获得数据",
            cause="",
            solution="检查硬件连接",
        ),
    ),
    42496: AlarmInfo(
        id=42496,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCAct start parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="力控启动参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42497: AlarmInfo(
        id=42497,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCAct has no input parameter",
            cause="",
            solution="input parameter",
        ),
        zh_CN=LocalizedText(
            description="FCAct指令无输入参数",
            cause="",
            solution="输入参数",
        ),
    ),
    42498: AlarmInfo(
        id=42498,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCAct parameter out of range 0/1",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCAct指令参数超出范围0/1",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42499: AlarmInfo(
        id=42499,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCDeact parameters error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCDeact 关闭力控参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42500: AlarmInfo(
        id=42500,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCSetComplianceNormal has no input parameter",
            cause="",
            solution="input parameter",
        ),
        zh_CN=LocalizedText(
            description="FCSetComplianceNormal 指令无输入参数",
            cause="",
            solution="输入参数",
        ),
    ),
    42501: AlarmInfo(
        id=42501,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCSetCompliance parameters error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCSetCompliance参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42502: AlarmInfo(
        id=42502,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCSetComplianceNormal has no input parameter",
            cause="",
            solution="input parameter",
        ),
        zh_CN=LocalizedText(
            description="FCSetComplianceNormal无输入参数",
            cause="",
            solution="输入参数",
        ),
    ),
    42503: AlarmInfo(
        id=42503,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCSetCompliance parameters error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCSetCompliance 指令参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42504: AlarmInfo(
        id=42504,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCLoad ID error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="负载辨识 ID 错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42505: AlarmInfo(
        id=42505,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCCalib has no input parameter",
            cause="",
            solution="input parameter",
        ),
        zh_CN=LocalizedText(
            description="FCCalib 无输入参数",
            cause="",
            solution="输入参数",
        ),
    ),
    42506: AlarmInfo(
        id=42506,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCCalib parameters error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCalib参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42507: AlarmInfo(
        id=42507,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCCalib optional parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCalib可选参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    42508: AlarmInfo(
        id=42508,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter IsInside error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 IsInside 选项错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42509: AlarmInfo(
        id=42509,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter timeout error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 timeout 选项错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42510: AlarmInfo(
        id=42510,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter IsAlarm error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 IsAlarm 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42511: AlarmInfo(
        id=42511,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckNotExistFCCondForceParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond参数中 force 不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42512: AlarmInfo(
        id=42512,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Force param in FCCond error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 中 Force 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42513: AlarmInfo(
        id=42513,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCCond Optional parameter Force error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 可选参数中 Force 项错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42514: AlarmInfo(
        id=42514,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckNotExistFCCondTCPSpeedParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond TCP 速度参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42515: AlarmInfo(
        id=42515,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckFCCondTCPSpeedErrorParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond TCP速度参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42516: AlarmInfo(
        id=42516,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Speed error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 可选参数中 Speed 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42517: AlarmInfo(
        id=42517,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Torque not exist.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 力矩参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42518: AlarmInfo(
        id=42518,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckFCCondTorqueErrorParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 力矩(Torque)参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42519: AlarmInfo(
        id=42519,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Torque error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond 可选参数 Torque 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42520: AlarmInfo(
        id=42520,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckNotExistFCCondDisplacParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond Displac 不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42521: AlarmInfo(
        id=42521,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="DataAlarmCheckFCCondDisplacErrorParam",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond Displac 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42522: AlarmInfo(
        id=42522,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Displac error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCCond Displac 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42523: AlarmInfo(
        id=42523,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter SpeedF error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef SpeedF 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42524: AlarmInfo(
        id=42524,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter TimeOut error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef可选参数中 TimeOut 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42525: AlarmInfo(
        id=42525,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef’s Optional parameter Direction error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef可选参数中 Direction 选项错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42526: AlarmInfo(
        id=42526,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef's Optional parameter Distance error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef Distance 选项错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42527: AlarmInfo(
        id=42527,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef Optional parameter SpeedL error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef 的可选参数 SpeedL 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42544: AlarmInfo(
        id=42544,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefForce parameter not exist",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefForce 参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42545: AlarmInfo(
        id=42545,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefForce's Optional parameter error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefForce 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42546: AlarmInfo(
        id=42546,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefForce parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefForce 参数错误 ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42547: AlarmInfo(
        id=42547,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefTorque parameter not exist",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefTorque 参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42548: AlarmInfo(
        id=42548,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefTorque's optional parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefTorque 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42549: AlarmInfo(
        id=42549,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefTorque parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefTorque 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42550: AlarmInfo(
        id=42550,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefline has no input params",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefline 无输入参数 ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42551: AlarmInfo(
        id=42551,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefline's optional parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefline 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42552: AlarmInfo(
        id=42552,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefline's parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefline 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42553: AlarmInfo(
        id=42553,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefRot's parameter not exist",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefRot 参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42554: AlarmInfo(
        id=42554,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef's optional parameter rotate error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefrotate 可选参数 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42555: AlarmInfo(
        id=42555,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef's parameter rotate error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef参数rotate错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42556: AlarmInfo(
        id=42556,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefSpiral parameter not exist.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefSpiral 参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42557: AlarmInfo(
        id=42557,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefSpiral's optional parameter error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefSpiral 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42558: AlarmInfo(
        id=42558,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRefSpiral's parameter error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRefSpiral参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42559: AlarmInfo(
        id=42559,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="FCRef limitValue error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="FCRef 错误的限制范围",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42688: AlarmInfo(
        id=42688,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The number of FCSetGain parameters is incorrect",
            cause="",
            solution="Please enter a floating point number",
        ),
        zh_CN=LocalizedText(
            description="FCSetGain参数个数错误",
            cause="",
            solution="请输入一个浮点数",
        ),
    ),
    42689: AlarmInfo(
        id=42689,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameter type of the FCSetGain is incorrect",
            cause="",
            solution="Please enter a floating point number",
        ),
        zh_CN=LocalizedText(
            description="FCSetGain参数类型错误",
            cause="",
            solution="请输入一个浮点数",
        ),
    ),
    42690: AlarmInfo(
        id=42690,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The FCSetGain parameter value range is incorrect",
            cause="",
            solution="Enter a floating point number ranging from 0 to 2",
        ),
        zh_CN=LocalizedText(
            description="FCSetGain参数范围错误",
            cause="",
            solution="请输入 0~2范围的浮点数",
        ),
    ),
    42752: AlarmInfo(
        id=42752,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SetSafeSkin not exist param",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="电子皮肤感应无输入参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42753: AlarmInfo(
        id=42753,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SetSafeSkin parameters error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="电子皮肤感应参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    42754: AlarmInfo(
        id=42754,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SetSafeSkin parameters out of range",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="电子皮肤感应参数超限",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45056: AlarmInfo(
        id=45056,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Circle3 command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Circle3指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45057: AlarmInfo(
        id=45057,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Jump command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jump指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45058: AlarmInfo(
        id=45058,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Arch command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45059: AlarmInfo(
        id=45059,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Arch3 command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Arch3 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45060: AlarmInfo(
        id=45060,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Jerk command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Jerk 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45061: AlarmInfo(
        id=45061,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of JerkR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="JerkR 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45062: AlarmInfo(
        id=45062,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of JerkS command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="JerkS 可选参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    45063: AlarmInfo(
        id=45063,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Accel command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Accel 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45064: AlarmInfo(
        id=45064,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of AccelR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AccelR指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45065: AlarmInfo(
        id=45065,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of AccelS command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="AccelS 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45066: AlarmInfo(
        id=45066,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of SpeedFactor command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedFactor 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45067: AlarmInfo(
        id=45067,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Speed command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Speed 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45068: AlarmInfo(
        id=45068,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of SpeedR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SpeedR 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45069: AlarmInfo(
        id=45069,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of LimZ command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="LimZ 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45070: AlarmInfo(
        id=45070,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of CP command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="CP 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45071: AlarmInfo(
        id=45071,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of DO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="DO 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45072: AlarmInfo(
        id=45072,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Go command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GO指令可选 参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    45073: AlarmInfo(
        id=45073,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Move command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Move 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45074: AlarmInfo(
        id=45074,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of MoveJ command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJ 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45075: AlarmInfo(
        id=45075,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter of Ecp command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Ecp 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45076: AlarmInfo(
        id=45076,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of EcpSet command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="EcpSet 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45077: AlarmInfo(
        id=45077,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of SetExicit Mode command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetExicitMode 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45078: AlarmInfo(
        id=45078,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Pallet command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Pallet 可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45079: AlarmInfo(
        id=45079,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter CP is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数 CP 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45080: AlarmInfo(
        id=45080,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter tool is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 TooL 参数错误",
            cause="",
            solution="输入正确参数",
        ),
    ),
    45081: AlarmInfo(
        id=45081,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter user is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中的 user 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45082: AlarmInfo(
        id=45082,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter speed is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 speed 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45083: AlarmInfo(
        id=45083,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter SpeedS is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 SpeedS 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45084: AlarmInfo(
        id=45084,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Accel is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 Accel 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45085: AlarmInfo(
        id=45085,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter AccelS is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 accels 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45086: AlarmInfo(
        id=45086,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter Arch is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数 Arch 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45087: AlarmInfo(
        id=45087,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter start is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 start 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45088: AlarmInfo(
        id=45088,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter zlimit is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 zlimit 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45089: AlarmInfo(
        id=45089,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter  end is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 end 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45090: AlarmInfo(
        id=45090,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter sync is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 sync 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45091: AlarmInfo(
        id=45091,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter arm is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中 arm 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45092: AlarmInfo(
        id=45092,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter ForceControl is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="可选参数中的 ForceControl 错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45093: AlarmInfo(
        id=45093,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="index of setTool overflow",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setTool 设置参数索引溢出",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45094: AlarmInfo(
        id=45094,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="index of setUser overflow",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setUser 设置参数索引溢出",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45095: AlarmInfo(
        id=45095,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="tool list in setTool params is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setTool 设置tool参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45096: AlarmInfo(
        id=45096,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="user list in setUser params is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setUser 设置user参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45135: AlarmInfo(
        id=45135,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="MoveR instruction type error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveR指令类型错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45136: AlarmInfo(
        id=45136,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of MoveR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveR指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45137: AlarmInfo(
        id=45137,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of GoR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoR指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45138: AlarmInfo(
        id=45138,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of MoveJR command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJR指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45139: AlarmInfo(
        id=45139,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of GoIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoIO指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45140: AlarmInfo(
        id=45140,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of MoveIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveIO指令可选参数错误 ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45141: AlarmInfo(
        id=45141,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of MoveJIO command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveJIO指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45142: AlarmInfo(
        id=45142,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of Path Recur command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="轨迹复现可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45312: AlarmInfo(
        id=45312,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of LoadSwitch command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="LoadSwitch指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45313: AlarmInfo(
        id=45313,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of LoadSet command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="LoadSet指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45568: AlarmInfo(
        id=45568,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameters of SetABZ command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetABZ指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45569: AlarmInfo(
        id=45569,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Optional parameter are of GetABZ command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetABZ()指令可选参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45824: AlarmInfo(
        id=45824,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetToolBaudRate command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetToolBaudRate()指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45825: AlarmInfo(
        id=45825,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetDOMode command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetDOMode()指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45826: AlarmInfo(
        id=45826,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetToolPower command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetToolPower()指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45827: AlarmInfo(
        id=45827,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 baud rate type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485() 的波特率参数类型错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45828: AlarmInfo(
        id=45828,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 baudrate range error 1200 ~ 4500000",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485() 波特率参数的范围不对 1200 ~ 4500000",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45829: AlarmInfo(
        id=45829,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 stop bits type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485() 的停止位的参数类型错误 ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45830: AlarmInfo(
        id=45830,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 stop bit value error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485()指令的停止位的值错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45831: AlarmInfo(
        id=45831,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 parity type error need a string N/O/E",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485()指令校验位类型错误 需要一个字符串  N/O/E ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45832: AlarmInfo(
        id=45832,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485 parity value error ,string N/O/E",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485()指令的值错误, 需要一个字符串 N    O  E ",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    45833: AlarmInfo(
        id=45833,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of SetTool485  number error  1 ~ 3 params.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="SetTool485()指令参数数量 错误 需要输入 1 ~ 3 个 参数",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    46096: AlarmInfo(
        id=46096,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of collisionLogInfo is wrong,interger only",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="collisionLogInfo() 参数错误,只允许输入整形数字",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    46097: AlarmInfo(
        id=46097,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of setCollisionLevel command is wrong,interger only",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setCollisionLevel() 参数错误,只允许输入整形",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    46098: AlarmInfo(
        id=46098,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="it is not promitted to set install angle during enable mode",
            cause="",
            solution="disable robot, repeat setting install angle",
        ),
        zh_CN=LocalizedText(
            description="使能状态不允许设置安装角度",
            cause="",
            solution="下使能，再设置安装角度",
        ),
    ),
    46080: AlarmInfo(
        id=46080,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of setExcitMod command is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ExcitMode() 参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    46112: AlarmInfo(
        id=46112,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='BlockHighlight("id") params number error',
            cause="",
            solution="Enter the correct parameters,only 1 params ",
        ),
        zh_CN=LocalizedText(
            description='BlockHighlight("id") 参数数量错误 ',
            cause="",
            solution="输入正确的参数只有一个参数",
        ),
    ),
    46113: AlarmInfo(
        id=46113,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='BlockHighlight("id") params type error.',
            cause="",
            solution="Enter the correct parameters,need a string ",
        ),
        zh_CN=LocalizedText(
            description='BlockHighlight("id") 参数类型错误',
            cause="",
            solution="输入正确的参数,需要一个字符串",
        ),
    ),
    46336: AlarmInfo(
        id=46336,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Input parameters of StartPath command are wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="StartPath()指令参数错误",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    46337: AlarmInfo(
        id=46337,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="StartPath command has no input parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="StartPath指令输入参数不存在",
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49153: AlarmInfo(
        id=49153,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Hardware emergency stop is pressed",
            cause="",
            solution="Please release the emergency stop",
        ),
        zh_CN=LocalizedText(
            description="硬件急停被按下",
            cause="",
            solution="请松开急停",
        ),
    ),
    49154: AlarmInfo(
        id=49154,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The software emergency stop is pressed",
            cause="",
            solution="Please release the emergency stop",
        ),
        zh_CN=LocalizedText(
            description="软件急停被按下",
            cause="",
            solution="请松开急停",
        ),
    ),
    49155: AlarmInfo(
        id=49155,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="User emergency stop is triggered",
            cause="",
            solution="Please check the hardware wiring",
        ),
        zh_CN=LocalizedText(
            description="用户急停被触发",
            cause="",
            solution="请检查硬件接线",
        ),
    ),
    49920: AlarmInfo(
        id=49920,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="",
            cause="",
            solution="",
        ),
        zh_CN=LocalizedText(
            description="电子皮肤未安装",
            cause="",
            solution="请安装电子皮肤再使用该api",
        ),
    ),
    49425: AlarmInfo(
        id=49425,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='InitCam("CAMn") params number error',
            cause="",
            solution='enter camer\'s name in string, eg. InitCam("CAMn")',
        ),
        zh_CN=LocalizedText(
            description='InitCam("CAMn") 的 参数个数不对',
            cause="",
            solution='只输入一个相机的名称即可   eg. InitCam("CAMn")',
        ),
    ),
    49426: AlarmInfo(
        id=49426,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='InitCam("CAMn") has recved a wrong type params. need string',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='InitCam("CAMn") 的输入参数1的类型出错, 只能输入字符串',
            cause="",
            solution="输入正确的相机名称!",
        ),
    ),
    49427: AlarmInfo(
        id=49427,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='InitCam("CAMn") has recved a wrong camer name, can not find this camer.',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='InitCam("CAMn") 参数1内容错误,相机名称出错，配置文件找不到这个相机',
            cause="",
            solution="正确输入相机的名称,注意大小写！",
        ),
    ),
    49441: AlarmInfo(
        id=49441,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='TriggerCam("CAMn") params number err , only need one camer name.',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='TriggerCam("CAMn") 的参数数量错误，只输入一个相机名称',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49442: AlarmInfo(
        id=49442,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='TriggerCam("CAMn") params type error,string only',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='TriggerCam("CAMn")参数1类型错误,只允许是string',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49443: AlarmInfo(
        id=49443,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='TriggerCam("CAMn") params content error, can not find this camer!',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='TriggerCam("CAMn") 的参数1内容错误，找不到这个相机',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49457: AlarmInfo(
        id=49457,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='SendCam("CAMn","string") params number err , only need camer name and string to send.',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='SendCam("CAMn","string") 的参数数量错误，需要输入两个参数，一个相机名称，一个发送的字符串',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49458: AlarmInfo(
        id=49458,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='SendCam("CAMn","string") params 1 type error,string only',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='SendCam("CAMn","string") 参数 1 类型错误,只允许是字符串string',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49459: AlarmInfo(
        id=49459,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='SendCam("CAMn","string") params 2 type error, string only ',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='SendCam("CAMn","string") 的参数 2 类型错误，只允许是字符串',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49460: AlarmInfo(
        id=49460,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='SendCam("CAMn","string") params 1 content error, can not find this camer!',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='SendCam("CAMn","string") 参数 1内容错误 找不到这个相机',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49473: AlarmInfo(
        id=49473,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='RecvCam("CAMn") params number err , need one camer name.',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='RecvCam("CAMn") 的参数数量错误',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49474: AlarmInfo(
        id=49474,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='RecvCam("CAMn") params 1  type error,string only',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='RecvCam("CAMn")参数 1 类型错误,只允许是string',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49475: AlarmInfo(
        id=49475,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='RecvCam("CAMn") params 2  type error,bool only',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='RecvCam("CAMn") 的参数2类型错误 需要一个bool 量',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49476: AlarmInfo(
        id=49476,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='RecvCam("CAMn",true/false) params 1 content error',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='RecvCam("CAMn", true / false) 的参数1的内容错误 找不到这个相机',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49477: AlarmInfo(
        id=49477,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='RecvCam("CAMn",true/false) params 2 content error',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='RecvCam("CAMn", true / false) 的参数2 内容错误',
            cause="",
            solution="输入正确的参数",
        ),
    ),
    49489: AlarmInfo(
        id=49489,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='DestroyCam("CAMn") params number error',
            cause="",
            solution='enter camer\'s name in string, eg. InitCam("CAMn")',
        ),
        zh_CN=LocalizedText(
            description='DestroyCam("CAMn") 的 参数个数不对',
            cause="",
            solution='只输入一个相机的名称即可   eg. DestroyCam("CAMn")',
        ),
    ),
    49490: AlarmInfo(
        id=49490,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='DestroyCam("CAMn") has recved a wrong type params. need string',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='DestroyCam("CAMn") 的输入参数的类型出错, 只能输入字符串',
            cause="",
            solution="输入正确的相机名称!",
        ),
    ),
    49491: AlarmInfo(
        id=49491,
        level=AlarmLevel(5),
        en=LocalizedText(
            description='DestroyCam("CAMn") has recved a wrong camer name, can not find this camer.',
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description='DestroyCam("CAMn") 的相机名称出错，配置文件找不到这个相机',
            cause="",
            solution="正确输入相机的名称,注意大小写！",
        ),
    ),
    49674: AlarmInfo(
        id=49674,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="ModbusClose Input params is error.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="不在OP状态，在PREOP状态，系统将尝试切换从站到OP",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    49664: AlarmInfo(
        id=49664,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Current master number is maximum, can not created.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="创建Modbus主站个数超过最大数量 4",
            cause="",
            solution="主站不能创建超过最大数量！",
        ),
    ),
    49665: AlarmInfo(
        id=49665,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Current master number is maximum, can not created.",
            cause="",
            solution="Not to create this master!",
        ),
        zh_CN=LocalizedText(
            description="创建Modbus主站个数超过最大数量 4",
            cause="",
            solution="主站不能创建超过最大数量！",
        ),
    ),
    49666: AlarmInfo(
        id=49666,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="ModbusCreate Input params is error.",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ModbusCreate 输入参数错误",
            cause="",
            solution="正确输入参数！",
        ),
    ),
    49667: AlarmInfo(
        id=49667,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Init socket failed.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="初始化失败！",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49668: AlarmInfo(
        id=49668,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetInBits params error ",
            cause="",
            solution="Please check  input",
        ),
        zh_CN=LocalizedText(
            description="GetInBits  参数错误",
            cause="",
            solution="请检查输入参数",
        ),
    ),
    49669: AlarmInfo(
        id=49669,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetInRegs Input params is error.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="GetInRegs 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49670: AlarmInfo(
        id=49670,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SetHoldRegs Input params is error.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="SetHoldRegs 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49671: AlarmInfo(
        id=49671,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetHoldRegs Input params is error.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="GetHoldRegs 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49672: AlarmInfo(
        id=49672,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetCoils Input params is error.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="GetCoils 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49673: AlarmInfo(
        id=49673,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="SetCoils Input params is error.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="SetCoils 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49675: AlarmInfo(
        id=49675,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="ModbusCreate The fourth input parameter is abnormal.The valid range is 0 or 1.",
            cause="",
            solution="Please check input params.",
        ),
        zh_CN=LocalizedText(
            description="ModbusCreate 第四个输入参数错误。取值范围为0或1。",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    49792: AlarmInfo(
        id=49792,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Incorrect number of arguments to InverseSolution() ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数数量错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49793: AlarmInfo(
        id=49793,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 1 of InverseSolution() is of type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数1类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49794: AlarmInfo(
        id=49794,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 2 of InverseSolution() is of type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数2类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49795: AlarmInfo(
        id=49795,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 3 of InverseSolution() is of type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数3类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49796: AlarmInfo(
        id=49796,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 4 of InverseSolution() is of type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数4类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49797: AlarmInfo(
        id=49797,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 5 of InverseSolution() is of type error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数5类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49798: AlarmInfo(
        id=49798,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 1 of InverseSolution() has an error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数1内容错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49799: AlarmInfo(
        id=49799,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Parameter 5 of InverseSolution() has an error ",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="InverseSolution()的参数5内容错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49808: AlarmInfo(
        id=49808,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong number of setbackdistance() entries",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setbackdistance()输入个数错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49809: AlarmInfo(
        id=49809,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong type of setbackdistance() input parameter",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setbackdistance()输入参数类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49810: AlarmInfo(
        id=49810,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The input parameter range of setbackdistance() is wrong",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="setbackdistance()输入参数范围错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50441: AlarmInfo(
        id=50441,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The second parameter number of goio is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="goio 第2个参数个数错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50442: AlarmInfo(
        id=50442,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The first value range of the second parameter in goio is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="goio 第2个参数的第一个值范围不对错误",
            cause="",
            solution="检查输入",
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
            description="ModbusClose 输入参数错误",
            cause="",
            solution="请检查输入参数！",
        ),
    ),
    60960: AlarmInfo(
        id=60960,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Safety IO is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="安全IO掉线，请确认控制器与安全IO板之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60961: AlarmInfo(
        id=60961,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="General IO is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="通用IO掉线，请确认本体与通用IO板之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60962: AlarmInfo(
        id=60962,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 1 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节1掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60963: AlarmInfo(
        id=60963,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 2 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节2掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60964: AlarmInfo(
        id=60964,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 3 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节3掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60965: AlarmInfo(
        id=60965,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 4 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节4掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60966: AlarmInfo(
        id=60966,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 5 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节5掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60967: AlarmInfo(
        id=60967,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Joint 6 is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="关节6掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    60968: AlarmInfo(
        id=60968,
        level=AlarmLevel(0),
        en=LocalizedText(
            description="Terminal IO is disconnected, please confirm the EtherCAT link between the controller and the safety IO board.",
            cause="",
            solution="Check whether the hardware is working properly, and restart the controller， or contact technical support engineer.",
        ),
        zh_CN=LocalizedText(
            description="末端IO掉线，请确认控制柜与本体之间的EtherCAT链路",
            cause="",
            solution="检查硬件是否正常并重新启动，或联系技术支持工程师",
        ),
    ),
    49713: AlarmInfo(
        id=49713,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="the number of params of CyHelix  is error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="CyHelix 的参数个数存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49714: AlarmInfo(
        id=49714,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="the range of params of CyHelix  is error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="CyHelix 的参数范围存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49728: AlarmInfo(
        id=49728,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params number error, 2 or 3 params",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数数量不对  2~3 个参数",
            cause="",
            solution="检查输入",
        ),
    ),
    49729: AlarmInfo(
        id=49729,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 1 type error,need a offser table {x,y,z,a,b,c}",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数1的类型错误 需要一个table  {x,y,z,a,b,c}",
            cause="",
            solution="检查输入",
        ),
    ),
    49730: AlarmInfo(
        id=49730,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 1 content error,need a offser table {x,y,z,a,b,c}",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数1的内容错误 需要一个table  {x,y,z,a,b,c}",
            cause="",
            solution="检查输入",
        ),
    ),
    49731: AlarmInfo(
        id=49731,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 2 type error,need an index of tool or user range 0 ~ 9",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数2的类型错误 需要一个整形的索引 范围是 0 ~ 9",
            cause="",
            solution="检查输入",
        ),
    ),
    49732: AlarmInfo(
        id=49732,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 2 content error,need an index of tool or user range 0~9",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数2的内容错误 需要一个整形的索引 范围是 0 ~ 9",
            cause="",
            solution="检查输入",
        ),
    ),
    49733: AlarmInfo(
        id=49733,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 3 type error,need a string",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数3的类型错误 需要一个字符串",
            cause="",
            solution="检查输入",
        ),
    ),
    49734: AlarmInfo(
        id=49734,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command GoToolR() or GoUserR() params 3 content error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GoToolR() 或者是 GoUserR()的参数3的内容错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49744: AlarmInfo(
        id=49744,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params number error, 2 or 3 params",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数数量不对  2~3 个参数",
            cause="",
            solution="检查输入",
        ),
    ),
    49745: AlarmInfo(
        id=49745,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 1 type error,need a offser table {x,y,z,a,b,c}",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数1的类型错误 需要一个table  {x,y,z,a,b,c}",
            cause="",
            solution="检查输入",
        ),
    ),
    49746: AlarmInfo(
        id=49746,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 1 content error,need a offser table {x,y,z,a,b,c}",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数1的内容错误 需要一个table  {x,y,z,a,b,c}",
            cause="",
            solution="检查输入",
        ),
    ),
    49747: AlarmInfo(
        id=49747,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 2 type error,need an index of tool or user range 0 ~ 9",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数2的类型错误 需要一个整形的索引 范围是 0 ~ 9",
            cause="",
            solution="检查输入",
        ),
    ),
    49748: AlarmInfo(
        id=49748,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 2 content error,need an index of tool or user range 0~9",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数2的内容错误 需要一个整形的索引 范围是 0 ~ 9",
            cause="",
            solution="检查输入",
        ),
    ),
    49749: AlarmInfo(
        id=49749,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 3 type error,need a string",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数3的类型错误 需要一个字符串",
            cause="",
            solution="检查输入",
        ),
    ),
    49750: AlarmInfo(
        id=49750,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="command MoveToolR() or MoveUserR() params 3 content error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="MoveToolR() 或者是 MoveUserR()的参数3的内容错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49921: AlarmInfo(
        id=49921,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the number of parameters of ScrewSetCurrentSN()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewSetCurrentSN()的参数个数存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49922: AlarmInfo(
        id=49922,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameter type of ScrewSetCurrentSN() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewSetCurrentSN()的参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49923: AlarmInfo(
        id=49923,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameter range of ScrewSetCurrentSN() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewSetCurrentSN()的参数范围存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49953: AlarmInfo(
        id=49953,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the number of parameters of ScrewCommitInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的参数个数存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49954: AlarmInfo(
        id=49954,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The first parameter type of ScrewCommitInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的第1个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49955: AlarmInfo(
        id=49955,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the first parameter range of ScrewCommitInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的第1个参数范围存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49957: AlarmInfo(
        id=49957,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The second parameter type of ScrewCommitInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的第2个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49960: AlarmInfo(
        id=49960,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The third parameter type of ScrewCommitInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的第3个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49963: AlarmInfo(
        id=49963,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The fourth parameter type of ScrewCommitInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitInfo()的第4个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49969: AlarmInfo(
        id=49969,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the number of parameters of ScrewCommitProductInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的参数个数存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49970: AlarmInfo(
        id=49970,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The first parameter type of ScrewCommitProductInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的第1个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49971: AlarmInfo(
        id=49971,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the first parameter range of ScrewCommitProductInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的第1个参数范围存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49973: AlarmInfo(
        id=49973,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the second number type of ScrewCommitProductInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的第2个数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49976: AlarmInfo(
        id=49976,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The third parameter type of ScrewCommitProductInfo() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的第3个参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49979: AlarmInfo(
        id=49979,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the fourth number type of ScrewCommitProductInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitProductInfo()的第4个数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49985: AlarmInfo(
        id=49985,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="There is an error in the number of parameters of ScrewCommitErrInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitErrInfo()的参数个数存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49986: AlarmInfo(
        id=49986,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong parameter type of ScrewCommitErrInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitErrInfo()的参数类型存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    49987: AlarmInfo(
        id=49987,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Error in parameter range of ScrewCommitErrInfo()",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="ScrewCommitErrInfo()的参数范围存在错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50176: AlarmInfo(
        id=50176,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The number of parameters for GetPose() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetPose()的参数个数不正确",
            cause="",
            solution="检查输入",
        ),
    ),
    50177: AlarmInfo(
        id=50177,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameter type of GetPose() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetPose()的参数类型不正确",
            cause="",
            solution="检查输入",
        ),
    ),
    50178: AlarmInfo(
        id=50178,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The parameter content of GetPose() is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetPose()的参数内容不正确",
            cause="",
            solution="检查输入",
        ),
    ),
    50179: AlarmInfo(
        id=50179,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="GetPose() execution error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetPose()执行错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50192: AlarmInfo(
        id=50192,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong number of tcpspeed () parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="tcpspeed()参数个数错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50193: AlarmInfo(
        id=50193,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="The tcpspeed () parameter type is incorrect",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="Wrong number of tcpspeed () parameters",
            cause="",
            solution="检查输入",
        ),
    ),
    50194: AlarmInfo(
        id=50194,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Tcpspeed () parameter range error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="tcpspeed()参数范围错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50195: AlarmInfo(
        id=50195,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Tcpspeed () internal execution error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="tcpspeed()内部执行错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50208: AlarmInfo(
        id=50208,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong number of tcpspeedend () parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="tcpspeedend()参数个数错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50209: AlarmInfo(
        id=50209,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Tcpspeedend () internal execution error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="GetPose()执行错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50224: AlarmInfo(
        id=50224,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong number of servoj() parameters",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()参数数量错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50225: AlarmInfo(
        id=50225,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Wrong type of servoj() parameter 1",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()参数1类型错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50226: AlarmInfo(
        id=50226,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Servoj() parameter 1 range error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()参数1范围错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50227: AlarmInfo(
        id=50227,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Servoj() optional parameter does not exist",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()可选参数不存在",
            cause="",
            solution="检查输入",
        ),
    ),
    50228: AlarmInfo(
        id=50228,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Servoj() optional parameter t error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()可选参数t错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50229: AlarmInfo(
        id=50229,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Servoj() optional parameter lookahead_time error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()可选参数lookahead_time错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50230: AlarmInfo(
        id=50230,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Servoj() optional parameter gain error",
            cause="",
            solution="Enter the correct parameters",
        ),
        zh_CN=LocalizedText(
            description="servoj()可选参数gain错误",
            cause="",
            solution="检查输入",
        ),
    ),
    50240: AlarmInfo(
        id=50240,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Abnormal communication between controller and algorithm",
            cause="",
            solution="Please rerun the script",
        ),
        zh_CN=LocalizedText(
            description="与算法通信异常",
            cause="",
            solution="请重新运行脚本",
        ),
    ),
    50241: AlarmInfo(
        id=50241,
        level=AlarmLevel(5),
        en=LocalizedText(
            description="Abnormal communication between Di() and algorithm",
            cause="",
            solution="Please rerun the script",
        ),
        zh_CN=LocalizedText(
            description="di与算法通信异常",
            cause="",
            solution="请重新运行脚本",
        ),
    ),
}
