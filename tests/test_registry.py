"""Tests for registry operations."""

import inspect

import pytest

from helm_sdkpy import Configuration, Push, RegistryLogin, RegistryLogout


class TestRegistryOperations:
    """Test registry login, logout, and push operations."""

    def test_registry_login_import(self):
        """Test that RegistryLogin can be imported."""
        assert RegistryLogin is not None

    def test_registry_logout_import(self):
        """Test that RegistryLogout can be imported."""
        assert RegistryLogout is not None

    def test_push_import(self):
        """Test that Push can be imported."""
        assert Push is not None

    def test_registry_login_instantiation(self):
        """Test that RegistryLogin can be instantiated."""
        config = Configuration()
        registry_login = RegistryLogin(config)
        assert registry_login is not None
        assert registry_login.config == config

    def test_registry_logout_instantiation(self):
        """Test that RegistryLogout can be instantiated."""
        config = Configuration()
        registry_logout = RegistryLogout(config)
        assert registry_logout is not None
        assert registry_logout.config == config

    def test_push_instantiation(self):
        """Test that Push can be instantiated."""
        config = Configuration()
        push = Push(config)
        assert push is not None
        assert push.config == config

    def test_registry_login_has_run_method(self):
        """Test that RegistryLogin has an async run method."""
        config = Configuration()
        registry_login = RegistryLogin(config)
        assert hasattr(registry_login, "run")
        assert inspect.iscoroutinefunction(registry_login.run)

    def test_registry_logout_has_run_method(self):
        """Test that RegistryLogout has an async run method."""
        config = Configuration()
        registry_logout = RegistryLogout(config)
        assert hasattr(registry_logout, "run")
        assert inspect.iscoroutinefunction(registry_logout.run)

    def test_push_has_run_method(self):
        """Test that Push has an async run method."""
        config = Configuration()
        push = Push(config)
        assert hasattr(push, "run")
        assert inspect.iscoroutinefunction(push.run)

    def test_registry_login_run_signature(self):
        """Test RegistryLogin.run() method signature."""
        sig = inspect.signature(RegistryLogin.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "hostname" in params
        assert "username" in params
        assert "password" in params
        assert "cert_file" in params
        assert "key_file" in params
        assert "ca_file" in params
        assert "insecure" in params
        assert "plain_http" in params

    def test_registry_logout_run_signature(self):
        """Test RegistryLogout.run() method signature."""
        sig = inspect.signature(RegistryLogout.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "hostname" in params

    def test_push_run_signature(self):
        """Test Push.run() method signature."""
        sig = inspect.signature(Push.run)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "chart_path" in params
        assert "remote" in params
        assert "cert_file" in params
        assert "key_file" in params
        assert "ca_file" in params
        assert "insecure_skip_tls_verify" in params
        assert "plain_http" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
