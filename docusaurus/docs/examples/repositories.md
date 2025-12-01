---
sidebar_position: 4
---

# Repository Management

Learn how to manage Helm repositories with helm-sdkpy.

## Add Repository

Add a Helm chart repository:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

# Add repository
result = repo.add(
    name="bitnami",
    url="https://charts.bitnami.com/bitnami"
)

print(f"Added repository: {result}")
```

## Add Repository with Authentication

Add a private repository with credentials:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

result = repo.add(
    name="private-repo",
    url="https://charts.example.com",
    username="user",
    password="password"
)
```

## Update Repositories

Update repository indexes to get latest charts:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

# Update all repositories
result = repo.update()
print(f"Updated repositories: {result}")
```

## List Repositories

List all configured repositories:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

# Get all repositories
repositories = repo.list()

for r in repositories:
    print(f"Name: {r['name']}")
    print(f"URL: {r['url']}")
    print("---")
```

## Remove Repository

Remove a repository:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

# Remove repository
result = repo.remove(name="bitnami")
print(f"Removed repository: {result}")
```

## Complete Repository Setup

Set up multiple repositories:

```python
from helm_sdkpy.repo import Repo
from helm_sdkpy.exceptions import HelmError

def setup_repositories():
    """Set up standard Helm repositories."""
    
    repo = Repo()
    
    repositories = [
        {
            "name": "bitnami",
            "url": "https://charts.bitnami.com/bitnami"
        },
        {
            "name": "prometheus-community",
            "url": "https://prometheus-community.github.io/helm-charts"
        },
        {
            "name": "grafana",
            "url": "https://grafana.github.io/helm-charts"
        },
        {
            "name": "jetstack",
            "url": "https://charts.jetstack.io"
        }
    ]
    
    for r in repositories:
        try:
            print(f"Adding repository '{r['name']}'...")
            repo.add(name=r['name'], url=r['url'])
            print(f"  ✓ Added {r['name']}")
        except HelmError as e:
            print(f"  ✗ Failed to add {r['name']}: {e}")
    
    # Update all repositories
    print("\nUpdating repositories...")
    try:
        repo.update()
        print("✓ Repositories updated")
    except HelmError as e:
        print(f"✗ Update failed: {e}")
    
    # List configured repositories
    print("\nConfigured repositories:")
    repos = repo.list()
    for r in repos:
        print(f"  - {r['name']}: {r['url']}")

if __name__ == "__main__":
    setup_repositories()
```

## Search Charts in Repository

After adding repositories, search for charts:

```python
from helm_sdkpy.repo import Repo
from helm_sdkpy.actions import Show

# Setup repository
repo = Repo()
repo.add(name="bitnami", url="https://charts.bitnami.com/bitnami")
repo.update()

# Search for charts (using show chart command)
show = Show()
chart_info = show.run(
    chart="bitnami/nginx",
    show_type="chart"
)

print(f"Chart info: {chart_info}")
```

## Add Repository with Custom CA

Add repository with custom certificate authority:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

result = repo.add(
    name="internal",
    url="https://charts.internal.example.com",
    ca_file="/path/to/ca.crt"
)
```

## Add Repository with Client Certificates

Add repository with mutual TLS:

```python
from helm_sdkpy.repo import Repo

repo = Repo()

result = repo.add(
    name="secure-repo",
    url="https://charts.secure.example.com",
    cert_file="/path/to/client.crt",
    key_file="/path/to/client.key",
    ca_file="/path/to/ca.crt"
)
```

## Repository Operations Example

Complete repository management workflow:

```python
from helm_sdkpy.repo import Repo
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError
import sys

def manage_repositories():
    """Complete repository management example."""
    
    repo = Repo()
    
    # 1. List existing repositories
    print("Current repositories:")
    try:
        existing = repo.list()
        for r in existing:
            print(f"  - {r['name']}: {r['url']}")
    except HelmError as e:
        print(f"Error listing repositories: {e}")
        existing = []
    
    # 2. Add new repository if not exists
    repo_name = "bitnami"
    repo_url = "https://charts.bitnami.com/bitnami"
    
    if not any(r['name'] == repo_name for r in existing):
        print(f"\nAdding repository '{repo_name}'...")
        try:
            repo.add(name=repo_name, url=repo_url)
            print(f"✓ Added {repo_name}")
        except HelmError as e:
            print(f"✗ Failed to add repository: {e}")
            return False
    else:
        print(f"\nRepository '{repo_name}' already exists")
    
    # 3. Update repositories
    print("\nUpdating repository indexes...")
    try:
        repo.update()
        print("✓ Repositories updated")
    except HelmError as e:
        print(f"✗ Update failed: {e}")
        return False
    
    # 4. Use repository to install chart
    print("\nInstalling chart from repository...")
    chart = Chart(
        name="test-nginx",
        repo=repo_url,
        chart="nginx"
    )
    
    try:
        result = chart.install(
            namespace="default",
            create_namespace=True,
            wait=True,
            timeout=300
        )
        print(f"✓ Chart installed: {result}")
        
        # Clean up
        print("\nCleaning up...")
        chart.uninstall(namespace="default", wait=True)
        print("✓ Chart uninstalled")
        
    except HelmError as e:
        print(f"✗ Chart operation failed: {e}")
        return False
    
    # 5. List repositories again
    print("\nFinal repository list:")
    repos = repo.list()
    for r in repos:
        print(f"  - {r['name']}: {r['url']}")
    
    return True

if __name__ == "__main__":
    success = manage_repositories()
    sys.exit(0 if success else 1)
```

