---
sidebar_position: 4
---

# Exceptions

## Exception Hierarchy

```
HelmError (base)
├── InstallError
├── UpgradeError
├── UninstallError
├── ReleaseError
├── RollbackError
├── ChartError
└── HelmLibraryNotFound
```

## `ChartError`

Raised when there's an error with chart operations.

## `ConfigurationError`

Raised when there's an error in Helm configuration.

## `HelmError`

Base exception for all Helm errors.

## `HelmLibraryNotFound`

Raised when the Helm shared library cannot be found.

## `InstallError`

Raised when chart installation fails.

## `RegistryError`

Raised when there's an error with registry operations.

## `ReleaseError`

Raised when there's an error with release operations.

## `RollbackError`

Raised when rollback fails.

## `UninstallError`

Raised when chart uninstallation fails.

## `UpgradeError`

Raised when chart upgrade fails.

## `ValidationError`

Raised when validation fails.
