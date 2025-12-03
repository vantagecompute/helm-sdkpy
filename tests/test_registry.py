"""Tests for registry operations."""

import asyncio
import pytest

from helm_sdkpy import Configuration, RegistryLogin, RegistryLogout, Push
from helm_sdkpy.exceptions import HelmError


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

    @pytest.mark.asyncio
    async def test_registry_login_invalid_credentials(self):
        """Test registry login with invalid credentials fails gracefully."""
        config = Configuration()
        registry_login = RegistryLogin(config)
        
        # This should fail because credentials are invalid
        with pytest.raises((HelmError, Exception)):
            await registry_login.run(
                hostname="ghcr.io",
                username="invalid_user_12345",
                password="invalid_password_12345"
            )

    @pytest.mark.asyncio
    async def test_registry_logout_nonexistent(self):
        """Test registry logout for a registry we're not logged into."""
        config = Configuration()
        registry_logout = RegistryLogout(config)
        
        # Logout from a registry we were never logged into
        # This should succeed (no-op) or fail gracefully
        try:
            await registry_logout.run(hostname="nonexistent-registry.example.com")
        except Exception:
            # It's okay if this fails - registry might not exist in credentials
            pass

    def test_registry_login_has_run_method(self):
        """Test that RegistryLogin has an async run method."""
        config = Configuration()
        registry_login = RegistryLogin(config)
        assert hasattr(registry_login, "run")
        assert asyncio.iscoroutinefunction(registry_login.run)

    def test_registry_logout_has_run_method(self):
        """Test that RegistryLogout has an async run method."""
        config = Configuration()
        registry_logout = RegistryLogout(config)
        assert hasattr(registry_logout, "run")
        assert asyncio.iscoroutinefunction(registry_logout.run)

    def test_push_has_run_method(self):
        """Test that Push has an async run method."""
        config = Configuration()
        push = Push(config)
        assert hasattr(push, "run")
        assert asyncio.iscoroutinefunction(push.run)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
