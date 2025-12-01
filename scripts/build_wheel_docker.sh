#!/bin/bash
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

set -e

echo "==> Building helm-sdkpy wheel using Docker"

# Build the wheel-build stage
docker build --target wheel-build --tag helm-sdkpy-wheel-builder .

# Create a container from the image
docker create --name helm-sdkpy-wheel-extract helm-sdkpy-wheel-builder

# Extract the wheel
docker cp helm-sdkpy-wheel-extract:/build/dist/. ./dist/

# Clean up
docker rm helm-sdkpy-wheel-extract

echo "==> Wheel built successfully"
ls -lh dist/*.whl
