---
sidebar_position: 2
---

# Quick Start

Get up and running with helmpy in minutes.

## Install helmpy

```bash
pip install helmpy
```

## Basic Usage

### 1. Install a Chart

```python
import asyncio
from helmpy import Configuration, Install

async def install_chart():
    # Create configuration
    config = Configuration(namespace="default")
    
    # Create install action
    install = Install(config)
    
    # Install nginx chart
    result = await install.run(
        release_name="my-nginx",
        chart_path="oci://registry-1.docker.io/bitnamicharts/nginx",
        version="18.2.5",
        create_namespace=True,
        wait=True
    )
    
    print(f"✅ Installed: {result['name']}")

asyncio.run(install_chart())
```

### 2. List Releases

```python
import asyncio
from helmpy import Configuration
from helmpy.actions import List

async def list_releases():
    config = Configuration(namespace="default")
    list_action = List(config)
    
    releases = await list_action.run(all=False)
    
    for release in releases:
        print(f"📦 {release['name']}: {release['status']}")

asyncio.run(list_releases())
```

### 3. Upgrade a Release

```python
import asyncio
from helmpy import Configuration, Upgrade

async def upgrade_release():
    config = Configuration(namespace="default")
    upgrade = Upgrade(config)
    
    result = await upgrade.run(
        release_name="my-nginx",
        chart_path="oci://registry-1.docker.io/bitnamicharts/nginx",
        version="18.2.6",
        values={"replicaCount": 3}
    )
    
    print(f"✅ Upgraded to version: {result['version']}")

asyncio.run(upgrade_release())
```

### 4. Check Release Status

```python
import asyncio
from helmpy import Configuration
from helmpy.actions import Status

async def check_status():
    config = Configuration(namespace="default")
    status = Status(config)
    
    result = await status.run(release_name="my-nginx")
    
    print(f"Status: {result['info']['status']}")
    print(f"Version: {result['version']}")

asyncio.run(check_status())
```

### 5. Uninstall a Release

```python
import asyncio
from helmpy import Configuration, Uninstall

async def uninstall_release():
    config = Configuration(namespace="default")
    uninstall = Uninstall(config)
    
    result = await uninstall.run(
        release_name="my-nginx",
        wait=True
    )
    
    print(f"✅ Uninstalled: {result['release']['name']}")

asyncio.run(uninstall_release())
```

## Concurrent Operations

Run multiple operations in parallel using `asyncio.gather`:

```python
import asyncio
from helmpy import Configuration, Install

async def install_multiple():
    config = Configuration(namespace="default")
    install = Install(config)
    
    # Install multiple charts concurrently
    results = await asyncio.gather(
        install.run("nginx-1", "oci://registry-1.docker.io/bitnamicharts/nginx"),
        install.run("nginx-2", "oci://registry-1.docker.io/bitnamicharts/nginx"),
        install.run("nginx-3", "oci://registry-1.docker.io/bitnamicharts/nginx"),
    )
    
    for result in results:
        print(f"✅ Installed: {result['name']}")

asyncio.run(install_multiple())
```

## Working with Values

### Passing Values

```python
values = {
    "replicaCount": 3,
    "image": {
        "tag": "1.25.0"
    },
    "service": {
        "type": "LoadBalancer",
        "port": 80
    }
}

result = await install.run(
    release_name="my-app",
    chart_path="./mychart",
    values=values
)
```

### Getting Values

```python
from helmpy.actions import GetValues

config = Configuration(namespace="default")
get_values = GetValues(config)

values = await get_values.run(
    release_name="my-app",
    all_values=True
)

print(values)
```

## Repository Management

```python
from helmpy.repo import RepoAdd, RepoUpdate, RepoList

async def manage_repos():
    config = Configuration()
    
    # Add a repository
    repo_add = RepoAdd(config)
    await repo_add.run(
        name="bitnami",
        url="https://charts.bitnami.com/bitnami"
    )
    
    # Update repositories
    repo_update = RepoUpdate(config)
    await repo_update.run()
    
    # List repositories
    repo_list = RepoList(config)
    repos = await repo_list.run()
    
    for repo in repos:
        print(f"📚 {repo['name']}: {repo['url']}")

asyncio.run(manage_repos())
```

## Next Steps

- [Full Usage Guide](usage)
- [API Reference](api/actions)
- [Examples](examples/chart-install)
- [Architecture](architecture/helmpy-architecture)
