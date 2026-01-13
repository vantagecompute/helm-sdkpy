#!/usr/bin/env python3
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

"""
Kubeconfig Usage Example

This example demonstrates different ways to configure kubeconfig in helm-sdkpy:
1. Using the default kubeconfig (~/.kube/config or $KUBECONFIG)
2. Using an explicit file path
3. Using a kubeconfig YAML string directly

The kubeconfig string approach is particularly useful when:
- Working with dynamic or programmatically generated configurations
- Retrieving kubeconfig from Kubernetes secrets, environment variables, or APIs
- Working in containerized environments where file access may be limited
"""

import asyncio
import os
from pathlib import Path

import helm_sdkpy


async def example_default_kubeconfig():
    """Example 1: Use default kubeconfig location.
    
    This uses $KUBECONFIG environment variable if set,
    otherwise falls back to ~/.kube/config.
    """
    print("=" * 60)
    print("Example 1: Default Kubeconfig")
    print("=" * 60)
    
    # When kubeconfig is None, uses default locations
    config = helm_sdkpy.Configuration(
        namespace="default",
        # kubeconfig=None uses default: $KUBECONFIG or ~/.kube/config
    )
    
    # List releases to verify connection
    list_action = helm_sdkpy.List(config)
    releases = await list_action.run()
    print(f"Found {len(releases)} releases in default namespace")
    
    return config


async def example_kubeconfig_filepath():
    """Example 2: Use explicit kubeconfig file path.
    
    Useful when you have multiple kubeconfig files for different clusters.
    """
    print("\n" + "=" * 60)
    print("Example 2: Kubeconfig from File Path")
    print("=" * 60)
    
    # Specify an explicit path to a kubeconfig file
    kubeconfig_path = os.path.expanduser("~/.kube/config")
    
    # Or use a different file for a specific cluster
    # kubeconfig_path = "/path/to/production-cluster.yaml"
    # kubeconfig_path = "/etc/rancher/k3s/k3s.yaml"
    
    config = helm_sdkpy.Configuration(
        namespace="kube-system",
        kubeconfig=kubeconfig_path,
    )
    
    # List releases in kube-system namespace
    list_action = helm_sdkpy.List(config)
    releases = await list_action.run()
    print(f"Found {len(releases)} releases in kube-system namespace")
    
    return config


async def example_kubeconfig_string():
    """Example 3: Use kubeconfig YAML content as a string.
    
    This is useful when:
    - Retrieving kubeconfig from environment variables
    - Loading from Kubernetes secrets
    - Programmatically generating configurations
    - Working in serverless or containerized environments
    """
    print("\n" + "=" * 60)
    print("Example 3: Kubeconfig from String")
    print("=" * 60)
    
    # Example: Read kubeconfig content from a file into a string
    # In practice, this could come from an environment variable,
    # API response, Kubernetes secret, etc.
    
    kubeconfig_path = os.path.expanduser("~/.kube/config")
    if Path(kubeconfig_path).exists():
        with open(kubeconfig_path, "r") as f:
            kubeconfig_content = f.read()
    else:
        # Example kubeconfig YAML structure (won't work without real cluster)
        kubeconfig_content = """
apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://kubernetes.example.com:6443
    certificate-authority-data: <base64-encoded-ca-cert>
  name: my-cluster
contexts:
- context:
    cluster: my-cluster
    user: my-user
    namespace: default
  name: my-context
current-context: my-context
users:
- name: my-user
  user:
    token: <your-token-here>
"""
    
    # Pass the YAML content directly as the kubeconfig parameter
    # helm-sdkpy automatically detects if it's a file path or YAML content
    config = helm_sdkpy.Configuration(
        namespace="default",
        kubeconfig=kubeconfig_content,  # YAML string, not a file path!
    )
    
    # List releases to verify connection
    list_action = helm_sdkpy.List(config)
    releases = await list_action.run()
    print(f"Found {len(releases)} releases using kubeconfig string")
    
    return config


