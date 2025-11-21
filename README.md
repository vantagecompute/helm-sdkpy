<div align="center">

# helmpy

Python bindings for Helm - The Kubernetes Package Manager

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)

</div>

Python bindings for the Helm v4 Go library. Ships with a self-contained Go shim that bundles the native Helm runtime—no system dependencies required.

## ✨ Features

- 🚀 **Complete Helm API** - Full access to Helm v4 functionality
- 📦 **Self-Contained** - No system dependencies required
- 🔒 **Type-Safe** - Python type hints for better IDE support
- 🐍 **Pythonic API** - Intuitive, object-oriented interface
- 🎯 **Production Ready** - Based on official Helm Go libraries

## 🚀 Quick Start

### Installation

```bash
pip install helmpy
```

### Basic Usage

```python
import helmpy

# Create a configuration
config = helmpy.Configuration(namespace="default")

# Install a chart from a local path
install = helmpy.Install(config)
result = install.run(
    release_name="my-nginx",
    chart_path="./nginx-chart",
    values={"replicaCount": 3}
)
print(f"Installed: {result['name']}")

# Install a chart from an OCI registry
result = install.run(
    release_name="my-app",
    chart_path="oci://ghcr.io/nginxinc/charts/nginx-ingress",
    values={"controller": {"service": {"type": "LoadBalancer"}}}
)
print(f"Installed: {result['name']}")

# Install a chart from an HTTPS URL
result = install.run(
    release_name="my-release",
    chart_path="https://charts.bitnami.com/bitnami/nginx-15.0.0.tgz",
    values={"replicaCount": 2}
)
print(f"Installed: {result['name']}")

# List releases
list_action = helmpy.List(config)
releases = list_action.run(all=True)
for release in releases:
    print(f"Release: {release['name']}")

# Upgrade a release
upgrade = helmpy.Upgrade(config)
result = upgrade.run(
    release_name="my-nginx",
    chart_path="./nginx-chart",
    values={"replicaCount": 5}
)

# Uninstall a release
uninstall = helmpy.Uninstall(config)
result = uninstall.run("my-nginx")
```

## 📖 Chart Path Formats

helmpy supports multiple chart location formats:

### Local Paths
Point to a chart directory or packaged chart (.tgz) on your local filesystem:
```python
chart_path="./nginx-chart"           # Local directory
chart_path="/path/to/mychart"        # Absolute path
chart_path="./mychart-1.0.0.tgz"     # Packaged chart
```

### OCI Registries
Reference charts stored in OCI-compatible container registries:
```python
chart_path="oci://ghcr.io/nginxinc/charts/nginx-ingress"
chart_path="oci://registry.example.com/charts/myapp"
```

### HTTP/HTTPS URLs
Download charts directly from web servers:
```python
chart_path="https://charts.bitnami.com/bitnami/nginx-15.0.0.tgz"
chart_path="https://example.com/charts/myapp-1.2.3.tgz"
```

## 📖 API Overview

### Core Actions

- **Configuration** - Manage Helm configuration and Kubernetes connection
- **Install** - Install charts to Kubernetes
- **Upgrade** - Upgrade existing releases
- **Uninstall** - Remove releases from cluster
- **List** - List deployed releases
- **Status** - Get release status information
- **Rollback** - Rollback to previous release versions
- **GetValues** - Retrieve release values
- **History** - View release history

### Chart Operations

- **Pull** - Download charts from repositories
- **Show** - Display chart information and values
- **Test** - Run release tests
- **Lint** - Validate charts for errors
- **Package** - Package charts into archives

## 🛠️ Development

### Prerequisites

- Python 3.12+
- Docker (for building the native library)
- [just](https://github.com/casey/just) task runner (optional but recommended)

### Building from Source

```bash
git clone https://github.com/vantagecompute/helmpy.git
cd helmpy

# Build native library using Docker
just build-lib

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run test suite
just unit

# Run linting
just lint

# Run type checking
just typecheck
```

### Project Commands

The project uses [just](https://github.com/casey/just) for task automation:

```bash
# Install just
sudo snap install just --classic
```

Available commands:
- `just build-lib` - Build native library (Docker)
- `just unit` - Run tests with coverage
- `just lint` - Check code style
- `just typecheck` - Run static type checking
- `just fmt` - Format code

## 📝 Examples

See the [examples/](examples/) directory for more usage examples.

## 🏗️ Architecture

helmpy follows the same architecture as [dqlitepy](https://github.com/vantagecompute/dqlitepy):

1. **Go Shim Layer** - Exposes Helm v4 API via C FFI
2. **Python FFI** - CFFI bindings to Go shared library
3. **Python API** - Pythonic wrapper classes

This ensures type safety, excellent performance, and seamless integration with the official Helm libraries.

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2025 Vantage Compute

## 🤝 Contributing

Contributions welcome! Please ensure:
- Code follows existing style (ruff formatting)
- Tests pass and coverage is maintained
- Type hints are included
- Documentation is updated

## 💬 Support

- [GitHub Issues](https://github.com/vantagecompute/helmpy/issues) - Bug reports and feature requests
- [Examples](examples/) - Sample code and use cases
