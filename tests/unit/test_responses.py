"""Unit tests for the typed response parser (dobot_api_v3.responses)."""

from __future__ import annotations

import pytest

from dobot_api_v3.responses import (
    AckResponse,
    DobotApiError,
    ErrorIdResponse,
    IntResponse,
    PoseResponse,
    parse_response,
)

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# DobotApiError
# ---------------------------------------------------------------------------


class TestDobotApiError:
    def test_attributes_set(self) -> None:
        err = DobotApiError(error_code=-1, command_id=0, message="bad", raw="raw_str")
        assert err.error_code == -1
        assert err.command_id == 0
        assert err.message == "bad"
        assert err.raw == "raw_str"

    def test_str_contains_error_code(self) -> None:
        err = DobotApiError(error_code=5, command_id=2, message="fail", raw="5,2,fail;")
        assert "5" in str(err)
        assert "fail" in str(err)

    def test_is_exception(self) -> None:
        with pytest.raises(DobotApiError):
            raise DobotApiError(error_code=1, command_id=0, message="x", raw="1,0,x;")


# ---------------------------------------------------------------------------
# AckResponse — 3-field format "0,cmd_id,payload;"
# ---------------------------------------------------------------------------


class TestParseAckResponse:
    def test_standard_ok(self) -> None:
        resp = parse_response("0,0,ok;", AckResponse)
        assert isinstance(resp, AckResponse)
        assert resp.command_id == 0

    def test_nonzero_command_id(self) -> None:
        resp = parse_response("0,42,ok;", AckResponse)
        assert resp.command_id == 42

    def test_with_command_echo(self) -> None:
        resp = parse_response("0,0,EnableRobot();", AckResponse)
        assert isinstance(resp, AckResponse)

    def test_frozen(self) -> None:
        resp = parse_response("0,0,ok;", AckResponse)
        with pytest.raises((AttributeError, TypeError)):
            resp.command_id = 99  # type: ignore[misc]

    def test_without_trailing_semicolon(self) -> None:
        """Parser should tolerate a missing trailing semicolon."""
        resp = parse_response("0,0,ok", AckResponse)
        assert isinstance(resp, AckResponse)

    def test_leading_trailing_whitespace(self) -> None:
        resp = parse_response("  0,0,ok;  ", AckResponse)
        assert isinstance(resp, AckResponse)


# ---------------------------------------------------------------------------
# AckResponse — error code raises DobotApiError
# ---------------------------------------------------------------------------


