---
sidebar_position: 1
---

# Installation

## Prerequisites

- Python 3.12 or higher
- A Kubernetes cluster (for runtime operations)
- kubectl configured (optional)

## Install via pip

```bash
pip install helmpy
```

## Install via uv

```bash
uv add helmpy
```

## Verify Installation

```python
import asyncio
from helmpy import Configuration

async def main():
    config = Configuration(namespace="default")
    print("helmpy is installed and ready!")

asyncio.run(main())
```

## Kubernetes Configuration

helmpy uses your kubeconfig to connect to Kubernetes clusters. By default, it uses:

1. The `KUBECONFIG` environment variable
2. `~/.kube/config` if no environment variable is set

You can also specify a custom kubeconfig path:

```python
from helmpy import Configuration

config = Configuration(
    namespace="my-namespace",
    kubeconfig="/path/to/kubeconfig",
    kubecontext="my-context"
)
```

## Development Installation

For development, clone the repository and install with development dependencies:

```bash
git clone https://github.com/vantagecompute/helmpy.git
cd helmpy
uv sync
```

## Docker

The project includes Docker support for building the native library. See [Architecture](architecture/build-packaging) for details.

## Next Steps

- [Quick Start Guide](quickstart)
- [Usage Examples](usage)
- [API Reference](api/actions)
