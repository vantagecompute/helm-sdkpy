---
sidebar_position: 2
---

# Build & Packaging

How helm-sdkpy is built and packaged for distribution.

## Build Architecture

helm-sdkpy uses a Docker-based build system to create platform-specific wheels containing compiled Go libraries.

## Build Process

### 1. Go Library Compilation

The Go shim is compiled to a shared library:

```bash
# Linux
go build -buildmode=c-shared -o libhelm-sdkpy.so

# macOS
go build -buildmode=c-shared -o libhelm-sdkpy.dylib

# Windows
go build -buildmode=c-shared -o helm-sdkpy.dll
```

### 2. Docker Multi-Stage Build

**Dockerfile stages:**

```dockerfile
# Stage 1: Builder - Install tools
FROM ubuntu:24.04 AS builder
RUN apt-get update && apt-get install -y \
    build-essential curl git golang-1.23

# Stage 2: Go Build - Compile library
FROM builder AS go-build
WORKDIR /build/go
RUN go mod download
RUN go build -buildmode=c-shared -o libhelm-sdkpy.so

# Stage 3: Extract - Copy to package
FROM scratch AS extract
COPY --from=go-build /build/helm_sdkpy/_lib/ /helm_sdkpy/_lib/
```

### 3. Python Wheel Creation

The wheel includes:
- Python source code (`helm_sdkpy/*.py`)
- Compiled shared library (`helm_sdkpy/_lib/<platform>/libhelm-sdkpy.*`)
- Metadata (`pyproject.toml`, `README.md`, etc.)

```bash
# Build wheel
uv build

# Produces:
# dist/helm-sdkpy-X.Y.Z-py3-none-any.whl
# dist/helm-sdkpy-X.Y.Z.tar.gz
```

## Directory Structure

```
helm_sdkpy/
├── helm_sdkpy/                    # Python package
│   ├── __init__.py
│   ├── actions.py
│   ├── chart.py
│   ├── repo.py
│   ├── _ffi.py
│   ├── exceptions.py
│   └── _lib/                  # Compiled libraries
│       ├── linux-amd64/
│       │   └── libhelm-sdkpy.so
│       ├── linux-arm64/
│       │   └── libhelm-sdkpy.so
│       ├── darwin-amd64/
│       │   └── libhelm-sdkpy.dylib
│       ├── darwin-arm64/
│       │   └── libhelm-sdkpy.dylib
│       └── windows-amd64/
│           └── helm-sdkpy.dll
├── go/                        # Go shim
│   ├── go.mod
│   ├── go.sum
│   └── shim/
│       └── main.go
├── scripts/
│   └── build_wheel_docker.sh
├── Dockerfile
└── pyproject.toml
```

## Build Scripts

### build_wheel_docker.sh

Main build script that:
1. Builds Docker image
2. Compiles Go library inside Docker
3. Extracts library to `helm_sdkpy/_lib/`
4. Builds Python wheel

```bash
./scripts/build_wheel_docker.sh
```

### Platform Detection

The Python package detects the platform at runtime:

```python
# helm_sdkpy/_ffi.py
system = platform.system()
machine = platform.machine()

if system == "Linux":
    lib_name = "libhelm-sdkpy.so"
    platform_dir = f"linux-{machine}"
elif system == "Darwin":
    lib_name = "libhelm-sdkpy.dylib"
    platform_dir = f"darwin-{machine}"
elif system == "Windows":
    lib_name = "helm-sdkpy.dll"
    platform_dir = f"windows-{machine}"
```

## Development Build

For local development:

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/vantagecompute/helm-sdkpy.git
cd helm-sdkpy

# Install dependencies
uv sync

# Build native library
just build-wheel

# Or manually with Docker
./scripts/build_wheel_docker.sh

# Install in development mode
uv pip install -e .
```

## Just Commands

The project uses `just` for task automation:

```bash
# Build wheel with Docker
just build-wheel

# Run tests
just unit
just integration
just coverage-all

# Code quality
just lint
just fmt
just typecheck

# Documentation
just docs-dev
just docs-build
```

## Dependencies

### Build Dependencies

**Go:**
- Go 1.23+
- Helm v4 library (`helm.sh/helm/v4`)
- Kubernetes client-go

**Python:**
- Python 3.12+
- uv (package manager)
- CFFI

**System:**
- Docker (for builds)
- Build tools (gcc, make, etc.)

### Runtime Dependencies

**Python packages:**
- cffi

**System libraries:**
- libc (glibc on Linux, libc++ on macOS)

## CI/CD Pipeline

### GitHub Actions Workflow

**`.github/workflows/publish.yml`:**

```yaml
jobs:
  build:
    - Set up Python
    - Install system dependencies
    - Build Python package
    - Upload build artifacts

  test-install:
    - Download artifacts
    - Test installation on multiple Python versions

  publish-pypi:
    - Publish to PyPI (on tags)

  create-release:
    - Create GitHub release
    - Attach wheel and source dist
```

## Publishing

### PyPI Release

```bash
# Tag version
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions automatically:
# 1. Builds wheel
# 2. Runs tests
# 3. Publishes to PyPI
# 4. Creates GitHub release
```

### Manual Publish

```bash
# Build
uv build

# Publish to PyPI
uv publish

# Or to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/
```

## Versioning

helm-sdkpy uses semantic versioning:

- **Major**: Breaking API changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes

Version is defined in `pyproject.toml`:

```toml
[project]
name = "helm-sdkpy"
version = "0.1.0"
```

## Platform Support

### Tested Platforms

- **Linux**: Ubuntu 24.04 (amd64, arm64)
- **macOS**: macOS 13+ (amd64, arm64/Apple Silicon)
- **Windows**: Windows 11 (amd64)

### Python Versions

- Python 3.12
- Python 3.13

## Troubleshooting Build Issues

### Docker build fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker build --no-cache -f Dockerfile .
```

### Library not found at runtime

```bash
# Check library exists
ls -la helm_sdkpy/_lib/

# Set library path explicitly
export HELMPY_LIBRARY_PATH=/path/to/libhelm-sdkpy.so
```

### Go compilation errors

```bash
# Update Go modules
cd go
go mod tidy
go mod download

# Check Go version
go version  # Should be 1.23+
```

## Next Steps

- [Architecture Overview](helm-sdkpy-architecture) - System design
- [API Reference](../api/actions) - API documentation
