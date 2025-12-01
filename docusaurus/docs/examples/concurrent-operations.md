---
sidebar_position: 5
---

# Concurrent Operations

Learn how to perform Helm operations concurrently using async/await patterns.

## Basic Async Install

Perform asynchronous chart installation:

```python
import asyncio
from helm_sdkpy import Chart

async def install_chart():
    chart = Chart(
        name="nginx",
        repo="https://charts.bitnami.com/bitnami",
        chart="nginx"
    )
    
    result = await chart.install_async(
        namespace="default",
        create_namespace=True,
        wait=True
    )
    
    return result

# Run async function
result = asyncio.run(install_chart())
print(f"Installed: {result}")
```

## Install Multiple Charts Concurrently

Deploy multiple applications simultaneously:

```python
import asyncio
from helm_sdkpy import Chart

async def install_chart(name: str, chart_name: str, repo: str, namespace: str):
    """Install a single chart."""
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    result = await chart.install_async(
        namespace=namespace,
        create_namespace=True,
        wait=True,
        timeout=600
    )
    
    print(f"✓ Installed {name}")
    return result

async def install_stack():
    """Install complete application stack concurrently."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    # Install all charts concurrently
    results = await asyncio.gather(
        install_chart("nginx", "nginx", repo_url, "web"),
        install_chart("redis", "redis", repo_url, "cache"),
        install_chart("postgres", "postgresql", repo_url, "database"),
        install_chart("mongodb", "mongodb", repo_url, "database")
    )
    
    print(f"\n✓ Installed {len(results)} charts")
    return results

if __name__ == "__main__":
    asyncio.run(install_stack())
```

## Concurrent Upgrades

Upgrade multiple releases simultaneously:

```python
import asyncio
from helm_sdkpy import Chart

async def upgrade_chart(name: str, chart_name: str, repo: str, version: str):
    """Upgrade a single chart."""
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name,
        version=version
    )
    
    result = await chart.upgrade_async(
        namespace="default",
        wait=True,
        atomic=True,
        timeout=600
    )
    
    print(f"✓ Upgraded {name} to {version}")
    return result

async def upgrade_all():
    """Upgrade multiple releases concurrently."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    upgrades = [
        ("nginx", "nginx", "15.2.0"),
        ("redis", "redis", "18.1.0"),
        ("postgres", "postgresql", "13.1.0"),
    ]
    
    tasks = [
        upgrade_chart(name, chart, repo_url, version)
        for name, chart, version in upgrades
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Check for errors
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            name = upgrades[i][0]
            print(f"✗ Failed to upgrade {name}: {result}")
    
    return results

asyncio.run(upgrade_all())
```

## Concurrent Status Checks

Check status of multiple releases:

```python
import asyncio
from helm_sdkpy import Chart
from helm_sdkpy.actions import List

async def check_status(name: str, namespace: str):
    """Check status of a single release."""
    chart = Chart(name=name)
    
    status = await chart.status_async(namespace=namespace)
    return {"name": name, "namespace": namespace, "status": status}

async def check_all_releases():
    """Check status of all releases concurrently."""
    
    # Get list of releases
    lister = List()
    releases = lister.run(all_namespaces=True)
    
    # Check status concurrently
    tasks = [
        check_status(rel['name'], rel['namespace'])
        for rel in releases
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Print results
    print("Release Status:")
    for result in results:
        if isinstance(result, Exception):
            print(f"  ✗ Error: {result}")
        else:
            print(f"  {result['namespace']}/{result['name']}: {result['status']}")
    
    return results

asyncio.run(check_all_releases())
```

## Error Handling in Concurrent Operations

Handle errors gracefully in async operations:

```python
import asyncio
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError

async def install_with_retry(name: str, chart_name: str, repo: str, max_retries: int = 3):
    """Install chart with retry logic."""
    
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    for attempt in range(max_retries):
        try:
            result = await chart.install_async(
                namespace="default",
                create_namespace=True,
                wait=True,
                timeout=300
            )
            
            print(f"✓ Installed {name} (attempt {attempt + 1})")
            return result
            
        except HelmError as e:
            if attempt < max_retries - 1:
                print(f"⚠ Attempt {attempt + 1} failed for {name}, retrying...")
                await asyncio.sleep(5)  # Wait before retry
            else:
                print(f"✗ Failed to install {name} after {max_retries} attempts: {e}")
                raise

async def install_with_error_handling():
    """Install multiple charts with error handling."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    charts = [
        ("nginx", "nginx"),
        ("redis", "redis"),
        ("invalid", "nonexistent"),  # This will fail
        ("postgres", "postgresql"),
    ]
    
    tasks = [
        install_with_retry(name, chart, repo_url)
        for name, chart in charts
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Separate successful and failed installations
    successful = []
    failed = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            failed.append((charts[i][0], str(result)))
        else:
            successful.append(charts[i][0])
    
    print(f"\n✓ Successfully installed: {', '.join(successful)}")
    if failed:
        print(f"✗ Failed installations:")
        for name, error in failed:
            print(f"  - {name}: {error}")
    
    return successful, failed

asyncio.run(install_with_error_handling())
```

