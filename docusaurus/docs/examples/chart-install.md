---
sidebar_position: 1
---

# Installing Charts

Learn how to install Helm charts to Kubernetes using helmpy.

## Basic Install

Install a chart with default values:

```python
from helmpy import Chart

# Create chart reference
chart = Chart(
    name="nginx",
    repo="https://charts.bitnami.com/bitnami",
    chart="nginx"
)

# Install to Kubernetes
result = chart.install(
    namespace="default",
    create_namespace=True
)

print(f"Installed: {result}")
```

## Install with Custom Values

Override default chart values:

```python
from helmpy import Chart

chart = Chart(
    name="my-app",
    repo="https://charts.example.com",
    chart="webapp"
)

# Custom configuration
values = {
    "replicaCount": 3,
    "image": {
        "repository": "myapp",
        "tag": "v1.2.3"
    },
    "service": {
        "type": "LoadBalancer",
        "port": 8080
    },
    "ingress": {
        "enabled": True,
        "hosts": ["app.example.com"]
    }
}

result = chart.install(
    namespace="production",
    values=values,
    create_namespace=True,
    wait=True,
    timeout=300  # 5 minutes
)
```

## Install from Values File

Load values from YAML file:

```python
from helmpy import Chart
import yaml

# Read values file
with open("values.yaml", "r") as f:
    values = yaml.safe_load(f)

chart = Chart(
    name="database",
    repo="https://charts.bitnami.com/bitnami",
    chart="postgresql"
)

result = chart.install(
    namespace="databases",
    values=values,
    create_namespace=True
)
```

**values.yaml:**
```yaml
auth:
  username: admin
  password: secretpassword
  database: myapp

primary:
  persistence:
    enabled: true
    size: 10Gi

readReplicas:
  replicaCount: 2
```

## Install Specific Version

Install a specific chart version:

```python
from helmpy import Chart

chart = Chart(
    name="prometheus",
    repo="https://prometheus-community.github.io/helm-charts",
    chart="prometheus",
    version="25.8.0"  # Pin to specific version
)

result = chart.install(
    namespace="monitoring",
    create_namespace=True,
    wait=True
)
```

## Install with Wait

Wait for resources to be ready:

```python
from helmpy import Chart

chart = Chart(
    name="mysql",
    repo="https://charts.bitnami.com/bitnami",
    chart="mysql"
)

result = chart.install(
    namespace="databases",
    create_namespace=True,
    wait=True,           # Wait for pods to be ready
    timeout=600,         # Wait up to 10 minutes
    atomic=True          # Rollback on failure
)
```

## Dry Run

Preview installation without applying:

```python
from helmpy import Chart

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp"
)

# Generate manifests without installing
result = chart.install(
    namespace="default",
    dry_run=True
)

print("Generated manifests:")
print(result)
```

## Async Install

Use async/await for concurrent operations:

```python
import asyncio
from helmpy import Chart

async def install_chart(name: str, chart_name: str, repo: str):
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    result = await chart.install_async(
        namespace="default",
        create_namespace=True,
        wait=True
    )
    
    print(f"✓ Installed {name}")
    return result

async def main():
    # Install multiple charts concurrently
    await asyncio.gather(
        install_chart("nginx", "nginx", "https://charts.bitnami.com/bitnami"),
        install_chart("redis", "redis", "https://charts.bitnami.com/bitnami"),
        install_chart("postgres", "postgresql", "https://charts.bitnami.com/bitnami")
    )

asyncio.run(main())
```

## Install from Local Chart

Install from a local chart directory:

```python
from helmpy import Chart

chart = Chart(
    name="my-local-app",
    chart="./path/to/chart"  # Local path instead of repo
)

result = chart.install(
    namespace="default",
    create_namespace=True
)
```

## Install with Dependencies

Ensure chart dependencies are updated:

```python
from helmpy import Chart

chart = Chart(
    name="complex-app",
    repo="https://charts.example.com",
    chart="fullstack-app"
)

# Install with dependency update
result = chart.install(
    namespace="production",
    create_namespace=True,
    dependency_update=True,  # Update dependencies first
    wait=True
)
```

## Install to Specific Kube Context

Install to a specific Kubernetes context:

```python
from helmpy import Chart

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp",
    kube_context="production-cluster"  # Specific context
)

result = chart.install(
    namespace="default",
    create_namespace=True
)
```

## Complete Example

Full workflow with error handling:

```python
from helmpy import Chart
from helmpy.exceptions import HelmError
import sys

def install_application():
    """Install application with comprehensive configuration."""
    
    chart = Chart(
        name="webapp",
        repo="https://charts.example.com",
        chart="webapp",
        version="2.1.0"
    )
    
    # Application configuration
    values = {
        "replicaCount": 3,
        "image": {
            "repository": "mycompany/webapp",
            "tag": "v2.1.0",
            "pullPolicy": "IfNotPresent"
        },
        "service": {
            "type": "ClusterIP",
            "port": 80
        },
        "ingress": {
            "enabled": True,
            "className": "nginx",
            "hosts": [
                {
                    "host": "webapp.example.com",
                    "paths": [
                        {
                            "path": "/",
                            "pathType": "Prefix"
                        }
                    ]
                }
            ],
            "tls": [
                {
                    "secretName": "webapp-tls",
                    "hosts": ["webapp.example.com"]
                }
            ]
        },
        "resources": {
            "limits": {
                "cpu": "500m",
                "memory": "512Mi"
            },
            "requests": {
                "cpu": "250m",
                "memory": "256Mi"
            }
        },
        "autoscaling": {
            "enabled": True,
            "minReplicas": 3,
            "maxReplicas": 10,
            "targetCPUUtilizationPercentage": 80
        }
    }
    
    try:
        print("Installing webapp...")
        
        result = chart.install(
            namespace="production",
            values=values,
            create_namespace=True,
            wait=True,
            timeout=600,
            atomic=True  # Rollback if install fails
        )
        
        print("✓ Installation successful!")
        print(f"Release: {chart.name}")
        print(f"Namespace: production")
        print(f"Status: {result}")
        
        # Verify installation
        status = chart.status(namespace="production")
        print(f"Chart Status: {status}")
        
        return True
        
    except HelmError as e:
        print(f"✗ Installation failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = install_application()
    sys.exit(0 if success else 1)
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | str | Kubernetes namespace (required) |
| `values` | dict | Value overrides |
| `create_namespace` | bool | Create namespace if missing |
| `wait` | bool | Wait for resources to be ready |
| `timeout` | int | Timeout in seconds |
| `atomic` | bool | Rollback on failure |
| `dry_run` | bool | Simulate installation |
| `dependency_update` | bool | Update dependencies |

## Error Handling

```python
from helmpy import Chart
from helmpy.exceptions import HelmError, InstallError

chart = Chart(
    name="app",
    repo="https://charts.example.com",
    chart="myapp"
)

try:
    result = chart.install(
        namespace="default",
        wait=True,
        timeout=300
    )
except InstallError as e:
    print(f"Install failed: {e}")
    # Handle installation failure
except HelmError as e:
    print(f"Helm error: {e}")
    # Handle general Helm errors
```

## Next Steps

- [Upgrading Charts](chart-upgrade) - Update existing releases
- [Managing Releases](release-management) - Status, rollback, uninstall
- [Repository Management](repositories) - Working with Helm repos
- [Concurrent Operations](concurrent-operations) - Async patterns
