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

"""Core Helm configuration and action classes."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ._ffi import check_error, ffi, get_library, string_from_c
from .exceptions import (
    ChartError,
    ConfigurationError,
    InstallError,
    ReleaseError,
    RollbackError,
    UninstallError,
    UpgradeError,
)


class Configuration:
    """Helm configuration for interacting with Kubernetes clusters.

    This class manages the connection to a Kubernetes cluster and provides
    the context for all Helm operations.

    Args:
        namespace: Kubernetes namespace to operate in (default: "default")
        kubeconfig: Path to kubeconfig file (default: uses $KUBECONFIG or ~/.kube/config)
        kubecontext: Kubernetes context to use (default: current context)

    Example:
        >>> config = Configuration(namespace="my-namespace")
        >>> install = Install(config)
        >>> result = install.run("my-release", "/path/to/chart")
    """

    def __init__(
        self,
        namespace: str = "default",
        kubeconfig: Optional[str] = None,
        kubecontext: Optional[str] = None,
    ):
        self._lib = get_library()
        self._handle = ffi.new("helmpy_handle *")

        ns_cstr = ffi.new("char[]", namespace.encode("utf-8"))
        kc_cstr = ffi.new("char[]", kubeconfig.encode("utf-8")) if kubeconfig else ffi.NULL
        kctx_cstr = ffi.new("char[]", kubecontext.encode("utf-8")) if kubecontext else ffi.NULL

        result = self._lib.helmpy_config_create(ns_cstr, kc_cstr, kctx_cstr, self._handle)
        check_error(result)

        self._handle_value = self._handle[0]

    def __del__(self):
        """Clean up the configuration handle."""
        if hasattr(self, "_lib") and hasattr(self, "_handle_value"):
            self._lib.helmpy_config_destroy(self._handle_value)

    def __enter__(self):
        """Support for context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager."""
        self.__del__()
        return False


class Install:
    """Helm install action.

    Installs a chart into a Kubernetes cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> install = Install(config)
        >>> result = install.run("my-release", "./mychart", values={"replicas": 3})
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(
        self,
        release_name: str,
        chart_path: str,
        values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Install a chart.

        Args:
            release_name: Name of the release
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
            values: Values to pass to the chart

        Returns:
            Dictionary containing release information

        Raises:
            InstallError: If installation fails
        """
        result_json = ffi.new("char **")

        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

        values_json = json.dumps(values) if values else ""
        values_cstr = ffi.new("char[]", values_json.encode("utf-8"))

        result = self._lib.helmpy_install(
            self.config._handle_value, name_cstr, path_cstr, values_cstr, result_json
        )

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise InstallError(f"Failed to parse install result: {e}") from e


class Upgrade:
    """Helm upgrade action.

    Upgrades an existing release.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> upgrade = Upgrade(config)
        >>> result = upgrade.run("my-release", "./mychart", values={"replicas": 5})
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(
        self,
        release_name: str,
        chart_path: str,
        values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Upgrade a release.

        Args:
            release_name: Name of the release
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
            values: Values to pass to the chart

        Returns:
            Dictionary containing release information

        Raises:
            UpgradeError: If upgrade fails
        """
        result_json = ffi.new("char **")

        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
        path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

        values_json = json.dumps(values) if values else ""
        values_cstr = ffi.new("char[]", values_json.encode("utf-8"))

        result = self._lib.helmpy_upgrade(
            self.config._handle_value, name_cstr, path_cstr, values_cstr, result_json
        )

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise UpgradeError(f"Failed to parse upgrade result: {e}") from e


class Uninstall:
    """Helm uninstall action.

    Uninstalls a release from the cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> uninstall = Uninstall(config)
        >>> result = uninstall.run("my-release")
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str) -> Dict[str, Any]:
        """Uninstall a release.

        Args:
            release_name: Name of the release

        Returns:
            Dictionary containing uninstall response

        Raises:
            UninstallError: If uninstall fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

        result = self._lib.helmpy_uninstall(self.config._handle_value, name_cstr, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise UninstallError(f"Failed to parse uninstall result: {e}") from e


class List:
    """Helm list action.

    Lists releases in the cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> list_action = List(config)
        >>> releases = list_action.run(all=True)
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, all: bool = False) -> List[Dict[str, Any]]:
        """List releases.

        Args:
            all: Show all releases, not just deployed ones

        Returns:
            List of release dictionaries

        Raises:
            ReleaseError: If listing fails
        """
        result_json = ffi.new("char **")
        all_flag = 1 if all else 0

        result = self._lib.helmpy_list(self.config._handle_value, all_flag, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ReleaseError(f"Failed to parse list result: {e}") from e


class Status:
    """Helm status action.

    Gets the status of a release.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> status = Status(config)
        >>> info = status.run("my-release")
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str) -> Dict[str, Any]:
        """Get release status.

        Args:
            release_name: Name of the release

        Returns:
            Dictionary containing release status

        Raises:
            ReleaseError: If status check fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

        result = self._lib.helmpy_status(self.config._handle_value, name_cstr, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ReleaseError(f"Failed to parse status result: {e}") from e


class Rollback:
    """Helm rollback action.

    Rolls back a release to a previous revision.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> rollback = Rollback(config)
        >>> result = rollback.run("my-release", revision=2)
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str, revision: int = 0) -> Dict[str, Any]:
        """Rollback a release.

        Args:
            release_name: Name of the release
            revision: Revision to rollback to (0 = previous)

        Returns:
            Dictionary containing rollback result

        Raises:
            RollbackError: If rollback fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

        result = self._lib.helmpy_rollback(
            self.config._handle_value, name_cstr, revision, result_json
        )

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise RollbackError(f"Failed to parse rollback result: {e}") from e


class GetValues:
    """Helm get values action.

    Gets the values for a release.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> get_values = GetValues(config)
        >>> values = get_values.run("my-release", all=True)
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str, all: bool = False) -> Dict[str, Any]:
        """Get release values.

        Args:
            release_name: Name of the release
            all: Get all values, including computed values

        Returns:
            Dictionary containing values

        Raises:
            ReleaseError: If getting values fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
        all_flag = 1 if all else 0

        result = self._lib.helmpy_get_values(
            self.config._handle_value, name_cstr, all_flag, result_json
        )

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ReleaseError(f"Failed to parse get values result: {e}") from e


class History:
    """Helm history action.

    Gets the release history.

    Args:
        config: Helm configuration object

    Example:
        >>> config = Configuration()
        >>> history = History(config)
        >>> revisions = history.run("my-release")
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    def run(self, release_name: str) -> List[Dict[str, Any]]:
        """Get release history.

        Args:
            release_name: Name of the release

        Returns:
            List of revision dictionaries

        Raises:
            ReleaseError: If getting history fails
        """
        result_json = ffi.new("char **")
        name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

        result = self._lib.helmpy_history(self.config._handle_value, name_cstr, result_json)

        if result != 0:
            check_error(result)

        json_str = string_from_c(result_json[0])
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ReleaseError(f"Failed to parse history result: {e}") from e
