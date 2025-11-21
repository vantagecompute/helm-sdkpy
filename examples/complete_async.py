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
Complete async example demonstrating all helmpy features.

This example shows how to use helmpy with async/await to:
1. Manage Helm configuration
2. Install, upgrade, and uninstall charts
3. Query release information
4. Work with chart operations
"""

import asyncio
import json
import sys

import helmpy


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def demo_install():
    """Demonstrate async chart installation."""
    print_section("Installing a Chart (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    install = helmpy.Install(config)
    
    # Install with async/await
    result = await install.run(
        release_name="my-nginx",
        chart_path="./nginx-chart",
        values={
            "replicaCount": 3,
            "image": {"repository": "nginx", "tag": "1.21.0"}
        },
        create_namespace=True,
        wait=True,
        timeout=300
    )
    print(f"✓ Installed: {result['name']}")
    """
    print(example_code)


async def demo_list():
    """Demonstrate async listing releases."""
    print_section("Listing Releases (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    list_action = helmpy.List(config)
    
    # List all releases asynchronously
    releases = await list_action.run(all=True)
    for release in releases:
        print(f"Release: {release['name']}")
        print(f"  Status: {release['info']['status']}")
        print(f"  Version: {release['version']}")
    """
    print(example_code)


async def demo_upgrade():
    """Demonstrate async upgrade."""
    print_section("Upgrading a Release (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    upgrade = helmpy.Upgrade(config)
    
    # Upgrade asynchronously
    result = await upgrade.run(
        release_name="my-nginx",
        chart_path="./nginx-chart",
        values={"replicaCount": 5}
    )
    print(f"✓ Upgraded to version: {result['version']}")
    """
    print(example_code)


async def demo_status():
    """Demonstrate async status check."""
    print_section("Getting Release Status (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    status = helmpy.Status(config)
    
    # Get status asynchronously
    result = await status.run("my-nginx")
    print(f"Status: {result['info']['status']}")
    print(f"Last Deployed: {result['info']['last_deployed']}")
    """
    print(example_code)


async def demo_rollback():
    """Demonstrate async rollback."""
    print_section("Rolling Back a Release (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    rollback = helmpy.Rollback(config)
    
    # Rollback asynchronously
    result = await rollback.run("my-nginx", revision=0)
    print("✓ Rolled back successfully")
    """
    print(example_code)


async def demo_get_values():
    """Demonstrate async get values."""
    print_section("Getting Release Values (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    get_values = helmpy.GetValues(config)
    
    # Get values asynchronously
    values = await get_values.run("my-nginx", all=False)
    print(f"User values: {json.dumps(values, indent=2)}")
    
    # Get all values
    all_values = await get_values.run("my-nginx", all=True)
    print(f"All values: {json.dumps(all_values, indent=2)}")
    """
    print(example_code)


async def demo_history():
    """Demonstrate async history."""
    print_section("Getting Release History (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    history = helmpy.History(config)
    
    # Get history asynchronously
    revisions = await history.run("my-nginx")
    for rev in revisions:
        print(f"Revision {rev['version']}: {rev['info']['status']}")
    """
    print(example_code)


async def demo_chart_operations():
    """Demonstrate async chart operations."""
    print_section("Chart Operations (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    
    # Pull a chart asynchronously
    pull = helmpy.Pull(config)
    await pull.run("stable/nginx", dest_dir="./charts")
    
    # Show chart information asynchronously
    show = helmpy.Show(config)
    chart_yaml = await show.chart("./nginx-chart")
    values_yaml = await show.values("./nginx-chart")
    
    # Lint a chart asynchronously
    lint = helmpy.Lint(config)
    result = await lint.run("./nginx-chart")
    print(f"Lint result: {result}")
    
    # Package a chart asynchronously
    package = helmpy.Package(config)
    archive_path = await package.run("./nginx-chart", dest_dir="./dist")
    print(f"Created: {archive_path}")
    
    # Test a release asynchronously
    test = helmpy.Test(config)
    result = await test.run("my-nginx")
    print(f"Test completed: {result['name']}")
    """
    print(example_code)


async def demo_concurrent_operations():
    """Demonstrate concurrent async operations."""
    print_section("Concurrent Operations (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    
    # Install multiple charts concurrently
    install = helmpy.Install(config)
    
    results = await asyncio.gather(
        install.run("app-1", "oci://registry.io/chart1"),
        install.run("app-2", "oci://registry.io/chart2"),
        install.run("app-3", "oci://registry.io/chart3"),
    )
    
    for result in results:
        print(f"Installed: {result['name']}")
    
    # List and check status concurrently
    list_action = helmpy.List(config)
    status = helmpy.Status(config)
    
    releases, status_app1 = await asyncio.gather(
        list_action.run(all=True),
        status.run("app-1")
    )
    """
    print(example_code)


async def demo_uninstall():
    """Demonstrate async uninstall."""
    print_section("Uninstalling a Release (Async)")
    
    example_code = """
    config = helmpy.Configuration(namespace="default")
    uninstall = helmpy.Uninstall(config)
    
    # Uninstall asynchronously
    result = await uninstall.run("my-nginx", wait=True, timeout=300)
    print(f"✓ Uninstalled: {result['release']['name']}")
    """
    print(example_code)


async def main():
    """Run all demonstrations."""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              helmpy Complete Async Example                  ║
║          Python Bindings for Helm v4 (Async API)            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Version: {helmpy.__version__}
""")
    
    # Check if library is available
    try:
        lib_version = helmpy.get_version()
        print(f"Library version: {lib_version}\n")
    except helmpy.HelmLibraryNotFound:
        print("⚠ Library not built yet. Run 'just build-lib' first.")
        print("⚠ Showing API examples only\n")
    
    # Demonstrate all operations
    await demo_install()
    await demo_list()
    await demo_upgrade()
    await demo_status()
    await demo_rollback()
    await demo_get_values()
    await demo_history()
    await demo_chart_operations()
    await demo_concurrent_operations()
    await demo_uninstall()
    
    print_section("Summary")
    print("""
This example demonstrated all major helmpy async features:

✓ Configuration management (namespace, kubeconfig, context)
✓ Async release management (install, upgrade, uninstall, rollback)
✓ Async release queries (list, status, get-values, history)
✓ Async chart operations (pull, show, lint, package, test)
✓ Concurrent operations with asyncio.gather()
✓ Exception handling for all async operations

All operations use async/await for non-blocking execution.
Perfect for web applications, event loops, and concurrent workflows!

For more details, see:
- README.md for installation and quick start
- API documentation for detailed class reference
- examples/ directory for more use cases
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
