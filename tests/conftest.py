"""Shared pytest configuration for the unified dobot_api test suite."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--dobot-ip",
        action="store",
        default=None,
        help="Robot IP address for hardware-in-the-loop tests.",
    )
    parser.addoption(
        "--dobot-protocol",
        action="store",
        default=None,
        choices=("v3", "v4"),
        help="Robot protocol version for HIL tests.",
    )


@pytest.fixture(params=["v3", "v4"])
def protocol(request: pytest.FixtureRequest) -> str:
    """Parametrized protocol fixture for cross-protocol unit tests."""
    return request.param  # type: ignore[no-any-return]
