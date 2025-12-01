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
Async Repository Management Example

This example demonstrates using helm-sdkpy's async API for repository management.
All operations are non-blocking and can be used in async applications.
"""

import asyncio
import json

import helm_sdkpy


async def add_repository(name: str, url: str, config: helm_sdkpy.Configuration):
    """Add a Helm repository asynchronously."""
    print(f"Adding repository: {name}")
    repo_add = helm_sdkpy.RepoAdd(config)
    
    try:
        await repo_add.run(name, url)
        print(f"✓ Repository '{name}' added successfully")
        return True
    except helm_sdkpy.HelmError as e:
        if "already exists" in str(e):
            print(f"ℹ Repository '{name}' already exists")
            return True
        else:
            print(f"✗ Failed to add '{name}': {e}")
            return False


async def list_repositories(config: helm_sdkpy.Configuration):
    """List all configured repositories asynchronously."""
    print("\nListing repositories...")
    repo_list = helm_sdkpy.RepoList(config)
    
    try:
        repos = await repo_list.run()
        print(f"Found {len(repos)} repositories:")
        for repo in repos:
            print(f"  - {repo.get('name', 'unknown')}: {repo.get('url', 'unknown')}")
        return repos
    except helm_sdkpy.HelmError as e:
        print(f"✗ Failed to list repositories: {e}")
        return []


async def update_repositories(config: helm_sdkpy.Configuration):
    """Update all repository indexes asynchronously."""
    print("\nUpdating repository indexes...")
    repo_update = helm_sdkpy.RepoUpdate(config)
    
    try:
        await repo_update.run()
        print("✓ Repository indexes updated successfully")
        return True
    except helm_sdkpy.HelmError as e:
        print(f"✗ Failed to update repositories: {e}")
        return False


async def remove_repository(name: str, config: helm_sdkpy.Configuration):
    """Remove a Helm repository asynchronously."""
    print(f"\nRemoving repository: {name}")
    repo_remove = helm_sdkpy.RepoRemove(config)
    
    try:
        await repo_remove.run(name)
        print(f"✓ Repository '{name}' removed successfully")
        return True
    except helm_sdkpy.HelmError as e:
        print(f"✗ Failed to remove '{name}': {e}")
        return False


async def main():
    """Main async function demonstrating repository management."""
    print("=" * 60)
    print("  helm-sdkpy Async Repository Management Demo")
    print("=" * 60)
    
    # Create configuration
    config = helm_sdkpy.Configuration()
    
    try:
        # Define repositories to add
        repositories = [
            ("bitnami", "https://charts.bitnami.com/bitnami"),
            ("jetstack", "https://charts.jetstack.io"),
            ("nginx", "https://helm.nginx.com/stable"),
        ]
        
        # Add repositories concurrently
        print("\nAdding repositories concurrently...")
        add_tasks = [
            add_repository(name, url, config)
            for name, url in repositories
        ]
        results = await asyncio.gather(*add_tasks, return_exceptions=True)
        
        # List repositories
        await list_repositories(config)
        
        # Update all repositories
        await update_repositories(config)
        
        # Remove repositories concurrently
        print("\nRemoving repositories concurrently...")
        remove_tasks = [
            remove_repository(name, config)
            for name, _ in repositories
        ]
        await asyncio.gather(*remove_tasks, return_exceptions=True)
        
        # List repositories again to confirm removal
        await list_repositories(config)
        
        print("\n" + "=" * 60)
        print("  Demo completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        if hasattr(config, '_cleanup'):
            config._cleanup()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
