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
"strings"

"k8s.io/apimachinery/pkg/api/meta"
"k8s.io/client-go/discovery"
"k8s.io/client-go/discovery/cached/memory"
"k8s.io/client-go/rest"
"k8s.io/client-go/restmapper"
"k8s.io/client-go/tools/clientcmd"
clientcmdapi "k8s.io/client-go/tools/clientcmd/api"
)

// kubeconfigStringGetter implements genericclioptions.RESTClientGetter
// for loading kubeconfig from a string instead of a file.
type kubeconfigStringGetter struct {
kubeconfigContent string
namespace         string
context           string
cachedDiscovery   discovery.CachedDiscoveryInterface
}

// NewKubeconfigStringGetter creates a RESTClientGetter that loads
// kubeconfig from a YAML string instead of a file path.
func NewKubeconfigStringGetter(kubeconfigContent, namespace, context string) *kubeconfigStringGetter {
return &kubeconfigStringGetter{
kubeconfigContent: kubeconfigContent,
namespace:         namespace,
context:           context,
}
}

// ToRESTConfig returns a REST config from the kubeconfig string content.
func (k *kubeconfigStringGetter) ToRESTConfig() (*rest.Config, error) {
config, err := clientcmd.RESTConfigFromKubeConfig([]byte(k.kubeconfigContent))
if err != nil {
return nil, err
}
return config, nil
}

// ToDiscoveryClient returns a discovery client.
func (k *kubeconfigStringGetter) ToDiscoveryClient() (discovery.CachedDiscoveryInterface, error) {
if k.cachedDiscovery != nil {
return k.cachedDiscovery, nil
}

config, err := k.ToRESTConfig()
if err != nil {
return nil, err
}

discoveryClient, err := discovery.NewDiscoveryClientForConfig(config)
if err != nil {
return nil, err
}

k.cachedDiscovery = memory.NewMemCacheClient(discoveryClient)
return k.cachedDiscovery, nil
}

// ToRESTMapper returns a RESTMapper.
func (k *kubeconfigStringGetter) ToRESTMapper() (meta.RESTMapper, error) {
discoveryClient, err := k.ToDiscoveryClient()
if err != nil {
return nil, err
}

mapper := restmapper.NewDeferredDiscoveryRESTMapper(discoveryClient)
return mapper, nil
}

// ToRawKubeConfigLoader returns a clientcmd.ClientConfig.
func (k *kubeconfigStringGetter) ToRawKubeConfigLoader() clientcmd.ClientConfig {
config, err := clientcmd.NewClientConfigFromBytes([]byte(k.kubeconfigContent))
if err != nil {
// Return a default config on error
return clientcmd.NewDefaultClientConfig(clientcmdapi.Config{}, &clientcmd.ConfigOverrides{})
}
return config
}

// isKubeconfigYAMLContent checks if the string is YAML content rather than a file path.
// It looks for typical kubeconfig YAML markers.
func isKubeconfigYAMLContent(s string) bool {
trimmed := strings.TrimSpace(s)
return strings.HasPrefix(trimmed, "apiVersion:") ||
strings.HasPrefix(trimmed, "kind:") ||
strings.Contains(trimmed, "\nclusters:") ||
strings.Contains(trimmed, "\ncontexts:")
}