async def example_kubeconfig_from_env():
    """Example 4: Load kubeconfig from environment variable.
    
    Many CI/CD systems and container orchestrators provide kubeconfig
    as an environment variable.
    """
    print("\n" + "=" * 60)
    print("Example 4: Kubeconfig from Environment Variable")
    print("=" * 60)
    
    # Common patterns for kubeconfig in environment variables:
    # - KUBECONFIG_CONTENT: Full YAML content
    # - KUBECONFIG_BASE64: Base64-encoded YAML content
    
    import base64
    
    kubeconfig_content = None
    
    # Try getting YAML content directly
    if "KUBECONFIG_CONTENT" in os.environ:
        kubeconfig_content = os.environ["KUBECONFIG_CONTENT"]
        print("Loaded kubeconfig from KUBECONFIG_CONTENT env var")
    
    # Try getting base64-encoded content (common in CI/CD)
    elif "KUBECONFIG_BASE64" in os.environ:
        kubeconfig_content = base64.b64decode(
            os.environ["KUBECONFIG_BASE64"]
        ).decode("utf-8")
        print("Loaded kubeconfig from KUBECONFIG_BASE64 env var")
    
    # Fall back to file path from KUBECONFIG env var
    elif "KUBECONFIG" in os.environ:
        kubeconfig_path = os.environ["KUBECONFIG"]
        print(f"Using kubeconfig file from KUBECONFIG env var: {kubeconfig_path}")
        config = helm_sdkpy.Configuration(
            namespace="default",
            kubeconfig=kubeconfig_path,
        )
        list_action = helm_sdkpy.List(config)
        releases = await list_action.run()
        print(f"Found {len(releases)} releases")
        return config
    
    else:
        print("No kubeconfig environment variable found")
        print("Set KUBECONFIG_CONTENT, KUBECONFIG_BASE64, or KUBECONFIG")
        return None
    
    # Use the content string directly
    config = helm_sdkpy.Configuration(
        namespace="default",
        kubeconfig=kubeconfig_content,
    )
    
    list_action = helm_sdkpy.List(config)
    releases = await list_action.run()
    print(f"Found {len(releases)} releases")
    
    return config


async def example_kubeconfig_with_context():
    """Example 5: Use kubeconfig with specific context.
    
    When your kubeconfig has multiple contexts (clusters), you can
    specify which one to use.
    """
    print("\n" + "=" * 60)
    print("Example 5: Kubeconfig with Specific Context")
    print("=" * 60)
    
    kubeconfig_path = os.path.expanduser("~/.kube/config")
    
    # Specify both the kubeconfig file and the context to use
    config = helm_sdkpy.Configuration(
        namespace="default",
        kubeconfig=kubeconfig_path,
        kubecontext="my-cluster-context",  # Use a specific context
    )
    
    print(f"Using kubeconfig: {kubeconfig_path}")
    print(f"Using context: my-cluster-context")
    
    # This would fail if the context doesn't exist
    # list_action = helm_sdkpy.List(config)
    # releases = await list_action.run()
    
    return config


async def main():
    """Run all kubeconfig usage examples."""
    print("helm-sdkpy Kubeconfig Usage Examples")
    print("=" * 60)
    print(f"helm-sdkpy version: {helm_sdkpy.__version__}")
    
    try:
        print(f"Library version: {helm_sdkpy.get_version()}")
    except helm_sdkpy.HelmLibraryNotFound:
        print("\nLibrary not found - please build the library first with 'just build-lib'")
        return
    
    # Run examples that work with available kubeconfig
    try:
        await example_default_kubeconfig()
    except Exception as e:
        print(f"Example 1 failed (expected if no cluster): {e}")
    
    try:
        await example_kubeconfig_filepath()
    except Exception as e:
        print(f"Example 2 failed (expected if no cluster): {e}")
    
    try:
        await example_kubeconfig_string()
    except Exception as e:
        print(f"Example 3 failed (expected if no cluster): {e}")
    
    try:
        await example_kubeconfig_from_env()
    except Exception as e:
        print(f"Example 4 failed (expected if no env vars set): {e}")
    
    print("\n" + "=" * 60)
    print("Summary: Kubeconfig Configuration Options")
    print("=" * 60)
    print("""
Configuration(namespace, kubeconfig, kubecontext) parameters:

1. kubeconfig=None (default)
   - Uses $KUBECONFIG environment variable if set
   - Falls back to ~/.kube/config

2. kubeconfig="/path/to/config.yaml"
   - Uses explicit file path to kubeconfig

3. kubeconfig="apiVersion: v1\\nkind: Config\\n..."
   - YAML content passed directly as a string
   - Auto-detected by looking for apiVersion:, kind:, or clusters: markers
   - Useful for dynamic configurations, secrets, or environment variables

4. kubecontext="my-context"
   - Select a specific context from the kubeconfig
   - Works with both file paths and string content
""")


if __name__ == "__main__":
    asyncio.run(main())