## Semaphore for Limiting Concurrency

Limit number of concurrent operations:

```python
import asyncio
from helm_sdkpy import Chart

async def install_with_limit(semaphore, name: str, chart_name: str, repo: str):
    """Install chart with concurrency limit."""
    
    async with semaphore:  # Acquire semaphore
        chart = Chart(
            name=name,
            repo=repo,
            chart=chart_name
        )
        
        print(f"Starting installation of {name}...")
        
        result = await chart.install_async(
            namespace="default",
            create_namespace=True,
            wait=True,
            timeout=600
        )
        
        print(f"✓ Completed {name}")
        return result

async def install_many_charts():
    """Install many charts with concurrency limit."""
    
    # Limit to 3 concurrent installations
    semaphore = asyncio.Semaphore(3)
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    charts = [
        ("nginx-1", "nginx"),
        ("nginx-2", "nginx"),
        ("nginx-3", "nginx"),
        ("redis-1", "redis"),
        ("redis-2", "redis"),
        ("postgres-1", "postgresql"),
        ("postgres-2", "postgresql"),
    ]
    
    tasks = [
        install_with_limit(semaphore, name, chart, repo_url)
        for name, chart in charts
    ]
    
    results = await asyncio.gather(*tasks)
    
    print(f"\n✓ Installed {len(results)} charts")
    return results

asyncio.run(install_many_charts())
```

## Progress Tracking

Track progress of concurrent operations:

```python
import asyncio
from helm_sdkpy import Chart

class ProgressTracker:
    def __init__(self, total: int):
        self.total = total
        self.completed = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            self.completed += 1
            progress = (self.completed / self.total) * 100
            print(f"Progress: {self.completed}/{self.total} ({progress:.1f}%)")

async def install_with_progress(tracker, name: str, chart_name: str, repo: str):
    """Install chart with progress tracking."""
    
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    try:
        result = await chart.install_async(
            namespace="default",
            create_namespace=True,
            wait=True
        )
        
        await tracker.increment()
        return result
        
    except Exception as e:
        print(f"✗ Failed {name}: {e}")
        await tracker.increment()
        raise

async def install_with_tracking():
    """Install charts with progress tracking."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    charts = [
        ("nginx", "nginx"),
        ("redis", "redis"),
        ("postgres", "postgresql"),
        ("mongodb", "mongodb"),
        ("mariadb", "mariadb"),
    ]
    
    tracker = ProgressTracker(total=len(charts))
    
    print(f"Installing {len(charts)} charts...")
    
    tasks = [
        install_with_progress(tracker, name, chart, repo_url)
        for name, chart in charts
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = sum(1 for r in results if not isinstance(r, Exception))
    print(f"\n✓ Successfully installed {successful}/{len(charts)} charts")
    
    return results

asyncio.run(install_with_tracking())
```

## Timeout Handling

Handle timeouts in async operations:

```python
import asyncio
from helm_sdkpy import Chart
from helm_sdkpy.exceptions import HelmError

async def install_with_timeout(name: str, chart_name: str, repo: str, operation_timeout: int = 120):
    """Install chart with overall operation timeout."""
    
    chart = Chart(
        name=name,
        repo=repo,
        chart=chart_name
    )
    
    try:
        result = await asyncio.wait_for(
            chart.install_async(
                namespace="default",
                create_namespace=True,
                wait=True,
                timeout=300  # Helm timeout
            ),
            timeout=operation_timeout  # Overall timeout
        )
        
        print(f"✓ Installed {name}")
        return result
        
    except asyncio.TimeoutError:
        print(f"✗ Installation of {name} timed out after {operation_timeout}s")
        raise
    except HelmError as e:
        print(f"✗ Failed to install {name}: {e}")
        raise

async def install_with_timeouts():
    """Install multiple charts with individual timeouts."""
    
    repo_url = "https://charts.bitnami.com/bitnami"
    
    # Different timeouts for different charts
    installations = [
        ("nginx", "nginx", 60),      # Quick install
        ("redis", "redis", 120),     # Medium
        ("postgres", "postgresql", 300),  # Slower database
    ]
    
    tasks = [
        install_with_timeout(name, chart, repo_url, timeout)
        for name, chart, timeout in installations
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            name = installations[i][0]
            print(f"Failed: {name}")
    
    return results

asyncio.run(install_with_timeouts())
```

