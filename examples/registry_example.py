#!/usr/bin/env python3
"""Example of using helm-sdkpy registry operations.

This example demonstrates:
1. Registry login
2. Registry logout
3. Chart push to OCI registry

Note: This is a demonstration. For actual use, you'll need:
- Valid registry credentials
- A packaged chart (.tgz file)
- Proper OCI registry URL
"""

import asyncio

from helm_sdkpy import Configuration, RegistryLogin, RegistryLogout, Push


async def registry_login_example():
    """Example: Login to an OCI registry."""
    config = Configuration()
    registry_login = RegistryLogin(config)
    
    print("Example: Registry Login")
    print("=" * 50)
    print("""
    # Login to GitHub Container Registry
    await registry_login.run(
        hostname="ghcr.io",
        username="your-github-username",
        password="your-github-token"
    )
    
    # Login with TLS configuration
    await registry_login.run(
        hostname="registry.example.com",
        username="user",
        password="pass",
        cert_file="/path/to/cert.pem",
        key_file="/path/to/key.pem",
        ca_file="/path/to/ca.pem"
    )
    
    # Login with insecure mode (skip TLS verification)
    await registry_login.run(
        hostname="localhost:5000",
        username="admin",
        password="admin",
        insecure=True
    )
    
    # Login with plain HTTP (for local testing)
    await registry_login.run(
        hostname="localhost:5000",
        username="admin",
        password="admin",
        plain_http=True
    )
    """)


async def registry_logout_example():
    """Example: Logout from an OCI registry."""
    config = Configuration()
    registry_logout = RegistryLogout(config)
    
    print("\n\nExample: Registry Logout")
    print("=" * 50)
    print("""
    # Logout from a registry
    await registry_logout.run(hostname="ghcr.io")
    
    # Logout from another registry
    await registry_logout.run(hostname="registry.example.com")
    """)


async def push_chart_example():
    """Example: Push a chart to an OCI registry."""
    config = Configuration()
    push = Push(config)
    
    print("\n\nExample: Push Chart to Registry")
    print("=" * 50)
    print("""
    # Push a packaged chart to GitHub Container Registry
    await push.run(
        chart_path="./mychart-1.0.0.tgz",
        remote="oci://ghcr.io/your-org/charts"
    )
    
    # Push with TLS configuration
    await push.run(
        chart_path="./mychart-1.0.0.tgz",
        remote="oci://registry.example.com/charts",
        cert_file="/path/to/cert.pem",
        key_file="/path/to/key.pem",
        ca_file="/path/to/ca.pem"
    )
    
    # Push with plain HTTP (for local registry)
    await push.run(
        chart_path="./mychart-1.0.0.tgz",
        remote="oci://localhost:5000/charts",
        plain_http=True
    )
    """)


async def complete_workflow_example():
    """Example: Complete workflow - login, push, logout."""
    print("\n\nExample: Complete Registry Workflow")
    print("=" * 50)
    print("""
    config = Configuration()
    
    # 1. Login to registry
    registry_login = RegistryLogin(config)
    await registry_login.run(
        hostname="ghcr.io",
        username="your-github-username",
        password="your-github-token"
    )
    print("✅ Logged in to ghcr.io")
    
    # 2. Push chart
    push = Push(config)
    await push.run(
        chart_path="./mychart-1.0.0.tgz",
        remote="oci://ghcr.io/your-org/charts"
    )
    print("✅ Chart pushed successfully")
    
    # 3. Logout
    registry_logout = RegistryLogout(config)
    await registry_logout.run(hostname="ghcr.io")
    print("✅ Logged out from ghcr.io")
    """)


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("helm-sdkpy Registry Operations Examples")
    print("=" * 60)
    
    await registry_login_example()
    await registry_logout_example()
    await push_chart_example()
    await complete_workflow_example()
    
    print("\n" + "=" * 60)
    print("All examples displayed!")
    print("=" * 60)
    print("\nNote: These are code examples. To run them with actual")
    print("credentials, replace the placeholder values and uncomment")
    print("the actual function calls.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
