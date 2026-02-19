"""Feedback polling example.

See also:
- docs/reference/command-patterns.md#pattern-5-feedback--error-monitoring
"""

from time import sleep

from dobot_api_v3 import DobotApiFeedback, PROTOCOL_FIELD_MAP


def main() -> None:
    """Read several feedback frames and print selected fields."""
    ip = "192.168.5.1"
    feedback = DobotApiFeedback(ip, 30004)

    try:
        for index in range(10):
            feedback_data = feedback.feedback_data()
            if feedback_data is None:
                print(f"[{index}] no frame")
                sleep(0.1)
                continue

            robot_mode = int(feedback_data["robot_mode"][0])
            is_enabled = int(feedback_data["enable_status"][0]) == 1
            tool_vector_actual = feedback_data["tool_vector_actual"][0].tolist()
            q_actual = feedback_data["q_actual"][0].tolist()
            tcp_force = feedback_data["tcp_force"][0].tolist()

            print(f"[{index}] robot_mode={robot_mode}, is_enabled={is_enabled}")
            print(f"  tool_vector_actual={tool_vector_actual}")
            print(f"  q_actual={q_actual}")
            print(f"  tcp_force={tcp_force}")
            print(
                "  protocol name for tcp_force: "
                f"{PROTOCOL_FIELD_MAP.get('tcp_force', 'tcp_force')}"
            )
            sleep(0.1)
    finally:
        feedback.close()


if __name__ == "__main__":
    main()
