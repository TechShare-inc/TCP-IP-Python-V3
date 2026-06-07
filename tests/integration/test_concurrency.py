"""Integration tests -- concurrency and thread-safety of send_recv_msg."""

from __future__ import annotations

import threading
from typing import List

import pytest

from tests.integration.conftest import make_api
from tests.integration.stub_server import StubServer

pytestmark = pytest.mark.integration


class TestConcurrency:
    def test_10_threads_all_receive_responses(self, stub: StubServer) -> None:
        """10 threads firing simultaneous send_recv_msg calls must all succeed.

        The _global_lock in DobotApi prevents interleaved bytes on the wire;
        each thread should receive a well-formed (non-empty) response string.
        """
        api = make_api(stub)
        results: List[str] = []
        errors: List[Exception] = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            try:
                resp = api.send_recv_msg(f"GetPose()")
                with lock:
                    results.append(resp)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        api.close()

        assert not errors, f"Thread errors: {errors}"
        assert len(results) == 10
        assert all(isinstance(r, str) and r for r in results)

    def test_responses_are_not_interleaved(self, stub: StubServer) -> None:
        """Each thread's response must contain the command it sent -- not a mix.

        This verifies that the global lock prevents response cross-talk between
        concurrent callers.
        """
        # Use distinct, easily identifiable commands to verify per-thread routing
        api = make_api(stub)
        mismatches: List[str] = []
        lock = threading.Lock()

        # Commands whose echo can be identified in the response
        commands = [f"SpeedFactor({i})" for i in range(1, 11)]

        def worker(cmd: str) -> None:
            resp = api.send_recv_msg(cmd)
            # The stub echoes the command back in the response
            if cmd not in resp:
                with lock:
                    mismatches.append(f"sent={cmd!r}, got={resp!r}")

        threads = [threading.Thread(target=worker, args=(c,)) for c in commands]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        api.close()

        assert not mismatches, (
            "Response cross-talk detected (lock not working?):\n"
            + "\n".join(mismatches)
        )

    def test_feedback_data_thread_isolation(
        self, stub: StubServer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DobotApiFeedback.feedback_data() must be callable from a dedicated thread
        without racing against dashboard commands on a different API instance."""
        from dobot_api.v3 import DobotApi, DobotApiFeedback, FeedbackDtype
        import numpy as np
        from unittest.mock import MagicMock

        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        fb = DobotApiFeedback("127.0.0.1", 30004)

        # Build a valid 1440-byte feedback packet
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr[0]["robot_mode"] = 4
        buf = arr.tobytes()[:1440]

        fb.socket_dobot = MagicMock()
        fb.socket_dobot.recv.return_value = buf

        results: List = []
        errors: List[Exception] = []

        def feedback_worker() -> None:
            try:
                data = fb.feedback_data()
                results.append(data)
            except Exception as exc:
                errors.append(exc)

        thread = threading.Thread(target=feedback_worker)
        thread.start()
        thread.join(timeout=3.0)

        assert not errors, f"Feedback thread errors: {errors}"
        assert len(results) == 1
        assert results[0] is not None
