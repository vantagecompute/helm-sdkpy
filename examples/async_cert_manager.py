#!/usr/bin/env python3
# Copyright 2025 Vantage Compute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Async cert-manager Installation Example

This example demonstrates installing cert-manager from the Jetstack repository
using helmpy's async API. cert-manager is a powerful certificate management 
controller for Kubernetes that automates the management and issuance of TLS 
certificates.

Based on: https://artifacthub.io/packages/helm/cert-manager/cert-manager

Prerequisites:
- Access to a Kubernetes cluster (e.g., minikube, kind, or production cluster)
- KUBECONFIG environment variable set to your cluster config
- Cluster-admin permissions (cert-manager requires CRD installation)
- Kubernetes 1.25+ recommended

To test with a local cluster:
    # Using kind
    kind create cluster --name cert-manager-test
    
    # Using minikube
    minikube start --profile cert-manager-test
    
    # Then run this script
    python examples/async_cert_manager.py
"""

import asyncio
import subprocess
import sys
import tempfile

import helmpy


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def print_banner():
    """Print application banner."""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         Async cert-manager Installation with helmpy              ║
║           Automated Certificate Management for Kubernetes        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")


async def main():
    """Install cert-manager using helmpy async API."""
    print_banner()
    
    print(f"helmpy version: {helmpy.__version__}")
    
    try:
        lib_version = helmpy.get_version()
        print(f"Library version: {lib_version}")
    except helmpy.HelmLibraryNotFound:
        print("✗ Helm library not found. Please build the library first:")
        print("  Run: just build-wheel")
        return 1
    
    # Step 1: Get kubeconfig from microk8s
    print_section("Step 1: Get Kubeconfig from MicroK8s")
    
    try:
        print("Retrieving kubeconfig from 'microk8s.config' command...")
        result = subprocess.run(
            ["microk8s.config"],
            capture_output=True,
            text=True,
            check=True
        )
        kubeconfig_content = result.stdout
        print("✓ Successfully retrieved kubeconfig from MicroK8s")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to get kubeconfig: {e}")
        print("  Make sure MicroK8s is installed and running")
        print("  Try: microk8s status")
        return 1
    except FileNotFoundError:
        print("✗ 'microk8s.config' command not found")
        print("  Make sure MicroK8s is installed")
        print("  Install: sudo snap install microk8s --classic")
        return 1
    
    # Step 2: Create Configuration
    print_section("Step 2: Configuration")
    
    try:
        # Write kubeconfig to a temporary file
        kubeconfig_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml')
        kubeconfig_file.write(kubeconfig_content)
        kubeconfig_file.close()
        
        print(f"✓ Kubeconfig written to: {kubeconfig_file.name}")
        
        # cert-manager should be installed in its own namespace
        config = helmpy.Configuration(
            namespace="cert-manager",
            kubeconfig=kubeconfig_file.name
        )
        print("✓ Created Helm configuration")
        print(f"  Namespace: cert-manager")
        print(f"  Note: The namespace will be created if it doesn't exist")
    except helmpy.ConfigurationError as e:
        print(f"✗ Configuration error: {e}")
        print("  Make sure you have access to a Kubernetes cluster")
        return 1
    
    # Step 3: Add Jetstack Repository
    print_section("Step 3: Add Jetstack Helm Repository (Async)")
    
    try:
        repo_add = helmpy.RepoAdd(config)
        
        print("Adding repository: jetstack")
        print("  URL: https://charts.jetstack.io")
        
        await repo_add.run(
            name="jetstack",
            url="https://charts.jetstack.io"
        )
        
        print("✓ Jetstack repository added successfully")
        
    except helmpy.HelmError as e:
        if "already exists" in str(e).lower():
            print("✓ Jetstack repository already exists")
        else:
            print(f"✗ Failed to add repository: {e}")
            return 1
    
    # Step 4: Update Repository Index
    print_section("Step 4: Update Repository Index (Async)")
    
    try:
        repo_update = helmpy.RepoUpdate(config)
        
        print("Updating repository indexes...")
        await repo_update.run()
        
        print("✓ Repository indexes updated successfully")
        
    except helmpy.HelmError as e:
        print(f"✗ Failed to update repository: {e}")
        return 1
    
    # Step 5: Install cert-manager
    print_section("Step 5: Install cert-manager (Async)")
    
    try:
        install = helmpy.Install(config)
        
        # cert-manager installation values
        values = {
            "crds": {
                "enabled": True
            }
        }
        
        print("Installing cert-manager chart asynchronously...")
        print("  Release name: cert-manager")
        print("  Chart: jetstack/cert-manager")
        print("  Namespace: cert-manager")
        print("  Version: v1.19.1 (latest available)")
        print("\nConfiguration:")
        print("  - CRDs enabled: True")
        print("  - Namespace will be created automatically")
        print("  - Wait enabled: True (will wait for pods to be ready)")
        
        result = await install.run(
            release_name="cert-manager",
            chart_path="jetstack/cert-manager",
            values=values,
            version="v1.19.1",
            create_namespace=True,
            wait=True,
            timeout=300
        )
        
        print("\n✓ cert-manager installed successfully!")
        print(f"  Release: {result['name']}")
        print(f"  Status: {result['info']['status']}")
        print(f"  Version: {result['version']}")
        print(f"  Chart Version: {result['chart']['metadata']['version']}")
        
    except helmpy.InstallError as e:
        print(f"✗ Installation failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure you have cluster-admin permissions")
        print("  2. Verify the namespace doesn't already have cert-manager installed")
        print("  3. Check if CRDs are already installed: kubectl get crds | grep cert-manager")
        return 1
    
    # Step 6: Verify Installation
    print_section("Step 6: Verify Installation (Async)")
    
    try:
        status = helmpy.Status(config)
        
        print("Checking installation status asynchronously...")
        result = await status.run("cert-manager")
        
        print(f"✓ Release Status: {result['info']['status']}")
        print(f"  Last Deployed: {result['info']['last_deployed']}")
        print(f"  Namespace: {result['namespace']}")
        
        # Count deployed resources
        resources = result['manifest'].split('---')
        print(f"  Deployed Resources: {len([r for r in resources if r.strip()])}")
        
    except helmpy.ReleaseError as e:
        print(f"⚠ Could not verify status: {e}")
    
    # Step 7: Display Post-Installation Information
    print_section("Post-Installation Steps")
    
    print("""
