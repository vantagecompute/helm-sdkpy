---
sidebar_position: 10
---

# Troubleshooting

Common issues and solutions when using helmpy.

## Installation Issues

### ImportError: No module named 'helmpy'

**Problem**: helmpy is not installed or not in Python path.

**Solution**:
```bash
pip install helmpy
# or
uv add helmpy
```

### HelmLibraryNotFound

**Problem**: The native Helm library couldn't be found.

**Solution**:
1. Ensure helmpy is properly installed
2. Check if the library exists for your platform (Linux, macOS, Windows)
3. Try reinstalling: `pip install --force-reinstall helmpy`

## Kubernetes Connection Issues

### Unable to connect to Kubernetes cluster

**Problem**: helmpy can't connect to your Kubernetes cluster.

**Solution**:
```python
# Verify kubectl works first
# kubectl cluster-info

# Specify kubeconfig explicitly
from helmpy import Configuration

config = Configuration(
    namespace="default",
    kubeconfig="/path/to/kubeconfig",
    kubecontext="my-context"
)
```

### Context/namespace not found

**Problem**: Specified context or namespace doesn't exist.

**Solution**:
```bash
# List available contexts
kubectl config get-contexts

# List namespaces
kubectl get namespaces

# Use correct names in Configuration
config = Configuration(
    namespace="existing-namespace",
    kubecontext="valid-context"
)
```

## Chart Installation Issues

### Chart not found

**Problem**: Chart path or reference is incorrect.

**Solution**:
```python
# For OCI registries, use full path
chart_path = "oci://registry-1.docker.io/bitnamicharts/nginx"

# For local charts, use absolute or relative path
chart_path = "./charts/mychart"  # or
chart_path = "/absolute/path/to/chart"

# For HTTP(S), use full URL
chart_path = "https://example.com/charts/mychart-1.0.0.tgz"
```

### Release already exists

**Problem**: Trying to install a release that already exists.

**Solution**:
```python
# Use upgrade instead
from helmpy import Upgrade

upgrade = Upgrade(config)
await upgrade.run(release_name="existing-release", chart_path="...")

# Or uninstall first
from helmpy import Uninstall

uninstall = Uninstall(config)
await uninstall.run(release_name="existing-release")
```

### Timeout during installation

**Problem**: Installation takes longer than default timeout.

**Solution**:
```python
# Increase timeout (in seconds)
await install.run(
    release_name="my-app",
    chart_path="./chart",
    wait=True,
    timeout=600  # 10 minutes
)
```

## Version Issues

### Chart version not found

**Problem**: Specified version doesn't exist.

**Solution**:
```python
# Check available versions first
# helm search repo chartname --versions

# Use valid version
await install.run(
    release_name="my-app",
    chart_path="oci://example.com/charts/app",
    version="1.2.3"  # Use valid version
)

# Or omit version to use latest
await install.run(
    release_name="my-app",
    chart_path="oci://example.com/charts/app"
)
```

## Async/Await Issues

### RuntimeError: This event loop is already running

**Problem**: Trying to use `asyncio.run()` in an already-running event loop (e.g., Jupyter).

**Solution**:
```python
# In Jupyter/IPython
await install.run(...)  # Use await directly

# In scripts
import asyncio
asyncio.run(install.run(...))  # Use asyncio.run()
```

### Coroutine was never awaited

**Problem**: Forgot to `await` an async function.

**Solution**:
```python
# Wrong
result = install.run(...)

# Correct
result = await install.run(...)
```

## Permission Issues

### Forbidden: User cannot create resource

**Problem**: Kubernetes user lacks permissions.

**Solution**:
```bash
# Check current permissions
kubectl auth can-i create deployments

# Contact cluster administrator for RBAC permissions
# Or use a different kubeconfig with proper permissions
```

## Value Overrides

### Values not being applied

**Problem**: Custom values aren't taking effect.

**Solution**:
```python
# Ensure values is a proper dictionary
values = {
    "replicaCount": 3,
    "image": {
        "tag": "1.2.3"
    }
}

# Verify values after installation
from helmpy.actions import GetValues

get_values = GetValues(config)
current_values = await get_values.run(
    release_name="my-app",
    all_values=True
)
print(current_values)
```

## Repository Issues

### Repository not found

**Problem**: Repository doesn't exist or wasn't added.

**Solution**:
```python
from helmpy.repo import RepoAdd, RepoUpdate

# Add repository first
repo_add = RepoAdd(config)
await repo_add.run(
    name="bitnami",
    url="https://charts.bitnami.com/bitnami"
)

# Update repository index
repo_update = RepoUpdate(config)
await repo_update.run()
```

### Authentication failed for private repository

**Problem**: Credentials are incorrect or missing.

**Solution**:
```python
await repo_add.run(
    name="private-repo",
    url="https://charts.example.com",
    username="correct-username",
    password="correct-password"
)
```

## Debugging Tips

### Enable verbose logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Check Helm library version

```python
from helmpy._ffi import get_version

print(f"Helm version: {get_version()}")
```

### Inspect release details

```python
from helmpy.actions import Status, GetValues, History

# Check status
status = Status(config)
result = await status.run(release_name="my-app")
print(result)

# Check values
get_values = GetValues(config)
values = await get_values.run(release_name="my-app", all_values=True)
print(values)

# Check history
history = History(config)
revisions = await history.run(release_name="my-app")
print(revisions)
```

## Getting Help

If you're still experiencing issues:

1. Check the [API Reference](api/actions) for correct usage
2. Review [Examples](examples/chart-install) for working code
3. Search [GitHub Issues](https://github.com/vantagecompute/helmpy/issues)
4. Open a new issue with:
   - helmpy version
   - Python version
   - Operating system
   - Minimal reproducible example
   - Full error message and traceback

## Common Error Messages

### "release: not found"

The release doesn't exist. Check the release name and namespace.

### "chart requires kubeVersion"

Your Kubernetes version doesn't match chart requirements. Check chart compatibility.

### "failed to download"

Network issue or chart doesn't exist at the specified location. Verify the chart path/URL.

### "namespace not found"

Create the namespace first or use `create_namespace=True`:

```python
await install.run(
    release_name="my-app",
    chart_path="./chart",
    create_namespace=True
)
```
