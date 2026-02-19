"""HIL (hardware-in-the-loop) conftest.

All HIL tests are skipped unless the environment variable ``DOBOT_TEST_IP``
is set to a reachable robot IP address.

Example usage::

    # Run HIL tests against a robot at 192.168.1.6
    DOBOT_TEST_IP=192.168.1.6 pytest tests/hil -v -m hil

Optional variables:

    DOBOT_DASHBOARD_PORT   Dashboard port (default: 29999)
    DOBOT_MOVE_PORT        Move port (default: 30003)
    DOBOT_FEEDBACK_PORT    Feedback port (default: 30004)
"""

from __future__ import annotations

import os
from typing import Generator

import pytest

from dobot_api_v3.dashboard import DobotApiDashboard
from dobot_api_v3.feedback import DobotApiFeedback
from dobot_api_v3.move import DobotApiMove

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

_ROBOT_IP = os.environ.get("DOBOT_TEST_IP", "")
_DASHBOARD_PORT = int(os.environ.get("DOBOT_DASHBOARD_PORT", "29999"))
_MOVE_PORT = int(os.environ.get("DOBOT_MOVE_PORT", "30003"))
_FEEDBACK_PORT = int(os.environ.get("DOBOT_FEEDBACK_PORT", "30004"))

_SKIP_REASON = (
    "HIL test skipped: set DOBOT_TEST_IP environment variable to the robot IP "
    "address to enable hardware-in-the-loop tests."
)

# ---------------------------------------------------------------------------
# Shared skip marker
# ---------------------------------------------------------------------------

requires_hardware = pytest.mark.skipif(
    not _ROBOT_IP,
    reason=_SKIP_REASON,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def real_dashboard() -> Generator[DobotApiDashboard, None, None]:
    """Live DobotApiDashboard connected to the robot under test."""
    if not _ROBOT_IP:
        pytest.skip(_SKIP_REASON)
    db = DobotApiDashboard(_ROBOT_IP, _DASHBOARD_PORT)
    yield db
    db.close()


@pytest.fixture(scope="module")
def real_move() -> Generator[DobotApiMove, None, None]:
    """Live DobotApiMove connected to the robot under test."""
    if not _ROBOT_IP:
        pytest.skip(_SKIP_REASON)
    mv = DobotApiMove(_ROBOT_IP, _MOVE_PORT)
    yield mv
    mv.close()


@pytest.fixture(scope="module")
def real_feedback() -> Generator[DobotApiFeedback, None, None]:
    """Live DobotApiFeedback connected to the robot under test."""
    if not _ROBOT_IP:
        pytest.skip(_SKIP_REASON)
    fb = DobotApiFeedback(_ROBOT_IP, _FEEDBACK_PORT)
    yield fb
    fb.close()
