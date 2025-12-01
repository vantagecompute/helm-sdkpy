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

"""Basic tests for helm-sdkpy package."""


import helm_sdkpy


def test_version():
    """Test that version is accessible."""
    assert helm_sdkpy.__version__ is not None
    assert isinstance(helm_sdkpy.__version__, str)


def test_imports():
    """Test that all main classes can be imported."""
    from helm_sdkpy import (
        Configuration,
        GetValues,
        History,
        Install,
        Lint,
        List,
        Package,
        Pull,
        RepoAdd,
        RepoList,
        RepoRemove,
        RepoUpdate,
        Rollback,
        Show,
        Status,
        Test,
        Uninstall,
        Upgrade,
    )

    assert Configuration is not None
    assert Install is not None
    assert Upgrade is not None
    assert Uninstall is not None
    assert List is not None
    assert Status is not None
    assert Rollback is not None
    assert GetValues is not None
    assert History is not None
    assert Pull is not None
    assert Show is not None
    assert Test is not None
    assert Lint is not None
    assert Package is not None
    assert RepoAdd is not None
    assert RepoRemove is not None
    assert RepoList is not None
    assert RepoUpdate is not None


def test_exceptions():
    """Test that exception classes are available."""
    from helm_sdkpy import (
        ChartError,
        ConfigurationError,
        HelmError,
        HelmLibraryNotFound,
        InstallError,
        ReleaseError,
        RollbackError,
        UninstallError,
        UpgradeError,
    )

    assert issubclass(HelmLibraryNotFound, HelmError)
    assert issubclass(ConfigurationError, HelmError)
    assert issubclass(InstallError, HelmError)
    assert issubclass(UpgradeError, HelmError)
    assert issubclass(UninstallError, HelmError)
    assert issubclass(RollbackError, HelmError)
    assert issubclass(ChartError, HelmError)
    assert issubclass(ReleaseError, HelmError)
