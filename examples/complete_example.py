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
Complete example demonstrating all helmpy features.

This example shows how to use helmpy to:
1. Manage Helm configuration
2. Install, upgrade, and uninstall charts
3. Query release information
4. Work with chart operations
"""

import json
import sys

import helmpy


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_configuration():
    """Demonstrate configuration management."""
    print_section("Configuration Management")
    
    try:
        # Create configuration with default namespace
        config = helmpy.Configuration(namespace="default")
        print("✓ Created configuration for 'default' namespace")
        
        # You can also specify custom kubeconfig and context
        # config = helmpy.Configuration(
        #     namespace="production",
        #     kubeconfig="/path/to/kubeconfig",
        #     kubecontext="my-context"
        # )
        
        return config
    except helmpy.HelmLibraryNotFound:
        print("✗ Library not found (this is expected without building)")
        print("  To build: docker build --target go-build -t helmpy-lib .")
        return None
    except helmpy.ConfigurationError as e:
        print(f"✗ Configuration error: {e}")
        return None


def demo_install(config):
    """Demonstrate chart installation."""
    print_section("Installing a Chart")
    
    try:
        install = helmpy.Install(config)
        
        # Example values to override defaults
        values = {
            "replicaCount": 3,
            "image": {
                "repository": "nginx",
                "tag": "1.21.0"
            },
            "service": {
                "type": "LoadBalancer",
                "port": 80
            }
        }
        
        print(f"Installing chart: my-nginx")
        print(f"Chart path: ./nginx-chart")
        print(f"Values: {json.dumps(values, indent=2)}")
        
        # This would actually install the chart
        # result = install.run(
        #     release_name="my-nginx",
        #     chart_path="./nginx-chart",
        #     values=values
        # )
        # print(f"✓ Installed release: {result['name']}")
        # print(f"  Status: {result['info']['status']}")
        # print(f"  Version: {result['version']}")
        
        print("✓ (Would install chart with specified values)")
        
    except helmpy.InstallError as e:
        print(f"✗ Install error: {e}")


def demo_list(config):
    """Demonstrate listing releases."""
    print_section("Listing Releases")
    
    try:
        list_action = helmpy.List(config)
        
        # List all releases (including failed ones)
        # releases = list_action.run(all=True)
        # 
        # for release in releases:
        #     print(f"Release: {release['name']}")
        #     print(f"  Namespace: {release['namespace']}")
        #     print(f"  Status: {release['info']['status']}")
        #     print(f"  Chart: {release['chart']['metadata']['name']}")
        #     print(f"  Version: {release['version']}")
        #     print()
        
        print("✓ (Would list all releases in namespace)")
        
    except helmpy.ReleaseError as e:
        print(f"✗ List error: {e}")


def demo_upgrade(config):
    """Demonstrate upgrading a release."""
    print_section("Upgrading a Release")
    
    try:
        upgrade = helmpy.Upgrade(config)
        
        # New values for upgrade
        values = {
            "replicaCount": 5,  # Scale up
            "image": {
                "tag": "1.21.1"  # Update version
            }
        }
        
        print(f"Upgrading release: my-nginx")
        print(f"New values: {json.dumps(values, indent=2)}")
        
        # result = upgrade.run(
        #     release_name="my-nginx",
        #     chart_path="./nginx-chart",
        #     values=values
        # )
        # print(f"✓ Upgraded to version: {result['version']}")
        
        print("✓ (Would upgrade release with new values)")
        
    except helmpy.UpgradeError as e:
        print(f"✗ Upgrade error: {e}")


def demo_status(config):
    """Demonstrate getting release status."""
    print_section("Getting Release Status")
    
    try:
        status = helmpy.Status(config)
        
        # result = status.run("my-nginx")
        # print(f"Release: {result['name']}")
        # print(f"Status: {result['info']['status']}")
        # print(f"Last Deployed: {result['info']['last_deployed']}")
        # print(f"Resources: {len(result['manifest'].split('---'))}")
        
        print("✓ (Would get current release status)")
        
    except helmpy.ReleaseError as e:
        print(f"✗ Status error: {e}")


def demo_rollback(config):
    """Demonstrate rolling back a release."""
    print_section("Rolling Back a Release")
    
    try:
        rollback = helmpy.Rollback(config)
        
        # Rollback to previous version (revision=0)
        # or specific version (revision=2)
        # result = rollback.run("my-nginx", revision=0)
        # print(f"✓ Rolled back successfully")
        
        print("✓ (Would rollback to previous revision)")
        
    except helmpy.RollbackError as e:
        print(f"✗ Rollback error: {e}")


def demo_get_values(config):
    """Demonstrate getting release values."""
    print_section("Getting Release Values")
    
    try:
        get_values = helmpy.GetValues(config)
        
        # Get user-supplied values only
        # values = get_values.run("my-nginx", all=False)
        # print(f"User values: {json.dumps(values, indent=2)}")
        
        # Get all values (including computed)
        # all_values = get_values.run("my-nginx", all=True)
        # print(f"All values: {json.dumps(all_values, indent=2)}")
        
        print("✓ (Would get release values)")
        
    except helmpy.ReleaseError as e:
        print(f"✗ Get values error: {e}")


def demo_history(config):
    """Demonstrate getting release history."""
    print_section("Getting Release History")
    
    try:
        history = helmpy.History(config)
        
        # revisions = history.run("my-nginx")
        # for rev in revisions:
        #     print(f"Revision {rev['version']}:")
        #     print(f"  Status: {rev['info']['status']}")
        #     print(f"  Updated: {rev['info']['last_deployed']}")
        #     print(f"  Description: {rev['info']['description']}")
        
        print("✓ (Would get release history)")
        
    except helmpy.ReleaseError as e:
        print(f"✗ History error: {e}")


def demo_chart_operations(config):
    """Demonstrate chart operations."""
    print_section("Chart Operations")
    
    try:
        # Pull a chart
        print("\n1. Pulling a chart:")
        pull = helmpy.Pull(config)
        # pull.run("stable/nginx", dest_dir="./charts")
        print("   ✓ (Would pull chart from repository)")
        
        # Show chart information
        print("\n2. Showing chart info:")
        show = helmpy.Show(config)
        # chart_yaml = show.chart("./nginx-chart")
        # print(f"   Chart.yaml: {chart_yaml[:100]}...")
        # values_yaml = show.values("./nginx-chart")
        # print(f"   values.yaml: {values_yaml[:100]}...")
        print("   ✓ (Would show Chart.yaml and values.yaml)")
        
        # Lint a chart
        print("\n3. Linting a chart:")
        lint = helmpy.Lint(config)
        # result = lint.run("./nginx-chart")
        # if result['errors']:
        #     print(f"   ✗ Errors found: {result['errors']}")
        # else:
        #     print(f"   ✓ Chart is valid")
        print("   ✓ (Would lint chart for errors)")
        
        # Package a chart
        print("\n4. Packaging a chart:")
        package = helmpy.Package(config)
        # archive_path = package.run("./nginx-chart", dest_dir="./dist")
        # print(f"   ✓ Created: {archive_path}")
        print("   ✓ (Would package chart into .tgz)")
        
        # Test a release
        print("\n5. Testing a release:")
        test = helmpy.Test(config)
        # result = test.run("my-nginx")
        # print(f"   ✓ Tests completed: {result['name']}")
        print("   ✓ (Would run release test hooks)")
        
    except helmpy.ChartError as e:
        print(f"✗ Chart operation error: {e}")


def demo_uninstall(config):
    """Demonstrate uninstalling a release."""
    print_section("Uninstalling a Release")
    
    try:
        uninstall = helmpy.Uninstall(config)
        
        # result = uninstall.run("my-nginx")
        # print(f"✓ Uninstalled release: {result['release']['name']}")
        # print(f"  Info: {result['info']}")
        
        print("✓ (Would uninstall release)")
        
    except helmpy.UninstallError as e:
        print(f"✗ Uninstall error: {e}")


def demo_context_manager(config):
    """Demonstrate using configuration with context manager."""
    print_section("Using Context Manager")
    
    try:
        # Configuration can be used as a context manager
        # to ensure proper cleanup
        with helmpy.Configuration(namespace="default") as config:
            # Use config for operations
            print("✓ Using configuration in context manager")
            # Operations here...
            pass
        
        print("✓ Configuration automatically cleaned up")
        
    except helmpy.HelmError as e:
        print(f"✗ Error: {e}")


def main():
    """Run all demonstrations."""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                  helmpy Complete Example                    ║
║          Python Bindings for Helm v4                        ║
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
        print("⚠ Showing API examples only (no actual operations)\n")
    
    # Create configuration
    config = demo_configuration()
    
    if config is None:
        print("\n✗ Could not create configuration. Examples will be shown but not executed.")
        # Create a mock config for demonstration purposes
        print("Note: Make sure you have access to a Kubernetes cluster.")
        print("      Set KUBECONFIG environment variable if needed.\n")
        return 1
    
    # Demonstrate all operations
    demo_install(config)
    demo_list(config)
    demo_upgrade(config)
    demo_status(config)
    demo_rollback(config)
    demo_get_values(config)
    demo_history(config)
    demo_chart_operations(config)
    demo_uninstall(config)
    demo_context_manager(config)
    
    print_section("Summary")
    print("""
This example demonstrated all major helmpy features:

✓ Configuration management (namespace, kubeconfig, context)
✓ Release management (install, upgrade, uninstall, rollback)
✓ Release queries (list, status, get-values, history)
✓ Chart operations (pull, show, lint, package, test)
✓ Context manager support for automatic cleanup
✓ Exception handling for all operations

For more details, see:
- README.md for installation and quick start
- API documentation for detailed class reference
- examples/ directory for more use cases
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
