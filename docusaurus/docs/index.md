# helmpy

**Python bindings for Helm - Kubernetes package manager**

helmpy provides async Python bindings for Helm v4, allowing you to programmatically manage Kubernetes applications using Helm charts from Python.

## Features

- 🚀 **Full Helm v4 Support** - Complete access to Helm v4 actions and chart operations
- ⚡ **Async/Await** - All operations are async for non-blocking execution
- 🔧 **Type Safe** - Full type hints for excellent IDE support
- 🎯 **Simple API** - Pythonic interface to Helm functionality
- 📦 **Chart Management** - Install, upgrade, uninstall, and manage releases
- 🔍 **Repository Operations** - Add, update, and manage chart repositories
- 🛠️ **Chart Operations** - Pull, test, lint, and package charts

## Quick Example

```python
import asyncio
from helmpy import Configuration, Install

async def main():
    # Create a configuration
    config = Configuration(namespace="default")
    
    # Install a chart
    install = Install(config)
    result = await install.run(
        release_name="my-nginx",
        chart_path="oci://registry-1.docker.io/bitnamicharts/nginx",
        version="18.2.5",
        create_namespace=True,
        wait=True
    )
    
    print(f"Installed release: {result['name']}")

asyncio.run(main())
```

## Core Concepts

### Configuration

The `Configuration` class manages connection to your Kubernetes cluster and provides context for all Helm operations.

### Actions

Actions perform operations on Helm releases:
- **Install** - Install a new chart
- **Upgrade** - Upgrade an existing release
- **Uninstall** - Remove a release
- **List** - List releases
- **Status** - Get release status
- **Rollback** - Rollback to a previous revision
- **GetValues** - Get values from a release
- **History** - View release history

### Chart Operations

Chart operations work with Helm charts:
- **Pull** - Download a chart
- **Show** - Display chart information
- **Test** - Run chart tests
- **Lint** - Check chart for issues
- **Package** - Package a chart directory

### Repository Management

Manage Helm chart repositories:
- **RepoAdd** - Add a repository
- **RepoRemove** - Remove a repository
- **RepoList** - List repositories
- **RepoUpdate** - Update repository index

## Installation

```bash
pip install helmpy
```

## Requirements

- Python 3.12+
- Kubernetes cluster (for operations)
- kubectl configured (optional, can provide kubeconfig path)

## Next Steps

- [Installation Guide](installation) - Detailed installation instructions
- [Quick Start](quickstart) - Get started quickly
- [API Reference](api/actions) - Complete API documentation
- [Examples](examples/chart-install) - Practical usage examples

## License

Apache License 2.0 - See LICENSE file for details
