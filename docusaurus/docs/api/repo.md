---
sidebar_position: 3
---

# Repository API

Repository management operations for Helm chart repositories.

## RepoAdd

Helm repo add action.

Adds a chart repository to the local configuration.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> repo_add = RepoAdd(config)
>>> asyncio.run(repo_add.run("stable", "https://charts.helm.sh/stable"))
>>> # With authentication
>>> asyncio.run(repo_add.run(
...     "private-repo",
...     "https://charts.example.com",
...     username="user",
...     password="pass"
... ))
```

### Methods

#### `run(self, name: 'str', url: 'str', username: 'str | None' = None, password: 'str | None' = None, insecure_skip_tls_verify: 'bool' = False, pass_credentials_all: 'bool' = False, cert_file: 'str | None' = None, key_file: 'str | None' = None, ca_file: 'str | None' = None) -> 'None'`

Add a chart repository asynchronously.

Args:
    name: Repository name
    url: Repository URL
    username: Username for authentication
    password: Password for authentication
    insecure_skip_tls_verify: Skip TLS certificate verification
    pass_credentials_all: Pass credentials to all domains
    cert_file: Path to TLS certificate file
    key_file: Path to TLS key file
    ca_file: Path to CA bundle file

Raises:
    RegistryError: If adding the repository fails


## RepoRemove

Helm repo remove action.

Removes a chart repository from the local configuration.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> repo_remove = RepoRemove(config)
>>> asyncio.run(repo_remove.run("stable"))
```

### Methods

#### `run(self, name: 'str') -> 'None'`

Remove a chart repository asynchronously.

Args:
    name: Repository name to remove

Raises:
    RegistryError: If removing the repository fails


## RepoList

Helm repo list action.

Lists all configured chart repositories.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> repo_list = RepoList(config)
>>> repos = asyncio.run(repo_list.run())
>>> for repo in repos:
...     print(f"{repo['name']}: {repo['url']}")
```

### Methods

#### `run(self) -> 'list[dict[str, Any]]'`

List configured repositories asynchronously.

Returns:
    List of repository dictionaries with name, url, and other fields

Raises:
    RegistryError: If listing repositories fails


## RepoUpdate

Helm repo update action.

Updates the local cache of chart repositories.

Args:
    config: Helm configuration object

Example:

```python
>>> import asyncio
>>> config = Configuration()
>>> repo_update = RepoUpdate(config)
>>> # Update all repositories
>>> asyncio.run(repo_update.run())
>>> # Update specific repository
>>> asyncio.run(repo_update.run("stable"))
```

### Methods

#### `run(self, name: 'str | None' = None) -> 'None'`

Update repository indexes asynchronously.

Args:
    name: Optional repository name to update. If not provided,
          updates all repositories.

Raises:
    RegistryError: If updating fails
