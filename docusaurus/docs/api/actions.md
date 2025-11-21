---
sidebar_position: 1
---

# Actions API

Core Helm actions for managing releases and deployments.

## Configuration

Helm configuration for interacting with Kubernetes clusters.

This class manages the connection to a Kubernetes cluster and provides
the context for all Helm operations.

Args:
    namespace: Kubernetes namespace to operate in (default: "default")
    kubeconfig: Path to kubeconfig file (default: uses $KUBECONFIG or ~/.kube/config)
    kubecontext: Kubernetes context to use (default: current context)

Example:

```python
>>> import asyncio
>>> config = Configuration(namespace="my-namespace")
>>> install = Install(config)
>>> result = asyncio.run(install.run("my-release", "/path/to/chart"))
```

### Methods

#### `__enter__(self)`

Support for context manager.

#### `__exit__(self, exc_type, exc_val, exc_tb)`

Support for context manager.


## Install

Helm install action.

Installs a chart into a Kubernetes cluster.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> install = Install(config)
>>> result = asyncio.run(install.run("my-release", "./mychart", values={"replicas": 3}))
```

### Methods

#### `run(self, release_name: 'str', chart_path: 'str', values: 'dict[str, Any] | None' = None, version: 'str | None' = None, create_namespace: 'bool' = False, wait: 'bool' = True, timeout: 'int' = 300) -> 'dict[str, Any]'`

Install a chart asynchronously.

Args:
    release_name: Name of the release
    chart_path: Path to the chart. Supports:
        - Local paths: "./mychart" or "/path/to/chart"
        - OCI registries: "oci://ghcr.io/org/chart"
        - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
    values: Values to pass to the chart
    version: Chart version to install (e.g., "1.2.3"). If not specified, uses latest
    create_namespace: Create the release namespace if not present
    wait: Wait for all resources to be ready (default: True)
    timeout: Timeout in seconds for wait (default: 300)

Returns:
    Dictionary containing release information

Raises:
    InstallError: If installation fails


## Upgrade

Helm upgrade action.

Upgrades an existing release.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> upgrade = Upgrade(config)
>>> result = asyncio.run(upgrade.run("my-release", "./mychart", values={"replicas": 5}))
```

### Methods

#### `run(self, release_name: 'str', chart_path: 'str', values: 'dict[str, Any] | None' = None, version: 'str | None' = None) -> 'dict[str, Any]'`

Upgrade a release asynchronously.

Args:
    release_name: Name of the release
    chart_path: Path to the chart. Supports:
        - Local paths: "./mychart" or "/path/to/chart"
        - OCI registries: "oci://ghcr.io/org/chart"
        - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
    values: Values to pass to the chart
    version: Chart version to upgrade to (e.g., "1.2.3"). If not specified, uses latest

Returns:
    Dictionary containing release information

Raises:
    UpgradeError: If upgrade fails


## Uninstall

Helm uninstall action.

Uninstalls a release from the cluster.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> uninstall = Uninstall(config)
>>> result = asyncio.run(uninstall.run("my-release"))
```

### Methods

#### `run(self, release_name: 'str', wait: 'bool' = True, timeout: 'int' = 300) -> 'dict[str, Any]'`

Uninstall a release asynchronously.

Args:
    release_name: Name of the release
    wait: Wait for all resources to be deleted (default: True)
    timeout: Timeout in seconds for wait (default: 300)

Returns:
    Dictionary containing uninstall response

Raises:
    UninstallError: If uninstall fails


## List

Helm list action.

Lists releases in the cluster.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> list_action = List(config)
>>> releases = asyncio.run(list_action.run(all=True))
```

### Methods

#### `run(self, all: 'bool' = False) -> 'list[dict[str, Any]]'`

List releases asynchronously.

Args:
    all: Show all releases, not just deployed ones

Returns:
    List of release dictionaries

Raises:
    ReleaseError: If listing fails


## Status

Helm status action.

Gets the status of a release.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> status = Status(config)
>>> info = asyncio.run(status.run("my-release"))
```

### Methods

#### `run(self, release_name: 'str') -> 'dict[str, Any]'`

Get release status asynchronously.

Args:
    release_name: Name of the release

Returns:
    Dictionary containing release status

Raises:
    ReleaseError: If status check fails


## Rollback

Helm rollback action.

Rolls back a release to a previous revision.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> rollback = Rollback(config)
>>> result = asyncio.run(rollback.run("my-release", revision=2))
```

### Methods

#### `run(self, release_name: 'str', revision: 'int' = 0) -> 'dict[str, Any]'`

Rollback a release asynchronously.

Args:
    release_name: Name of the release
    revision: Revision to rollback to (0 = previous)

Returns:
    Dictionary containing rollback result

Raises:
    RollbackError: If rollback fails


## GetValues

Helm get values action.

Gets the values for a release.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> get_values = GetValues(config)
>>> values = asyncio.run(get_values.run("my-release", all=True))
```

### Methods

#### `run(self, release_name: 'str', all: 'bool' = False) -> 'dict[str, Any]'`

Get release values asynchronously.

Args:
    release_name: Name of the release
    all: Get all values, including computed values

Returns:
    Dictionary containing values

Raises:
    ReleaseError: If getting values fails


## History

Helm history action.

Gets the release history.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> history = History(config)
>>> revisions = asyncio.run(history.run("my-release"))
```

### Methods

#### `run(self, release_name: 'str') -> 'list[dict[str, Any]]'`

Get release history asynchronously.

Args:
    release_name: Name of the release

Returns:
    List of revision dictionaries

Raises:
    ReleaseError: If getting history fails
