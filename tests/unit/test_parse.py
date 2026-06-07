"""Unit tests for the shared _parse module."""

from __future__ import annotations

import pytest

from dobot_api._parse import (
    DobotApiError,
    parse_ack,
    parse_error_ids,
    parse_int,
    parse_pose,
    parse_response,
)


class TestParseResponse:
    def test_valid_response(self) -> None:
        cmd_id, payload = parse_response("0,{42},EnableRobot();")
        assert cmd_id == 0
        assert payload == "42"

    def test_error_response_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("-1,{some error},EnableRobot();")
        assert exc_info.value.error_code == -1

    def test_error_code_zero_with_payload(self) -> None:
        """Command ID of 0 with error_code=0 is valid (first field is error_code)."""
        cmd_id, payload = parse_response("0,{42},RobotMode();")
        assert cmd_id == 0
        assert payload == "42"

    def test_empty_payload(self) -> None:
        cmd_id, payload = parse_response("0,{},DisableRobot();")
        assert cmd_id == 0
        assert payload == ""


class TestParseAck:
    def test_success_returns_none(self) -> None:
        assert parse_ack("0,{},EnableRobot();") is None

    def test_error_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_ack("-5,{},Something();")


class TestParseInt:
    def test_returns_int(self) -> None:
        assert parse_int("0,{42},RobotMode();") == 42

    def test_negative_int(self) -> None:
        assert parse_int("0,{-1},Something();") == -1

    def test_error_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_int("-1,{99},Something();")


class TestParsePose:
    def test_returns_pose(self) -> None:
        p = parse_pose("0,{1.0,2.0,3.0,4.0,5.0,6.0},GetPose();")
        assert p.x == 1.0
        assert p.y == 2.0
        assert p.z == 3.0
        assert p.rx == 4.0
        assert p.ry == 5.0
        assert p.rz == 6.0

    def test_negative_values(self) -> None:
        p = parse_pose("0,{-10.0,-20.0,-30.0,-1.0,-2.0,-3.0},GetAngle();")
        assert p.x == -10.0
        assert p.rz == -3.0

    def test_error_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_pose("-1,{1,2,3,4,5,6},GetPose();")


class TestParseErrorIds:
    def test_no_errors(self) -> None:
        ids = parse_error_ids("0,{[]},GetErrorID();")
        assert ids == ()

    def test_single_error(self) -> None:
        ids = parse_error_ids("0,{[16]},GetErrorID();")
        assert ids == (16,)

    def test_multiple_errors(self) -> None:
        ids = parse_error_ids("0,{[16,42,100]},GetErrorID();")
        assert ids == (16, 42, 100)

    def test_filters_zero_ids(self) -> None:
        ids = parse_error_ids("0,{[16,0,42,0,100]},GetErrorID();")
        assert ids == (16, 42, 100)

    def test_no_brackets(self) -> None:
        ids = parse_error_ids("0,{16,42},GetErrorID();")
        assert ids == (16, 42)

    def test_error_response_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_error_ids("-1,{[16]},GetErrorID();")
