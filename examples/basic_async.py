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

"""Example showing basic async helm-sdkpy usage."""

import asyncio
import helm_sdkpy


async def main():
    """Basic example of using helm-sdkpy with async/await."""
    print(f"helm-sdkpy version: {helm_sdkpy.__version__}")
    
    try:
        print(f"Library version: {helm_sdkpy.get_version()}")
    except helm_sdkpy.HelmLibraryNotFound:
        print("Library not found - please build the library first with 'just build-lib'")
        return

    print("\nAvailable action classes:")
    print("- Configuration: Manage Helm configuration")
    print("- Install: Install a chart (async)")
    print("- Upgrade: Upgrade a release (async)")
    print("- Uninstall: Uninstall a release (async)")
    print("- List: List releases (async)")
    print("- Status: Get release status (async)")
    print("- Rollback: Rollback a release (async)")
    print("- GetValues: Get release values (async)")
    print("- History: Get release history (async)")
    print("\nChart operations:")
    print("- Pull: Download a chart (async)")
    print("- Show: Show chart information (async)")
    print("- Test: Run release tests (async)")
    print("- Lint: Lint a chart (async)")
    print("- Package: Package a chart (async)")

    print("\n" + "="*60)
    print("Example usage:")
    print("="*60)
    
    example_code = """
    import asyncio
    from helm_sdkpy import Configuration, Install, List

    async def main():
        # Create a configuration for the default namespace
        config = Configuration(namespace="default")

        # Install a chart from a local path
        install = Install(config)
        result = await install.run(
            release_name="my-nginx",
            chart_path="./nginx-chart",
            values={"replicaCount": 3}
        )
        print(f"Installed release: {result}")

        # Install a chart from an OCI registry
        result = await install.run(
            release_name="my-app",
            chart_path="oci://ghcr.io/nginxinc/charts/nginx-ingress",
            values={"controller": {"service": {"type": "LoadBalancer"}}}
        )
        print(f"Installed from OCI: {result}")

        # Install a chart from an HTTPS URL
        result = await install.run(
            release_name="my-release",
            chart_path="https://charts.bitnami.com/bitnami/nginx-15.0.0.tgz",
            values={"replicaCount": 2}
        )
        print(f"Installed from HTTPS: {result}")

        # List releases
        list_action = List(config)
        releases = await list_action.run(all=True)
        for release in releases:
            print(f"Release: {release['name']}, Status: {release['status']}")

    asyncio.run(main())
    """
    
    print(example_code)


if __name__ == "__main__":
    asyncio.run(main())
