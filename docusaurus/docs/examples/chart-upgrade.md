---
sidebar_position: 2
---

# Upgrading Charts

Learn how to upgrade existing Helm releases with helm-sdkpy.

## Basic Upgrade

Upgrade a release with new values:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="nginx",
    repo="https://charts.bitnami.com/bitnami",
    chart="nginx"
)

# Upgrade existing release
result = chart.upgrade(
    namespace="default",
    wait=True
)

print(f"Upgraded: {result}")
```

## Upgrade with New Values

Update configuration during upgrade:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="webapp",
    repo="https://charts.example.com",
    chart="webapp"
)

# New configuration
new_values = {
    "replicaCount": 5,  # Scale up
    "image": {
        "tag": "v2.0.0"  # New version
    },
    "resources": {
        "limits": {
            "cpu": "1000m",
            "memory": "1Gi"
        }
    }
}

result = chart.upgrade(
    namespace="production",
    values=new_values,
    wait=True,
    timeout=600
)
```

## Upgrade to Specific Version

Upgrade to a specific chart version:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="prometheus",
    repo="https://prometheus-community.github.io/helm-charts",
    chart="prometheus",
    version="25.9.0"  # New chart version
)

result = chart.upgrade(
    namespace="monitoring",
    wait=True,
    atomic=True  # Rollback if upgrade fails
)
```

## Upgrade or Install

Install if release doesn't exist, upgrade if it does:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import NotFoundError

chart = Chart(
    name="redis",
    repo="https://charts.bitnami.com/bitnami",
    chart="redis"
)

values = {
    "auth": {
        "enabled": True,
        "password": "secretpassword"
    }
}

# Try upgrade first, fall back to install
try:
    result = chart.upgrade(
        namespace="default",
        values=values,
        wait=True
    )
    print("Upgraded existing release")
except NotFoundError:
    result = chart.install(
        namespace="default",
        values=values,
        create_namespace=True,
        wait=True
    )
    print("Installed new release")
```

## Atomic Upgrade

Rollback automatically on failure:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="database",
    repo="https://charts.bitnami.com/bitnami",
    chart="postgresql"
)

result = chart.upgrade(
    namespace="databases",
    values={
        "auth": {
            "database": "newdb"
        }
    },
    wait=True,
    atomic=True,  # Auto-rollback on failure
    timeout=300
)
```

## Force Upgrade

Force resource updates:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp"
)

result = chart.upgrade(
    namespace="default",
    force=True,  # Force resource updates
    wait=True
)
```

## Upgrade with Cleanup

Clean up old resources during upgrade:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="webapp",
    repo="https://charts.example.com",
    chart="webapp"
)

result = chart.upgrade(
    namespace="production",
    cleanup_on_fail=True,  # Clean up on failure
    wait=True,
    atomic=True
)
```

## Dry Run Upgrade

Preview upgrade without applying:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp"
)

# See what would change
result = chart.upgrade(
    namespace="default",
    values={"replicaCount": 5},
    dry_run=True
)

print("Upgrade preview:")
print(result)
```

## Reuse Values

Keep existing values and add new ones:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="webapp",
    repo="https://charts.example.com",
    chart="webapp"
)

# Get current values
current_status = chart.status(namespace="production")

# Only update specific values, keep others
new_values = {
    "image": {
        "tag": "v2.1.0"  # Only update image tag
    }
}

result = chart.upgrade(
    namespace="production",
    values=new_values,
    reuse_values=True,  # Keep other values
    wait=True
)
```

## Reset Values

Discard previous values and use only new ones:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp"
)

# Start fresh with only these values
fresh_values = {
    "replicaCount": 3,
    "image": {
        "tag": "v3.0.0"
    }
}

result = chart.upgrade(
    namespace="default",
    values=fresh_values,
    reset_values=True,  # Discard previous values
    wait=True
)
```

## Async Upgrade

Use async/await for concurrent upgrades:

```python
import asyncio
from helm_sdkpy import Chart

async def upgrade_chart(name: str, chart_name: str, repo: str, version: str):
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name,
        version=version
    )
    
    result = await chart.upgrade_async(
        namespace="default",
        wait=True,
        atomic=True
    )
    
    print(f"✓ Upgraded {name} to {version}")
    return result

async def main():
    # Upgrade multiple releases concurrently
    await asyncio.gather(
        upgrade_chart("nginx", "nginx", "https://charts.bitnami.com/bitnami", "15.2.0"),
        upgrade_chart("redis", "redis", "https://charts.bitnami.com/bitnami", "18.1.0"),
        upgrade_chart("postgres", "postgresql", "https://charts.bitnami.com/bitnami", "13.1.0")
    )

asyncio.run(main())
```

## Rolling Update

Upgrade with rolling update strategy:

