// Copyright 2025 Vantage Compute
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"os"

	"k8s.io/apimachinery/pkg/api/meta"
	"k8s.io/client-go/discovery"
	"k8s.io/client-go/discovery/cached/memory"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/restmapper"
	"k8s.io/client-go/tools/clientcmd"
	clientcmdapi "k8s.io/client-go/tools/clientcmd/api"
)

const (
	serviceAccountTokenPath = "/var/run/secrets/kubernetes.io/serviceaccount/token"
)

// isRunningInCluster checks if we're running inside a Kubernetes pod
// by verifying the ServiceAccount token exists and KUBERNETES_SERVICE_HOST is set.
func isRunningInCluster() bool {
	_, err := os.Stat(serviceAccountTokenPath)
	if err != nil {
		return false
	}
	return os.Getenv("KUBERNETES_SERVICE_HOST") != ""
}

// inClusterGetter implements genericclioptions.RESTClientGetter
// for in-cluster ServiceAccount authentication.
type inClusterGetter struct {
	namespace       string
	cachedDiscovery discovery.CachedDiscoveryInterface
	restConfig      *rest.Config
}

// NewInClusterGetter creates a RESTClientGetter that uses
// the ServiceAccount token mounted in the pod.
func NewInClusterGetter(namespace string) *inClusterGetter {
	return &inClusterGetter{
		namespace: namespace,
	}
}

// ToRESTConfig returns a REST config using in-cluster credentials.
// This automatically reads:
// - Token from /var/run/secrets/kubernetes.io/serviceaccount/token
// - CA cert from /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
// - API server from KUBERNETES_SERVICE_HOST and KUBERNETES_SERVICE_PORT env vars
func (i *inClusterGetter) ToRESTConfig() (*rest.Config, error) {
	if i.restConfig != nil {
		return i.restConfig, nil
	}

	config, err := rest.InClusterConfig()
	if err != nil {
		return nil, err
	}
	i.restConfig = config
	return config, nil
}

// ToDiscoveryClient returns a cached discovery client.
func (i *inClusterGetter) ToDiscoveryClient() (discovery.CachedDiscoveryInterface, error) {
	if i.cachedDiscovery != nil {
		return i.cachedDiscovery, nil
	}

	config, err := i.ToRESTConfig()
	if err != nil {
		return nil, err
	}

	discoveryClient, err := discovery.NewDiscoveryClientForConfig(config)
	if err != nil {
		return nil, err
	}

	i.cachedDiscovery = memory.NewMemCacheClient(discoveryClient)
	return i.cachedDiscovery, nil
}

// ToRESTMapper returns a RESTMapper for resource mapping.
func (i *inClusterGetter) ToRESTMapper() (meta.RESTMapper, error) {
	discoveryClient, err := i.ToDiscoveryClient()
	if err != nil {
		return nil, err
	}

	mapper := restmapper.NewDeferredDiscoveryRESTMapper(discoveryClient)
	return mapper, nil
}

// ToRawKubeConfigLoader returns a clientcmd.ClientConfig.
// For in-cluster config, we create a minimal config with the namespace override.
func (i *inClusterGetter) ToRawKubeConfigLoader() clientcmd.ClientConfig {
	overrides := &clientcmd.ConfigOverrides{}
	if i.namespace != "" {
		overrides.Context.Namespace = i.namespace
	}
	return clientcmd.NewDefaultClientConfig(clientcmdapi.Config{}, overrides)
}
