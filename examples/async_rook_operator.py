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
Async Rook-Ceph Operator Installation Example

This example demonstrates installing the Rook-Ceph operator from the Rook release
repository using helm-sdkpy's async API. Rook is a cloud-native storage orchestrator
for Kubernetes, providing platform-agnostic distributed storage solutions.

Based on: https://artifacthub.io/packages/helm/rook/rook-ceph

Prerequisites:
- Access to a Kubernetes cluster (e.g., minikube, kind, or production cluster)
- KUBECONFIG environment variable set to your cluster config
- Cluster-admin permissions (Rook requires CRD installation)
- Kubernetes 1.25+ recommended
- At least 3 worker nodes for production (1 node sufficient for testing)
- Raw block devices or local storage available on nodes

To test with a local cluster:
    # Using kind (with extra mounts for storage)
    kind create cluster --name rook-test --config kind-config.yaml
    
    # Using minikube
    minikube start --profile rook-test --nodes 3 --disk-size=20g
    
    # Then run this script
    python examples/async_rook_operator.py

Note: This installs the Rook operator only. After installation, you'll need to
create a CephCluster custom resource to deploy the actual Ceph storage cluster.
"""

import asyncio
import subprocess
import sys
import tempfile

import helm_sdkpy


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
║       Async Rook-Ceph Operator Installation with helm-sdkpy       ║
║          Cloud-Native Storage Orchestrator for Kubernetes         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")


async def main():
    """Install Rook-Ceph operator using helm-sdkpy async API."""
    print_banner()
    
    print(f"helm-sdkpy version: {helm_sdkpy.__version__}")
    
    try:
        lib_version = helm_sdkpy.get_version()
        print(f"Library version: {lib_version}")
    except helm_sdkpy.HelmLibraryNotFound:
        print("✗ Helm library not found. Please build the library first:")
        print("  Run: just build-wheel")
        return 1
    except (AttributeError, Exception):
        # Library exists but version function not available (older build)
        print("Library version: (using development build)")
        pass
    
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
        
        # Rook operator should be installed in rook-ceph namespace
        config = helm_sdkpy.Configuration(
            namespace="rook-ceph",
            kubeconfig=kubeconfig_file.name
        )
        
        print("✓ Helm configuration created for namespace: rook-ceph")
        
    except helm_sdkpy.ConfigurationError as e:
        print(f"✗ Configuration failed: {e}")
        return 1
    
    # Step 3: Add Rook Release Repository
    print_section("Step 3: Add Rook Repository (Async)")
    
    try:
        repo_add = helm_sdkpy.RepoAdd(config)
        
        print("Adding Rook release repository asynchronously...")
        print("  Name: rook-release")
        print("  URL: https://charts.rook.io/release")
        
        await repo_add.run(
            name="rook-release",
            url="https://charts.rook.io/release"
        )
        
        print("✓ Rook repository added successfully")
        
    except helm_sdkpy.HelmError as e:
        if "already exists" in str(e).lower():
            print("✓ Rook repository already exists")
        else:
            print(f"✗ Failed to add repository: {e}")
            return 1
    
    # Step 4: Update Repository Index
    print_section("Step 4: Update Repository Index (Async)")
    
    try:
        repo_update = helm_sdkpy.RepoUpdate(config)
        
        print("Updating repository indexes...")
        await repo_update.run()
        
        print("✓ Repository indexes updated successfully")
        
    except helm_sdkpy.HelmError as e:
        print(f"✗ Failed to update repository: {e}")
        return 1
    
    # Step 5: Install Rook-Ceph Operator
    print_section("Step 5: Install Rook-Ceph Operator (Async)")
    
    try:
        install = helm_sdkpy.Install(config)
        
        # Rook operator installation values
        # These are recommended settings for most deployments
        values = {
            # Enable CRDs installation
            "crds": {
                "enabled": True
            },
            # Resource requests and limits for the operator
            "resources": {
                "limits": {
                    "memory": "512Mi"
                },
                "requests": {
                    "cpu": "100m",
                    "memory": "128Mi"
                }
            },
            # Enable monitoring with Prometheus
            "monitoring": {
                "enabled": False  # Set to True if you have Prometheus installed
            },
            # CSI driver settings
            "csi": {
                "enableCephfsDriver": True,
                "enableRbdDriver": True,
                "enableCSIHostNetwork": True,
                "pluginTolerations": [],
                "provisionerTolerations": []
            },
            # Discovery daemon settings
            "enableDiscoveryDaemon": True,
            # Admission controller settings
            "admissionController": {
                "tolerations": []
            }
        }
        
        print("Installing Rook-Ceph operator chart asynchronously...")
        print("  Release name: rook-ceph")
        print("  Chart: rook-release/rook-ceph")
        print("  Namespace: rook-ceph")
        print("  Version: v1.18.0")
        print("\nConfiguration:")
        print("  - CRDs enabled: True")
        print("  - CephFS Driver: Enabled")
        print("  - RBD Driver: Enabled")
        print("  - Discovery Daemon: Enabled")
        print("  - Namespace will be created automatically")
        print("  - Wait enabled: True (will wait for pods to be ready)")
        
        result = await install.run(
            release_name="rook-ceph",
            chart_path="rook-release/rook-ceph",
            values=values,
            version="v1.18.0",
            create_namespace=True,
            wait=True,
            timeout=600  # Rook operator can take a bit longer
        )
        
        print("\n✓ Rook-Ceph operator installed successfully!")
        print(f"  Release: {result['name']}")
        print(f"  Status: {result['info']['status']}")
        print(f"  Version: {result['version']}")
        print(f"  Chart Version: {result['chart']['metadata']['version']}")
        
    except helm_sdkpy.InstallError as e:
        print(f"✗ Installation failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure you have cluster-admin permissions")
        print("  2. Verify the namespace doesn't already have Rook installed")
        print("  3. Check if CRDs are already installed: kubectl get crds | grep rook")
        print("  4. Ensure your cluster has sufficient resources")
        return 1
    
    # Step 6: Verify Installation
    print_section("Step 6: Verify Installation (Async)")
    
    try:
        status = helm_sdkpy.Status(config)
        
        print("Checking installation status asynchronously...")
        result = await status.run("rook-ceph")
        
        print(f"✓ Release Status: {result['info']['status']}")
        print(f"  Last Deployed: {result['info']['last_deployed']}")
        print(f"  Namespace: {result['namespace']}")
        
        # Count deployed resources
        resources = result['manifest'].split('---')
        print(f"  Deployed Resources: {len([r for r in resources if r.strip()])}")
        
    except helm_sdkpy.ReleaseError as e:
        print(f"⚠ Could not verify status: {e}")
    
    # Step 7: Display Post-Installation Information
    print_section("Post-Installation Steps")
    
    print("""
