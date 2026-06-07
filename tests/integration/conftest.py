"""Integration-level conftest: stub server fixtures and a port-agnostic DobotApi."""

from __future__ import annotations

import socket as _socket
from typing import Generator

import pytest

from dobot_api.v3 import DobotApi
from tests.integration.stub_server import (
    DelayedStubServer,
    FragmentedStubServer,
    GarbageStubServer,
    StubServer,
)


# ---------------------------------------------------------------------------
# Port-agnostic subclass
# ---------------------------------------------------------------------------


class _AnyPortApi(DobotApi):
    """DobotApi subclass that accepts any TCP port (bypasses whitelist).

    The whitelist is tested in unit/test_base.py.  Integration tests need to
    connect to a randomly-assigned loopback port returned by the stub server.
    """

    def _connect(self) -> None:
        try:
            self.socket_dobot = _socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
        except OSError as exc:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}"
            ) from exc


# ---------------------------------------------------------------------------
# Module-scoped stub server — reused across all integration tests for speed.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def stub() -> Generator[StubServer, None, None]:
    """Basic echo stub server (module-scoped)."""
    server = StubServer()
    server.start()
    yield server
    server.stop()


@pytest.fixture
def delayed_stub() -> Generator[DelayedStubServer, None, None]:
    """Stub server that adds 50 ms latency (function-scoped)."""
    server = DelayedStubServer(delay=0.05)
    server.start()
    yield server
    server.stop()


@pytest.fixture
def fragmented_stub() -> Generator[FragmentedStubServer, None, None]:
    """Stub server that fragments each response into two halves."""
    server = FragmentedStubServer(gap=0.02)
    server.start()
    yield server
    server.stop()


@pytest.fixture
def garbage_stub() -> Generator[GarbageStubServer, None, None]:
    """Stub server that sends random garbage responses."""
    server = GarbageStubServer()
    server.start()
    yield server
    server.stop()


# ---------------------------------------------------------------------------
# Helper: build a _AnyPortApi connected to a given stub
# ---------------------------------------------------------------------------


def make_api(stub: StubServer) -> _AnyPortApi:
    return _AnyPortApi("127.0.0.1", stub.port)