## Async Repository Operations

Concurrent repository management:

```python
import asyncio
from helm_sdkpy.repo import Repo

async def add_repository(name: str, url: str):
    """Add repository asynchronously."""
    repo = Repo()
    result = await repo.add_async(name=name, url=url)
    print(f"✓ Added {name}")
    return result

async def setup_repos():
    """Add multiple repositories concurrently."""
    
    repos = [
        ("bitnami", "https://charts.bitnami.com/bitnami"),
        ("prometheus", "https://prometheus-community.github.io/helm-charts"),
        ("grafana", "https://grafana.github.io/helm-charts"),
    ]
    
    # Add repositories concurrently
    await asyncio.gather(
        *[add_repository(name, url) for name, url in repos]
    )
    
    # Update all
    repo = Repo()
    await repo.update_async()
    print("✓ All repositories updated")

asyncio.run(setup_repos())
```

## Repository Cleanup

Clean up unused repositories:

```python
from helm_sdkpy.repo import Repo
from helm_sdkpy.actions import List
from helm_sdkpy.exceptions import HelmError

def cleanup_repositories():
    """Remove repositories not used by any release."""
    
    repo = Repo()
    
    # Get all repositories
    try:
        all_repos = repo.list()
    except HelmError as e:
        print(f"Error listing repositories: {e}")
        return False
    
    # Get all releases
    lister = List()
    try:
        releases = lister.run(all_namespaces=True)
    except HelmError as e:
        print(f"Error listing releases: {e}")
        return False
    
    # Extract chart repositories from releases
    used_repos = set()
    for release in releases:
        chart = release.get('chart', '')
        if '/' in chart:
            repo_name = chart.split('/')[0]
            used_repos.add(repo_name)
    
    # Find unused repositories
    all_repo_names = {r['name'] for r in all_repos}
    unused = all_repo_names - used_repos
    
    if not unused:
        print("No unused repositories found")
        return True
    
    print(f"Unused repositories: {', '.join(unused)}")
    
    # Confirm removal
    response = input("Remove unused repositories? [y/N]: ")
    if response.lower() != 'y':
        print("Cleanup cancelled")
        return False
    
    # Remove unused repositories
    for repo_name in unused:
        try:
            print(f"Removing '{repo_name}'...")
            repo.remove(name=repo_name)
            print(f"  ✓ Removed {repo_name}")
        except HelmError as e:
            print(f"  ✗ Failed to remove {repo_name}: {e}")
    
    return True

if __name__ == "__main__":
    cleanup_repositories()
```

## Common Parameters

### Add Repository
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Repository name (required) |
| `url` | str | Repository URL (required) |
| `username` | str | Basic auth username |
| `password` | str | Basic auth password |
| `ca_file` | str | Path to CA certificate |
| `cert_file` | str | Path to client certificate |
| `key_file` | str | Path to client key |

### Update
| Parameter | Type | Description |
|-----------|------|-------------|
| None | - | Updates all repositories |

### List
| Parameter | Type | Description |
|-----------|------|-------------|
| None | - | Returns all repositories |

### Remove
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Repository name (required) |

## Error Handling

```python
from helm_sdkpy.repo import Repo
from helm_sdkpy.exceptions import HelmError, RepoError

repo = Repo()

try:
    repo.add(name="test", url="https://charts.example.com")
except RepoError as e:
    print(f"Repository error: {e}")
except HelmError as e:
    print(f"Helm error: {e}")
```

## Next Steps

- [Installing Charts](chart-install) - Deploy charts from repositories
- [Upgrading Charts](chart-upgrade) - Update chart versions
- [Concurrent Operations](concurrent-operations) - Async patterns
- [Managing Releases](release-management) - Release operations
