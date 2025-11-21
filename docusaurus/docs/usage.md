---
sidebar_position: 3
---

# Usage Guide

Comprehensive guide to using helmpy for Helm operations.

## Configuration

All Helm operations require a `Configuration` object that manages the connection to your Kubernetes cluster.

```python
from helmpy import Configuration

# Basic configuration
config = Configuration(namespace="default")

# With custom kubeconfig
config = Configuration(
    namespace="production",
    kubeconfig="/path/to/kubeconfig",
    kubecontext="my-cluster"
)
```

## Release Management

### Installing Charts

Install charts from various sources:

```python
import asyncio
from helmpy import Configuration, Install

async def install_examples():
    config = Configuration(namespace="default")
    install = Install(config)
    
    # From OCI registry
    await install.run(
        release_name="my-nginx",
        chart_path="oci://registry-1.docker.io/bitnamicharts/nginx",
        version="18.2.5"
    )
    
    # From local path
    await install.run(
        release_name="local-chart",
        chart_path="./charts/mychart"
    )
    
    # From HTTP(S) URL
    await install.run(
        release_name="remote-chart",
        chart_path="https://example.com/charts/mychart-1.0.0.tgz"
    )
    
    # With custom values
    await install.run(
        release_name="custom-app",
        chart_path="oci://example.com/charts/app",
        values={
            "replicaCount": 3,
            "image": {"tag": "v2.0.0"},
            "resources": {
                "limits": {"cpu": "1000m", "memory": "1Gi"}
            }
        },
        create_namespace=True,
        wait=True,
        timeout=600
    )

asyncio.run(install_examples())
```

### Upgrading Releases

```python
from helmpy import Configuration, Upgrade

async def upgrade_release():
    config = Configuration(namespace="default")
    upgrade = Upgrade(config)
    
    result = await upgrade.run(
        release_name="my-nginx",
        chart_path="oci://registry-1.docker.io/bitnamicharts/nginx",
        version="18.2.6",
        values={"replicaCount": 5}
    )
    
    print(f"Upgraded to revision: {result['version']}")

asyncio.run(upgrade_release())
```

### Listing Releases

```python
from helmpy.actions import List

async def list_releases():
    config = Configuration(namespace="default")
    list_action = List(config)
    
    # List deployed releases
    releases = await list_action.run(all=False)
    
    # List all releases (including failed, pending, etc.)
    all_releases = await list_action.run(all=True)
    
    for release in releases:
        print(f"{release['name']}: {release['status']}")

asyncio.run(list_releases())
```

### Checking Status

```python
from helmpy.actions import Status

async def check_status():
    config = Configuration(namespace="default")
    status = Status(config)
    
    result = await status.run(release_name="my-nginx")
    
    print(f"Name: {result['name']}")
    print(f"Namespace: {result['namespace']}")
    print(f"Status: {result['info']['status']}")
    print(f"Version: {result['version']}")

asyncio.run(check_status())
```

### Rolling Back

```python
from helmpy.actions import Rollback

async def rollback_release():
    config = Configuration(namespace="default")
    rollback = Rollback(config)
    
    # Rollback to previous version
    result = await rollback.run(
        release_name="my-nginx",
        revision=0  # 0 means previous revision
    )
    
    # Rollback to specific revision
    result = await rollback.run(
        release_name="my-nginx",
        revision=3
    )

asyncio.run(rollback_release())
```

### Getting Values

```python
from helmpy.actions import GetValues

async def get_values():
    config = Configuration(namespace="default")
    get_values = GetValues(config)
    
    # Get user-supplied values only
    values = await get_values.run(release_name="my-nginx")
    
    # Get all values (computed)
    all_values = await get_values.run(
        release_name="my-nginx",
        all_values=True
    )

asyncio.run(get_values())
```

### Viewing History

```python
from helmpy.actions import History

async def view_history():
    config = Configuration(namespace="default")
    history = History(config)
    
    revisions = await history.run(release_name="my-nginx")
    
    for rev in revisions:
        print(f"Revision {rev['revision']}: {rev['status']}")

asyncio.run(view_history())
```

### Uninstalling

```python
from helmpy import Configuration, Uninstall

async def uninstall_release():
    config = Configuration(namespace="default")
    uninstall = Uninstall(config)
    
    result = await uninstall.run(
        release_name="my-nginx",
        wait=True,
        timeout=300
    )
    
    print(f"Uninstalled: {result['release']['name']}")

asyncio.run(uninstall_release())
```