```python
from helm_sdkpy import Chart

chart = Chart(
    name="webapp",
    repo="https://charts.example.com",
    chart="webapp"
)

values = {
    "image": {
        "tag": "v2.0.0"
    },
    "strategy": {
        "type": "RollingUpdate",
        "rollingUpdate": {
            "maxSurge": 1,
            "maxUnavailable": 0
        }
    }
}

result = chart.upgrade(
    namespace="production",
    values=values,
    wait=True,
    timeout=600
)
```

## Blue-Green Deployment

Upgrade with blue-green deployment pattern:

```python
from helm_sdkpy import Chart

# Deploy green version
green_chart = Chart(
    name="webapp-green",
    repo="https://charts.example.com",
    chart="webapp"
)

green_values = {
    "image": {
        "tag": "v2.0.0"
    },
    "service": {
        "name": "webapp-green"
    }
}

# Install green version
green_chart.install(
    namespace="production",
    values=green_values,
    wait=True
)

# Test green version...
# If successful, switch traffic and remove blue

# Uninstall blue version
blue_chart = Chart(name="webapp-blue")
blue_chart.uninstall(namespace="production")
```

## Complete Upgrade Example

Full upgrade workflow with validation:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError
import sys
import time

def upgrade_application(new_version: str):
    """Upgrade application with validation and rollback capability."""
    
    chart = Chart(
        name="webapp",
        repo="https://charts.example.com",
        chart="webapp",
        version=new_version
    )
    
    # Get current status
    try:
        current_status = chart.status(namespace="production")
        print(f"Current release status: {current_status}")
    except HelmError as e:
        print(f"Error getting current status: {e}")
        return False
    
    # Get current revision for potential rollback
    history = chart.history(namespace="production")
    current_revision = len(history)
    
    # New configuration
    values = {
        "replicaCount": 5,
        "image": {
            "repository": "mycompany/webapp",
            "tag": new_version,
            "pullPolicy": "Always"
        },
        "resources": {
            "limits": {
                "cpu": "1000m",
                "memory": "1Gi"
            },
            "requests": {
                "cpu": "500m",
                "memory": "512Mi"
            }
        }
    }
    
    try:
        print(f"Upgrading to version {new_version}...")
        
        result = chart.upgrade(
            namespace="production",
            values=values,
            wait=True,
            timeout=600,
            atomic=True,  # Auto-rollback on failure
            cleanup_on_fail=True
        )
        
        print("✓ Upgrade successful!")
        
        # Verify upgrade
        time.sleep(5)  # Wait for resources to stabilize
        new_status = chart.status(namespace="production")
        print(f"New release status: {new_status}")
        
        # Get values to verify configuration
        deployed_values = chart.get_values(namespace="production")
        print(f"Deployed image tag: {deployed_values.get('image', {}).get('tag')}")
        
        return True
        
    except HelmError as e:
        print(f"✗ Upgrade failed: {e}", file=sys.stderr)
        print(f"Attempting manual rollback to revision {current_revision}...")
        
        try:
            chart.rollback(
                namespace="production",
                revision=current_revision,
                wait=True
            )
            print("✓ Rollback successful")
        except HelmError as rollback_error:
            print(f"✗ Rollback failed: {rollback_error}", file=sys.stderr)
        
        return False

if __name__ == "__main__":
    new_version = sys.argv[1] if len(sys.argv) > 1 else "v2.0.0"
    success = upgrade_application(new_version)
    sys.exit(0 if success else 1)
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace (required) |
| `values` | dict | New value overrides |
| `wait` | bool | Wait for resources to be ready |
| `timeout` | int | Timeout in seconds |
| `atomic` | bool | Rollback on failure |
| `force` | bool | Force resource updates |
| `cleanup_on_fail` | bool | Clean up on failure |
| `dry_run` | bool | Simulate upgrade |
| `reuse_values` | bool | Reuse existing values |
| `reset_values` | bool | Reset to chart defaults |

## Error Handling

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError, UpgradeError

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp",
    version="2.0.0"
)

try:
    result = chart.upgrade(
        namespace="default",
        wait=True,
        atomic=True,
        timeout=300
    )
except UpgradeError as e:
    print(f"Upgrade failed: {e}")
    # Check if rollback happened
    status = chart.status(namespace="default")
    print(f"Current status: {status}")
except HelmError as e:
    print(f"Helm error: {e}")
```

## Best Practices

1. **Always use atomic upgrades** in production
2. **Set appropriate timeouts** for large applications
3. **Test upgrades in staging first**
4. **Monitor after upgrade** to verify success
5. **Keep previous values** unless you need a clean slate
6. **Use specific versions** to avoid unexpected changes

## Next Steps

- [Managing Releases](release-management) - Status, rollback, uninstall
- [Installing Charts](chart-install) - Install new releases
- [Concurrent Operations](concurrent-operations) - Async patterns
- [Error Handling](error-handling) - Robust error management
