---
sidebar_position: 6
---

# Error Handling

Learn how to handle errors robustly in helm-sdkpy applications.

## Exception Hierarchy

helm-sdkpy provides a hierarchy of exceptions:

```python
HelmError                    # Base exception
├── InstallError            # Installation failures
├── UpgradeError            # Upgrade failures
├── UninstallError          # Uninstall failures
├── RollbackError           # Rollback failures
├── NotFoundError           # Resource not found
├── AlreadyExistsError      # Resource already exists
├── ValidationError         # Validation failures
├── TimeoutError            # Operation timeout
└── RepoError               # Repository errors
```

## Basic Error Handling

Catch specific exceptions:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError, InstallError, NotFoundError

chart = Chart(
    name="nginx",
    repo="https://charts.bitnami.com/bitnami",
    chart="nginx"
)

try:
    result = chart.install(
        namespace="default",
        create_namespace=True,
        wait=True
    )
    print(f"✓ Installed: {result}")
    
except InstallError as e:
    print(f"Installation failed: {e}")
    # Handle installation failure
    
except NotFoundError as e:
    print(f"Chart not found: {e}")
    # Handle missing chart
    
except HelmError as e:
    print(f"Helm error: {e}")
    # Handle any other Helm error
```

## Install with Fallback

Try installation with fallback to defaults:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError

def install_with_fallback(name: str, chart: str, repo: str, values: dict):
    """Try installing with custom values, fall back to defaults."""
    
    chart_obj = Chart(name=name, repo=repo, chart=chart)
    
    # Try with custom values
    try:
        result = chart_obj.install(
            namespace="default",
            values=values,
            create_namespace=True,
            wait=True,
            timeout=300
        )
        print(f"✓ Installed with custom values")
        return result
        
    except HelmError as e:
        print(f"⚠ Custom values failed: {e}")
        print("Retrying with default values...")
        
        # Retry with defaults
        try:
            result = chart_obj.install(
                namespace="default",
                create_namespace=True,
                wait=True,
                timeout=300
            )
            print(f"✓ Installed with default values")
            return result
            
        except HelmError as e2:
            print(f"✗ Installation failed completely: {e2}")
            raise

# Usage
values = {"replicaCount": 100}  # May be too high
install_with_fallback("nginx", "nginx", "https://charts.bitnami.com/bitnami", values)
```

## Upgrade with Automatic Rollback

Handle upgrade failures with automatic rollback:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError, UpgradeError

def safe_upgrade(name: str, namespace: str, values: dict):
    """Upgrade with automatic rollback on failure."""
    
    chart = Chart(name=name)
    
    # Get current revision before upgrade
    try:
        history = chart.history(namespace=namespace)
        current_revision = len(history)
    except HelmError as e:
        print(f"Error getting history: {e}")
        current_revision = None
    
    # Attempt upgrade
    try:
        result = chart.upgrade(
            namespace=namespace,
            values=values,
            wait=True,
            timeout=600,
            atomic=True  # Auto-rollback on failure
        )
        print(f"✓ Upgrade successful")
        return result
        
    except UpgradeError as e:
        print(f"✗ Upgrade failed: {e}")
        
        # Atomic upgrade should have rolled back automatically
        # Verify rollback occurred
        if current_revision:
            try:
                new_history = chart.history(namespace=namespace)
                if len(new_history) > current_revision:
                    print("ℹ Automatic rollback completed")
                else:
                    print("⚠ Manual rollback may be required")
            except HelmError:
                pass
        
        raise

# Usage
safe_upgrade(
    "webapp",
    "production",
    {"replicaCount": 5, "image": {"tag": "v2.0.0"}}
)
```

## Install or Upgrade Pattern

Install if release doesn't exist, upgrade if it does:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError, NotFoundError

def install_or_upgrade(name: str, chart_name: str, repo: str,
                       namespace: str, values: dict = None):
    """Install or upgrade a chart based on existence."""
    
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    # Check if release exists
    try:
        status = chart.status(namespace=namespace)
        print(f"Release exists with status: {status}")
        
        # Release exists, upgrade it
        try:
            result = chart.upgrade(
                namespace=namespace,
                values=values or {},
                wait=True,
                atomic=True,
                timeout=600
            )
            print(f"✓ Upgraded release '{name}'")
            return ("upgraded", result)
            
        except HelmError as e:
            print(f"✗ Upgrade failed: {e}")
            raise
            
    except NotFoundError:
        # Release doesn't exist, install it
        print(f"Release not found, installing...")
        
        try:
            result = chart.install(
                namespace=namespace,
                values=values or {},
                create_namespace=True,
                wait=True,
                atomic=True,
                timeout=600
            )
            print(f"✓ Installed release '{name}'")
            return ("installed", result)
            
        except HelmError as e:
            print(f"✗ Installation failed: {e}")
            raise

# Usage
action, result = install_or_upgrade(
    "nginx",
    "nginx",
    "https://charts.bitnami.com/bitnami",
    "default",
    {"replicaCount": 3}
)
print(f"Action taken: {action}")
```