## Chart Operations

### Pulling Charts

```python
from helmpy.chart import Pull

async def pull_chart():
    config = Configuration()
    pull = Pull(config)
    
    await pull.run(
        chart_ref="oci://registry-1.docker.io/bitnamicharts/nginx",
        dest_dir="./charts"
    )

asyncio.run(pull_chart())
```

### Showing Chart Info

```python
from helmpy.chart import Show

async def show_chart():
    config = Configuration()
    show = Show(config)
    
    # Show chart metadata
    chart_info = await show.chart("./charts/mychart")
    
    # Show chart values
    values_info = await show.values("./charts/mychart")

asyncio.run(show_chart())
```

### Testing Charts

```python
from helmpy.chart import Test

async def test_chart():
    config = Configuration(namespace="default")
    test = Test(config)
    
    result = await test.run(release_name="my-nginx")
    print(result)

asyncio.run(test_chart())
```

### Linting Charts

```python
from helmpy.chart import Lint

async def lint_chart():
    config = Configuration()
    lint = Lint(config)
    
    result = await lint.run(chart_path="./charts/mychart")
    print(result)

asyncio.run(lint_chart())
```

### Packaging Charts

```python
from helmpy.chart import Package

async def package_chart():
    config = Configuration()
    package = Package(config)
    
    result = await package.run(
        chart_path="./charts/mychart",
        dest_dir="./dist"
    )
    
    print(f"Packaged: {result}")

asyncio.run(package_chart())
```

## Repository Management

### Adding Repositories

```python
from helmpy.repo import RepoAdd

async def add_repository():
    config = Configuration()
    repo_add = RepoAdd(config)
    
    # Add public repository
    await repo_add.run(
        name="bitnami",
        url="https://charts.bitnami.com/bitnami"
    )
    
    # Add with authentication
    await repo_add.run(
        name="private-repo",
        url="https://charts.example.com",
        username="user",
        password="pass"
    )

asyncio.run(add_repository())
```

### Updating Repositories

```python
from helmpy.repo import RepoUpdate

async def update_repos():
    config = Configuration()
    repo_update = RepoUpdate(config)
    
    # Update all repositories
    await repo_update.run()
    
    # Update specific repository
    await repo_update.run(name="bitnami")

asyncio.run(update_repos())
```

### Listing Repositories

```python
from helmpy.repo import RepoList

async def list_repos():
    config = Configuration()
    repo_list = RepoList(config)
    
    repos = await repo_list.run()
    
    for repo in repos:
        print(f"{repo['name']}: {repo['url']}")

asyncio.run(list_repos())
```

### Removing Repositories

```python
from helmpy.repo import RepoRemove

async def remove_repo():
    config = Configuration()
    repo_remove = RepoRemove(config)
    
    await repo_remove.run(name="bitnami")

asyncio.run(remove_repo())
```

## Error Handling

```python
from helmpy import Configuration, Install
from helmpy.exceptions import HelmError, InstallError

async def safe_install():
    config = Configuration(namespace="default")
    install = Install(config)
    
    try:
        result = await install.run(
            release_name="my-app",
            chart_path="./charts/myapp",
            wait=True
        )
        print(f"✅ Success: {result['name']}")
    except InstallError as e:
        print(f"❌ Install failed: {e}")
    except HelmError as e:
        print(f"❌ Helm error: {e}")

asyncio.run(safe_install())
```

## Concurrent Operations

Execute multiple Helm operations in parallel:

```python
import asyncio
from helmpy import Configuration, Install

async def install_multiple_charts():
    config = Configuration(namespace="default")
    install = Install(config)
    
    # Install 3 charts concurrently
    results = await asyncio.gather(
        install.run("app-1", "oci://example.com/charts/app1"),
        install.run("app-2", "oci://example.com/charts/app2"),
        install.run("app-3", "oci://example.com/charts/app3"),
        return_exceptions=True
    )
    
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"❌ app-{i} failed: {result}")
        else:
            print(f"✅ app-{i} installed")

asyncio.run(install_multiple_charts())
```

## Next Steps

- [API Reference](api/actions) - Complete API documentation
- [Examples](examples/chart-install) - More practical examples
- [Architecture](architecture/helmpy-architecture) - Understanding helmpy internals