## Complete Concurrent Example

Full workflow with concurrent operations:

```python
import asyncio
from helm_sdkpy import Chart
from helm_sdkpy.repo import Repo
from helm_sdkpy.exceptions import HelmError
from typing import List, Tuple
import sys

class ConcurrentDeployer:
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []
    
    async def install_chart(self, name: str, chart_name: str, repo: str,
                           namespace: str, values: dict = None):
        """Install a single chart with concurrency control."""
        
        async with self.semaphore:
            chart = Chart(
                name=name,
                repo=repo,
                chart=chart_name
            )
            
            print(f"[{name}] Starting installation...")
            
            try:
                result = await chart.install_async(
                    namespace=namespace,
                    values=values or {},
                    create_namespace=True,
                    wait=True,
                    timeout=600
                )
                
                print(f"[{name}] ✓ Installed successfully")
                self.results.append((name, True, None))
                return result
                
            except HelmError as e:
                print(f"[{name}] ✗ Installation failed: {e}")
                self.results.append((name, False, str(e)))
                raise
    
    async def deploy_stack(self, stack: List[Tuple]):
        """Deploy complete application stack."""
        
        tasks = []
        for name, chart, repo, namespace, values in stack:
            task = self.install_chart(name, chart, repo, namespace, values)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Print summary
        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - successful
        
        print(f"\nDeployment Summary:")
        print(f"  ✓ Successful: {successful}")
        print(f"  ✗ Failed: {failed}")
        
        if failed > 0:
            print("\nFailed deployments:")
            for name, success, error in self.results:
                if not success:
                    print(f"  - {name}: {error}")
        
        return successful == len(results)

async def main():
    """Main deployment workflow."""
    
    # Setup repositories
    repo = Repo()
    try:
        repo.add(name="bitnami", url="https://charts.bitnami.com/bitnami")
        repo.update()
        print("✓ Repository configured\n")
    except HelmError as e:
        print(f"Warning: Repository setup: {e}\n")
    
    # Define application stack
    stack = [
        # (name, chart, repo, namespace, values)
        (
            "web-nginx",
            "nginx",
            "https://charts.bitnami.com/bitnami",
            "web",
            {"replicaCount": 3}
        ),
        (
            "cache-redis",
            "redis",
            "https://charts.bitnami.com/bitnami",
            "cache",
            {"auth": {"enabled": True}}
        ),
        (
            "db-postgres",
            "postgresql",
            "https://charts.bitnami.com/bitnami",
            "database",
            {"primary": {"persistence": {"size": "10Gi"}}}
        ),
        (
            "db-mongodb",
            "mongodb",
            "https://charts.bitnami.com/bitnami",
            "database",
            {"replicaCount": 2}
        ),
    ]
    
    # Deploy with concurrency limit of 2
    deployer = ConcurrentDeployer(max_concurrent=2)
    
    print("Starting concurrent deployment...\n")
    success = await deployer.deploy_stack(stack)
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
```

## Best Practices

1. **Limit Concurrency**: Use semaphores to avoid overwhelming Kubernetes API
2. **Handle Errors**: Always use `gather(*tasks, return_exceptions=True)`
3. **Set Timeouts**: Use `asyncio.wait_for()` for operation-level timeouts
4. **Progress Tracking**: Provide feedback for long-running operations
5. **Retry Logic**: Implement retries for transient failures
6. **Resource Cleanup**: Ensure cleanup even if operations fail

## Performance Considerations

```python
# Bad: Sequential (slow)
for chart in charts:
    chart.install(namespace="default")

# Good: Concurrent (fast)
await asyncio.gather(
    *[chart.install_async(namespace="default") for chart in charts]
)
```

## Next Steps

- [Installing Charts](chart-install) - Basic installation
- [Upgrading Charts](chart-upgrade) - Chart upgrades
- [Error Handling](error-handling) - Robust error management
- [Managing Releases](release-management) - Release operations
