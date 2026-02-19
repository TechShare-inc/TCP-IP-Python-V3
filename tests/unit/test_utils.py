"""Unit tests for the deprecated_alias decorator in utils.py."""

from __future__ import annotations

import warnings

import pytest

from dobot_api_v3.utils import deprecated_alias

pytestmark = pytest.mark.unit


class TestDeprecatedAlias:
    """deprecated_alias wraps a method, delegates its call, and warns."""

    def _make_class(self) -> type:
        class Dummy:
            def new_name(self, x: int = 0) -> int:
                return x * 2

            @deprecated_alias("new_name")
            def OldName(self, x: int = 0) -> int:  # type: ignore[return-value]
                return self.new_name(x)

        return Dummy

    def test_emits_deprecation_warning(self) -> None:
        Dummy = self._make_class()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Dummy().OldName()
        dep_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(dep_warnings) == 1

    def test_warning_message_names_old_and_new(self) -> None:
        Dummy = self._make_class()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Dummy().OldName()
        msg = str(w[0].message)
        assert "OldName" in msg
        assert "new_name" in msg

    def test_delegates_return_value(self) -> None:
        Dummy = self._make_class()
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = Dummy().OldName(7)
        assert result == 14

    def test_delegates_positional_and_keyword_args(self) -> None:
        class Dummy:
            def new_name(self, a: int, b: int = 0) -> int:
                return a + b

            @deprecated_alias("new_name")
            def OldName(self, a: int, b: int = 0) -> int:  # type: ignore[return-value]
                return self.new_name(a, b)

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            assert Dummy().OldName(3, b=4) == 7

    def test_stacklevel_points_at_direct_caller_frame(self) -> None:
        """The warning filename should reference this test file, not utils.py."""
        Dummy = self._make_class()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Dummy().OldName()
        assert w[0].filename == __file__
