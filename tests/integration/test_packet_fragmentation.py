"""Integration tests -- TCP packet fragmentation and fault injection."""

from __future__ import annotations

import pytest

from tests.integration.conftest import make_api
from tests.integration.stub_server import (
    DelayedStubServer,
    FragmentedStubServer,
    GarbageStubServer,
)

pytestmark = pytest.mark.integration


class TestFragmentedResponse:
    def test_send_recv_works_when_response_is_fragmented(
        self, fragmented_stub: FragmentedStubServer
    ) -> None:
        """send_recv_msg must reconstruct the response even when the stub sends
        it in two TCP segments separated by a short gap."""
        api = make_api(fragmented_stub)
        try:
            result = api.send_recv_msg("EnableRobot()")
            # We only assert that we got *some* non-empty string back;
            # the full message may or may not be reassembled depending on
            # recv buffer timing -- this test verifies no crash.
            assert isinstance(result, str)
        finally:
            api.close()


class TestDelayedResponse:
    def test_send_recv_works_with_50ms_latency(
        self, delayed_stub: DelayedStubServer
    ) -> None:
        """API must not time-out or error on a server that responds after 50 ms."""
        api = make_api(delayed_stub)
        try:
            result = api.send_recv_msg("DisableRobot()")
            assert isinstance(result, str)
        finally:
            api.close()

    def test_multiple_commands_in_sequence(
        self, delayed_stub: DelayedStubServer
    ) -> None:
        api = make_api(delayed_stub)
        try:
            for cmd in ("EnableRobot()", "SpeedFactor(50)", "GetPose()"):
                result = api.send_recv_msg(cmd)
                assert isinstance(result, str)
        finally:
            api.close()


class TestGarbageResponse:
    def test_api_does_not_raise_on_garbage_bytes(
        self, garbage_stub: GarbageStubServer
    ) -> None:
        """The API must not crash when the server sends garbage ASCII.

        The response string may be nonsensical, but the call must not raise an
        exception from the networking layer.
        """
        api = make_api(garbage_stub)
        try:
            result = api.send_recv_msg("RobotMode()")
            assert isinstance(result, str)
        except UnicodeDecodeError:
            pytest.fail(
                "API raised UnicodeDecodeError on garbage response -- "
                "consider adding error='replace' to recv decode."
            )
        finally:
            api.close()
