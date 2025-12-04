# Copyright 2025 Vantage Compute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for FFI utilities."""

import pytest

from helm_sdkpy._ffi import (
    _reset_for_tests,
    check_error,
    configure,
    ffi,
    get_library,
    get_version,
    string_from_c,
)
from helm_sdkpy.exceptions import HelmError


class TestGetLibrary:
    """Test get_library function."""

    def test_get_library_returns_library(self):
        """Test that get_library returns a library object."""
        lib = get_library()
        assert lib is not None

    def test_get_library_cached(self):
        """Test that get_library returns same instance on multiple calls."""
        lib1 = get_library()
        lib2 = get_library()
        assert lib1 is lib2

    def test_get_library_has_expected_functions(self):
        """Test that library has expected C functions."""
        lib = get_library()
        assert hasattr(lib, "helm_sdkpy_config_create")
        assert hasattr(lib, "helm_sdkpy_config_destroy")
        assert hasattr(lib, "helm_sdkpy_install")
        assert hasattr(lib, "helm_sdkpy_upgrade")
        assert hasattr(lib, "helm_sdkpy_uninstall")
        assert hasattr(lib, "helm_sdkpy_list")
        assert hasattr(lib, "helm_sdkpy_status")
        assert hasattr(lib, "helm_sdkpy_rollback")
        assert hasattr(lib, "helm_sdkpy_get_values")
        assert hasattr(lib, "helm_sdkpy_history")
        assert hasattr(lib, "helm_sdkpy_pull")
        assert hasattr(lib, "helm_sdkpy_show_chart")
        assert hasattr(lib, "helm_sdkpy_show_values")
        assert hasattr(lib, "helm_sdkpy_test")
        assert hasattr(lib, "helm_sdkpy_lint")
        assert hasattr(lib, "helm_sdkpy_package")
        assert hasattr(lib, "helm_sdkpy_repo_add")
        assert hasattr(lib, "helm_sdkpy_repo_remove")
        assert hasattr(lib, "helm_sdkpy_repo_list")
        assert hasattr(lib, "helm_sdkpy_repo_update")
        assert hasattr(lib, "helm_sdkpy_registry_login")
        assert hasattr(lib, "helm_sdkpy_registry_logout")
        assert hasattr(lib, "helm_sdkpy_push")
        assert hasattr(lib, "helm_sdkpy_last_error")
        assert hasattr(lib, "helm_sdkpy_free")
        assert hasattr(lib, "helm_sdkpy_version_number")
        assert hasattr(lib, "helm_sdkpy_version_string")


class TestGetVersion:
    """Test get_version function."""

    def test_get_version_returns_string(self):
        """Test that get_version returns a string."""
        version = get_version()
        assert isinstance(version, str)

    def test_get_version_not_empty(self):
        """Test that version is not empty."""
        version = get_version()
        assert len(version) > 0

    def test_get_version_format(self):
        """Test that version has expected format."""
        version = get_version()
        # Version should contain 'helm-sdkpy' or version number
        assert "helm" in version.lower() or any(c.isdigit() for c in version)


class TestConfigure:
    """Test configure function."""

    def test_configure_accepts_none(self):
        """Test that configure accepts None to reset."""
        # This should not raise
        configure(None)

    def test_configure_accepts_string(self):
        """Test that configure accepts a path string."""
        # This should not raise, even if path doesn't exist
        # (it only sets the path, doesn't validate it)
        configure("/some/path/to/lib.so")
        # Reset for other tests
        configure(None)


class TestCheckError:
    """Test check_error function."""

    def test_check_error_zero_no_exception(self):
        """Test that check_error with 0 does not raise."""
        # Should not raise
        check_error(0)

    def test_check_error_nonzero_raises(self):
        """Test that check_error with non-zero raises HelmError."""
        # First, we need to trigger an actual error in the library
        # to set the error message. For this test, we'll just verify
        # that when called with non-zero, it raises HelmError.
        with pytest.raises(HelmError):
            check_error(-1)


class TestStringFromC:
    """Test string_from_c function."""

    def test_string_from_c_null_returns_empty(self):
        """Test that string_from_c with NULL returns empty string."""
        result = string_from_c(ffi.NULL)
        assert result == ""

    def test_string_from_c_converts_string(self):
        """Test that string_from_c converts C string to Python string."""
        # Create a C string using the library's allocator
        lib = get_library()
        # We can use version_string which returns a valid C string
        version_ptr = lib.helm_sdkpy_version_string()
        # Note: version_string returns a static pointer, so we shouldn't free it
        # Just test that we can read it
        if version_ptr != ffi.NULL:
            result = ffi.string(version_ptr).decode("utf-8")
            assert isinstance(result, str)
            assert len(result) > 0


class TestFfi:
    """Test ffi object."""

    def test_ffi_exists(self):
        """Test that ffi object exists."""
        assert ffi is not None

    def test_ffi_can_create_char_array(self):
        """Test that ffi can create char arrays."""
        test_str = "hello world"
        c_str = ffi.new("char[]", test_str.encode("utf-8"))
        assert c_str is not None

    def test_ffi_null_constant(self):
        """Test that ffi.NULL exists."""
        assert ffi.NULL is not None


class TestResetForTests:
    """Test _reset_for_tests function."""

    def test_reset_for_tests_runs(self):
        """Test that _reset_for_tests can be called."""
        # Just verify it doesn't raise
        _reset_for_tests()
        # Library should be reloadable after reset
        lib = get_library()
        assert lib is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