class TestParseAckResponseErrors:
    def test_nonzero_error_code_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("-1,0,error;", AckResponse)
        assert exc_info.value.error_code == -1

    def test_positive_error_code_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("10,0,fail;", AckResponse)
        assert exc_info.value.error_code == 10

    def test_error_carries_command_id(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("2,7,bad;", AckResponse)
        assert exc_info.value.command_id == 7

    def test_error_carries_raw(self) -> None:
        raw = "3,0,err;"
        with pytest.raises(DobotApiError) as exc_info:
            parse_response(raw, AckResponse)
        assert exc_info.value.raw == raw

    def test_empty_string_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("", AckResponse)
        assert exc_info.value.error_code == -1

    def test_malformed_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("garbage", AckResponse)
        assert exc_info.value.error_code == -1

    def test_only_semicolon_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_response(";", AckResponse)


# ---------------------------------------------------------------------------
# IntResponse — 2-field brace format "0,{value};"
# ---------------------------------------------------------------------------


class TestParseIntResponse:
    def test_robot_mode_style(self) -> None:
        resp = parse_response("0,{5};", IntResponse)
        assert isinstance(resp, IntResponse)
        assert resp.value == 5
        assert resp.command_id == 0

    def test_negative_value(self) -> None:
        resp = parse_response("0,{-3};", IntResponse)
        assert resp.value == -3

    def test_three_field_plain_int(self) -> None:
        """3-field format with a plain integer payload."""
        resp = parse_response("0,0,5;", IntResponse)
        assert resp.value == 5

    def test_three_field_brace_int(self) -> None:
        resp = parse_response("0,0,{7};", IntResponse)
        assert resp.value == 7

    def test_no_integer_in_payload_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_response("0,0,none;", IntResponse)

    def test_error_code_still_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("1,{5};", IntResponse)
        assert exc_info.value.error_code == 1


# ---------------------------------------------------------------------------
# PoseResponse — 6 floats  "0,{x,y,z,rx,ry,rz};"
# ---------------------------------------------------------------------------


class TestParsePoseResponse:
    def test_standard_pose(self) -> None:
        resp = parse_response("0,{200.5,-10.3,300.0,0.0,90.0,0.0};", PoseResponse)
        assert isinstance(resp, PoseResponse)
        assert resp.x == pytest.approx(200.5)
        assert resp.y == pytest.approx(-10.3)
        assert resp.z == pytest.approx(300.0)
        assert resp.rx == pytest.approx(0.0)
        assert resp.ry == pytest.approx(90.0)
        assert resp.rz == pytest.approx(0.0)

    def test_command_id_zero_when_two_field(self) -> None:
        resp = parse_response("0,{1.0,2.0,3.0,4.0,5.0,6.0};", PoseResponse)
        assert resp.command_id == 0

    def test_three_field_brace_pose(self) -> None:
        resp = parse_response("0,0,{1.0,2.0,3.0,4.0,5.0,6.0};", PoseResponse)
        assert resp.command_id == 0
        assert resp.x == pytest.approx(1.0)

    def test_all_zeros(self) -> None:
        resp = parse_response("0,{0.0,0.0,0.0,0.0,0.0,0.0};", PoseResponse)
        assert resp.x == pytest.approx(0.0)
        assert resp.rz == pytest.approx(0.0)

    def test_negative_angles(self) -> None:
        resp = parse_response("0,{-100.0,-200.0,-300.0,-1.0,-2.0,-3.0};", PoseResponse)
        assert resp.x == pytest.approx(-100.0)
        assert resp.ry == pytest.approx(-2.0)

    def test_integer_values_coerced_to_float(self) -> None:
        resp = parse_response("0,{1,2,3,4,5,6};", PoseResponse)
        assert isinstance(resp.x, float)

    def test_fewer_than_six_floats_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_response("0,{1.0,2.0,3.0};", PoseResponse)

    def test_error_code_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_response("2,{0.0,0.0,0.0,0.0,0.0,0.0};", PoseResponse)

    def test_frozen(self) -> None:
        resp = parse_response("0,{1.0,2.0,3.0,4.0,5.0,6.0};", PoseResponse)
        with pytest.raises((AttributeError, TypeError)):
            resp.x = 999.0  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ErrorIdResponse — "0,{id1,id2,...};"
# ---------------------------------------------------------------------------


class TestParseErrorIdResponse:
    def test_no_errors(self) -> None:
        resp = parse_response("0,{0};", ErrorIdResponse)
        assert isinstance(resp, ErrorIdResponse)
        assert resp.error_ids == ()

    def test_single_error(self) -> None:
        resp = parse_response("0,{1001,0};", ErrorIdResponse)
        assert resp.error_ids == (1001,)

    def test_multiple_errors(self) -> None:
        resp = parse_response("0,{1001,1002};", ErrorIdResponse)
        assert resp.error_ids == (1001, 1002)

    def test_zeros_filtered(self) -> None:
        """Zero sentinel values must be excluded from error_ids."""
        resp = parse_response("0,{0,0,0};", ErrorIdResponse)
        assert resp.error_ids == ()

    def test_negative_ids(self) -> None:
        resp = parse_response("0,{-1,2};", ErrorIdResponse)
        assert -1 in resp.error_ids
        assert 2 in resp.error_ids

    def test_empty_brace_payload(self) -> None:
        resp = parse_response("0,{};", ErrorIdResponse)
        assert resp.error_ids == ()

    def test_command_id_preserved(self) -> None:
        resp = parse_response("0,0,{1001};", ErrorIdResponse)
        assert resp.command_id == 0
        assert 1001 in resp.error_ids

    def test_error_code_raises(self) -> None:
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("5,{1001};", ErrorIdResponse)
        assert exc_info.value.error_code == 5

    def test_empty_string_raises(self) -> None:
        with pytest.raises(DobotApiError):
            parse_response("", ErrorIdResponse)

    def test_frozen(self) -> None:
        resp = parse_response("0,{0};", ErrorIdResponse)
        with pytest.raises((AttributeError, TypeError)):
            resp.error_ids = (99,)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Public package export
# ---------------------------------------------------------------------------


class TestPublicExport:
    def test_all_types_importable_from_package(self) -> None:
        import dobot_api_v3

        for name in (
            "AckResponse",
            "IntResponse",
            "PoseResponse",
            "ErrorIdResponse",
            "DobotApiError",
            "parse_response",
        ):
            assert hasattr(dobot_api_v3, name), f"{name} not exported from package"
            assert name in dobot_api_v3.__all__, f"{name} not in __all__"