## Retry Logic

Implement retry logic for transient failures:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError
import time

def install_with_retry(name: str, chart: str, repo: str,
                       max_retries: int = 3, retry_delay: int = 5):
    """Install chart with retry logic."""
    
    chart_obj = Chart(name=name, repo=repo, chart=chart)
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            
            result = chart_obj.install(
                namespace="default",
                create_namespace=True,
                wait=True,
                timeout=300
            )
            
            print(f"✓ Installation successful on attempt {attempt + 1}")
            return result
            
        except HelmError as e:
            last_error = e
            print(f"⚠ Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"✗ All {max_retries} attempts failed")
    
    # All retries exhausted
    raise last_error

# Usage
install_with_retry("nginx", "nginx", "https://charts.bitnami.com/bitnami")
```

## Async Error Handling

Handle errors in async operations:

```python
import asyncio
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError

async def install_with_error_handling(name: str, chart: str, repo: str):
    """Install chart with comprehensive async error handling."""
    
    chart_obj = Chart(name=name, repo=repo, chart=chart)
    
    try:
        result = await chart_obj.install_async(
            namespace="default",
            create_namespace=True,
            wait=True,
            timeout=300
        )
        
        print(f"✓ Installed {name}")
        return (True, result)
        
    except asyncio.TimeoutError:
        print(f"✗ Installation of {name} timed out")
        return (False, "timeout")
        
    except HelmError as e:
        print(f"✗ Installation of {name} failed: {e}")
        return (False, str(e))
        
    except Exception as e:
        print(f"✗ Unexpected error installing {name}: {e}")
        return (False, str(e))

async def install_multiple_safe():
    """Install multiple charts with error handling."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    charts = [
        ("nginx", "nginx"),
        ("redis", "redis"),
        ("invalid", "nonexistent"),  # This will fail
    ]
    
    tasks = [
        install_with_error_handling(name, chart, repo_url)
        for name, chart in charts
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Analyze results
    successful = [name for (success, _), (name, _) in zip(results, charts) if success]
    failed = [name for (success, _), (name, _) in zip(results, charts) if not success]
    
    print(f"\n✓ Successful: {', '.join(successful)}")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")
    
    return results

asyncio.run(install_multiple_safe())
```

## Validation Before Operations

Validate before performing operations:

```python
from helm_sdkpy import Chart
from helm_sdkpy.repo import Repo
from helm_sdkpy.exceptions import HelmError, ValidationError

def validate_and_install(name: str, chart: str, repo_url: str,
                         namespace: str, values: dict):
    """Validate configuration before installation."""
    
    # Validate namespace name
    if not namespace or not namespace.islower():
        raise ValidationError("Namespace must be lowercase")
    
    # Validate release name
    if not name or len(name) > 53:
        raise ValidationError("Release name must be 1-53 characters")
    
    # Validate repository is accessible
    repo = Repo()
    try:
        repo.add(name="temp-repo", url=repo_url)
        repo.update()
        print("✓ Repository validated")
    except HelmError as e:
        raise ValidationError(f"Repository validation failed: {e}")
    finally:
        try:
            repo.remove(name="temp-repo")
        except HelmError:
            pass
    
    # Proceed with installation
    chart_obj = Chart(name=name, repo=repo_url, chart=chart)
    
    try:
        result = chart_obj.install(
            namespace=namespace,
            values=values,
            create_namespace=True,
            wait=True,
            timeout=600
        )
        print(f"✓ Installation successful")
        return result
        
    except HelmError as e:
        print(f"✗ Installation failed: {e}")
        raise

# Usage
try:
    validate_and_install(
        "my-app",
        "nginx",
        "https://charts.bitnami.com/bitnami",
        "production",
        {"replicaCount": 3}
    )
except ValidationError as e:
    print(f"Validation error: {e}")
except HelmError as e:
    print(f"Helm error: {e}")
```

## Complete Error Handling Example

Comprehensive error handling workflow:

```python
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import (
    HelmError, InstallError, UpgradeError, NotFoundError,
    ValidationError, TimeoutError
)
import sys
import time
from typing import Optional, Tuple

class ChartDeployer:
    def __init__(self, max_retries: int = 3, retry_delay: int = 5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def validate_inputs(self, name: str, namespace: str) -> None:
        """Validate input parameters."""
        if not name or len(name) > 53:
            raise ValidationError("Release name must be 1-53 characters")
        
        if not namespace or not namespace.replace('-', '').isalnum():
            raise ValidationError("Invalid namespace name")
    
    def deploy_chart(self, name: str, chart: str, repo: str,
                    namespace: str, values: dict = None) -> Tuple[bool, Optional[str]]:
        """Deploy chart with comprehensive error handling."""
        
        try:
            # Validate inputs
            self.validate_inputs(name, namespace)
            
        except ValidationError as e:
            print(f"✗ Validation failed: {e}")
            return (False, f"validation_error: {e}")
        
        chart_obj = Chart(name=name, repo=repo, chart=chart)
        
        # Try install or upgrade
        for attempt in range(self.max_retries):
            try:
                # Check if release exists
                try:
                    status = chart_obj.status(namespace=namespace)
                    operation = "upgrade"
                    
                    # Upgrade existing release
                    result = chart_obj.upgrade(
                        namespace=namespace,
                        values=values or {},
                        wait=True,
                        atomic=True,
                        timeout=600
                    )
                    
                except NotFoundError:
                    operation = "install"
                    
                    # Install new release
                    result = chart_obj.install(
                        namespace=namespace,
                        values=values or {},
                        create_namespace=True,
                        wait=True,
                        atomic=True,
                        timeout=600
                    )
                
                print(f"✓ Successfully {operation}ed '{name}' (attempt {attempt + 1})")
                return (True, result)
                
            except TimeoutError as e:
                print(f"⚠ Timeout on attempt {attempt + 1}: {e}")
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    return (False, f"timeout: {e}")
                
            except (InstallError, UpgradeError) as e:
                print(f"⚠ Operation failed on attempt {attempt + 1}: {e}")
                
                # Check if release is in bad state
                try:
                    status = chart_obj.status(namespace=namespace)
                    if status == "failed":
                        print("Release in failed state, cleaning up...")
                        chart_obj.uninstall(namespace=namespace, wait=True)
                except Exception:
                    pass
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    return (False, f"operation_failed: {e}")
                
            except HelmError as e:
                print(f"✗ Helm error: {e}")
                return (False, f"helm_error: {e}")
                
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
                return (False, f"unexpected_error: {e}")
        
        return (False, "max_retries_exceeded")
    
    def cleanup_on_error(self, name: str, namespace: str) -> bool:
        """Clean up failed release."""
        chart = Chart(name=name)
        
        try:
            status = chart.status(namespace=namespace)
            
            if status == "failed":
                print(f"Cleaning up failed release '{name}'...")
                chart.uninstall(namespace=namespace, wait=True)
                print(f"✓ Cleaned up '{name}'")
                return True
            
            return False
            
        except NotFoundError:
            print(f"Release '{name}' not found, nothing to clean up")
            return False
            
        except HelmError as e:
            print(f"✗ Cleanup failed: {e}")
            return False

def main():
    """Main deployment workflow with error handling."""
    
    deployer = ChartDeployer(max_retries=3, retry_delay=5)
    
    # Deploy chart
    success, result = deployer.deploy_chart(
        name="webapp",
        chart="nginx",
        repo="https://charts.bitnami.com/bitnami",
        namespace="production",
        values={"replicaCount": 3}
    )
    
    if success:
        print(f"\n✓ Deployment successful: {result}")
        sys.exit(0)
    else:
        print(f"\n✗ Deployment failed: {result}")
        
        # Attempt cleanup
        deployer.cleanup_on_error("webapp", "production")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Error Handling Best Practices

1. **Catch Specific Exceptions**: Handle specific exceptions before general ones
2. **Always Clean Up**: Ensure resources are cleaned up on errors
3. **Retry Transient Failures**: Implement retry logic for network issues
4. **Validate Early**: Validate inputs before expensive operations
5. **Log Errors**: Provide detailed error messages for debugging
6. **Use Atomic Operations**: Use `atomic=True` for automatic rollback
7. **Handle Timeouts**: Set appropriate timeouts and handle timeout errors
8. **Fallback Strategies**: Have fallback plans for critical operations

## Common Error Scenarios

### Chart Not Found
```python
try:
    chart.install(namespace="default")
except NotFoundError:
    print("Chart not found. Check repository and chart name.")
```

### Release Already Exists
```python
try:
    chart.install(namespace="default")
except AlreadyExistsError:
    print("Release already exists. Use upgrade instead.")
```

### Insufficient Resources
```python
try:
    chart.install(namespace="default", wait=True)
except TimeoutError:
    print("Installation timed out. May need more resources.")
```

## Next Steps

- [Installing Charts](chart-install) - Chart installation
- [Upgrading Charts](chart-upgrade) - Chart upgrades
- [Concurrent Operations](concurrent-operations) - Async patterns
- [Troubleshooting](../troubleshooting) - Common issues
