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

"""Tests for Helm chart classes."""

import inspect

import pytest

from helm_sdkpy import Configuration, Lint, Package, Pull, ReleaseTest, Show, Test


class TestPull:
    """Test Pull class."""

    def test_pull_import(self):
        """Test that Pull can be imported."""
        assert Pull is not None

    def test_pull_instantiation(self):
        """Test Pull instantiation."""
        config = Configuration()
        pull = Pull(config)
        assert pull is not None
        assert pull.config == config

    def test_pull_has_run_method(self):
        """Test that Pull has an async run method."""
        config = Configuration()
        pull = Pull(config)
        assert hasattr(pull, "run")
        assert inspect.iscoroutinefunction(pull.run)

    def test_pull_run_signature(self):
        """Test Pull.run() method signature includes version parameter."""
        sig = inspect.signature(Pull.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_ref" in params
        assert "dest_dir" in params
        assert "version" in params, "Pull.run() must have version parameter"

    def test_pull_run_version_default(self):
        """Test that Pull.run() version parameter has None as default."""
        sig = inspect.signature(Pull.run)
        version_param = sig.parameters.get("version")
        assert version_param is not None
        assert version_param.default is None


class TestShow:
    """Test Show class."""

    def test_show_import(self):
        """Test that Show can be imported."""
        assert Show is not None

    def test_show_instantiation(self):
        """Test Show instantiation."""
        config = Configuration()
        show = Show(config)
        assert show is not None
        assert show.config == config

    def test_show_has_chart_method(self):
        """Test that Show has an async chart method."""
        config = Configuration()
        show = Show(config)
        assert hasattr(show, "chart")
        assert inspect.iscoroutinefunction(show.chart)

    def test_show_has_values_method(self):
        """Test that Show has an async values method."""
        config = Configuration()
        show = Show(config)
        assert hasattr(show, "values")
        assert inspect.iscoroutinefunction(show.values)

    def test_show_chart_signature(self):
        """Test Show.chart() method signature."""
        sig = inspect.signature(Show.chart)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_path" in params

    def test_show_values_signature(self):
        """Test Show.values() method signature."""
        sig = inspect.signature(Show.values)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_path" in params


class TestReleaseTest:
    """Test ReleaseTest class (Helm test action)."""

    def test_releasetest_import(self):
        """Test that ReleaseTest can be imported."""
        assert ReleaseTest is not None

    def test_test_alias_import(self):
        """Test that Test alias works for backwards compatibility."""
        assert Test is not None
        assert Test is ReleaseTest

    def test_releasetest_instantiation(self):
        """Test ReleaseTest instantiation."""
        config = Configuration()
        test = ReleaseTest(config)
        assert test is not None
        assert test.config == config

    def test_releasetest_has_run_method(self):
        """Test that ReleaseTest has an async run method."""
        config = Configuration()
        test = ReleaseTest(config)
        assert hasattr(test, "run")
        assert inspect.iscoroutinefunction(test.run)

    def test_releasetest_run_signature(self):
        """Test ReleaseTest.run() method signature."""
        sig = inspect.signature(ReleaseTest.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "release_name" in params


class TestLint:
    """Test Lint class."""

    def test_lint_import(self):
        """Test that Lint can be imported."""
        assert Lint is not None

    def test_lint_instantiation(self):
        """Test Lint instantiation."""
        config = Configuration()
        lint = Lint(config)
        assert lint is not None
        assert lint.config == config

    def test_lint_has_run_method(self):
        """Test that Lint has an async run method."""
        config = Configuration()
        lint = Lint(config)
        assert hasattr(lint, "run")
        assert inspect.iscoroutinefunction(lint.run)

    def test_lint_run_signature(self):
        """Test Lint.run() method signature."""
        sig = inspect.signature(Lint.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_path" in params


class TestPackage:
    """Test Package class."""

    def test_package_import(self):
        """Test that Package can be imported."""
        assert Package is not None

    def test_package_instantiation(self):
        """Test Package instantiation."""
        config = Configuration()
        package = Package(config)
        assert package is not None
        assert package.config == config

    def test_package_has_run_method(self):
        """Test that Package has an async run method."""
        config = Configuration()
        package = Package(config)
        assert hasattr(package, "run")
        assert inspect.iscoroutinefunction(package.run)

    def test_package_run_signature(self):
        """Test Package.run() method signature."""
        sig = inspect.signature(Package.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_path" in params
        assert "dest_dir" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
