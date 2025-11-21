---
sidebar_position: 3
---

# Managing Releases

Learn how to manage Helm releases: status checks, history, rollbacks, and uninstalls.

## Check Release Status

Get the current status of a release:

```python
from helmpy import Chart

chart = Chart(name="nginx")

# Get status
status = chart.status(namespace="default")
print(f"Status: {status}")
```

## List All Releases

List releases in a namespace:

```python
from helmpy.actions import List

# List all releases in namespace
lister = List()
releases = lister.run(namespace="default")

for release in releases:
    print(f"Name: {release['name']}")
    print(f"Namespace: {release['namespace']}")
    print(f"Revision: {release['revision']}")
    print(f"Status: {release['status']}")
    print(f"Chart: {release['chart']}")
    print("---")
```

## List All Releases (All Namespaces)

```python
from helmpy.actions import List

lister = List()
releases = lister.run(all_namespaces=True)

for release in releases:
    print(f"{release['namespace']}/{release['name']}: {release['status']}")
```

## Filter Releases

Filter by status or name:

```python
from helmpy.actions import List

lister = List()

# Filter by status
deployed = lister.run(
    namespace="production",
    filter="deployed"  # deployed, failed, pending, etc.
)

# Filter by name pattern
webapps = lister.run(
    namespace="default",
    filter="web"  # Releases containing "web"
)
```

## Get Release History

View revision history:

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Get history
history = chart.history(namespace="production")

for revision in history:
    print(f"Revision: {revision['revision']}")
    print(f"Updated: {revision['updated']}")
    print(f"Status: {revision['status']}")
    print(f"Chart: {revision['chart']}")
    print(f"Description: {revision['description']}")
    print("---")
```

## Get Release Values

Retrieve deployed values:

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Get all values
values = chart.get_values(namespace="production")

print("Current configuration:")
print(f"Replicas: {values.get('replicaCount')}")
print(f"Image: {values.get('image', {}).get('tag')}")
```

## Get User-Supplied Values Only

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Get only user-supplied values (not defaults)
user_values = chart.get_values(
    namespace="production",
    all_values=False
)

print("User-supplied values:", user_values)
```

## Rollback Release

Rollback to a previous revision:

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Rollback to previous revision
result = chart.rollback(
    namespace="production",
    wait=True
)

print(f"Rolled back: {result}")
```

## Rollback to Specific Revision

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Get history to find revision
history = chart.history(namespace="production")
print("Available revisions:")
for rev in history:
    print(f"  {rev['revision']}: {rev['description']}")

# Rollback to specific revision
result = chart.rollback(
    namespace="production",
    revision=3,  # Rollback to revision 3
    wait=True,
    timeout=300
)
```

## Uninstall Release

Remove a release:

```python
from helmpy import Chart

chart = Chart(name="nginx")

# Uninstall
result = chart.uninstall(namespace="default")
print(f"Uninstalled: {result}")
```

## Uninstall with Cleanup

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Uninstall and wait for cleanup
result = chart.uninstall(
    namespace="production",
    wait=True,
    timeout=300
)
```

## Keep Release History

Uninstall but keep release history:

```python
from helmpy import Chart

chart = Chart(name="webapp")

# Uninstall but keep history for potential restore
result = chart.uninstall(
    namespace="production",
    keep_history=True
)
```

## Complete Release Management Example

Full workflow with status checks and operations:

```python
from helmpy import Chart
from helmpy.actions import List
from helmpy.exceptions import HelmError
import sys

def manage_release(release_name: str, namespace: str):
    """Comprehensive release management."""
    
    chart = Chart(name=release_name)
    
    try:
        # 1. Check if release exists
        print(f"Checking release '{release_name}' in namespace '{namespace}'...")
        
        try:
            status = chart.status(namespace=namespace)
            print(f"✓ Release found")
            print(f"  Status: {status}")
        except HelmError:
            print(f"✗ Release not found")
            return False
        
        # 2. Get release details
        print("\nRelease Details:")
        
        # Get history
        history = chart.history(namespace=namespace)
        print(f"  Revisions: {len(history)}")
        print(f"  Current revision: {history[-1]['revision']}")
        
        # Get values
        values = chart.get_values(namespace=namespace, all_values=False)
        print(f"  Custom values: {len(values)} keys")
        
        # 3. List all releases in namespace
        print(f"\nAll releases in '{namespace}':")
        lister = List()
        releases = lister.run(namespace=namespace)
        for rel in releases:
            marker = "→" if rel['name'] == release_name else " "
            print(f"  {marker} {rel['name']}: {rel['status']}")
        
        # 4. Show history
        print(f"\nRevision History for '{release_name}':")
        for rev in history[-5:]:  # Last 5 revisions
            print(f"  Revision {rev['revision']}:")
            print(f"    Updated: {rev['updated']}")
            print(f"    Status: {rev['status']}")
            print(f"    Description: {rev['description']}")
        
        return True
        
    except HelmError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return False

def rollback_if_needed(release_name: str, namespace: str):
    """Rollback release if in failed state."""
    
    chart = Chart(name=release_name)
    
    try:
        status = chart.status(namespace=namespace)
        
        if status == "failed":
            print(f"Release is in failed state, rolling back...")
            
            history = chart.history(namespace=namespace)
            if len(history) < 2:
                print("No previous revision to rollback to")
                return False
            
            # Rollback to previous revision
            prev_revision = history[-2]['revision']
            print(f"Rolling back to revision {prev_revision}...")
            
            result = chart.rollback(
                namespace=namespace,
                revision=prev_revision,
                wait=True,
                timeout=300
            )
            
            print(f"✓ Rollback successful: {result}")
            
            # Verify
            new_status = chart.status(namespace=namespace)
            print(f"New status: {new_status}")
            
            return True
        else:
            print(f"Release status is '{status}', no rollback needed")
            return True
            
    except HelmError as e:
        print(f"✗ Rollback failed: {e}", file=sys.stderr)
        return False

def cleanup_failed_releases(namespace: str):
    """Find and clean up failed releases."""
    
    lister = List()
    
    try:
        # List all releases
        all_releases = lister.run(namespace=namespace)
        
        failed = [r for r in all_releases if r['status'] == 'failed']
        
        if not failed:
            print(f"No failed releases in '{namespace}'")
            return True
        
        print(f"Found {len(failed)} failed releases:")
        for release in failed:
            print(f"  - {release['name']}: {release['chart']}")
        
        # Confirm cleanup
        response = input("Uninstall failed releases? [y/N]: ")
        if response.lower() != 'y':
            print("Cleanup cancelled")
            return False
        
        # Uninstall each failed release
        for release in failed:
            chart = Chart(name=release['name'])
            try:
                print(f"Uninstalling {release['name']}...")
                chart.uninstall(namespace=namespace, wait=True)
                print(f"  ✓ Uninstalled {release['name']}")
            except HelmError as e:
                print(f"  ✗ Failed to uninstall {release['name']}: {e}")
        
        return True
        
    except HelmError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python release_management.py <release-name> <namespace>")
        sys.exit(1)
    
    release_name = sys.argv[1]
    namespace = sys.argv[2]
    
    # Manage release
    success = manage_release(release_name, namespace)
    
    # Check for rollback
    if success:
        rollback_if_needed(release_name, namespace)
    
    sys.exit(0 if success else 1)
```

## Async Release Operations

Concurrent release management:

```python
import asyncio
from helmpy import Chart
from helmpy.actions import List

async def check_release_status(name: str, namespace: str):
    """Check status of a release."""
    chart = Chart(name=name)
    status = await chart.status_async(namespace=namespace)
    return {"name": name, "status": status}

async def check_all_releases(namespace: str):
    """Check status of all releases concurrently."""
    
    # Get list of releases
    lister = List()
    releases = lister.run(namespace=namespace)
    
    # Check status concurrently
    tasks = [
        check_release_status(rel['name'], namespace)
        for rel in releases
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Print results
    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(f"{result['name']}: {result['status']}")

asyncio.run(check_all_releases("production"))
```

## Monitoring Releases

Periodic status checks:

```python
import asyncio
from helmpy import Chart
from helmpy.exceptions import HelmError

async def monitor_release(name: str, namespace: str, interval: int = 30):
    """Monitor release status periodically."""
    
    chart = Chart(name=name)
    
    while True:
        try:
            status = await chart.status_async(namespace=namespace)
            print(f"[{name}] Status: {status}")
            
            if status == "failed":
                print(f"⚠ Release {name} is in failed state!")
                # Could trigger alerts or auto-rollback here
                
        except HelmError as e:
            print(f"Error checking {name}: {e}")
        
        await asyncio.sleep(interval)

# Monitor multiple releases
async def main():
    await asyncio.gather(
        monitor_release("webapp", "production", interval=30),
        monitor_release("api", "production", interval=30),
        monitor_release("database", "production", interval=60)
    )

asyncio.run(main())
```

## Common Parameters

### Status
| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace (required) |

### List
| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace |
| `all_namespaces` | bool | List across all namespaces |
| `filter` | str | Filter by name or status |

### Rollback
| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace (required) |
| `revision` | int | Specific revision (default: previous) |
| `wait` | bool | Wait for completion |
| `timeout` | int | Timeout in seconds |

### Uninstall
| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace (required) |
| `wait` | bool | Wait for cleanup |
| `timeout` | int | Timeout in seconds |
| `keep_history` | bool | Keep release history |

## Error Handling

```python
from helmpy import Chart
from helmpy.exceptions import HelmError, NotFoundError

chart = Chart(name="webapp")

try:
    status = chart.status(namespace="production")
    print(f"Status: {status}")
except NotFoundError:
    print("Release not found")
except HelmError as e:
    print(f"Helm error: {e}")
```

## Next Steps

- [Installing Charts](chart-install) - Deploy new releases
- [Upgrading Charts](chart-upgrade) - Update releases
- [Concurrent Operations](concurrent-operations) - Async patterns
- [Error Handling](error-handling) - Robust error management
