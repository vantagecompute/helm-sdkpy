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

/*
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned long long helmpy_handle;
*/
import "C"

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"unsafe"

	"helm.sh/helm/v4/pkg/action"
	"helm.sh/helm/v4/pkg/chart/v2/loader"
	"helm.sh/helm/v4/pkg/cli"
)

// Configuration state
type configState struct {
	cfg  *action.Configuration
	envs *cli.EnvSettings
	mu   sync.Mutex
}

var (
	handleSeq atomic.Uint64
	configs   sync.Map

	errMu          sync.Mutex
	lastErr        string
	versionCString *C.char
)

func init() {
	versionCString = C.CString("helmpy-v0.0.1")
}

func setError(err error) C.int {
	errMu.Lock()
	defer errMu.Unlock()
	if err != nil {
		lastErr = err.Error()
		return -1
	}
	lastErr = ""
	return 0
}

func recordErrorf(format string, args ...any) C.int {
	return setError(fmt.Errorf(format, args...))
}

func nextHandle() C.helmpy_handle {
	return C.helmpy_handle(handleSeq.Add(1))
}

//export helmpy_last_error
func helmpy_last_error() *C.char {
	errMu.Lock()
	defer errMu.Unlock()
	if lastErr == "" {
		return nil
	}
	return C.CString(lastErr)
}

//export helmpy_free
func helmpy_free(ptr unsafe.Pointer) {
	C.free(ptr)
}

//export helmpy_version_string
func helmpy_version_string() *C.char {
	return versionCString
}

//export helmpy_version_number
func helmpy_version_number() C.int {
	return 1 // Version 0.0.1
}

// Configuration management

//export helmpy_config_create
func helmpy_config_create(namespace *C.char, kubeconfig *C.char, kubecontext *C.char, handle_out *C.helmpy_handle) C.int {
	ns := C.GoString(namespace)
	kc := C.GoString(kubeconfig)
	kctx := C.GoString(kubecontext)

	// Create environment settings
	envs := cli.New()
	if ns != "" {
		envs.SetNamespace(ns)
	}
	if kc != "" {
		envs.KubeConfig = kc
	}
	if kctx != "" {
		envs.KubeContext = kctx
	}

	// Create action configuration
	cfg := new(action.Configuration)

	// Initialize the configuration with Kubernetes settings
	err := cfg.Init(envs.RESTClientGetter(), envs.Namespace(), os.Getenv("HELM_DRIVER"))
	if err != nil {
		return setError(fmt.Errorf("failed to initialize helm config: %w", err))
	}

	state := &configState{
		cfg:  cfg,
		envs: envs,
	}

	handle := nextHandle()
	configs.Store(handle, state)
	*handle_out = handle

	return 0
}

//export helmpy_config_destroy
func helmpy_config_destroy(handle C.helmpy_handle) {
	configs.Delete(handle)
}

func getConfig(handle C.helmpy_handle) (*configState, error) {
	val, ok := configs.Load(handle)
	if !ok {
		return nil, fmt.Errorf("invalid configuration handle")
	}
	return val.(*configState), nil
}

// Install action

