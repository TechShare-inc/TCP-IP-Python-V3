"""Basic connection and movement demo."""

from dobot_api_v3 import DobotApiDashboard, DobotApiMove, DobotApiFeedback


def main() -> None:
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)
    move = DobotApiMove(ip, 30003)
    feed = DobotApiFeedback(ip, 30004)

    dashboard.enable_robot()
    dashboard.clear_error()
    dashboard.speed_factor(50)
    move.mov_j(200, 0, 200, 0, 0, 0)

    data = feed.feedback_data()
    if data is not None:
        print(f"Enable status: {data['enable_status'][0]}")

    dashboard.disable_robot()
    dashboard.close()
    move.close()
    feed.close()


if __name__ == "__main__":
    main()
