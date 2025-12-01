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
Async Installation Example

This example demonstrates using helm-sdkpy with Python asyncio for non-blocking
Helm operations. This is useful for web applications, event loops, or when
managing multiple installations concurrently.
"""

import asyncio
import subprocess
import sys
import tempfile

import helm_sdkpy


async def install_chart_async(name: str, chart: str, namespace: str = "default"):
    """Install a chart asynchronously with wait strategy."""
    
    # Get kubeconfig from microk8s
    result = subprocess.run(['microk8s.config'], capture_output=True, text=True)
    kubeconfig_content = result.stdout
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(kubeconfig_content)
        kubeconfig_file = f.name
    
    print(f"[{name}] Creating configuration...")
    config = helm_sdkpy.Configuration(namespace=namespace, kubeconfig=kubeconfig_file)
    
    print(f"[{name}] Starting async installation...")
    print(f"[{name}] Chart: {chart}")
    print(f"[{name}] Namespace: {namespace}")
    print(f"[{name}] Wait enabled: will wait for resources to be ready")
    
    install = helm_sdkpy.Install(config)
    
    try:
        # Use async run for non-blocking operation with wait strategy
        result = await install.run(
            release_name=name,
            chart_path=chart,
            values={"replicaCount": 1},
            create_namespace=True,
            wait=True,  # Wait for resources to be ready
            timeout=300
        )
        
        print(f"[{name}] ✓ Installation complete!")
        print(f"[{name}]   Status: {result['info']['status']}")
        print(f"[{name}]   Version: {result['version']}")
        return result
        
    except helm_sdkpy.InstallError as e:
        print(f"[{name}] ✗ Installation failed: {e}")
        raise


async def uninstall_chart_async(name: str, namespace: str = "default"):
    """Uninstall a chart asynchronously with wait strategy."""
    
    # Get kubeconfig from microk8s
    result = subprocess.run(['microk8s.config'], capture_output=True, text=True)
    kubeconfig_content = result.stdout
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(kubeconfig_content)
        kubeconfig_file = f.name
    
    print(f"[{name}] Creating configuration...")
    config = helm_sdkpy.Configuration(namespace=namespace, kubeconfig=kubeconfig_file)
    
    print(f"[{name}] Starting async uninstall...")
    print(f"[{name}] Wait enabled: will wait for resources to be deleted")
    
    uninstall = helm_sdkpy.Uninstall(config)
    
    try:
        # Use async run for non-blocking operation with wait strategy
        result = await uninstall.run(
            release_name=name,
            wait=True,  # Wait for resources to be deleted
            timeout=300
        )
        
        print(f"[{name}] ✓ Uninstall complete!")
        return result
        
    except helm_sdkpy.UninstallError as e:
        print(f"[{name}] ✗ Uninstall failed: {e}")
        raise


async def install_multiple_charts():
    """Install multiple charts concurrently using asyncio."""
    
    print("="*70)
    print("  Installing Multiple Charts Concurrently")
    print("="*70)
    print()
    
    # Define charts to install
    charts = [
        ("nginx-1", "oci://registry-1.docker.io/bitnamicharts/nginx", "demo-1"),
        ("nginx-2", "oci://registry-1.docker.io/bitnamicharts/nginx", "demo-2"),
    ]
    
    # Install all charts concurrently
    tasks = [
        install_chart_async(name, chart, namespace)
        for name, chart, namespace in charts
    ]
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print("\n" + "="*70)
        print("  Installation Summary")
        print("="*70)
        
        for (name, chart, namespace), result in zip(charts, results):
            if isinstance(result, Exception):
                print(f"✗ {name}: Failed - {result}")
            else:
                print(f"✓ {name}: Success")
        
        return results
        
    except Exception as e:
        print(f"\nError during concurrent installation: {e}")
        raise


async def cleanup_charts():
    """Clean up installed charts."""
    
    print("\n" + "="*70)
    print("  Cleaning Up Charts")
    print("="*70)
    print()
    
    charts = [
        ("nginx-1", "demo-1"),
        ("nginx-2", "demo-2"),
    ]
    
    tasks = [
        uninstall_chart_async(name, namespace)
        for name, namespace in charts
    ]
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print("\n" + "="*70)
        print("  Cleanup Summary")
        print("="*70)
        
        for (name, namespace), result in zip(charts, results):
            if isinstance(result, Exception):
                print(f"✗ {name}: Failed - {result}")
            else:
                print(f"✓ {name}: Success")
        
    except Exception as e:
        print(f"\nError during cleanup: {e}")


async def main():
    """Main async function."""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              Async Installation with helm-sdkpy                       ║
║          Non-blocking Helm Operations with Python asyncio        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

This example demonstrates:
- Async chart installation with wait strategy
- Concurrent installation of multiple charts
- Non-blocking operations for event-driven applications
- Proper resource cleanup with async uninstall

""")
    
    print(f"helm-sdkpy version: {helm_sdkpy.__version__}")
    print(f"Library version: {helm_sdkpy.get_version()}")
    print()
    
    try:
        # Install multiple charts concurrently
        await install_multiple_charts()
        
        # Give some time to verify installations
        print("\nWaiting 5 seconds before cleanup...")
        await asyncio.sleep(5)
        
        # Clean up
        await cleanup_charts()
        
        print("\n✓ Async operations demo completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
