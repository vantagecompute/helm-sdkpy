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

"""Chart-related Helm operations."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from ._ffi import check_error, ffi, get_library, string_from_c
from .exceptions import ChartError


class Pull:
    """Helm pull action.

    Downloads a chart from a repository.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> pull = Pull(config)
        >>> pull.run("stable/nginx", dest_dir="./charts")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    def run(self, chart_ref: str, dest_dir: Optional[str] = None) -> None:
        """Pull a chart.

        Args:
            chart_ref: Chart reference (e.g., "repo/chart" or "oci://...")
            dest_dir: Destination directory (default: current directory)

        Raises:
            ChartError: If pull fails
        """
        ref_cstr = ffi.new("char[]", chart_ref.encode("utf-8"))
        dest_cstr = ffi.new("char[]", dest_dir.encode("utf-8")) if dest_dir else ffi.NULL

        result = self._lib.helmpy_pull(self.config._handle_value, ref_cstr, dest_cstr)

        if result != 0:
            check_error(result)


class Show:
    """Helm show actions.

    Shows information about a chart.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> show = Show(config)
        >>> chart_yaml = show.chart("./mychart")
        >>> values_yaml = show.values("./mychart")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    def chart(self, chart_path: str) -> str:
        """Show the chart's Chart.yaml content.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            Chart.yaml content as string

        Raises:
            ChartError: If show fails
        """
        result_json = ffi.new("char **")
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

        result = self._lib.helmpy_show_chart(self.config._handle_value, path_cstr, result_json)

        if result != 0:
            check_error(result)

        return string_from_c(result_json[0])

    def values(self, chart_path: str) -> str:
        """Show the chart's values.yaml content.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            values.yaml content as string

        Raises:
            ChartError: If show fails
        """
        result_json = ffi.new("char **")
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

        result = self._lib.helmpy_show_values(self.config._handle_value, path_cstr, result_json)

        if result != 0:
            check_error(result)

        return string_from_c(result_json[0])


class Test:
    """Helm test action.

    Runs tests for a release.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> test = Test(config)
        >>> result = test.run("my-release")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str) -> Dict[str, Any]:
        """Run tests for a release.

        Args:
            release_name: Name of the release

        Returns:
            Dictionary containing test results

        Raises:
            ChartError: If test fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

        result = self._lib.helmpy_test(self.config._handle_value, name_cstr, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ChartError(f"Failed to parse test result: {e}") from e


class Lint:
    """Helm lint action.

    Lints a chart for errors.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> lint = Lint(config)
        >>> result = lint.run("./mychart")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    def run(self, chart_path: str) -> Dict[str, Any]:
        """Lint a chart.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            Dictionary containing lint results

        Raises:
            ChartError: If lint operation fails
        """
        result_json = ffi.new("char **")
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

        result = self._lib.helmpy_lint(self.config._handle_value, path_cstr, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ChartError(f"Failed to parse lint result: {e}") from e


class Package:
    """Helm package action.

    Packages a chart into a versioned archive.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> package = Package(config)
        >>> archive_path = package.run("./mychart", dest_dir="./dist")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    def run(self, chart_path: str, dest_dir: Optional[str] = None) -> str:
        """Package a chart.

        Args:
            chart_path: Path to the chart directory to package
            dest_dir: Destination directory (default: current directory)

        Returns:
            Path to the packaged chart archive

        Raises:
            ChartError: If package fails
        """
        result_path = ffi.new("char **")
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))
        dest_cstr = ffi.new("char[]", dest_dir.encode("utf-8")) if dest_dir else ffi.NULL

        result = self._lib.helmpy_package(
            self.config._handle_value, path_cstr, dest_cstr, result_path
        )

        if result != 0:
            check_error(result)

        return string_from_c(result_path[0])
