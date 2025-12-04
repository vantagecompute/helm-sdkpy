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

"""Tests for Helm action classes."""

import inspect

import pytest

from helm_sdkpy import (
    Configuration,
    GetValues,
    History,
    Install,
    List,
    Rollback,
    Status,
    Uninstall,
    Upgrade,
)


class TestConfiguration:
    """Test Configuration class."""

    def test_configuration_import(self):
        """Test that Configuration can be imported."""
        assert Configuration is not None

    def test_configuration_default_instantiation(self):
        """Test Configuration with default parameters."""
        config = Configuration()
        assert config is not None
        assert hasattr(config, "_handle_value")

    def test_configuration_with_namespace(self):
        """Test Configuration with custom namespace."""
        config = Configuration(namespace="test-namespace")
        assert config is not None

    def test_configuration_with_kubeconfig(self):
        """Test Configuration with kubeconfig path."""
        # Using a non-existent path is fine for instantiation test
        config = Configuration(kubeconfig="/tmp/nonexistent-kubeconfig")
        assert config is not None

    def test_configuration_with_kubecontext(self):
        """Test Configuration with kubecontext."""
        config = Configuration(kubecontext="my-context")
        assert config is not None

    def test_configuration_with_all_params(self):
        """Test Configuration with all parameters."""
        config = Configuration(
            namespace="test-ns",
            kubeconfig="/tmp/kubeconfig",
            kubecontext="test-context",
        )
        assert config is not None

    def test_configuration_context_manager(self):
        """Test Configuration as context manager."""
        with Configuration() as config:
            assert config is not None
            assert hasattr(config, "_handle_value")

    def test_configuration_has_handle(self):
        """Test that Configuration creates a valid handle."""
        config = Configuration()
        assert hasattr(config, "_handle_value")
        assert config._handle_value is not None


class TestInstall:
    """Test Install class."""

    def test_install_import(self):
        """Test that Install can be imported."""
        assert Install is not None

    def test_install_instantiation(self):
        """Test Install instantiation."""
        config = Configuration()
        install = Install(config)
        assert install is not None
        assert install.config == config

    def test_install_has_run_method(self):
        """Test that Install has an async run method."""
        config = Configuration()
        install = Install(config)
        assert hasattr(install, "run")
        assert inspect.iscoroutinefunction(install.run)

    def test_install_run_signature(self):
        """Test Install.run() method signature."""
        sig = inspect.signature(Install.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params
        assert "chart_path" in params
        assert "values" in params
        assert "version" in params
        assert "create_namespace" in params
        assert "wait" in params
        assert "timeout" in params


class TestUpgrade:
    """Test Upgrade class."""

    def test_upgrade_import(self):
        """Test that Upgrade can be imported."""
        assert Upgrade is not None

    def test_upgrade_instantiation(self):
        """Test Upgrade instantiation."""
        config = Configuration()
        upgrade = Upgrade(config)
        assert upgrade is not None
        assert upgrade.config == config

    def test_upgrade_has_run_method(self):
        """Test that Upgrade has an async run method."""
        config = Configuration()
        upgrade = Upgrade(config)
        assert hasattr(upgrade, "run")
        assert inspect.iscoroutinefunction(upgrade.run)

    def test_upgrade_run_signature(self):
        """Test Upgrade.run() method signature."""
        sig = inspect.signature(Upgrade.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params
        assert "chart_path" in params
        assert "values" in params
        assert "version" in params


class TestUninstall:
    """Test Uninstall class."""

    def test_uninstall_import(self):
        """Test that Uninstall can be imported."""
        assert Uninstall is not None

    def test_uninstall_instantiation(self):
        """Test Uninstall instantiation."""
        config = Configuration()
        uninstall = Uninstall(config)
        assert uninstall is not None
        assert uninstall.config == config

    def test_uninstall_has_run_method(self):
        """Test that Uninstall has an async run method."""
        config = Configuration()
        uninstall = Uninstall(config)
        assert hasattr(uninstall, "run")
        assert inspect.iscoroutinefunction(uninstall.run)

    def test_uninstall_run_signature(self):
        """Test Uninstall.run() method signature."""
        sig = inspect.signature(Uninstall.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params
        assert "wait" in params
        assert "timeout" in params


class TestList:
    """Test List class."""

    def test_list_import(self):
        """Test that List can be imported."""
        assert List is not None

    def test_list_instantiation(self):
        """Test List instantiation."""
        config = Configuration()
        list_action = List(config)
        assert list_action is not None
        assert list_action.config == config

    def test_list_has_run_method(self):
        """Test that List has an async run method."""
        config = Configuration()
        list_action = List(config)
        assert hasattr(list_action, "run")
        assert inspect.iscoroutinefunction(list_action.run)

    def test_list_run_signature(self):
        """Test List.run() method signature."""
        sig = inspect.signature(List.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "all" in params


class TestStatus:
    """Test Status class."""

    def test_status_import(self):
        """Test that Status can be imported."""
        assert Status is not None

    def test_status_instantiation(self):
        """Test Status instantiation."""
        config = Configuration()
        status = Status(config)
        assert status is not None
        assert status.config == config

    def test_status_has_run_method(self):
        """Test that Status has an async run method."""
        config = Configuration()
        status = Status(config)
        assert hasattr(status, "run")
        assert inspect.iscoroutinefunction(status.run)

    def test_status_run_signature(self):
        """Test Status.run() method signature."""
        sig = inspect.signature(Status.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params


class TestRollback:
    """Test Rollback class."""

    def test_rollback_import(self):
        """Test that Rollback can be imported."""
        assert Rollback is not None

    def test_rollback_instantiation(self):
        """Test Rollback instantiation."""
        config = Configuration()
        rollback = Rollback(config)
        assert rollback is not None
        assert rollback.config == config

    def test_rollback_has_run_method(self):
        """Test that Rollback has an async run method."""
        config = Configuration()
        rollback = Rollback(config)
        assert hasattr(rollback, "run")
        assert inspect.iscoroutinefunction(rollback.run)

    def test_rollback_run_signature(self):
        """Test Rollback.run() method signature."""
        sig = inspect.signature(Rollback.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params
        assert "revision" in params


class TestGetValues:
    """Test GetValues class."""

    def test_getvalues_import(self):
        """Test that GetValues can be imported."""
        assert GetValues is not None

    def test_getvalues_instantiation(self):
        """Test GetValues instantiation."""
        config = Configuration()
        get_values = GetValues(config)
        assert get_values is not None
        assert get_values.config == config

    def test_getvalues_has_run_method(self):
        """Test that GetValues has an async run method."""
        config = Configuration()
        get_values = GetValues(config)
        assert hasattr(get_values, "run")
        assert inspect.iscoroutinefunction(get_values.run)

    def test_getvalues_run_signature(self):
        """Test GetValues.run() method signature."""
        sig = inspect.signature(GetValues.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params
        assert "all" in params


class TestHistory:
    """Test History class."""

    def test_history_import(self):
        """Test that History can be imported."""
        assert History is not None

    def test_history_instantiation(self):
        """Test History instantiation."""
        config = Configuration()
        history = History(config)
        assert history is not None
        assert history.config == config

    def test_history_has_run_method(self):
        """Test that History has an async run method."""
        config = Configuration()
        history = History(config)
        assert hasattr(history, "run")
        assert inspect.iscoroutinefunction(history.run)

    def test_history_run_signature(self):
        """Test History.run() method signature."""
        sig = inspect.signature(History.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