Rook-Ceph operator has been installed using async operations! 

Here's what you can do next:

1. Verify all operator pods are running:
   kubectl get pods -n rook-ceph

   You should see:
   - rook-ceph-operator-<id>
   - rook-discover-<id> (on each node)

2. Check the installed CRDs:
   kubectl get crds | grep rook

   You should see CRDs for:
   - cephclusters.ceph.rook.io
   - cephblockpools.ceph.rook.io
   - cephfilesystems.ceph.rook.io
   - cephobjectstores.ceph.rook.io
   - And many more...

3. Create a Ceph Cluster:
   The operator is now ready, but you need to create a CephCluster resource
   to deploy the actual Ceph storage cluster. Example:

   cat <<EOF | kubectl apply -f -
   apiVersion: ceph.rook.io/v1
   kind: CephCluster
   metadata:
     name: rook-ceph
     namespace: rook-ceph
   spec:
     cephVersion:
       image: quay.io/ceph/ceph:v18.2.0
       allowUnsupported: false
     dataDirHostPath: /var/lib/rook
     mon:
       count: 3
       allowMultiplePerNode: false
     mgr:
       count: 1
       allowMultiplePerNode: false
     dashboard:
       enabled: true
       ssl: false
     storage:
       useAllNodes: true
       useAllDevices: true
   EOF

4. Create Storage Classes:
   After the cluster is ready, create StorageClasses for:
   - Block Storage (RBD)
   - Shared Filesystem (CephFS)
   - Object Storage (S3-compatible)

5. Monitor cluster status:
   kubectl get cephcluster -n rook-ceph
   kubectl get pods -n rook-ceph

6. Access the Ceph Dashboard (optional):
   kubectl port-forward -n rook-ceph svc/rook-ceph-mgr-dashboard 7000:7000
   
   Get admin password:
   kubectl get secret -n rook-ceph rook-ceph-dashboard-password \\
     -o jsonpath="{['data']['password']}" | base64 --decode

For more information:
- Rook Documentation: https://rook.io/docs/rook/latest/
- Ceph Documentation: https://docs.ceph.com/
- Artifact Hub: https://artifacthub.io/packages/helm/rook/rook-ceph
""")
    
    print_section("Installation Complete")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n✗ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
