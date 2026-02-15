package main

import (
	"strings"
	"testing"

	"helm.sh/helm/v4/pkg/registry"
)

// buildOCIRef builds the full OCI reference with version tag.
// This replicates the logic in loadChartFromOCI for testing.
func buildOCIRef(chartRef string, version string) string {
	ref := strings.TrimPrefix(chartRef, registry.OCIScheme+"://")

	// Check if the chart name (after the last /) already has a version tag
	// We need to check only the chart name part, not the whole ref, because
	// the registry URL may contain a port number (e.g., localhost:5001/chart)
	// which would incorrectly match a simple Contains(ref, ":") check
	lastSlash := strings.LastIndex(ref, "/")
	chartName := ref
	if lastSlash >= 0 {
		chartName = ref[lastSlash+1:]
	}
	if version != "" && !strings.Contains(chartName, ":") {
		ref = ref + ":" + version
	}
	return ref
}

func TestBuildOCIRef(t *testing.T) {
	tests := []struct {
		name     string
		chartRef string
		version  string
		expected string
	}{
		{
			name:     "standard OCI URL with version",
			chartRef: "oci://ghcr.io/project/chart",
			version:  "1.0.0",
			expected: "ghcr.io/project/chart:1.0.0",
		},
		{
			name:     "OCI URL with port and version",
			chartRef: "oci://localhost:5001/project/chart",
			version:  "2.5.0",
			expected: "localhost:5001/project/chart:2.5.0",
		},
		{
			name:     "OCI URL with port no subdirectory",
			chartRef: "oci://localhost:5001/chart",
			version:  "1.2.3",
			expected: "localhost:5001/chart:1.2.3",
		},
		{
			name:     "OCI URL already has version tag",
			chartRef: "oci://ghcr.io/project/chart:existing",
			version:  "1.0.0",
			expected: "ghcr.io/project/chart:existing",
		},
		{
			name:     "OCI URL with port already has version tag",
			chartRef: "oci://localhost:5001/project/chart:existing",
			version:  "2.0.0",
			expected: "localhost:5001/project/chart:existing",
		},
		{
			name:     "empty version should not append tag",
			chartRef: "oci://ghcr.io/project/chart",
			version:  "",
			expected: "ghcr.io/project/chart",
		},
		{
			name:     "nested path with port",
			chartRef: "oci://192.168.1.100:5000/helm-charts/stable/nginx",
			version:  "15.0.0",
			expected: "192.168.1.100:5000/helm-charts/stable/nginx:15.0.0",
		},
		{
			name:     "without oci:// prefix",
			chartRef: "localhost:5001/charts/app",
			version:  "3.0.0",
			expected: "localhost:5001/charts/app:3.0.0",
		},
		{
			name:     "registry with high port number",
			chartRef: "oci://registry.internal:32000/myorg/mychart",
			version:  "0.1.0",
			expected: "registry.internal:32000/myorg/mychart:0.1.0",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := buildOCIRef(tt.chartRef, tt.version)
			if result != tt.expected {
				t.Errorf("buildOCIRef(%q, %q) = %q, want %q",
					tt.chartRef, tt.version, result, tt.expected)
			}
		})
	}
}
