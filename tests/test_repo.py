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

"""Tests for Helm repository classes."""

import inspect

import pytest

from helm_sdkpy import Configuration, RepoAdd, RepoList, RepoRemove, RepoUpdate


class TestRepoAdd:
    """Test RepoAdd class."""

    def test_repoadd_import(self):
        """Test that RepoAdd can be imported."""
        assert RepoAdd is not None

    def test_repoadd_instantiation(self):
        """Test RepoAdd instantiation."""
        config = Configuration()
        repo_add = RepoAdd(config)
        assert repo_add is not None
        assert repo_add.config == config

    def test_repoadd_has_run_method(self):
        """Test that RepoAdd has an async run method."""
        config = Configuration()
        repo_add = RepoAdd(config)
        assert hasattr(repo_add, "run")
        assert inspect.iscoroutinefunction(repo_add.run)

    def test_repoadd_run_signature(self):
        """Test RepoAdd.run() method signature."""
        sig = inspect.signature(RepoAdd.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "name" in params
        assert "url" in params
        assert "username" in params
        assert "password" in params
        assert "insecure_skip_tls_verify" in params
        assert "pass_credentials_all" in params
        assert "cert_file" in params
        assert "key_file" in params
        assert "ca_file" in params


class TestRepoRemove:
    """Test RepoRemove class."""

    def test_reporemove_import(self):
        """Test that RepoRemove can be imported."""
        assert RepoRemove is not None

    def test_reporemove_instantiation(self):
        """Test RepoRemove instantiation."""
        config = Configuration()
        repo_remove = RepoRemove(config)
        assert repo_remove is not None
        assert repo_remove.config == config

    def test_reporemove_has_run_method(self):
        """Test that RepoRemove has an async run method."""
        config = Configuration()
        repo_remove = RepoRemove(config)
        assert hasattr(repo_remove, "run")
        assert inspect.iscoroutinefunction(repo_remove.run)

    def test_reporemove_run_signature(self):
        """Test RepoRemove.run() method signature."""
        sig = inspect.signature(RepoRemove.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "name" in params


class TestRepoList:
    """Test RepoList class."""

    def test_repolist_import(self):
        """Test that RepoList can be imported."""
        assert RepoList is not None

    def test_repolist_instantiation(self):
        """Test RepoList instantiation."""
        config = Configuration()
        repo_list = RepoList(config)
        assert repo_list is not None
        assert repo_list.config == config

    def test_repolist_has_run_method(self):
        """Test that RepoList has an async run method."""
        config = Configuration()
        repo_list = RepoList(config)
        assert hasattr(repo_list, "run")
        assert inspect.iscoroutinefunction(repo_list.run)

    def test_repolist_run_signature(self):
        """Test RepoList.run() method signature."""
        sig = inspect.signature(RepoList.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        # RepoList.run() takes no arguments besides self


class TestRepoUpdate:
    """Test RepoUpdate class."""

    def test_repoupdate_import(self):
        """Test that RepoUpdate can be imported."""
        assert RepoUpdate is not None

    def test_repoupdate_instantiation(self):
        """Test RepoUpdate instantiation."""
        config = Configuration()
        repo_update = RepoUpdate(config)
        assert repo_update is not None
        assert repo_update.config == config

    def test_repoupdate_has_run_method(self):
        """Test that RepoUpdate has an async run method."""
        config = Configuration()
        repo_update = RepoUpdate(config)
        assert hasattr(repo_update, "run")
        assert inspect.iscoroutinefunction(repo_update.run)

    def test_repoupdate_run_signature(self):
        """Test RepoUpdate.run() method signature."""
        sig = inspect.signature(RepoUpdate.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "name" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
