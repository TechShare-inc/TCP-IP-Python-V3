"""Basic connection and movement demo."""

from dobot_api_v3 import DobotApiDashboard, DobotApiMove, DobotApiFeedBack


def main() -> None:
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)
    move = DobotApiMove(ip, 30003)
    feed = DobotApiFeedBack(ip, 30004)

    dashboard.EnableRobot()
    dashboard.ClearError()
    dashboard.SpeedFactor(50)
    move.MovJ(200, 0, 200, 0, 0, 0)

    data = feed.feedBackData()
    if data is not None:
        print(f"Enable status: {data['enable_status'][0]}")

    dashboard.DisableRobot()
    dashboard.close()
    move.close()
    feed.close()


if __name__ == "__main__":
    main()
