# Development Guide

This document provides detailed information for developers working on helmpy.

## Architecture

helmpy follows a three-layer architecture:

1. **Go Shim Layer** (`go/shim/main.go`)
   - Wraps Helm v4 Go API
   - Exposes C-compatible FFI functions
   - Handles memory management and error propagation
   - Thread-safe with mutex protection

2. **Python FFI Layer** (`helmpy/_ffi.py`)
   - Uses CFFI to interface with Go shared library
   - Handles library loading and discovery
   - Provides type conversion helpers
   - Manages error checking

3. **Python API Layer** (`helmpy/actions.py`, `helmpy/chart.py`)
   - Pythonic wrapper classes
   - Type hints for IDE support
   - Context manager support
   - Exception hierarchy

## Development Setup

### Prerequisites

- Python 3.12+
- Go 1.22+
- Docker (for building the native library)
- [just](https://github.com/casey/just) (recommended)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/vantagecompute/helmpy.git
cd helmpy

# Install Python dependencies
pip install -e ".[dev]"

# Build the native library
just build-lib

# Run tests
just unit
```

### Development Workflow

1. **Make code changes** to Python or Go files

2. **If you modified Go code**, rebuild the library:
   ```bash
   just build-lib
   ```

3. **Run tests**:
   ```bash
   just unit          # Run all tests with coverage
   just lint          # Check code style
   just typecheck     # Run static type checking
   ```

4. **Format code**:
   ```bash
   just fmt           # Auto-format Python code
   ```

## Building the Native Library

The Go shared library can be built in two ways:

### Docker Build (Recommended)

This ensures consistent builds across different platforms:

```bash
just build-lib
```

This runs a multi-stage Docker build that:
1. Sets up Go 1.22 build environment
2. Downloads Helm v4 and all dependencies
3. Compiles the Go shim to a shared library
4. Extracts the library to `helmpy/_lib/linux-amd64/`

### Local Build (Development)

For faster iteration during development:

```bash
cd go/shim
go build -buildmode=c-shared -o ../../helmpy/_lib/linux-amd64/libhelmpy.so main.go
```

Note: This requires Go 1.22+ and all dependencies to be available locally.

## Testing

### Running Tests

```bash
# Run all tests with coverage
just unit

# Run specific test file
pytest tests/test_basic.py -v

# Run with verbose output
pytest -vv
```

### Writing Tests

Tests are located in the `tests/` directory. Follow these guidelines:

1. **Import from top-level package**:
   ```python
   import helmpy
   from helmpy import Configuration, Install
   ```

2. **Use pytest fixtures** for common setup:
   ```python
   @pytest.fixture
   def config():
       return helmpy.Configuration(namespace="test")
   ```

3. **Test exception handling**:
   ```python
   def test_install_error():
       with pytest.raises(helmpy.InstallError):
           # Code that should raise
   ```

## Code Style

### Python

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
just fmt       # Auto-format code
just lint      # Check for issues
just typecheck # Run pyright
```

Configuration is in `pyproject.toml`:
- Line length: 100 characters
- Target: Python 3.12+
- Type checking with pyright

### Go

Follow standard Go conventions:
- Use `gofmt` for formatting
- Run `go vet` for issues
- Use meaningful variable names
- Add comments for exported functions

## Adding New Helm Actions

To add support for a new Helm action:

1. **Add FFI definition** in `helmpy/_ffi.py`:
   ```python
   ffi.cdef("""
       int helmpy_new_action(helmpy_handle handle, const char *param, char **result);
   """)
   ```

2. **Implement Go function** in `go/shim/main.go`:
   ```go
   //export helmpy_new_action
   func helmpy_new_action(handle C.helmpy_handle, param *C.char, result **C.char) C.int {
       // Implementation
   }
   ```

3. **Create Python wrapper** in `helmpy/actions.py` or `helmpy/chart.py`:
   ```python
   class NewAction:
       def __init__(self, config: Configuration):
           self.config = config
           self._lib = get_library()
       
       def run(self, param: str) -> Dict[str, Any]:
           # Implementation
   ```

4. **Export in `__init__.py`**:
   ```python
   from .actions import NewAction
   __all__ = [..., "NewAction"]
   ```

5. **Add tests** in `tests/`:
   ```python
   def test_new_action():
       assert NewAction is not None
   ```

## Release Process

1. Update version in:
   - `pyproject.toml`
   - `helmpy/__init__.py`
   - `go/shim/main.go` (versionCString)

2. Build and test:
   ```bash
   just build-lib
   just unit
   just lint
   just typecheck
   ```

3. Build wheel:
   ```bash
   ./scripts/build_wheel_docker.sh
   ```

4. Tag release:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## Troubleshooting

### Library Not Found

If you get `HelmLibraryNotFound`:

1. Check if library exists:
   ```bash
   ls -lh helmpy/_lib/linux-amd64/libhelmpy.so
   ```

2. Rebuild if missing:
   ```bash
   just build-lib
   ```

3. Check library dependencies:
   ```bash
   ldd helmpy/_lib/linux-amd64/libhelmpy.so
   ```

### Import Errors

If Python can't find the module:

1. Install in development mode:
   ```bash
   pip install -e .
   ```

2. Or set PYTHONPATH:
   ```bash
   export PYTHONPATH=/path/to/helmpy:$PYTHONPATH
   ```

### Go Build Errors

If Go build fails:

1. Check Go version:
   ```bash
   go version  # Should be 1.22+
   ```

2. Clean and retry:
   ```bash
   cd go
   go clean -cache
   go mod download
   go mod tidy
   ```

3. Check for API changes in Helm v4:
   ```bash
   cd /tmp
   git clone https://github.com/helm/helm
   # Check relevant action files
   ```

## Performance Considerations

- Go shared library is ~115MB (includes Helm and Kubernetes clients)
- First library load takes ~100ms
- Subsequent operations are fast (Go performance)
- Thread-safe: safe to use from multiple Python threads
- Memory: Each Configuration object allocates minimal memory

## Security

- Always validate chart sources
- Use RBAC to limit Kubernetes permissions
- Don't pass untrusted values to chart installations
- Keep Helm and Kubernetes clients updated
- Report security issues privately

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Run linting and tests
6. Submit a pull request

See CONTRIBUTING.md for detailed guidelines.
