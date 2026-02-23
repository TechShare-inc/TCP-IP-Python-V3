"""Feedback polling example.

See also:
- docs/reference/command-patterns.md#pattern-5-feedback--error-monitoring
"""

import json
import time
from pathlib import Path

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Read several feedback frames and print selected fields."""
    ip = "192.168.5.1"

    num_cycles = 100
    cycle_time = 0.008  # 8 ms

    recorded_data = []
    timestamps = []

    print(f"Starting {num_cycles} cycles of {cycle_time * 1000} ms...")

    with DobotRobot(ip) as robot:
        # robot.feedback is lazy — port 30004 connects on first access here.
        feedback = robot.feedback
        start_time = time.perf_counter()
        next_time = start_time

        for index in range(num_cycles):
            current_time = time.perf_counter()
            timestamps.append(current_time)

            feedback_data = feedback.feedback_data()
            if feedback_data is not None:
                entry = {
                    "index": index,
                    "timestamp": current_time,
                    "robot_mode": feedback_data.robot_mode,
                    "is_enabled": feedback_data.enable_status == 1,
                    "tool_vector_actual": list(feedback_data.tool_vector_actual),
                    "q_actual": list(feedback_data.q_actual),
                    "tcp_force": list(feedback_data.tcp_force),
                }
                recorded_data.append(entry)
            else:
                print(f"[{index}] no frame")

            # Wait for the next 8ms cycle
            next_time += cycle_time
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

    # All connections (dashboard, move, feedback) closed automatically on exit.

    # Record the data in file
    output_file = Path("feedback_data.json")
    with open(output_file, "w") as f:
        json.dump(recorded_data, f, indent=2)
    print(f"Data recorded to {output_file}")

    # Analyze the timing related metrics
    if len(timestamps) > 1:
        intervals = [
            timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))
        ]
        avg_interval = sum(intervals) / len(intervals)
        min_interval = min(intervals)
        max_interval = max(intervals)

        print("\nTiming Analysis:")
        print(f"  Total cycles: {len(timestamps)}")
        print(f"  Target cycle time: {cycle_time * 1000:.2f} ms")
        print(f"  Average cycle time: {avg_interval * 1000:.2f} ms")
        print(f"  Min cycle time: {min_interval * 1000:.2f} ms")
        print(f"  Max cycle time: {max_interval * 1000:.2f} ms")
        print(f"  Jitter (Max - Min): {(max_interval - min_interval) * 1000:.2f} ms")


if __name__ == "__main__":
    main()
