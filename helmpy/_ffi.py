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

from __future__ import annotations

import os
import platform
import threading
from pathlib import Path
from typing import Any

from cffi import FFI  # type: ignore[import]

from .exceptions import HelmError, HelmLibraryNotFound

ffi: Any = FFI()
ffi.cdef(
    """
    typedef unsigned long long helmpy_handle;

    // Configuration management
    int helmpy_config_create(const char *namespace, const char *kubeconfig, const char *kubecontext, helmpy_handle *handle_out);
    void helmpy_config_destroy(helmpy_handle handle);

    // Install action
    int helmpy_install(helmpy_handle handle, const char *release_name, const char *chart_path, const char *values_json, const char *version, int create_namespace, int wait, int timeout_seconds, char **result_json);

    // Upgrade action
    int helmpy_upgrade(helmpy_handle handle, const char *release_name, const char *chart_path, const char *values_json, const char *version, char **result_json);

    // Uninstall action
    int helmpy_uninstall(helmpy_handle handle, const char *release_name, int wait, int timeout_seconds, char **result_json);

    // List action
    int helmpy_list(helmpy_handle handle, int all, char **result_json);

    // Status action
    int helmpy_status(helmpy_handle handle, const char *release_name, char **result_json);

    // Rollback action
    int helmpy_rollback(helmpy_handle handle, const char *release_name, int revision, char **result_json);

    // Get values action
    int helmpy_get_values(helmpy_handle handle, const char *release_name, int all_values, char **result_json);

    // History action
    int helmpy_history(helmpy_handle handle, const char *release_name, char **result_json);

    // Pull action
    int helmpy_pull(helmpy_handle handle, const char *chart_ref, const char *dest_dir);

    // Show chart action
    int helmpy_show_chart(helmpy_handle handle, const char *chart_path, char **result_json);

    // Show values action
    int helmpy_show_values(helmpy_handle handle, const char *chart_path, char **result_json);

    // Test action
    int helmpy_test(helmpy_handle handle, const char *release_name, char **result_json);

    // Lint action
    int helmpy_lint(helmpy_handle handle, const char *chart_path, char **result_json);

    // Package action
    int helmpy_package(helmpy_handle handle, const char *chart_path, const char *dest_dir, char **result_path);

    // Repository management actions
    int helmpy_repo_add(helmpy_handle handle, const char *name, const char *url, const char *username, const char *password, const char *options_json);
    int helmpy_repo_remove(helmpy_handle handle, const char *name);
    int helmpy_repo_list(helmpy_handle handle, char **result_json);
    int helmpy_repo_update(helmpy_handle handle, const char *name);

    // Utility functions
    const char *helmpy_last_error(void);
    void helmpy_free(void *ptr);
    int helmpy_version_number(void);
    const char *helmpy_version_string(void);
    """
)


__all__ = [
    "HelmError",
    "HelmLibraryNotFound",
    "configure",
    "ffi",
    "get_library",
    "get_version",
    "string_from_c",
    "_reset_for_tests",
]


_library_lock = threading.Lock()
_library = None
_library_path: str | None = None


def configure(path: str | None) -> None:
    """Force the bindings to load libhelmpy from ``path``.

    Passing ``None`` clears the override and re-enables auto-discovery.
    """

    global _library_path, _library
    with _library_lock:
        _library_path = path
        _library = None


def _find_library() -> str | None:
    """Find the helmpy shared library."""

    # Check for configured path first
    if _library_path is not None:
        return _library_path

    # Determine platform-specific library name and search paths
    system = platform.system()
    machine = platform.machine()

    # Normalize architecture names to match Go's convention
    if machine == "x86_64":
        machine = "amd64"
    elif machine == "aarch64":
        machine = "arm64"

    if system == "Linux":
        lib_name = "libhelmpy.so"
        platform_dir = f"linux-{machine}"
    elif system == "Darwin":
        lib_name = "libhelmpy.dylib"
        platform_dir = f"darwin-{machine}"
    elif system == "Windows":
        lib_name = "helmpy.dll"
        platform_dir = f"windows-{machine}"
    else:
        return None

    # Search in package directory first
    package_dir = Path(__file__).parent
    lib_dir = package_dir / "_lib" / platform_dir
    lib_path = lib_dir / lib_name

    if lib_path.exists():
        return str(lib_path)

    # Try just the platform directory
    lib_path = lib_dir / lib_name
    if lib_path.exists():
        return str(lib_path)

    # Try environment variable
    env_path = os.environ.get("HELMPY_LIBRARY_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    return None


def get_library():
    """Get the loaded Helm library, loading it if necessary."""
    global _library

    with _library_lock:
        if _library is not None:
            return _library

        lib_path = _find_library()
        if lib_path is None:
            raise HelmLibraryNotFound(
                "Could not find helmpy shared library. Please ensure helmpy is properly installed."
            )

        try:
            _library = ffi.dlopen(lib_path)
        except OSError as e:
            raise HelmLibraryNotFound(f"Failed to load helmpy library from {lib_path}: {e}") from e

        return _library


def get_version() -> str:
    """Get the version string from the native library."""
    lib = get_library()
    version_ptr = lib.helmpy_version_string()
    if version_ptr == ffi.NULL:
        return "unknown"
    return ffi.string(version_ptr).decode("utf-8")


def string_from_c(c_str) -> str:
    """Convert a C string to Python string and free it."""
    if c_str == ffi.NULL:
        return ""
    try:
        s = ffi.string(c_str).decode("utf-8")
        return s
    finally:
        lib = get_library()
        lib.helmpy_free(c_str)


def check_error(result: int) -> None:
    """Check if a C function returned an error and raise an exception if so."""
    if result != 0:
        lib = get_library()
        err_ptr = lib.helmpy_last_error()
        if err_ptr != ffi.NULL:
            err_msg = ffi.string(err_ptr).decode("utf-8")
            raise HelmError(err_msg)
        else:
            raise HelmError("Unknown error occurred")


def _reset_for_tests() -> None:
    """Reset library state for testing. Internal use only."""
    global _library, _library_path
    with _library_lock:
        _library = None
        _library_path = None
