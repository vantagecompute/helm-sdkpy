---
sidebar_position: 2
---

# Chart API

Chart operations for managing Helm charts.

## Pull

Helm pull action.

Downloads a chart from a repository.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> pull = Pull(config)
>>> asyncio.run(pull.run("stable/nginx", dest_dir="./charts"))
```

### Methods

#### `run(self, chart_ref: 'str', dest_dir: 'str | None' = None, version: 'str | None' = None) -> 'None'`

Pull a chart asynchronously.

Args:
    chart_ref: Chart reference (e.g., "repo/chart" or "oci://...")
    dest_dir: Destination directory (default: current directory)
    version: Chart version to pull (e.g., "1.2.3"). If not specified, uses latest

Raises:
    ChartError: If pull fails


## Show

Helm show actions.

Shows information about a chart.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> show = Show(config)
>>> chart_yaml = asyncio.run(show.chart("./mychart"))
>>> values_yaml = asyncio.run(show.values("./mychart"))
```

### Methods

#### `chart(self, chart_path: 'str') -> 'str'`

Show the chart's Chart.yaml content asynchronously.

Args:
    chart_path: Path to the chart. Supports:
        - Local paths: "./mychart" or "/path/to/chart"
        - OCI registries: "oci://ghcr.io/org/chart"
        - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

Returns:
    Chart.yaml content as string

Raises:
    ChartError: If show fails

#### `values(self, chart_path: 'str') -> 'str'`

Show the chart's values.yaml content asynchronously.

Args:
    chart_path: Path to the chart. Supports:
        - Local paths: "./mychart" or "/path/to/chart"
        - OCI registries: "oci://ghcr.io/org/chart"
        - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

Returns:
    values.yaml content as string

Raises:
    ChartError: If show fails


## ReleaseTest

Helm test action.

Runs tests for a release.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> test = ReleaseTest(config)
>>> result = asyncio.run(test.run("my-release"))
```

### Methods

#### `run(self, release_name: 'str') -> 'dict[str, Any]'`

Run tests for a release asynchronously.

Args:
    release_name: Name of the release

Returns:
    Dictionary containing test results

Raises:
    ChartError: If test fails


## Lint

Helm lint action.

Lints a chart for errors.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> lint = Lint(config)
>>> result = asyncio.run(lint.run("./mychart"))
```

### Methods

#### `run(self, chart_path: 'str') -> 'dict[str, Any]'`

Lint a chart asynchronously.

Args:
    chart_path: Path to the chart. Supports:
        - Local paths: "./mychart" or "/path/to/chart"
        - OCI registries: "oci://ghcr.io/org/chart"
        - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

Returns:
    Dictionary containing lint results

Raises:
    ChartError: If lint operation fails


## Package

Helm package action.

Packages a chart into a versioned archive.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> package = Package(config)
>>> archive_path = asyncio.run(package.run("./mychart", dest_dir="./dist"))
```

### Methods

#### `run(self, chart_path: 'str', dest_dir: 'str | None' = None) -> 'str'`

Package a chart asynchronously.

Args:
    chart_path: Path to the chart directory to package
    dest_dir: Destination directory (default: current directory)

Returns:
    Path to the packaged chart archive

Raises:
    ChartError: If package fails
