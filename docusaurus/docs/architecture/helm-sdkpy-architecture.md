---
sidebar_position: 1
---

# helm-sdkpy Architecture

Overview of helm-sdkpy's architecture and design.

## High-Level Architecture

helm-sdkpy provides Python bindings for Helm v4 through a multi-layer architecture:

```
┌─────────────────────────────────────┐
│     Python Application              │
│  (async/await, type hints)          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Python Layer (helm-sdkpy)           │
│  - Configuration                    │
│  - Actions (Install, Upgrade, etc.) │
│  - Chart Operations                 │
│  - Repository Management            │
└──────────────┬──────────────────────┘
               │ asyncio.to_thread()
┌──────────────▼──────────────────────┐
│     FFI Layer (CFFI)                │
│  - C function bindings              │
│  - Type marshalling                 │
│  - Error handling                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Go Shim Layer                   │
│  - C exports                        │
│  - Helm v4 Go API calls             │
│  - State management                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Helm v4 Go Library              │
│  helm.sh/helm/v4/pkg/action         │
│  helm.sh/helm/v4/pkg/chart          │
│  helm.sh/helm/v4/pkg/cli            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Kubernetes API                  │
└─────────────────────────────────────┘
```

## Components

### Python Layer

**Location**: `helm_sdkpy/`

The Python layer provides a Pythonic, async/await interface to Helm:

- **Configuration**: Manages Kubernetes connection and Helm settings
- **Actions**: Core Helm operations (Install, Upgrade, Uninstall, etc.)
- **Chart**: Chart operations (Pull, Show, Test, Lint, Package)
- **Repo**: Repository management (Add, Remove, List, Update)
- **Exceptions**: Typed exception hierarchy

All operations are async, using `asyncio.to_thread()` to wrap blocking Go calls.

### FFI Layer

**Location**: `helm_sdkpy/_ffi.py`

Uses CFFI to bridge Python and the Go shared library:

- Defines C function signatures
- Handles type conversion (Python ↔ C)
- Manages library loading
- Provides error checking

### Go Shim Layer

**Location**: `go/shim/`

A thin Go layer that:

- Exports C-compatible functions
- Calls Helm v4 Go APIs
- Manages Helm configuration state
- Handles JSON serialization
- Provides error reporting

Key functions:
- `helm-sdkpy_config_create()` - Initialize Helm configuration
- `helm-sdkpy_install()` - Install a chart
- `helm-sdkpy_upgrade()` - Upgrade a release
- `helm-sdkpy_list()` - List releases
- etc.

### Helm v4 Library

Official Helm v4 Go library:
- `helm.sh/helm/v4/pkg/action` - Helm actions
- `helm.sh/helm/v4/pkg/chart` - Chart operations
- `helm.sh/helm/v4/pkg/cli` - CLI environment

## Data Flow

### Install Operation Example

1. **Python**: User calls `await install.run(...)`
2. **Python**: `asyncio.to_thread()` schedules blocking call
3. **FFI**: Convert Python types to C types
4. **FFI**: Call `helm-sdkpy_install()` in shared library
5. **Go Shim**: Receive C call, unmarshal parameters
6. **Go Shim**: Create Helm `action.Install` client
7. **Go Shim**: Call `client.Run(chart, values)`
8. **Helm**: Execute Kubernetes operations
9. **Helm**: Return release info
10. **Go Shim**: Marshal result to JSON
11. **Go Shim**: Return JSON string via C
12. **FFI**: Convert C string to Python
13. **FFI**: Parse JSON to Python dict
14. **Python**: Return result to user

## Async Architecture

All helm-sdkpy operations are async to prevent blocking:

```python
# Blocking Go call wrapped in asyncio.to_thread()
async def run(self, ...):
    def _install():
        # C FFI call (blocking)
        result = lib.helm-sdkpy_install(...)
        return parse_json(result)
    
    # Run in thread pool
    return await asyncio.to_thread(_install)
```

This allows:
- Concurrent Helm operations
- Non-blocking event loops
- Integration with async frameworks

## State Management

The Go shim maintains per-configuration state:

```go
type configState struct {
    cfg  *action.Configuration
    envs *cli.EnvSettings
    mu   sync.Mutex
}
```

- `cfg`: Helm action configuration
- `envs`: Helm environment settings
- `mu`: Mutex for thread safety

Each Python `Configuration` object maps to one `configState` in Go.

## Error Handling

Errors flow through the stack:

1. **Helm/Kubernetes**: Returns Go error
2. **Go Shim**: Converts to string, stores in thread-local
3. **FFI**: Checks return code, retrieves error string
4. **Python**: Raises typed exception (InstallError, etc.)

Exception hierarchy:
```
HelmError
├── InstallError
├── UpgradeError
├── UninstallError
├── ReleaseError
├── RollbackError
├── ChartError
└── HelmLibraryNotFound
```

## Build System

helm-sdkpy uses Docker multi-stage builds to create platform-specific shared libraries:

1. **Builder stage**: Compiles Go code to `.so`/`.dylib`/`.dll`
2. **Extract stage**: Copies library to package
3. **Wheel**: Distributes library with Python code

Supported platforms:
- Linux (amd64, arm64)
- macOS (amd64, arm64)
- Windows (amd64)

## Thread Safety

- **Go Shim**: Uses mutexes to protect Helm configuration
- **Python**: Each `Configuration` is independent
- **Concurrent ops**: Safe with multiple configurations

## Performance Considerations

- **First call overhead**: Loading shared library
- **Serialization**: JSON marshalling for complex objects
- **Thread pool**: `asyncio.to_thread()` uses default executor
- **Memory**: Helm keeps release history in memory

## Dependencies

### Python
- CFFI for FFI bindings
- asyncio for concurrency

### Go
- Helm v4 (`helm.sh/helm/v4`)
- Kubernetes client-go

### Runtime
- Kubernetes cluster access
- kubectl configuration (optional)

## Design Decisions

### Why Async?

Helm operations can be long-running. Async prevents blocking the event loop and enables concurrent operations.

### Why Go Shim?

Direct Python-Go integration is complex. A C shim provides a stable ABI and simplifies distribution.

### Why CFFI?

CFFI provides robust, cross-platform FFI with good performance and maintainability.

### Why Helm v4?

Latest Helm version with improved APIs, better performance, and long-term support.

## Security

- **Credentials**: Uses kubeconfig, not stored by helm-sdkpy
- **Validation**: Input validation in Python and Go layers
- **Isolation**: Each Configuration is isolated
- **Permissions**: Inherits kubectl user permissions

## Future Enhancements

Potential improvements:
- Connection pooling
- Caching mechanisms
- Streaming logs
- Plugin support
- Custom backends

## Next Steps

- [Build & Packaging](build-packaging) - Build system details
- [API Reference](../api/actions) - Complete API documentation
- [Examples](../examples/chart-install) - Practical usage examples