//export helmpy_install
func helmpy_install(handle C.helmpy_handle, release_name *C.char, chart_path *C.char, values_json *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)
	chartPath := C.GoString(chart_path)
	valuesJSON := C.GoString(values_json)

	// Create install action
	client := action.NewInstall(state.cfg)
	client.ReleaseName = releaseName
	client.Namespace = state.envs.Namespace()

	// Locate and load the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Load the chart from the located path
	chart, err := loader.Load(cp)
	if err != nil {
		return setError(fmt.Errorf("failed to load chart: %w", err))
	}

	// Parse values
	var values map[string]interface{}
	if valuesJSON != "" {
		if err := json.Unmarshal([]byte(valuesJSON), &values); err != nil {
			return setError(fmt.Errorf("failed to parse values JSON: %w", err))
		}
	}

	// Run the install
	rel, err := client.Run(chart, values)
	if err != nil {
		return setError(fmt.Errorf("install failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Upgrade action

//export helmpy_upgrade
func helmpy_upgrade(handle C.helmpy_handle, release_name *C.char, chart_path *C.char, values_json *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)
	chartPath := C.GoString(chart_path)
	valuesJSON := C.GoString(values_json)

	// Create upgrade action
	client := action.NewUpgrade(state.cfg)
	client.Namespace = state.envs.Namespace()

	// Locate and load the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Load the chart from the located path
	chart, err := loader.Load(cp)
	if err != nil {
		return setError(fmt.Errorf("failed to load chart: %w", err))
	}

	// Parse values
	var values map[string]interface{}
	if valuesJSON != "" {
		if err := json.Unmarshal([]byte(valuesJSON), &values); err != nil {
			return setError(fmt.Errorf("failed to parse values JSON: %w", err))
		}
	}

	// Run the upgrade
	rel, err := client.Run(releaseName, chart, values)
	if err != nil {
		return setError(fmt.Errorf("upgrade failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Uninstall action

//export helmpy_uninstall
func helmpy_uninstall(handle C.helmpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create uninstall action
	client := action.NewUninstall(state.cfg)

	// Run the uninstall
	resp, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("uninstall failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(resp)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// List action

//export helmpy_list
func helmpy_list(handle C.helmpy_handle, all C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	// Create list action
	client := action.NewList(state.cfg)
	if all != 0 {
		client.All = true
	}

	// Run the list
	releases, err := client.Run()
	if err != nil {
		return setError(fmt.Errorf("list failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(releases)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Get/Status action

//export helmpy_status
func helmpy_status(handle C.helmpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create status action
	client := action.NewStatus(state.cfg)

	// Run the status
	rel, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("status failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Rollback action

//export helmpy_rollback
func helmpy_rollback(handle C.helmpy_handle, release_name *C.char, revision C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create rollback action
	client := action.NewRollback(state.cfg)
	client.Version = int(revision)

	// Run the rollback
	err = client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("rollback failed: %w", err))
	}

	// Return success message
	result := map[string]string{"status": "success"}
	resultData, err := json.Marshal(result)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Get values action

//export helmpy_get_values
func helmpy_get_values(handle C.helmpy_handle, release_name *C.char, all_values C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create get values action
	client := action.NewGetValues(state.cfg)
	if all_values != 0 {
		client.AllValues = true
	}

	// Run the get values
	values, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("get values failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(values)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// History action

//export helmpy_history
func helmpy_history(handle C.helmpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create history action
	client := action.NewHistory(state.cfg)

	// Run the history
	releases, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("history failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(releases)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Pull action

//export helmpy_pull
func helmpy_pull(handle C.helmpy_handle, chart_ref *C.char, dest_dir *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartRef := C.GoString(chart_ref)
	destDir := C.GoString(dest_dir)

	// Create pull action
	client := action.NewPull()
	client.Settings = state.envs
	if destDir != "" {
		client.DestDir = destDir
	}

	// Run the pull
	_, err = client.Run(chartRef)
	if err != nil {
		return setError(fmt.Errorf("pull failed: %w", err))
	}

	return 0
}

// Show chart action

//export helmpy_show_chart
func helmpy_show_chart(handle C.helmpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// Create show action
	client := action.NewShow(action.ShowChart, state.cfg)
	client.ChartPathOptions.RegistryClient = state.cfg.RegistryClient

	// Locate the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Run the show
	output, err := client.Run(cp)
	if err != nil {
		return setError(fmt.Errorf("show chart failed: %w", err))
	}

	*result_json = C.CString(output)
	return 0
}

// Show values action

//export helmpy_show_values
func helmpy_show_values(handle C.helmpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// Create show action
	client := action.NewShow(action.ShowValues, state.cfg)
	client.ChartPathOptions.RegistryClient = state.cfg.RegistryClient

	// Locate the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Run the show
	output, err := client.Run(cp)
	if err != nil {
		return setError(fmt.Errorf("show values failed: %w", err))
	}

	*result_json = C.CString(output)
	return 0
}

// Test action

//export helmpy_test
func helmpy_test(handle C.helmpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create test action
	client := action.NewReleaseTesting(state.cfg)

	// Run the test
	rel, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("test failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Lint action

//export helmpy_lint
func helmpy_lint(handle C.helmpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// For remote charts (OCI/HTTP), we need to locate them first
	// For local charts, LocateChart will just return the path as-is
	var pathOpts action.ChartPathOptions
	pathOpts.RegistryClient = state.cfg.RegistryClient

	cp, err := pathOpts.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Create lint action
	client := action.NewLint()

	// Run the lint
	result := client.Run([]string{cp}, map[string]interface{}{})

	// Serialize result
	resultData, err := json.Marshal(result)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Package action

//export helmpy_package
func helmpy_package(handle C.helmpy_handle, chart_path *C.char, dest_dir *C.char, result_path **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)
	destDir := C.GoString(dest_dir)

	// Create package action
	client := action.NewPackage()
	if destDir != "" {
		client.Destination = destDir
	}

	// Run the package
	path, err := client.Run(chartPath, nil)
	if err != nil {
		return setError(fmt.Errorf("package failed: %w", err))
	}

	*result_path = C.CString(path)
	return 0
}

func main() {
	// Required for CGO shared library
}
