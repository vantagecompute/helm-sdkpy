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

"""Example showing basic helmpy usage."""

import helmpy


def main():
    """Basic example of using helmpy."""
    print(f"helmpy version: {helmpy.__version__}")
    
    try:
        print(f"Library version: {helmpy.get_version()}")
    except helmpy.HelmLibraryNotFound:
        print("Library not found - please build the library first with 'just build-lib'")
        return

    print("\nAvailable action classes:")
    print("- Configuration: Manage Helm configuration")
    print("- Install: Install a chart")
    print("- Upgrade: Upgrade a release")
    print("- Uninstall: Uninstall a release")
    print("- List: List releases")
    print("- Status: Get release status")
    print("- Rollback: Rollback a release")
    print("- GetValues: Get release values")
    print("- History: Get release history")
    print("\nChart operations:")
    print("- Pull: Download a chart")
    print("- Show: Show chart information")
    print("- Test: Run release tests")
    print("- Lint: Lint a chart")
    print("- Package: Package a chart")

    print("\n" + "="*60)
    print("Example usage:")
    print("="*60)
    
    example_code = """
    from helmpy import Configuration, Install, List

    # Create a configuration for the default namespace
    config = Configuration(namespace="default")

    # Install a chart
    install = Install(config)
    result = install.run(
        release_name="my-nginx",
        chart_path="./nginx-chart",
        values={"replicaCount": 3}
    )
    print(f"Installed release: {result}")

    # List releases
    list_action = List(config)
    releases = list_action.run(all=True)
    for release in releases:
        print(f"Release: {release['name']}, Status: {release['status']}")
    """
    
    print(example_code)


if __name__ == "__main__":
    main()