cert-manager has been installed using async operations! 

Here's what you can do next:

1. Verify all pods are running:
   kubectl get pods -n cert-manager

   You should see:
   - cert-manager-<id>
   - cert-manager-cainjector-<id>
   - cert-manager-webhook-<id>

2. Check the installed CRDs:
   kubectl get crds | grep cert-manager

   You should see CRDs for:
   - certificates.cert-manager.io
   - certificaterequests.cert-manager.io
   - challenges.acme.cert-manager.io
   - clusterissuers.cert-manager.io
   - issuers.cert-manager.io
   - orders.acme.cert-manager.io

3. Create a ClusterIssuer (example for Let's Encrypt):
   
   cat <<EOF | kubectl apply -f -
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-staging
   spec:
     acme:
       server: https://acme-staging-v02.api.letsencrypt.org/directory
       email: your-email@example.com
       privateKeySecretRef:
         name: letsencrypt-staging
       solvers:
       - http01:
           ingress:
             class: nginx
   EOF

4. Create your first certificate:
   
   cat <<EOF | kubectl apply -f -
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata:
     name: example-com
     namespace: default
   spec:
     secretName: example-com-tls
     issuerRef:
       name: letsencrypt-staging
       kind: ClusterIssuer
     dnsNames:
     - example.com
     - www.example.com
   EOF

5. View cert-manager logs:
   kubectl logs -n cert-manager -l app.kubernetes.io/name=cert-manager

For more information:
- Documentation: https://cert-manager.io/docs/
- Chart: https://artifacthub.io/packages/helm/cert-manager/cert-manager
- GitHub: https://github.com/cert-manager/cert-manager
""")
    
    print_section("Summary")
    
    print("""
✓ Jetstack repository added (async)
✓ Repository index updated (async)
✓ cert-manager installed with CRDs (async with wait)
✓ Installation verified (async)

All operations completed using async/await for non-blocking execution!

cert-manager is now ready to manage your certificates!

To uninstall (if needed):
    python -c "
    import asyncio
    import helmpy
    
    async def uninstall():
        config = helmpy.Configuration(namespace='cert-manager')
        uninstall = helmpy.Uninstall(config)
        await uninstall.run('cert-manager', wait=True)
    
    asyncio.run(uninstall())
    "

Note: Uninstalling will NOT remove the CRDs automatically.
To remove CRDs: kubectl delete crds -l app.kubernetes.io/name=cert-manager
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
